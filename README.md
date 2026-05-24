color-eva
=========

Ringkasan
---------
color-eva adalah utilitas baris perintah (CLI) sederhana untuk mengirimkan kode warna (hex) ke layanan "EVA painter" dan menyimpan balasan JSON yang sudah diolah.

Persyaratan
-----------
- Python 3.8 atau lebih baru

Instalasi (cara cepat)
----------------------
1) Install untuk pengguna (membuat perintah `color-eva` tersedia):

```powershell
python -m pip install --user .
```

2) (Windows) Tambahkan folder `Scripts` Python user ke PATH — repo ini menyediakan helper `install-global.bat`:

```powershell
.\install-global.bat
# Setelah menjalankan helper: tutup dan buka kembali terminal
```

3) Alternatif terisolasi (pipx):

```powershell
pipx install .
```

4) Untuk pengembangan (editable install):

```powershell
python -m pip install -e .
```

Menjalankan tanpa instalasi
--------------------------
Jika belum ingin memasang paket, jalankan langsung dari folder proyek:

```powershell
python color-eva.py generate "#9D2A28"
```

Penggunaan CLI
-------------
Sintaks dasar:

```text
color-eva generate <color> [options]
```

Opsi utama:
- `-o, --out` : path file output yang diinginkan (jika tidak diberikan, file disimpan ke folder Downloads)
- `--open` : buka file hasil setelah disimpan
- `--retries N` : jumlah retry pada kegagalan jaringan (default: 2)
- `--timeout N` : batas waktu request (detik, default: 30)
- `--backoff N` : base backoff (detik, default: 1.0)
- `-v, --verbose` : tampilkan log debug

Contoh cepat:

```powershell
color-eva generate "#FF0000"
color-eva generate "#9D2A28" --out .\palette.json --open
```

Contoh menjalankan langsung tanpa menginstal:

```powershell
python -m color_eva.cli generate "#9D2A28"
```

Hasil output
------------
- Secara default file JSON disimpan ke folder Downloads sebagai `color-eva-generate-<HEX>.json` (HEX tanpa `#`).
- CLI mengonversi respons API menjadi array berisi objek yang memiliki kunci seperti `color-<group>-<scale>` dengan nilai `["#HEX", "rgb(r, g, b)"]`.

Contoh (potongan):

```json
[
  {
    "color-primary-100": ["#DDE7FA", "rgb(221, 231, 250)"],
    "color-primary-200": ["#BCCFF6", "rgb(188, 207, 246)"],
    "color-primary-300": ["#94ACE6", "rgb(148, 172, 230)"]
  }
]
```

Masalah umum & solusi
---------------------
- Jika perintah `color-eva` tidak ditemukan setelah instalasi user, pastikan folder `Scripts` user Python ada di PATH. Untuk mengetahui lokasinya jalankan:

```powershell
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```

Lalu tambahkan lokasi tersebut ke PATH (atau jalankan `install-global.bat` yang sudah disediakan). Tutup dan buka kembali terminal setelah mengubah PATH.

- Jika request ke server gagal: periksa koneksi internet dan coba tambahkan `--retries` atau ubah `--timeout`.

Catatan teknis untuk pengembang
--------------------------------
- Entrypoint console script didefinisikan di `pyproject.toml`: `color-eva = color_eva.cli:main`.
- Kode utama ada di: `color_eva/cli.py`.
- Untuk menjalankan tes atau melakukan perubahan cepat, gunakan `pip install -e .` lalu jalankan `color-eva` langsung.

Butuh bantuan lagi?
------------------
Jika masih bingung, beri tahu bagian mana yang kurang jelas — saya bisa menambahkan contoh lebih banyak atau screenshot langkah instalasi di Windows.


