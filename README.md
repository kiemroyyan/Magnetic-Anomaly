# Magnetic Anomaly Mapping – Tkinter GUI Application

Aplikasi GUI untuk memetakan **Anomali Magnetik Total** menggunakan Python.  
Dibangun dengan **Tkinter**, **Matplotlib**, dan **RBFInterpolator (SciPy)** untuk menghasilkan peta kontur dan grafik profil yang halus dan interaktif.

Aplikasi ini dirancang untuk kebutuhan analisis geofisika—khususnya pemetaan data magnetik di lapangan.

---

## Fitur Utama

### 🗺️ 1. **Peta Kontur (2D Magnetic Anomaly Map)**
- Interpolasi menggunakan **Thin Plate Spline RBF**
- Kontur berwarna (256 levels) dengan colormap *jet*
- Titik pengukuran ditampilkan lengkap dengan label
- Colorbar otomatis

### 📉 2. **Grafik Profil**
- Sorting otomatis berdasarkan nomor titik (misal: M21 → M40)
- Smoothing menggunakan **Cubic Interpolation**
- Menampilkan titik asli + kurva halus
- Label titik otomatis

### 📁 3. **Manajemen Data**
- Load file Excel (*.xlsx*)  
- Validasi struktur data (*x, y, Anomali Magnetik*)
- Cleaning otomatis untuk nilai kosong atau non-numeric

### 💾 4. **Ekspor Hasil**
- Save peta kontur (PNG)
- Save grafik profil (PNG)
- Save semua sekaligus + ekspor data CSV

---

## 🧰 Requirements

Install semua dependency:

```
pip install -r requirements.txt
```

---

## 🛠 Teknologi yang Digunakan

- **Python 3.x**
- **Tkinter** – GUI utama
- **Matplotlib** – visualisasi
- **SciPy (RBFInterpolator, interp1d)** – interpolasi
- **Pandas** – load & cleaning data
- **NumPy** – numerik

---

## 📂 Struktur Folder

```
Magnetic-Anomaly/
│
├── src/
│   └── app.py                # main program
│
├── data/
│   └── contoh.xlsx           # optional sample
│
├── output/
│   └── (hasil peta & grafik)
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ Cara Menjalankan Aplikasi

1. Clone repository:
   ```
   git clone https://github.com/kiemroyyan/Magnetic-Anomaly.git
   ```

2. Masuk ke direktori:
   ```
   cd Magnetic-Anomaly
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi:
   ```
   python src/app.py
   ```
