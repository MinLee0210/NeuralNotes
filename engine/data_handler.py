import yaml
import os, pickle

import numpy as np

from tqdm import tqdm
from models.data_piece import ContentPiece, AttributePiece, DataPiece


from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .utils import pickle_load, pickle_dump

src_dir = r'agent\remi_dataset'
leaf_polyph = r'agent\remi_dataset\attr_cls\polyph'
leaf_rhythm = r'agent\remi_dataset\attr_cls\rhythm'
dataset_name = 'AILabs.tw-Pop1K7'

tgt_dir = r'dataset\resource'
tgt_leaf_polyph = r'dataset\resource\polyph'
tgt_leaf_rhythm = r'dataset\resource\rhythm'

def is_file(filename, format):
  if format in str(filename):
    return True
  return False

def npint2native(events: list):
  for event in events: 
    e_value = event['value']
    if type(e_value) == np.int64 or type(e_value) == np.int32:
        event['value'] = int(e_value)

  return events

async def init():
    # Create Motor client
    client = AsyncIOMotorClient(
        "mongodb://user:pass@host:27017"
    )

    # Initialize beanie with the Product document class and a database
    await init_beanie(database=client.db_name, document_models=[DataPiece])


async def storing_lcl_db(dataset_name=None, version=None):
   if dataset_name:
      dataset_name = dataset_name
   else: 
      dataset_name = 'Unknown'

   if version: 
      version = version 
   else: 
      version = 'Unknown'

   for filename in tqdm(os.listdir(src_dir), desc='Transfering to DB ... '):
    name = filename
    filename = os.path.join(src_dir, filename)
    if not is_file(filename, format='.pkl'):
        continue

    # Gather a file that contain events. 
    bar_pos, events = pickle_load(filename)
    events = npint2native(events=events)
    content_piece = ContentPiece(name=name, bar_pos=bar_pos, content=events)

    # Go to leaf dir to gather appropriate attribute-files to the file. 
    polyph_file = os.path.join(leaf_polyph, name)
    rhythm_file = os.path.join(leaf_rhythm, name)

    pol_content = pickle_load(polyph_file)
    rhy_content = pickle_load(rhythm_file)

    attr_piece = AttributePiece(polyph=pol_content, rythm=rhy_content)
    
    # Store to DB. 
    data_piece = DataPiece( 
                           dataset=dataset_name, 
                           version=version,
                           content=content_piece, 
                           attr_cls=attr_piece)
    
    await data_piece.insert()


def initialize_local_db(data_collection, tgt_dir, tgt_leaf_polyph, tgt_leaf_rhythm): 
    for document in tqdm(data_collection, desc='Intializing Local DB'): 
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
    samples = [sample for sample in os.listdir(tgt_dir) if '.pkl' in sample]
    if len(samples) <= k_samples:
        print('Small than expected') 
        return 
    rand_idx = np.random.choice(len(samples), k_samples, replace=False)
    for idx in tqdm(range(k_samples), desc='Removing files'):
        rand_sample = samples[rand_idx[idx]]
        rand_file = os.path.join(tgt_dir, rand_sample)
        rand_polyph = os.path.join(tgt_leaf_polyph, rand_sample)
        rand_rhythm = os.path.join(tgt_leaf_rhythm, rand_sample)

        os.remove(rand_file)
        os.remove(rand_polyph)
        os.remove(rand_rhythm)
