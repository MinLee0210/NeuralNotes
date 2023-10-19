# Use for automatically update local dataset for usage. 
import os, time
import asyncio
import yaml
from pathlib import Path

import numpy as np

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


from engine.utils import pickle_dump
from models.data_piece import DataPiece

# ==================================================================
#                      CONFIGURATION
# ==================================================================

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # NeuralNotes root directory
static_path = os.path.join(str(ROOT), 'ui', 'static')
template_path = os.path.join(str(ROOT), 'ui', 'templates')
soundfont_dir = os.path.join(str(ROOT), 'engine', 'soundfonts', 'default.sf2')

env = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
# ==================================================================

async def initialize_local_db(tgt_dir, tgt_leaf_polyph, tgt_leaf_rhythm, n_samples=20): 
    client = AsyncIOMotorClient(
        "mongodb://localhost:27017"
    )
    # Initialize beanie with the Sample document class and a database
    await init_beanie(database=client.NeuralNotes, document_models=[DataPiece])
    print('Intializing Local DB')
    data_collection = await DataPiece.find().aggregate([{'$sample': {'size': n_samples}}]).to_list()
    for document in data_collection: 
        id, dataset, version, content, attr_cls = document.values()

        name, bar_pos, events = content.values()
        polyph, rhythm = attr_cls.values()

        tgt_filename = os.path.join(tgt_dir, name)
        tgt_polyph = os.path.join(tgt_leaf_polyph, name)
        tgt_rhythm = os.path.join(tgt_leaf_rhythm, name)

        pickle_dump((bar_pos, events), f=tgt_filename)
        pickle_dump(polyph, tgt_polyph)
        pickle_dump(rhythm, tgt_rhythm)

def remove_samples_from_local_db(tgt_dir, tgt_leaf_polyph, tgt_leaf_rhythm, k_samples=10):
    print('Removing Files')
    samples = [sample for sample in os.listdir(tgt_dir) if '.pkl' in sample]
    if len(samples) <= k_samples:
        print('Small than expected') 
        return 
    rand_idx = np.random.choice(len(samples), k_samples, replace=False)
    for idx in range(k_samples):
        rand_sample = samples[rand_idx[idx]]
        rand_file = os.path.join(tgt_dir, rand_sample)
        rand_polyph = os.path.join(tgt_leaf_polyph, rand_sample)
        rand_rhythm = os.path.join(tgt_leaf_rhythm, rand_sample)

        os.remove(rand_file)
        os.remove(rand_polyph)
        os.remove(rand_rhythm)

# ==================================================================

tgt_dir = env['ROUTE']['resource']
tgt_leaf_polyph = os.path.join(tgt_dir, 'attr_cls', 'polyph')
tgt_leaf_rhythm = os.path.join(tgt_dir, 'attr_cls', 'rhythm')

n_samples = 100
k_samples = 95
period_time = 60 * 30

if __name__ == "__main__":
    # Initialize beanie with the Product document class and a database
    asyncio.run(initialize_local_db(tgt_dir, tgt_leaf_polyph, tgt_leaf_rhythm, n_samples))
    with open(r'log.txt', 'a') as file: 
        moment = time.ctime()
        samples = [sample for sample in os.listdir(tgt_dir) if '.pkl' in sample]
        sentence = f'[{moment}] Adding {n_samples} from {tgt_dir}, there are {len(samples)} left. \n'
        file.write(sentence)

    while True: 
        time.sleep(period_time)

        remove_samples_from_local_db(tgt_dir, tgt_leaf_polyph, tgt_leaf_rhythm, k_samples=k_samples)
        with open(r'log.txt', 'a') as file: 
            moment = time.ctime()
            samples = [sample for sample in os.listdir(tgt_dir) if '.pkl' in sample]
            sentence = f'[{moment}]: Remove {k_samples} from {tgt_dir}, there are {len(samples)} left. \n'
            file.write(sentence)

        asyncio.run(initialize_local_db(tgt_dir, tgt_leaf_polyph, tgt_leaf_rhythm, n_samples))
        with open(r'log.txt', 'a') as file: 
            moment = time.ctime()
            samples = [sample for sample in os.listdir(tgt_dir) if '.pkl' in sample]
            sentence = f'[{moment}] Adding {n_samples} from {tgt_dir}, there are {len(samples)} left. \n'
            file.write(sentence)
