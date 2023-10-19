import yaml, os, sys, platform
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # NeuralNotes root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if platform.system() != 'Windows':
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

static_path = os.path.join(str(ROOT), 'ui', 'static')
template_path = os.path.join(str(ROOT), 'ui', 'templates')

# ==================================================================
#                          CONFIGURATION
# ==================================================================

from starlette.requests import Request 
from starlette.config import Config

from fastapi import APIRouter, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response
from fastapi import HTTPException, status

from models.feedback import Comment

from engine.auth_handler import get_current_user


feedback_router = APIRouter()
templates = Jinja2Templates(directory=template_path)

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
# ==================================================================


@feedback_router.get('/rating')
async def rating_sample(request: Request): 
    try: 
        token = request.cookies.get('access_token') 
        username = get_current_user(token)
    except: 
        username = None

@feedback_router.post('/comment/{filename}')
async def post_comment(filename: str, comment: str=Form(...)):
    try:
        comment_info = Comment(filename=filename, content=comment)
        await comment_info.insert()
    except HTTPException as error: 
        print(error)
    response = RedirectResponse(f'/music_detail/{filename}', status_code=status.HTTP_303_SEE_OTHER)
    return response