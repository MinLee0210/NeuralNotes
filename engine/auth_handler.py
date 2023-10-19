import os
import sys, yaml
import platform

from datetime import datetime, timedelta
from jose import JWTError, jwt
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # NeuralNotes root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if platform.system() != 'Windows':
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)


# Run in cmd: openssl rand -hex 32
SECRET_KEY = env['SECRET_KEY']
ALGORITHM = env['ALGORITHM']

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(input_pwd, hash_pwd):
    if input_pwd == hash_pwd:
        return True
    return


def get_current_user(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return username