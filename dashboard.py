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

# ── Warna konsisten ───────────────────────────────────────────────────────────
COLOR_BASE    = "#1976D2"   # biru utama untuk semua bar non-komparatif
COLOR_HIGHEST = "#0D47A1"   # biru gelap untuk bar tertinggi (highlight)
COLOR_LATE    = "#B71C1C"   # merah untuk "Terlambat"
COLOR_ONTIME  = "#1565C0"   # biru untuk "Tepat Waktu"

# Palet untuk tren kategori (multi-line)
LINE_PALETTE  = px.colors.qualitative.Bold

@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    q1 = pd.read_csv(os.path.join(base, 'q1_df.csv'))
    q2 = pd.read_csv(os.path.join(base, 'q2_df.csv'))

    # Parse datetime
    dt_cols_q1 = ['order_purchase_timestamp', 'order_approved_at',
                   'order_delivered_carrier_date', 'order_delivered_customer_date',
                   'order_estimated_delivery_date']
    for col in dt_cols_q1:
        if col in q1.columns:
            q1[col] = pd.to_datetime(q1[col], errors='coerce')

    dt_cols_q2 = ['order_purchase_timestamp', 'order_approved_at',
                   'order_delivered_carrier_date', 'order_delivered_customer_date',
                   'order_estimated_delivery_date']
    for col in dt_cols_q2:
        if col in q2.columns:
            q2[col] = pd.to_datetime(q2[col], errors='coerce')

    # Fitur turunan q1
    q1['delivery_time_days'] = (
        q1['order_delivered_customer_date'] - q1['order_purchase_timestamp']
    ).dt.days
    q1['revenue']    = q1['price'] + q1['freight_value']
    q1['year_month'] = q1['order_purchase_timestamp'].dt.to_period('M')
    q1['month']      = q1['order_purchase_timestamp'].dt.month
    q1['year']       = q1['order_purchase_timestamp'].dt.year
    q1['is_late']    = q1['order_delivered_customer_date'] > q1['order_estimated_delivery_date']

    # Fitur turunan q2
    q2['delivery_time_days'] = (
        q2['order_delivered_customer_date'] - q2['order_purchase_timestamp']
    ).dt.days
    q2['year']    = q2['order_purchase_timestamp'].dt.year
    q2['is_late'] = q2['order_delivered_customer_date'] > q2['order_estimated_delivery_date']

    q1 = q1[q1['year'].isin([2017, 2018])]
    q2 = q2[q2['year'].isin([2017, 2018])]

    return q1, q2


try:
    q1_df, q2_df = load_data()
    data_loaded = True
except FileNotFoundError as e:
    data_loaded = False
    missing_file = str(e)

st.markdown("# 🛒 Brazilian E-Commerce Analytics Dashboard")
st.markdown("**Dataset:** Brazilian E-Commerce &nbsp;|&nbsp; **Periode:** 2017–2018")
st.divider()

if not data_loaded:
    st.error(
        f"File dataset tidak ditemukan. Pastikan file `q1_df.csv` dan `q2_df.csv` "
        f"ada di folder `dashboard/`.\n\n`{missing_file}`"
    )
    st.info(
        "Generate file tersebut dengan menjalankan seluruh cell di notebook "
        "hingga bagian **Analisis Lanjutan**."
    )
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Profil Pembuat")
    st.divider()
    st.markdown("""
    **Nama:** Agil Mardian Hawari  
    **Jurusan:** Informatika  
    **Learning Path:** Data Scientist  

    📊 Tertarik pada analisis data, machine learning, dan visualisasi data interaktif.
    """)
    st.markdown("""
    - GitHub: https://github.com/zupergilz  
    - LinkedIn: https://linkedin.com/in/agil-mardian-hawari  
    """)
    st.divider()
    st.markdown("## 🔍 Filter Data")
    st.divider()

    min_date = q1_df['order_purchase_timestamp'].min().date()
    max_date = q1_df['order_purchase_timestamp'].max().date()

    date_range = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    top_n = st.slider("Top N Kategori", 5, 20, 10)
    st.divider()
    st.markdown(
        "**Pertanyaan Bisnis:**\n"
        "1. Kategori produk dengan pendapatan tertinggi & trennya\n"
        "2. Hubungan waktu pengiriman dengan kepuasan pelanggan"
    )

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.warning("Silakan pilih tanggal mulai dan tanggal akhir di sidebar.")
    st.stop()

# Filter q1
fq1 = q1_df[
    (q1_df['order_purchase_timestamp'].dt.date >= start_date) &
    (q1_df['order_purchase_timestamp'].dt.date <= end_date)
]
# Filter q2
fq2 = q2_df[
    (q2_df['order_purchase_timestamp'].dt.date >= start_date) &
    (q2_df['order_purchase_timestamp'].dt.date <= end_date)
] if 'order_purchase_timestamp' in q2_df.columns else q2_df

if fq1.empty:
    st.warning("Tidak ada data untuk rentang waktu yang dipilih.")
    st.stop()

# ── KPI ───────────────────────────────────────────────────────────────────────
st.markdown("### 📊 Key Performance Indicators")
c1, c2, c3, c4, c5 = st.columns(5)
total_rev    = fq1['revenue'].sum()
total_orders = fq1['order_id'].nunique()
avg_review   = fq2['review_score'].mean() if 'review_score' in fq2.columns else float('nan')
avg_delivery = fq1['delivery_time_days'].mean()
late_pct     = fq1['is_late'].mean() * 100
late_color   = "#D32F2F" if late_pct > 10 else "#43A047"

for col, val, label, clr in [
    (c1, f"R$ {total_rev/1e6:.1f}M",  "Total Pendapatan",     COLOR_BASE),
    (c2, f"{total_orders:,}",          "Total Pesanan",         COLOR_BASE),
    (c3, f"{avg_review:.2f} ⭐",       "Rata-rata Review",      COLOR_BASE),
    (c4, f"{avg_delivery:.1f} hari",   "Avg. Delivery Time",    COLOR_BASE),
    (c5, f"{late_pct:.1f}%",          "Tingkat Keterlambatan", late_color),
]:
    col.markdown(
        f'<div class="metric-card">'
        f'<div class="value" style="color:{clr}">{val}</div>'
        f'<div class="label">{label}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── PERTANYAAN 1 ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 📦 Kategori Produk dengan Pendapatan Tertinggi & Tren Bulanan")

rev_by_cat = (
    fq1.groupby('product_category_name_english')['revenue']
    .sum().reset_index()
    .sort_values('revenue', ascending=False)
    .head(top_n)
)
top5_cats = rev_by_cat.head(5)['product_category_name_english'].tolist()

# Warna bar: sorot kategori tertinggi, sisanya seragam
max_rev = rev_by_cat['revenue'].max()
bar_colors = [
    COLOR_HIGHEST if rev == max_rev else COLOR_BASE
    for rev in rev_by_cat.sort_values('revenue', ascending=True)['revenue']
]

monthly_rev = (
    fq1[fq1['product_category_name_english'].isin(top5_cats)]
    .groupby(['year_month', 'product_category_name_english'])['revenue']
    .sum().reset_index()
)
monthly_rev['ym_str'] = monthly_rev['year_month'].astype(str)

col1, col2 = st.columns(2)

with col1:
    sorted_cat = rev_by_cat.sort_values('revenue', ascending=True)
    fig_bar = px.bar(
        sorted_cat,
        x='revenue', y='product_category_name_english',
        orientation='h',
        title=f"Top {top_n} Kategori Produk (Pendapatan)",
        labels={
            'revenue': 'Total Pendapatan (R$)',
            'product_category_name_english': ''
        },
    )
    fig_bar.update_traces(marker_color=bar_colors)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_line = px.line(
        monthly_rev,
        x='ym_str', y='revenue', color='product_category_name_english',
        markers=True,
        title="Tren Pendapatan Bulanan Top 5 Kategori",
        labels={
            'revenue': 'Pendapatan (R$)',
            'ym_str': 'Periode',
            'product_category_name_english': 'Kategori'
        },
        color_discrete_sequence=LINE_PALETTE
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Insight dinamis 1
top3_names = ", ".join(
    [f"**{cat.replace('_', ' ').title()}**" for cat in top5_cats[:3]]
)
if not monthly_rev.empty:
    peak_idx   = monthly_rev['revenue'].idxmax()
    peak_month = monthly_rev.loc[peak_idx, 'ym_str']
    peak_val   = monthly_rev.loc[peak_idx, 'revenue']
else:
    peak_month, peak_val = "N/A", 0

st.markdown(f"""<div class="insight-box">
💡 <strong>Insight Dinamis:</strong> Berdasarkan periode waktu yang Anda pilih, kategori {top3_names}
mendominasi pendapatan platform. Pendapatan tertinggi untuk salah satu kategori Top 5
jatuh pada <strong>{peak_month}</strong> dengan nilai mencapai
<strong>R$ {peak_val/1000:.1f} Ribu</strong>.
</div>""", unsafe_allow_html=True)

# ── PERTANYAAN 2 ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🚚 Hubungan Waktu Pengiriman & Kepuasan Pelanggan")

# Menggunakan fq2 langsung karena informasi delivery dan review_score sudah lengkap
if 'review_score' in fq2.columns:
    clean = fq2.dropna(subset=['review_score']).copy()
else:
    # Fallback: pakai q1 jika review_score ada di sana
    clean = fq1.dropna(subset=['review_score', 'delivery_time_days']).copy()

clean = clean.dropna(subset=['delivery_time_days'])
clean['review_score'] = clean['review_score'].astype(int)
clean['Status Pengiriman'] = np.where(clean['is_late'], 'Terlambat', 'Tepat Waktu')

delivery_review = (
    clean.groupby('review_score')['delivery_time_days']
    .mean().reset_index()
    .rename(columns={'delivery_time_days': 'avg_days'})
)
# Warna bar: merah untuk score rendah, biru untuk score tinggi (petunjuk buruk→baik)
score_color_map = {1: '#B71C1C', 2: '#E64A19', 3: '#F9A825', 4: '#43A047', 5: '#1565C0'}
bar2_colors = [score_color_map.get(s, COLOR_BASE) for s in delivery_review['review_score']]

col3, col4 = st.columns(2)

with col3:
    fig_bar2 = px.bar(
        delivery_review,
        x='review_score', y='avg_days',
        title="Rata-rata Waktu Pengiriman per Review Score",
        labels={
            'review_score': 'Review Score (1–5)',
            'avg_days': 'Rata-rata Waktu (Hari)'
        },
    )
    fig_bar2.update_traces(marker_color=bar2_colors)
    fig_bar2.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    st.plotly_chart(fig_bar2, use_container_width=True)

with col4:
    fig_box = px.box(
        clean,
        x='Status Pengiriman', y='review_score', color='Status Pengiriman',
        title="Distribusi Review Score: Tepat Waktu vs Terlambat",
        labels={'review_score': 'Review Score'},
        color_discrete_map={'Tepat Waktu': COLOR_ONTIME, 'Terlambat': COLOR_LATE},
        category_orders={'Status Pengiriman': ['Tepat Waktu', 'Terlambat']}
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Insight dinamis 2
try:
    p1_days   = delivery_review[delivery_review['review_score'] == 1]['avg_days'].values[0]
    p5_days   = delivery_review[delivery_review['review_score'] == 5]['avg_days'].values[0]
    on_time_mean = clean[clean['Status Pengiriman'] == 'Tepat Waktu']['review_score'].mean()
    late_mean    = clean[clean['Status Pengiriman'] == 'Terlambat']['review_score'].mean()

    st.markdown(f"""<div class="insight-box">
    💡 <strong>Insight Dinamis:</strong> Review score berkorelasi dengan lama pengiriman.
    Review score 1 rata-rata dikirim dalam <strong>{p1_days:.1f} hari</strong>, sedangkan score 5 hanya
    <strong>{p5_days:.1f} hari</strong>. Pesanan yang <strong>terlambat</strong> mendapat rata-rata rating
    <strong>{late_mean:.2f}</strong>, anjlok drastis dibanding pesanan tepat waktu
    (<strong>{on_time_mean:.2f}</strong>).
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
    .rename(columns={
        'review_score': 'Review Score',
        'mean': 'Rata-rata (Hari)',
        'median': 'Median (Hari)',
        'min': 'Min (Hari)',
        'max': 'Max (Hari)',
        'count': 'Jumlah Pesanan'
    })
    .round(1)
)
st.dataframe(detail, use_container_width=True, hide_index=True)

st.divider()
st.markdown(
    "<div style='text-align:center;color:#aaa;font-size:12px;'>"
    "Dashboard — Proyek Analisis Data Dicoding · Dataset: Brazilian E-Commerce"
    "</div>",
    unsafe_allow_html=True
)