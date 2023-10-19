import yaml, os, sys, platform
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # NeuralNotes root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if platform.system() != 'Windows':
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from starlette.responses import HTMLResponse, FileResponse
from starlette.requests import Request

from agent.utils import get_events_from_midis, get_remi_features, pickle_dump, group_pieces
from agent.attributes import compute_polyph_rhythm_piece
from agent.generate import generate_dataloader, generate
from engine.utils import write_bytes_to_mid,get_filename_from_storage
from engine.auth_handler import get_current_user

static_path = os.path.join(str(ROOT), 'ui', 'static')
template_path = os.path.join(str(ROOT), 'ui', 'templates')
soundfont_dir = os.path.join(str(ROOT), 'engine', 'soundfonts', 'default.sf2')

# ==================================================================
#                          CONFIGURATION
# ==================================================================

from starlette.requests import Request 

from fastapi import APIRouter, UploadFile
from fastapi.templating import Jinja2Templates

music_router = APIRouter()
templates = Jinja2Templates(directory=template_path)

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
# ==================================================================


# ==================================================================
#                      AUDIO PROCESS BY AGENT 
# ==================================================================
@music_router.get("/music")
async def get_file(request:Request):
    # return  {'message': 'receive'}
    receive_dir = r'data\receive'
    resource_dir = r'data\resource'
    results_dir = r'data\results'
    try:
        file_storage = []
        for mid_file in os.listdir(results_dir):
            if '.mid' in mid_file: 
                file_storage.append(mid_file)

        token = request.cookies.get('access_token') 
        username = get_current_user(token)
    except:
        return templates.TemplateResponse('page-404.html', {'request': request})
    return templates.TemplateResponse('index.html', {'request': request, 'file_storage': file_storage, 'message': username})

@music_router.get("/music/{filename}", response_class=FileResponse)
async def retrieve_wav(filename:str):
    audio_client_path = r'data\results'
    if audio_client_path not in filename:
        filename = os.path.join(audio_client_path, filename)
        print(filename)
    return filename

@music_router.post("/music")
async def receive_file(request:Request, file: UploadFile):
    receive_dir = r'data\receive'
    resource_dir = r'data\resource'
    results_dir = r'data\results'
    # try:
    content = file.file.read()
    filename = file.filename.split('.')[0]
    file_storage = []
    if filename+'.mid' not in receive_dir: 
        # file_storage.append(filename + '.mid')
        write_bytes_to_mid(filename+'.mid', content, dir=receive_dir)
        
    # Write REMI from MIDI file
    print('Preparing step::From user')
    mid_filename = os.path.join(str(ROOT), receive_dir, filename + '.mid')
    events_from_midi = get_events_from_midis(midipath=mid_filename)
    remi_feats = get_remi_features(events_from_midi)
    pkl_idx = get_filename_from_storage(data_dir=resource_dir)
    pkl_filepath = os.path.join(str(ROOT), resource_dir, '{}.pkl'.format(pkl_idx))
    with open('log.txt', 'a+') as log:
        log.write('Change name of pkl file from {} into {}\n'.format(filename, pkl_filepath))
    pickle_dump(remi_feats, pkl_filepath)
    compute_polyph_rhythm_piece(data_dir=resource_dir, piece='{}.pkl'.format(pkl_idx))

    print('Generating step')
    pieces = group_pieces(content=str(pkl_idx)+'.pkl', resource=resource_dir, n_pieces=1)
    print(pieces)
    dset = generate_dataloader(data_dir=resource_dir, pieces=pieces, vocab_path=env['AGENT']['vocab_path'])
    files_generated = generate(dset=dset, out_dir=results_dir, soundfont_dir=soundfont_dir)
    file.file.close()
    for idx in range(len(files_generated)):
        files_generated[idx] = files_generated[idx].split('\\')[-1]
        file_storage.append(files_generated[idx])
    # except:
    #     return templates.TemplateResponse('page-404.html', {'request': request})
    return templates.TemplateResponse('index.html', {'request': request, 'file_storage': file_storage})

@music_router.get('/music_detail/{filename}')
def get_music_detail(request: Request, filename: str):
    try: 
        token = request.cookies.get('access_token') 
        username = get_current_user(token)
    except: 
        username = None
    response = templates.TemplateResponse('music_detail.html', {'request': request, 'filename': filename, 'message': username})
    response.set_cookie('filename', filename)
    return response
# ==================================================================
