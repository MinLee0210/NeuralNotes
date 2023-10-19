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

static_path = os.path.join(str(ROOT), 'ui', 'static')
template_path = os.path.join(str(ROOT), 'ui', 'templates')
soundfont_dir = os.path.join(str(ROOT), 'engine', 'soundfonts', 'default.sf2')

# ==================================================================
#                          CONFIGURATION
# ==================================================================

from starlette.requests import Request 

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from engine.auth_handler import get_current_user

smpl_router = APIRouter()
templates = Jinja2Templates(directory=template_path)

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
route = env['ROUTE']

# ==================================================================



@smpl_router.get('/gallery')
def get_gallery(request: Request): 
    return templates.TemplateResponse('gallery.html', {'request': request})

@smpl_router.get("/gallery/{filename}", response_class=FileResponse)
async def retrieve_files(filename:str):
    audio_client_path = f'data/examples/results_v211'
    if audio_client_path not in filename:
        filename = os.path.join(audio_client_path, filename)
        print(filename)
    return filename

@smpl_router.get('/about')
def get_about_use(request: Request):
        try: 
            token = request.cookies.get('access_token') 
            username = get_current_user(token)
        except: 
            username = None
        return templates.TemplateResponse('about-us.html', {'request': request,
                                                            'message': username})
