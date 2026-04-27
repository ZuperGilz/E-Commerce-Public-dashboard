# 🛒 Brazilian E-Commerce Analytics Dashboard

Dashboard interaktif berbasis Streamlit untuk menganalisis data Brazilian E-Commerce (Olist Dataset).  
Dashboard ini digunakan untuk mengeksplorasi pola pendapatan, kategori produk, serta hubungan antara waktu pengiriman dan kepuasan pelanggan.

---

## 📊 Fitur Dashboard

- Key Performance Indicators (KPI)
  - Total pendapatan
  - Total pesanan
  - Rata-rata review
  - Rata-rata waktu pengiriman
  - Tingkat keterlambatan

- Analisis Kategori Produk
  - Top kategori berdasarkan pendapatan
  - Visualisasi distribusi revenue

- Analisis Pengiriman
  - Hubungan waktu pengiriman dengan review
  - Perbandingan pesanan tepat waktu vs terlambat

- Filter Interaktif
  - Filter berdasarkan tahun
  - Pengaturan jumlah top kategori

---

## 📁 Struktur Folder
project/
│
├── dashboard.py
├── requirements.txt
├── README.md
│
├── orders_dataset.csv
├── order_items_dataset.csv
├── order_reviews_dataset.csv
├── products_dataset.csv
├── product_category_name_translation.csv


---

## ⚙️ Cara Menjalankan Dashboard

### 1. Clone / Download Project
```bash
git clone <repository-url>
cd project
pip install -r requirements.txt
streamlit run app.py
http://localhost:8501
