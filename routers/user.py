import yaml, os, sys, platform
from pathlib import Path
from datetime import timedelta

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # NeuralNotes root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if platform.system() != 'Windows':
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from engine.utils import generate_salt, hash_input, hash_password

static_path = os.path.join(str(ROOT), 'ui', 'static')
template_path = os.path.join(str(ROOT), 'ui', 'templates')
# ==================================================================
#                          CONFIGURATION
# ==================================================================

from fastapi import APIRouter, Form
from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from starlette.requests import Request 
from starlette.config import Config

from authlib.integrations.starlette_client import OAuth, OAuthError

from models.user import UserInfo
from engine.auth_handler import verify_password, create_access_token

auth_router = APIRouter()
templates = Jinja2Templates(directory=template_path)

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)

db_uri = env['DATABASE']
salt = env['SALT']
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ==================================================================
#                           AUTHENTICATION 
# ==================================================================

@auth_router.get('/signin', response_class=HTMLResponse)
async def get_user_signin(request: Request):
    return templates.TemplateResponse('sign-in.html', {'request': request})

@auth_router.post('/signin')
async def post_user_signin(email: str=Form(...), password: str=Form(...)):

    try: 
        password_hash = hash_input(password)
        password_hash = hash_password(password_hash, salt)
        user_info = await UserInfo.find({"email": email, "password": password_hash}).to_list()
        username = user_info[0].firstname + user_info[0].lastname
        password_verified = verify_password(password_hash, user_info[0].password)

        if user_info == None or password_verified == False: 
            raise HTTPException(status_code=404, detail="User not found")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key='access_token', value=access_token, httponly=True)
    except: 
        response = RedirectResponse(url='/signin', status_code=status.HTTP_303_SEE_OTHER)
    return response

@auth_router.get('/signup', response_class=HTMLResponse)
async def get_auth_user_signup(request:Request):
    return templates.TemplateResponse('sign-up.html', {'request': request})

@auth_router.post('/signup')
async def post_user_signup(firstname: str=Form(...), lastname: str=Form(...), email: str=Form(...), password: str=Form(...)):
    password_hash = hash_input(password)
    password = hash_password(password_hash, salt)
    if firstname == None or lastname == None: 
        firstname = hash_input(email)
        lastname = hash_input(firstname)
    user_info = UserInfo(firstname=firstname, lastname=lastname, 
                         email=email, password=password)
    
    await user_info.insert()

    response = RedirectResponse('signin', status_code=status.HTTP_303_SEE_OTHER)
    return response

@auth_router.get('/signout')
async def get_auth_user_signout(response: Response):
    response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response
# ==================================================================


# ==================================================================
#                           OAuth 
# ==================================================================
google_config = {
    'GOOGLE_CLIENT_ID': env['GOOGLE_CLIENT_ID'],
    'GOOGLE_CLIENT_SECRET': env['GOOGLE_CLIENT_SECRET']
}
st_gg_config = Config(environ=google_config)
gg_oath = OAuth(st_gg_config)
gg_oath.register(
    name='google', 
    server_metadata_url=env['GOOGLE_CONF_URL'],
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@auth_router.get('/google_login')
async def google_login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('google_auth')
    print(redirect_uri)
    return await gg_oath.google.authorize_redirect(request, redirect_uri)

@auth_router.get('/google_signup')
async def google_login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('google_auth')
    print(redirect_uri)
    return await gg_oath.google.authorize_redirect(request, redirect_uri)


@auth_router.get('/google_auth')
async def google_auth(request: Request):
    print('google_auth')
    try:
        token = await gg_oath.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    print(user)
    # request.session['user'] = dict(user)
    username = user['name']
    user_email = user['email']

    user_info = await UserInfo.find({"email": user_email}).to_list()
    print(user_info)
    if not user_info: 
        firstname = user['given_name']
        lastname = user['family_name']
        password = hash_password(str(user_email) + str(username), salt=salt)
        user_info = UserInfo(firstname=firstname, lastname=lastname, 
                        email=user_email, password=password)
        await user_info.insert()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    return response
# ==================================================================
