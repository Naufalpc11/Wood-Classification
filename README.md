# Wood Knots Detection

Tugas Besar Mata Kuliah Pengolahan Citra Digital - Kelompok 3A

Sistem untuk mendeteksi dan menganalisis cacat mata kayu (wood knots) pada gambar kayu menggunakan teknik pengolahan citra digital.

## Struktur Project

```
tubes-pcd/
├── backend/                   # Flask API
│   ├── app.py
│   ├── requirements.txt
│   └── processing/            # Modul pengolahan citra
│
└─── frontend/                 # Vue 3 + Tailwind CSS
      └── src/
          ├── components/      # Komponen UI
          ├── pages/           # Halaman
          └── assets/          # CSS & assets


```

## Cara Menjalankan

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Server berjalan di `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Buka `http://localhost:5173`

## Fitur

- Upload gambar kayu (drag & drop atau klik)
- Visualisasi pipeline preprocessing (6 tahap)
- Deteksi wood knots dengan bounding box
- Ekstraksi fitur GLCM dan tekstur
- Analisis komparatif teknik-teknik yang digunakan

## Tech Stack

**Backend:** Flask, OpenCV, NumPy, Pillow, scikit-learn
**Frontend:** Vue 3, Vite, Tailwind CSS, Lucide Icons

## API

| Endpoint            | Method | Fungsi        |
| ------------------- | ------ | ------------- |
| `/api/health`       | GET    | Health check  |
| `/api/upload`       | POST   | Upload gambar |
| `/api/process/<id>` | POST   | Proses gambar |

## Tim

Kelompok 3A PCD - Informatika ITK

- Cinta Satilla (11221071)
- Michael Peter Valentino Situmeang (11231039)
- Muhammad Shadiq Al-Fatiy (11231065)
- Naufal Tiarana Putra (11231071)
- Rahmi Syafitri (11231085)

Dosen Pengampu: Rizky Amelia, S.Si., M.Han.
Asisten Matkul: Ahmad Maulana Rismadin, S.Kom.
