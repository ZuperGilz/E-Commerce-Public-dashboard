import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brazilian E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
)

st.markdown("""
<style>
    .metric-card {
        background: var(--secondary-background-color);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-card .value {
        font-size: 28px;
        font-weight: 700;
        color: var(--primary-color);
    }
    .metric-card .label {
        font-size: 13px;
        color: var(--text-color);
        margin-top: 4px;
    }
    .insight-box {
        background: rgba(25, 118, 210, 0.1);
        border-left: 4px solid var(--primary-color);
        border-radius: 6px;
        padding: 12px 16px;
        margin-top: 12px;
        font-size: 14px;
        color: var(--text-color);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    orders   = pd.read_csv(os.path.join(base, 'orders_dataset.csv'))
    items    = pd.read_csv(os.path.join(base, 'order_items_dataset.csv'))
    reviews  = pd.read_csv(os.path.join(base, 'order_reviews_dataset.csv'))
    products = pd.read_csv(os.path.join(base, 'products_dataset.csv'))
    transl   = pd.read_csv(os.path.join(base, 'product_category_name_translation.csv'))

    dt_cols = ['order_purchase_timestamp', 'order_approved_at',
               'order_delivered_carrier_date', 'order_delivered_customer_date',
               'order_estimated_delivery_date']
    for col in dt_cols:
        orders[col] = pd.to_datetime(orders[col])

    orders   = orders[orders['order_status'] == 'delivered'].dropna(subset=['order_delivered_customer_date'])
    products['product_category_name'] = products['product_category_name'].fillna('unknown')
    reviews  = reviews.drop_duplicates(subset=['order_id'], keep='last')
    items    = items.drop_duplicates()

    products = products.merge(transl, on='product_category_name', how='left')
    products['product_category_name_english'] = (
        products['product_category_name_english'].fillna(products['product_category_name'])
    )

    df = orders.merge(items, on='order_id', how='inner')
    df = df.merge(products[['product_id', 'product_category_name_english']], on='product_id', how='left')
    df = df.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')

    df['delivery_time_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    df['revenue']    = df['price'] + df['freight_value']
    df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    df['month']      = df['order_purchase_timestamp'].dt.month
    df['year']       = df['order_purchase_timestamp'].dt.year
    df['is_late']    = df['order_delivered_customer_date'] > df['order_estimated_delivery_date']

    return df[df['year'].isin([2017, 2018])]

try:
    df = load_data()
    data_loaded = True
except FileNotFoundError as e:
    data_loaded = False
    missing_file = str(e)

st.markdown("# 🛒 Brazilian E-Commerce Analytics Dashboard")
st.markdown("**Dataset:** Brazilian E-Commerce &nbsp;|&nbsp; **Periode:** 2017–2018")
st.divider()

if not data_loaded:
    st.error(f"File dataset tidak ditemukan. Pastikan file CSV ada di folder `dashboard/`.\n\n`{missing_file}`")
    st.info("File yang dibutuhkan: `orders_dataset.csv`, `order_items_dataset.csv`, `order_reviews_dataset.csv`, `products_dataset.csv`, `product_category_name_translation.csv`")
    st.stop()

with st.sidebar:
    st.markdown("## Profil Pembuat")
    st.divider()
    st.markdown("""
    **Nama:** Agil Mardian Hawari  
    **Jurusan:** Informatika  
    **learning path:** Data Scienctist  

    📊 Tertarik pada analisis data, machine learning, dan visualisasi data interaktif.
    """)

    st.markdown("""
    - GitHub: https://github.com/zupergilz  
    - LinkedIn: https://linkedin.com/in/agil-mardian-hawari  
    """)
    st.divider()
    st.markdown("## 🔍 Filter Data")
    st.divider()
    
    # Ambil nilai minimum dan maksimum tanggal dari dataset
    min_date = df['order_purchase_timestamp'].min().date()
    max_date = df['order_purchase_timestamp'].max().date()
    
    # Buat input date_range
    # Streamlit akan mengembalikan tuple/list berisi 1 atau 2 tanggal
    date_range = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date], # Default value (pilih semua)
        min_value=min_date,
        max_value=max_date
    )
    
    top_n = st.slider("Top N Kategori", 5, 20, 10)
    st.divider()
    st.markdown("**Pertanyaan Bisnis:**\n1. Kategori produk dengan pendapatan tertinggi & trennya\n2. Hubungan waktu pengiriman dengan kepuasan pelanggan")

# Validasi input tanggal
# Saat user baru ngeklik 1 tanggal, panjang date_range = 1. 
# Kita butuh user milih tanggal awal dan akhir (panjang = 2)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.warning("Silakan pilih tanggal mulai dan tanggal akhir di sidebar.")
    st.stop()

# Terapkan Filter berdasarkan tanggal
fdf = df[(df['order_purchase_timestamp'].dt.date >= start_date) & 
         (df['order_purchase_timestamp'].dt.date <= end_date)]

if fdf.empty:
    st.warning("Tidak ada data untuk rentang waktu yang dipilih.")
    st.stop()

# KPI
st.markdown("### 📊 Key Performance Indicators")
c1, c2, c3, c4, c5 = st.columns(5)
total_rev    = fdf['revenue'].sum()
total_orders = fdf['order_id'].nunique()
avg_review   = fdf['review_score'].mean()
avg_delivery = fdf['delivery_time_days'].mean()
late_pct     = fdf['is_late'].mean() * 100
late_color   = "#D32F2F" if late_pct > 10 else "#43A047"

for col, val, label, clr in [
    (c1, f"R$ {total_rev/1e6:.1f}M",  "Total Pendapatan",        "#1976D2"),
    (c2, f"{total_orders:,}",          "Total Pesanan",            "#1976D2"),
    (c3, f"{avg_review:.2f} ⭐",       "Rata-rata Review",         "#1976D2"),
    (c4, f"{avg_delivery:.1f} hari",   "Avg. Delivery Time",       "#1976D2"),
    (c5, f"{late_pct:.1f}%",          "Tingkat Keterlambatan",    late_color),
]:
    col.markdown(f'<div class="metric-card"><div class="value" style="color:{clr}">{val}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── PERTANYAAN 1 ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## Kategori Produk dengan Pendapatan Tertinggi & Tren Bulanan")

rev_by_cat = (
    fdf.groupby('product_category_name_english')['revenue']
    .sum().reset_index()
    .sort_values('revenue', ascending=False)
    .head(top_n)
)
top5_cats = rev_by_cat.head(5)['product_category_name_english'].tolist()

monthly_rev = (
    fdf[fdf['product_category_name_english'].isin(top5_cats)]
    .groupby(['year_month', 'product_category_name_english'])['revenue']
    .sum().reset_index()
)
monthly_rev['ym_str'] = monthly_rev['year_month'].astype(str)

# Gunakan Plotly untuk interaktivitas
col1, col2 = st.columns(2)

with col1:
    fig_bar = px.bar(
        rev_by_cat.sort_values('revenue', ascending=True), 
        x='revenue', y='product_category_name_english',
        orientation='h',
        title=f"Top {top_n} Kategori Produk (Pendapatan)",
        labels={'revenue': 'Total Pendapatan (R$)', 'product_category_name_english': ''},
        color_discrete_sequence=['#1976D2']
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_line = px.line(
        monthly_rev, 
        x='ym_str', y='revenue', color='product_category_name_english',
        markers=True,
        title="Tren Pendapatan Bulanan Top 5 Kategori",
        labels={'revenue': 'Pendapatan (R$)', 'ym_str': 'Periode', 'product_category_name_english': 'Kategori'}
    )
    st.plotly_chart(fig_line, use_container_width=True)

# INSIGHT DINAMIS 1
top3_names = ", ".join([f"**{cat.replace('_', ' ').title()}**" for cat in top5_cats[:3]])
if not monthly_rev.empty:
    peak_idx = monthly_rev['revenue'].idxmax()
    peak_month = monthly_rev.loc[peak_idx, 'ym_str']
    peak_val = monthly_rev.loc[peak_idx, 'revenue']
else:
    peak_month, peak_val = "N/A", 0

st.markdown(f"""<div class="insight-box">
💡 <strong>Insight Dinamis:</strong> Berdasarkan periode waktu yang Anda pilih, kategori {top3_names} 
mendominasi pendapatan platform. Terlihat juga bahwa pendapatan tertinggi untuk salah satu kategori Top 5 
jatuh pada <strong>{peak_month}</strong> dengan nilai mencapai <strong>R$ {peak_val/1000:.1f} Ribu</strong>.
</div>""", unsafe_allow_html=True)


# ── PERTANYAAN 2 ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🚚 Hubungan Waktu Pengiriman & Kepuasan Pelanggan")

clean = fdf.dropna(subset=['review_score', 'delivery_time_days']).copy()
clean['review_score'] = clean['review_score'].astype(int)
clean['Status Pengiriman'] = np.where(clean['is_late'], 'Terlambat', 'Tepat Waktu')

delivery_review = (
    clean.groupby('review_score')['delivery_time_days']
    .mean().reset_index()
    .rename(columns={'delivery_time_days': 'avg_days'})
)

col3, col4 = st.columns(2)

with col3:
    fig_bar2 = px.bar(
        delivery_review, 
        x='review_score', y='avg_days',
        title="Rata-rata Waktu Pengiriman per Review Score",
        labels={'review_score': 'Review Score (1-5)', 'avg_days': 'Rata-rata Waktu (Hari)'},
        color='review_score',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_bar2, use_container_width=True)

with col4:
    fig_box = px.box(
        clean, 
        x='Status Pengiriman', y='review_score', color='Status Pengiriman',
        title="Distribusi Review Score: Tepat Waktu vs Terlambat",
        labels={'review_score': 'Review Score'},
        color_discrete_map={'Tepat Waktu': '#1565C0', 'Terlambat': '#B71C1C'}
    )
    st.plotly_chart(fig_box, use_container_width=True)

# INSIGHT DINAMIS 2
try:
    p1_days = delivery_review[delivery_review['review_score'] == 1]['avg_days'].values[0]
    p5_days = delivery_review[delivery_review['review_score'] == 5]['avg_days'].values[0]
    on_time_mean = clean[clean['Status Pengiriman'] == 'Tepat Waktu']['review_score'].mean()
    late_mean = clean[clean['Status Pengiriman'] == 'Terlambat']['review_score'].mean()
    
    st.markdown(f"""<div class="insight-box">
    💡 <strong>Insight Dinamis:</strong> Review score berkorelasi dengan lama pengiriman. 
    Review score 1 rata-rata dikirim dalam <strong>{p1_days:.1f} hari</strong>, sedangkan score 5 hanya
    <strong>{p5_days:.1f} hari</strong>. Pesanan yang <strong>terlambat</strong> mendapat rata-rata rating 
    <strong>{late_mean:.2f}</strong>, anjlok drastis dibanding pesanan tepat waktu (<strong>{on_time_mean:.2f}</strong>).
    </div>""", unsafe_allow_html=True)
except Exception:
    st.info("Data tidak cukup untuk menghitung komparasi pengiriman pada filter ini.")

# Tabel detail
st.markdown("---")
st.markdown("### 📋 Detail: Statistik Pengiriman per Review Score")
detail = (
    clean.groupby('review_score')['delivery_time_days']
    .agg(['mean', 'median', 'min', 'max', 'count'])
    .reset_index()
    .rename(columns={'review_score': 'Review Score', 'mean': 'Rata-rata (Hari)',
                     'median': 'Median (Hari)', 'min': 'Min (Hari)',
                     'max': 'Max (Hari)', 'count': 'Jumlah Pesanan'})
    .round(1)
)
st.dataframe(detail, use_container_width=True, hide_index=True)

st.divider()
st.markdown("<div style='text-align:center;color:#aaa;font-size:12px;'>Dashboard — Proyek Analisis Data Dicoding · Dataset: Brazilian E-Commerce</div>", unsafe_allow_html=True)