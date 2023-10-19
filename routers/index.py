import yaml, os, sys, platform
from pathlib import Path
from datetime import timedelta

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # NeuralNotes root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if platform.system() != 'Windows':
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


static_path = os.path.join(str(ROOT), 'ui', 'static')
template_path = os.path.join(str(ROOT), 'ui', 'templates')
soundfont_dir = os.path.join(str(ROOT), 'engine', 'soundfonts', 'default.sf2')

# ==================================================================
#                          CONFIGURATION
# ==================================================================

from starlette.requests import Request 
from starlette.responses import HTMLResponse

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from engine.auth_handler import get_current_user
from models.feedback import Rating

index_router = APIRouter()
templates = Jinja2Templates(directory=template_path)

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
# ==================================================================


@index_router.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    try: 
        token = request.cookies.get('access_token') 
        username = get_current_user(token)
    except: 
        username = None

    rating_event = request.cookies.get('rating-event')
    if rating_event: 
        rating_obj = []
        rating_fields = rating_event.split('&')
        for field in rating_fields:
            content = field.split('=')[-1]
            rating_obj.append(content)

        # The schema of rating-event in cookie is "filename=...&value=..."
        rating = Rating(filename=rating_obj[0], 
                        rating=rating_obj[1])
        await rating.insert()
        
    return templates.TemplateResponse('index.html', {'request': request, 
                                                     'message': username})

