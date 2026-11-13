"""Rakit ulang index.html dari sumber asli HEAD, lebih hati-hati."""
import re

orig = open('_orig.html', encoding='utf-8').read()
shell = open('_shell.html', encoding='utf-8').read()
script = open('_script.html', encoding='utf-8').read()

# --- ambil body asli ---
body = orig[orig.index('<div class="wrap">'):orig.index('<script>')]

# --- buang header lama UTUH (dari <header class="band"> sampai </header>) ---
h_start = body.index('<header class="band">')
h_end = body.index('</header>', h_start) + len('</header>')
body = body[:h_start] + '@@HEADER@@' + body[h_end:]

# --- buang blok progress lama UTUH (div seimbang), simpan penanda ---
p_start = body.index('<div class="progress">')
depth = 0
i = p_start
while True:
    nxt_open = body.find('<div', i)
    nxt_close = body.find('</div>', i)
    if nxt_close == -1:
        raise SystemExit('progress block tidak tertutup')
    if nxt_open != -1 and nxt_open < nxt_close:
        depth += 1
        i = nxt_open + 4
    else:
        depth -= 1
        i = nxt_close + 6
        if depth == 0:
            break
before = body[:p_start].rstrip()
after = body[i:].lstrip()
body = before + '\n\n  @@PROGRESS@@\n\n' + after

new_header = '''<header class="band">
  <p class="eyebrow">PBL-202601-07 · MOGOKIN · Fase Implementasi</p>
  <h1>Porsi Kerja &amp; Timeline UTS</h1>

  <p class="lede"><b>Status akhir 13 November 2026.</b> Seluruh revisi UTS 4 poin dari Pak Suko dan 7 poin revisi dosen sudah di-merge di kedua repo. Setelah revisi, peran ditukar agar jejak commit tiap anggota tersebar di dua repo: <b>Jizdan &amp; Ifa</b> menggarap <code>mogokin_backend</code>, <b>Raskha &amp; Rangga</b> menggarap <code>mogokin_app</code>. Fitur penarikan saldo dihapus total sesuai model bisnis tanpa dompet, dan alasan penolakan order kini dikirim ke API serta tampil di detail order admin. Kedua repo bertanda <code>vUTS-final</code> &mdash; backend <code>d4eefa5</code>, mobile <code>fa5b428</code> (<code>kai/main</code>).</p>

  <p class="lede">Dua tim, dua orang per modul. <b>Tim 1</b> (Jizdan &amp; Raskha) memegang alur order dan admin; <b>Tim 2</b> (Rangga &amp; Ifa) memegang autentikasi, notifikasi, dan tampilan pendukung. Sejak 27 Oktober seluruh alur order di Flutter tersambung ke API, bukan mock. Tanggal 29 Oktober alur penuh lulus 100&thinsp;% di HP fisik Redmi Note 9 Pro melawan backend sungguhan tanpa mock.</p>

  <div class="stamp">
    <span><b>Diperbarui</b> 13 November 2026</span>
    <span><b>Beku fitur</b> 30 Oktober 2026</span>
    <span><b>Revisi</b> selesai &mdash; tidak ada PR terbuka</span>
    <span><b>Progres UTS</b> 84&thinsp;%</span>
  </div>
</header>'''

new_progress = '''<div class="progress">
    <div class="progress-head">
      <div>
        <span class="progress-cap">Progress keseluruhan proyek &mdash; Milestone UTS</span>
        <span class="progress-num">84<small>&thinsp;%</small></span>
      </div>
      <div class="progress-tally">
        <span><b>13</b> sel selesai penuh</span>
        <span><b>6</b> sel sebagian</span>
        <span><b>0</b> belum mulai</span>
        <span><b>2</b> n/a</span>
      </div>
    </div>
    <div class="bar" role="img" aria-label="Dari 19 sel yang berlaku, 13 selesai dan 6 sebagian; hasilnya 84 persen">
      <i class="d" style="width:68.4%"></i>
      <i class="p" style="width:15.8%"></i>
    </div>
    <p>Dihitung per sel: 7 modul &times; 3 lapisan (backend, mobile, admin) = <b>21 sel</b>, dua di antaranya tidak berlaku, jadi <b>19 sel</b> dinilai. Persen tiap modul = (sel selesai + &frac12; sel sebagian) &divide; sel berlaku. Capaian fungsional UTS <b>(13 + 6 &times; 0,5) &divide; 19 = 84&thinsp;%</b>; skor konservatif murni tuntas <b>13 &divide; 19 = 68&thinsp;%</b>. Sel berlabel sebagian berarti fitur inti sudah berjalan untuk skenario demo, namun masih menyisakan catatan bug, penanganan edge-case, atau penyempurnaan menuju UAS.</p>
  </div>'''

body = body.replace('@@HEADER@@', new_header)
body = body.replace('@@PROGRESS@@', new_progress)

assert '@@' not in body, 'penanda tersisa'
assert body.count('<h2') == 5, 'jumlah bab berubah: %d' % body.count('<h2')

out = shell + '\n<div class="wrap">\n' + body.lstrip() + '\n' + script
open('index.html', 'w', encoding='utf-8').write(out)
print('OK, chars', len(out))