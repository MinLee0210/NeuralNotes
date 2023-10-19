from torch import nn, optim
import torch


device = 'cuda' if torch.cuda.is_available() else 'cpu'

def validate(model, dloader, n_rounds=8, use_attr_cls=True):
  model.eval()
  loss_rec = []
  kl_loss_rec = []

  print ('[info] validating ...')
  with torch.no_grad():
    for i in range(n_rounds):
      print ('[round {}]'.format(i+1))

      for batch_idx, batch_samples in enumerate(dloader):
        model.zero_grad()

        batch_enc_inp = batch_samples['enc_input'].permute(2, 0, 1).to(device)
        batch_dec_inp = batch_samples['dec_input'].permute(1, 0).to(device)
        batch_dec_tgt = batch_samples['dec_target'].permute(1, 0).to(device)
        batch_inp_bar_pos = batch_samples['bar_pos'].to(device)
        batch_padding_mask = batch_samples['enc_padding_mask'].to(device)
        if use_attr_cls:
          batch_rfreq_cls = batch_samples['rhymfreq_cls'].permute(1, 0).to(device)
          batch_polyph_cls = batch_samples['polyph_cls'].permute(1, 0).to(device)
        else:
          batch_rfreq_cls = None
          batch_polyph_cls = None

        mu, logvar, dec_logits = model(
          batch_enc_inp, batch_dec_inp, 
          batch_inp_bar_pos, batch_rfreq_cls, batch_polyph_cls,
          padding_mask=batch_padding_mask
        )

        losses = model.compute_loss(mu, logvar, 0.0, 0.0, dec_logits, batch_dec_tgt)
        if not (batch_idx + 1) % 10:
          print ('batch #{}:'.format(batch_idx + 1), round(losses['recons_loss'].item(), 3))

        loss_rec.append(losses['recons_loss'].item())
        kl_loss_rec.append(losses['kldiv_raw'].item())
    
  return loss_rec, kl_loss_rec