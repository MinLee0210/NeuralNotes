import torch
from torch import nn
import torch.nn.functional as F

from .transformer_helpers import generate_causal_mask

class VAETransformerDecoder(nn.Module):
  def __init__(self, n_layer, n_head, d_model, d_ff, d_seg_emb, dropout=0.1, activation='relu', cond_mode='in-attn'):
    super(VAETransformerDecoder, self).__init__()
    self.n_layer = n_layer
    self.n_head = n_head
    self.d_model = d_model
    self.d_ff = d_ff
    self.d_seg_emb = d_seg_emb
    self.dropout = dropout
    self.activation = activation
    self.cond_mode = cond_mode

    if cond_mode == 'in-attn':
      self.seg_emb_proj = nn.Linear(d_seg_emb, d_model, bias=False)
    elif cond_mode == 'pre-attn':
      self.seg_emb_proj = nn.Linear(d_seg_emb + d_model, d_model, bias=False)

    self.decoder_layers = nn.ModuleList()
    for i in range(n_layer):
      self.decoder_layers.append(
        nn.TransformerEncoderLayer(d_model, n_head, d_ff, dropout, activation)
      )

  def forward(self, x, seg_emb):
    if not hasattr(self, 'cond_mode'):
      self.cond_mode = 'in-attn'
    attn_mask = generate_causal_mask(x.size(0)).to(x.device)
    # print (attn_mask.size())

    if self.cond_mode == 'in-attn':
      seg_emb = self.seg_emb_proj(seg_emb)
    elif self.cond_mode == 'pre-attn':
      x = torch.cat([x, seg_emb], dim=-1)
      x = self.seg_emb_proj(x)

    out = x
    for i in range(self.n_layer):
      if self.cond_mode == 'in-attn':
        out += seg_emb
      out = self.decoder_layers[i](out, src_mask=attn_mask)

    return out
  

class VAETransformerDecoderV2(nn.Module):
  def __init__(self, n_layer, n_head, d_model, d_ff, d_seg_emb, dropout=0.1, activation='relu', cond_mode='in-attn'):
    super(VAETransformerDecoder, self).__init__()
    self.n_layer = n_layer
    self.n_head = n_head
    self.d_model = d_model
    self.d_ff = d_ff
    self.d_seg_emb = d_seg_emb
    self.dropout = dropout
    self.activation = activation
    self.cond_mode = cond_mode

    if cond_mode == 'in-attn':
      self.seg_emb_proj = nn.Linear(d_seg_emb, d_model, bias=False)
    elif cond_mode == 'pre-attn':
      self.seg_emb_proj = nn.Linear(d_seg_emb + d_model, d_model, bias=False)

    self.decoder_layers = nn.ModuleList()
    for i in range(n_layer):
      self.decoder_layers.append(
        nn.TransformerEncoderLayer(d_model, n_head, d_ff, dropout, activation)
      )

  def forward(self, x, seg_emb):
    if not hasattr(self, 'cond_mode'):
      self.cond_mode = 'in-attn'
    attn_mask = generate_causal_mask(x.size(0)).to(x.device)

    if self.cond_mode == 'in-attn':
      seg_emb = self.seg_emb_proj(seg_emb)
    elif self.cond_mode == 'pre-attn':
      x = torch.cat([x, seg_emb], dim=-1)
      x = self.seg_emb_proj(x)

    out = x
    for i in range(self.n_layer):
      if self.cond_mode == 'in-attn':
        out += seg_emb
      out = self.decoder_layers[i](out, src_mask=attn_mask)

    return out