import torch
import yaml

from .model.musemorphose import MuseMorphose, MuseMorphoseV2, MuseMorphoseV3

version_control = ['original', 'version_2', 'version_3']
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class Factory:
    def __init__(self, version='original'): 
        if version in version_control:
            self.version = version
        else: 
            self.version = None
            print('We do not have your input version, we serve \n{}'.format(version_control))

    def generate(self, dset): 
        if self.version == version_control[0]: 
            config = yaml.load(open('./config/musemorphose_small_v1.yaml', 'r'), Loader=yaml.FullLoader)
            mconf =  config['model']
            model = MuseMorphose(
            mconf['enc_n_layer'], mconf['enc_n_head'], mconf['enc_d_model'], mconf['enc_d_ff'],
            mconf['dec_n_layer'], mconf['dec_n_head'], mconf['dec_d_model'], mconf['dec_d_ff'],
            mconf['d_latent'], mconf['d_embed'], dset.vocab_size,
            d_polyph_emb=mconf['d_polyph_emb'], d_rfreq_emb=mconf['d_rfreq_emb'],
            cond_mode=mconf['cond_mode']
            ).to(device)
            ckpt_path = config['training']['ckpt_dir']
            model.eval()
            model.load_state_dict(torch.load(ckpt_path, map_location='cpu'))
        elif self.version == version_control[1]: 
            config = yaml.load(open('./config/musemorphose_small_v2.yaml', 'r'), Loader=yaml.FullLoader)
            mconf =  config['model']
            model =  MuseMorphoseV2(
            mconf['enc_n_layer'], mconf['enc_n_head'], mconf['enc_d_model'], mconf['enc_d_ff'],
            mconf['dec_n_layer'], mconf['dec_n_head'], mconf['dec_d_model'], mconf['dec_d_ff'],
            mconf['d_latent'], mconf['d_embed'], dset.vocab_size,
            d_polyph_emb=mconf['d_polyph_emb'], d_rfreq_emb=mconf['d_rfreq_emb'],
            cond_mode=mconf['cond_mode'], gen_len=mconf['gen_len'], gen_mode=mconf['gen_mode']
            ).to(device)
            ckpt_path = config['training']['ckpt_dir']
            model.eval()
            model.load_state_dict(torch.load(ckpt_path, map_location='cpu'))
        else: 
            config = yaml.load(open('./agent/config/musemorphose_small_v3.yaml', 'r'), Loader=yaml.FullLoader)
            mconf =  config['model']
            model = MuseMorphoseV3(
            mconf['enc_n_layer'], mconf['enc_n_head'], mconf['enc_d_model'], mconf['enc_d_ff'],
            mconf['dec_n_layer'], mconf['dec_n_head'], mconf['dec_d_model'], mconf['dec_d_ff'],
            mconf['d_latent'], mconf['d_embed'], dset.vocab_size,
            d_polyph_emb=mconf['d_polyph_emb'], d_rfreq_emb=mconf['d_rfreq_emb'],
            cond_mode=mconf['cond_mode'], gen_len=mconf['gen_len'], gen_mode=mconf['gen_mode']
            ).to(device)
            ckpt_path = config['training']['ckpt_dir']
            model.eval()
            model.load_state_dict(torch.load(ckpt_path, map_location='cpu'))
        return model, config