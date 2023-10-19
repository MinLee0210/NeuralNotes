import os
import sys
import platform
import hashlib
import uuid
import pickle
import numpy as np

from midi2audio import FluidSynth

from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # NeuralNotes root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if platform.system() != 'Windows':
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def midi_to_wav(mid_file, startpoint, endpoint=None, sample_rate=22050):
    soundfont = r'engine\soundfonts\default.sf2'
    st_point = os.path.join(startpoint, mid_file)
    fs = FluidSynth(sound_font=soundfont, sample_rate=sample_rate)
    filename = mid_file.split('.')[0] + '.wav'
    if endpoint is not None: 
        endpoint = os.path.join(endpoint, filename) # if endpoint is not clarified, files would be save at the same place as the startpoint. 
    else: 
        endpoint_path = os.path.join(startpoint, filename)
    fs.midi_to_audio(st_point, f'{endpoint_path}')

def write_bytes_to_mid(filename, content, dir='/audio'):
    filepath = os.path.join(ROOT, dir, filename)
    open(filepath, 'wb+').write(content)

def rand_samples(length, max, list_dir):
    samples = []
    for idx in range(length):
        rand_idx = np.random.randint(0, max)
        sample = list_dir[rand_idx]
        samples.append(sample)
    return samples

def generate_salt():
    salt = uuid.uuid4().hex
    return salt

def get_filename_from_storage(data_dir):
    # The dataset receive integer index as an input, therefore, a name of a file should be change. 
    file_storage = os.listdir(data_dir)
    files = [int(pkl_file.split('.')[0]) for pkl_file in file_storage if '.pkl' in pkl_file]
    files.sort()
    filename = files[-1]  + 1
    return filename

def hash_input(input_string):
    string = bytes(input_string, encoding='utf-8')
    sha256 = hashlib.sha256()
    sha256.update(string)
    result = sha256.hexdigest()
    return result

def hash_password(password, salt):
    temp_pwd = password + salt
    temp_pwd = bytes(temp_pwd, encoding='utf-8')
    sha512 = hashlib.sha512()
    sha512.update(temp_pwd)
    result = sha512.hexdigest()
    return result

def pickle_dump(obj, f):
    pickle.dump(obj, open(f, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

def pickle_load(path):
    return pickle.load(open(path, 'rb'))