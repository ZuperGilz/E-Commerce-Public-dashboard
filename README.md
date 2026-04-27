# 🛒 Brazilian E-Commerce Analytics Dashboard

Dashboard interaktif berbasis Streamlit untuk menganalisis data Brazilian E-Commerce (Olist Dataset).  
Dashboard ini digunakan untuk mengeksplorasi pola pendapatan, kategori produk, serta hubungan antara waktu pengiriman dan kepuasan pelanggan.

🔗 **Live Demo:** [https://submission-analysis-data-agilmardian.streamlit.app/](https://submission-analysis-data-agilmardian.streamlit.app/)

---

## 📊 Fitur Dashboard

- **Key Performance Indicators (KPI)**
  - Total pendapatan
  - Total pesanan
  - Rata-rata review
  - Rata-rata waktu pengiriman
  - Tingkat keterlambatan

- **Analisis Kategori Produk**
  - Top kategori berdasarkan pendapatan
  - Visualisasi distribusi revenue dan tren bulanan

- **Analisis Pengiriman**
  - Hubungan waktu pengiriman dengan review score
  - Perbandingan distribusi rating pada pesanan tepat waktu vs terlambat

- **Filter Interaktif**
  - Filter rentang waktu (tanggal)
  - Pengaturan jumlah Top N kategori

---

## 📁 Struktur Folder

```
project/
│
├── dashboard/
│   ├── dashboard.py
│   ├── q1_df.csv
│   └── q2_df.csv
├── data/
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── order_dataset.csv
│   ├── product_category_name_translation.csv
│   └── products_dataset.csv
├── Proyek_Analisis_Data_Agil_Mardian_Hawari.ipynb
├── requirements.txt
└── README.md
```

---

## ⚙️ Cara Menjalankan Dashboard Secara Lokal

### 1. Clone Repository

```bash
git clone https://github.com/ZuperGilz/E-Commerce-Public-dashboard.git
cd E-Commerce-Public-dashboard
```

### 2. Setup Environment (Conda)

```bash
conda create --name main-ds python=3.9
conda activate main-ds
```

> Atau gunakan virtual environment bawaan Python:
> ```bash
> python -m venv venv
> source venv/bin/activate        # Linux / macOS
> venv\Scripts\activate           # Windows
> ```

### 3. Install Library

```bash
pip install -r requirements.txt
```

### 4. Jalankan Notebook (Generate Dataset)

Buka dan jalankan semua cell di notebook `Proyek_Analisis_Data_Agil_Mardian_Hawari.ipynb`.  
Pastikan seluruh cell dijalankan hingga bagian **Analisis Lanjutan** agar file `q1_df.csv` dan `q2_df.csv` tersimpan secara otomatis ke folder `dashboard/`.

### 5. Jalankan Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di browser pada alamat:

```
http://localhost:8501
```

---

## 👤 Profil Pembuat

**Nama:** Agil Mardian Hawari  
**Jurusan:** Informatika  
**Learning Path:** Data Scientist

- GitHub: [https://github.com/zupergilz](https://github.com/zupergilz)
- LinkedIn: [https://linkedin.com/in/agil-mardian-hawari](https://linkedin.com/in/agil-mardian-hawari)