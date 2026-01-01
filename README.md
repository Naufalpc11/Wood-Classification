# Wood Knots Detection

Tugas Besar Mata Kuliah Pengolahan Citra Digital - Kelompok 3A

Sistem untuk mendeteksi cacat kayu menggunakan **Machine Learning (Random Forest)** dengan teknik pengolahan citra digital. Mengklasifikasikan gambar kayu menjadi **Cacat** atau **Tidak Cacat**.

## Fitur Utama

- 🖼️ Upload gambar kayu (drag & drop atau klik)
- 🔬 Visualisasi pipeline preprocessing (7 tahap)
- 🤖 Klasifikasi ML: **Cacat / Tidak Cacat** dengan confidence score
- 📊 Ekstraksi fitur shape (num_knots, area, circularity, aspect_ratio)

## Struktur Project

```
tubes-pcd/
├── backend/                      # Flask API
│   ├── app.py                    # Endpoints
│   ├── requirements.txt
│   └── processing/
│       ├── __init__.py           # Image processing & ML
│       └── wood_classifier_rf.pkl  # Trained model
│
└── frontend/                     # Vue 3 + Tailwind CSS
    └── src/
        ├── components/           # UI components
        └── pages/                # Pages
```

## Cara Menjalankan

### Quick Start (Recommended) 🚀

**Double-click `start.bat`** di folder project, atau jalankan dari terminal:

```powershell
.\start.bat
```

Script akan otomatis:

1. Menjalankan Backend (Flask)
2. Menjalankan Frontend (Vite)
3. Membuka browser ke `http://localhost:5173`

### Manual Setup

**Backend:**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

### Re-train Model (Opsional)

1. Buka `ml.py` di Google Colab
2. Sesuaikan path dataset
3. Jalankan training
4. Export model ke `backend/processing/wood_classifier_rf.pkl`

## Pipeline Preprocessing

| Step | Teknik             | Deskripsi             |
| ---- | ------------------ | --------------------- |
| 1    | Image Resizing     | Resize ke max 512px   |
| 2    | Grayscale          | Konversi ke grayscale |
| 3    | CLAHE              | Enhance kontras lokal |
| 4    | Gaussian Blur      | Reduksi noise         |
| 5    | Binary Threshold   | Segmentasi            |
| 6    | Morphology         | Noise removal         |
| 7    | Feature Extraction | Shape features        |

## API Endpoints

| Endpoint             | Method | Fungsi                      |
| -------------------- | ------ | --------------------------- |
| `/api/health`        | GET    | Health check                |
| `/api/upload`        | POST   | Upload gambar               |
| `/api/process/<id>`  | POST   | Proses & klasifikasi gambar |
| `/api/classify/<id>` | POST   | Klasifikasi saja            |

## Model ML

- **Algorithm**: Random Forest
- **Accuracy**: ~94%
- **Features**: num_knots, total_area, avg_circularity, avg_aspect_ratio
- **Classes**: Tidak Cacat (0), Cacat (1)

## Tech Stack

**Backend:** Flask, OpenCV, NumPy, scikit-learn, joblib  
**Frontend:** Vue 3, Vite, Tailwind CSS, Lucide Icons

## Tim

Kelompok 3A PCD - Informatika ITK

- Cinta Satilla (11221071)
- Michael Peter Valentino Situmeang (11231039)
- Muhammad Shadiq Al-Fatiy (11231065)
- Naufal Tiarana Putra (11231071)
- Rahmi Syafitri (11231085)

Dosen Pengampu: Rizky Amelia, S.Si., M.Han.  
Asisten Matkul: Ahmad Maulana Rismadin, S.Kom.
