# REPO-PROJECT-1---MINI-GAME-BASED-ON-HAND-COLOR

Game mengemudi 2D interaktif yang dikembangkan menggunakan **Python**, **Pygame**, dan **OpenCV**. Proyek ini menggabungkan mekanika game arcade klasik dengan kontrol berbasis *computer vision* untuk mendeteksi kemudi atau gerakan secara real-time melalui kamera web.

---

## Fitur Utama
* **Menu Utama & State Management:** Alur game yang rapi antara layar Menu Utama (*Start Menu*) dan Gameplay.
* **Integrasi OpenCV:** Pemrosesan frame kamera secara real-time untuk mendeteksi kontrol kemudi (*steering*).
* **Mekanika Player & Hitbox Presisi:** Karakter mobil dengan logika *lean angle* (kemiringan sudut saat berbelok), sistem *hitbox* ganda (normal dan kecil), serta efek visual saat terkena tabrakan (*hit timer*).
* **Sistem Lingkungan & NPC:** Manajemen jalan yang berputar (*scrolling road*) dan rintangan NPC dinamis.
* **UI & Alat Kalibrasi Warna:** Fitur pendukung untuk debugging warna langsung dari layar Pygame menggunakan klik mouse (`hsva`).

---

## Teknologi yang Digunakan
* **Python 3.10+**
* **Pygame** (Rendering game, sprite, dan UI)
* **OpenCV (`cv2`)** (Pengambilan video dan pemrosesan citra komputer)
* **NumPy** (Manipulasi array dan data piksel)

---

## Struktur Proyek
```text
PCV_Game/
│
├── main.py          # Script utama (Game loop, state menu & gameplay, event handler)
├── mechanic.py      # Modul kelas (Player, Road, NPC, dan logika sprite)
└── control.py       # Modul Kendali berbasis warna (CameraProcessor)
```

## Cara Instalasi
1. Clone repository ini (atau pastikan semua file berada dalam satu folder):

```
git clone [https://github.com/Kun-a-i/REPO-PROJECT-1---MINI-GAME-BASED-ON-HAND-COLOR](https://github.com/Kun-a-i/REPO-PROJECT-1---MINI-GAME-BASED-ON-HAND-COLOR)
```
2. Install dependencies yang diperlukan:
```
pip install pygame opencv-python numpy
```

3. Jalankan game:
```
python main.py
```
## Panduan Main
Untuk menggunakan kendali berbasis citra diperlukan hal berikut.
1. Tangan Kiri menggunakan marker biru. Tangan Kanan menggunakan marker merah. Disarankan menggunakan marker berukuran setidaknya 3x3 cm.
2. Lakukan kalibrasi dengan menjalankan `main.py` dan klik marker yang tampil ketika bermain. Mobil pemain dapat dikendalikan menggunakan `a` dan `d` atau `<-` dan `->` selama kalibrasi.
3. Perhatikan nilai HSV dari marker pada terminal.
```
H : 60.0, S : 255.0, V : 200.00000000000003
H : 60.0, S : 255.0, V : 200.00000000000003
H : 60.0, S : 255.0, V : 200.00000000000003
H : 60.0, S : 255.0, V : 200.00000000000003
```
4. Ubah nilai threshold mask pada `control.py`.
