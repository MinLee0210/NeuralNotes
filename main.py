import os
import yaml, time
import uvicorn
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware

from routers.user import auth_router
from routers.music import music_router
from routers.index import index_router
from routers.feedback import feedback_router
from routers.samples import smpl_router


from database import MongoDB

# ==================================================================
#                      CONFIGURATION
# ==================================================================

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # NeuralNotes root directory
static_path = os.path.join(str(ROOT), 'ui', 'static')
template_path = os.path.join(str(ROOT), 'ui', 'templates')
soundfont_dir = os.path.join(str(ROOT), 'engine', 'soundfonts', 'default.sf2')

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)

app = FastAPI()
app.mount('/static', StaticFiles(directory=static_path), name='static')
app.add_middleware(SessionMiddleware, secret_key=env['SECRET_KEY'])

templates = Jinja2Templates(directory=template_path)

# ==================================================================
@app.on_event("startup")
async def on_startup():
    await MongoDB.init(env['DATABASE']['URI'], env['DATABASE']['name'])


app.include_router(index_router)
app.include_router(auth_router)
app.include_router(music_router)
app.include_router(feedback_router)
app.include_router(smpl_router)

# ==================================================================
if __name__ == "__main__":
    print(r' _______                                  .__    _______            __                   ')
    print(r' \      \    ____   __ __ _______ _____   |  |   \      \    ____ _/  |_   ____    ______')
    print(r' /   |   \ _/ __ \ |  |  \\_  __ \\__  \  |  |   /   |   \  /  _ \\   __\_/ __ \  /  ___/')
    print(r'/    |    \\  ___/ |  |  / |  | \/ / __ \_|  |__/    |    \(  <_> )|  |  \  ___/  \___ \ ')
    print(r'\____|__  / \___  >|____/  |__|   (____  /|____/\____|__  / \____/ |__|   \___  >/____  >')
    print(r'        \/      \/                     \/               \/                    \/      \/ ')

    uvicorn.run("main:app", 
                host=str(env['HOST']), 
                port=env['PORT_NUMBER'], 
                reload=True,
                ssl_keyfile="certificate/key.pem", 
                ssl_certfile="certificate/cert.pem"
                )
    