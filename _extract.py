"""Rombak tampilan timeline MOGOKIN: ekstrak konten, tulis ulang shell CSS."""
import re

SRC = 'index.html'
s = open(SRC, encoding='utf-8').read()

body_start = s.index('<div class="wrap">')
body_end = s.index('<script>')
body = s[body_start:body_end]

# ---- bersihkan markup lama ----
# hapus baris kosong berlebih
body = re.sub(r'\n\s*\n+', '\n', body)
# kompatibilitas: pill id lama dipertahankan, hanya kelas wadah yang dipetakan
open('_body.html', 'w', encoding='utf-8').write(body)
print('body chars', len(body))
print('h2 count', body.count('<h2'))
print('table count', body.count('<table'))
print('details count', body.count('<details'))