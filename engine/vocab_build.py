import os, pickle, pathlib, shutil

from tqdm import tqdm

def events2words(events:dict):
  n_events = len(events)
  events_arr = []
  for event in events:
    name = event['name']
    if name == 'Tempo Value':
      name = 'Tempo'
    value = event['value']
    word = name + '_' + str(value)
    events_arr.append(word)
  return events_arr


def building_vocab(dir):
    vocab = []
    for f in tqdm(os.listdir(dir), desc='Create vocabulary ... '):
        filename = os.path.join(dir, f)
        bar_pos, events = pickle.load(open(filename, 'rb'))
        words = events2words(events)
        for word in words: 
            vocab.append(word)
    return vocab

def splitting_filename(filename, format=['.mid', '.MID', '.midi']):
  for fm in format:
    if fm in filename:
      result = filename.replace(fm, '')
      return result, fm
  return None, None

def renaming_files(dir):
  file_idx = 0
  files = os.listdir(dir)
  for f in tqdm(files, desc='Renaming files ... '):
    filename, format = splitting_filename(f)
    if filename == None:
      continue
    old_name = os.path.join(dir, '{}{}'.format(filename, format))
    new_name = os.path.join(dir, '{}{}'.format(str(file_idx), format))
    if old_name not in dir:
      continue
    os.rename(old_name, new_name)
    file_idx += 1

class REMIConverter:
  def __init__(self, dir, tgt_dir=None):
    self.dir = dir
    self.engine = ConvertingEngine()
    if tgt_dir != None:
      self.engine.path_exist(tgt_dir)
      self.tgt_dir = tgt_dir

  def get_events_from_midis(self, midipath):
    note_items, tempo_items = read_items(str(midipath))
    note_items = quantize_items(note_items)
    chord_items = extract_chords(note_items)
    items = chord_items + tempo_items + note_items
    max_time = note_items[-1].end
    groups = group_items(items, max_time)
    midievents = item2event(groups)
    return midievents

  def get_events(self, event):
    name = event.name
    value = event.value

    if ' ' in name:
      name = name.replace(' ', '_')
    if type(value) == str and ':' in value:
      value = value.replace(':', '_')

    pair = {'name': name, 'value': value}
    return pair

  def get_remi_features(self, events):
    bar_event = []
    feature_ext = []

    for idx in range(len(events)):
      if events[idx].name == 'Bar':
        bar_event.append(idx)

      event = self.get_events(events[idx])
      feature_ext.append(event)

    result = (bar_event, feature_ext)
    return result

  def pickle_dump(self, obj, f):
    pickle.dump(obj, open(f, 'wb+'), protocol=pickle.HIGHEST_PROTOCOL)

  def run(self):
    idx = 0
    for filename in tqdm(os.listdir(self.dir), desc='Processing MIDI to REMI events'):
      try:
        file_path = os.path.join(self.dir, filename)
        sample_events = self.get_events_from_midis(file_path)
        sample_features = self.get_remi_features(sample_events)
        if self.tgt_dir:
          sample_name = os.path.join(self.tgt_dir, f'{idx}.pkl')
          self.pickle_dump(sample_features, sample_name)
        else:
          sample_name = os.path.join(self.dir, f'{idx}.pkl')
          self.pickle_dump(sample_features, sample_name)
        idx += 1
      except:
        print(f'Processing files No.{idx} get errors. Passing this file.')
        continue
      

class ConvertingEngine:
  def __init__(self):
    pass

  def path_exist(self,dir):
    if not os.path.exists(dir):
      print(f'Make dir {dir}')
      os.mkdir(dir)

  def extract_name(self, dir):
    name = dir.split('/')[-1]
    return name

  def splitting_filename(self, filename, format=['.mid', '.MID']):
    for fm in format:
      if fm in filename:
        result = filename.replace(fm, '')
        return result, fm
    return None, None

  def measuring(self, dir):
    files = os.listdir(dir)
    w_file = 0
    print(f'There are {len(files)} in {dir}')
    for content in files:
      src_file = os.path.join(dir, content)
      w = os.path.getsize(src_file)
      w_file += w
    equi_w = self.format_bytes(w_file)
    print(f'There are {w_file} bytes, equivalent to {equi_w}')

  def format_bytes(self, size):
      # 2**10 = 1024
      power = 2**10
      n = 0
      power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
      while size > power:
          size /= power
          n += 1
      return size, power_labels[n]+'bytes'


class TransferingFiles:
  def __init__(self):
    self.engine = ConvertingEngine()

  def transfering_files(self, src_dir, tgt_dir, format):
    resource = pathlib.Path(src_dir)
    for fm in format:
      print(f'Extracting format {fm} ...')
      pattern = f'*{fm}'
      for src_file in tqdm(list(resource.rglob(pattern)), desc='Transfering file ...'):
        src_file = str(src_file)
        filename = self.engine.extract_name(src_file)
        tgt_file = os.path.join(tgt_dir, filename)
        shutil.copy(src_file, tgt_file)

  def renaming_files(self, dir, format):
    file_idx = 0
    files = os.listdir(dir)
    for f in tqdm(files, desc='Renaming files ... '):
      filename, format = self.engine.splitting_filename(f, format=format)
      if filename == None:
        continue
      old_name = os.path.join(dir, '{}{}'.format(filename, format))
      new_name = os.path.join(dir, '{}{}'.format(str(file_idx), format))
      if old_name not in dir:
        continue
      os.rename(old_name, new_name)
      file_idx += 1

  def run(self, src_dir, tgt_dir, format=['.mid', '.MID', '.midi']):
    self.engine.path_exist(tgt_dir)
    self.transfering_files(src_dir=src_dir, tgt_dir=tgt_dir, format=format)
    self.engine.measuring(dir=tgt_dir)
    self.renaming_files(dir=tgt_dir, format=format)