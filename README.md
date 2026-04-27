# 🛒 Brazilian E-Commerce Analytics Dashboard

Dashboard interaktif berbasis Streamlit untuk menganalisis data Brazilian E-Commerce (Olist Dataset).  
Dashboard ini digunakan untuk mengeksplorasi pola pendapatan, kategori produk, serta hubungan antara waktu pengiriman dan kepuasan pelanggan.

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

E-Commerce-Public-dashboard/
│
├── dashboard.py
├── requirements.txt
├── README.md
├── orders_dataset.csv
├── order_items_dataset.csv
├── order_reviews_dataset.csv
├── products_dataset.csv
└── product_category_name_translation.csv

---

## ⚙️ Cara Menjalankan Dashboard

### 1. Clone / Download Project
Buka terminal/command prompt Anda dan jalankan perintah berikut:

```bash
# Clone repositori
git clone [https://github.com/ZuperGilz/E-Commerce-Public-dashboard.git](https://github.com/ZuperGilz/E-Commerce-Public-dashboard.git)

# Masuk ke direktori proyek
cd E-Commerce-Public-dashboard

# Instal library yang dibutuhkan
pip install -r requirements.txt

# Jalankan aplikasi Streamlit
streamlit run dashboard.py
