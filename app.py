import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import ast
import warnings
warnings.filterwarnings("ignore")

# ================================================================
#  PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="Retail Intelligence Dashboard",
    page_icon="assets/favicon.png",   # ganti path jika ada favicon
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
#  GLOBAL CSS
#  Filosofi desain:
#   - Background gelap navy (#0d1525) sebagai kanvas utama
#   - Aksen biru elektrik (#3b82f6) untuk elemen interaktif
#   - Font: Inter (Google Fonts) — tebal di heading, reguler di body
#   - TANPA emoji di UI struktural (heading, label, menu)
# ================================================================
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background-color: #0d1525;
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0f1623;
    border-right: 1px solid #1a2540;
}
[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif !important;
}

/* ── Sidebar logo / title ── */
.sidebar-brand {
    font-size: 18px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.3px;
    padding: 4px 0 2px 0;
}
.sidebar-sub {
    font-size: 10px;
    font-weight: 600;
    color: #475569;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* ── Nav radio — hide default bullets, add custom circle indicator ── */
div[data-testid="stRadio"] > div {
    gap: 0 !important;
}
div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: 10px 12px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    margin: 2px 0 !important;
}
div[data-testid="stRadio"] label:hover {
    background: #162032 !important;
    color: #cbd5e1 !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
}
/* Hide the default radio circle */
div[data-testid="stRadio"] label span:first-child {
    display: none !important;
}
/* Custom circle indicator via pseudo-element on the label */
div[data-testid="stRadio"] label::before {
    content: '';
    width: 10px;
    height: 10px;
    min-width: 10px;
    border-radius: 50%;
    border: 2px solid #334155;
    background: transparent;
    display: inline-block;
    transition: all 0.15s;
}
div[data-testid="stRadio"] label:has(input:checked)::before {
    background: #ef4444;
    border-color: #ef4444;
    box-shadow: 0 0 6px rgba(239,68,68,0.5);
}

/* ── Page headings ── */
.page-title {
    font-size: 28px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 14px;
    font-weight: 400;
    color: #64748b;
    margin-bottom: 24px;
}

/* ── Section headers ── */
.section-header {
    font-size: 15px;
    font-weight: 700;
    color: #cbd5e1;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 2px solid #1e2d47;
    padding-bottom: 8px;
    margin: 24px 0 14px 0;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, #162032 0%, #0d1a2e 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 20px 22px;
    text-align: center;
}
.metric-card .m-label {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.metric-card .m-value {
    font-size: 30px;
    font-weight: 800;
    color: #3b82f6;
    letter-spacing: -0.5px;
}
.metric-card .m-sub {
    font-size: 11px;
    font-weight: 500;
    color: #475569;
    margin-top: 4px;
}

/* ── Segment badge ── */
.segment-badge {
    display: inline-block;
    padding: 8px 24px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 8px 0;
}
.badge-champion { background: #14532d; color: #4ade80; border: 1px solid #166534; }
.badge-loyalist  { background: #1e3a8a; color: #60a5fa; border: 1px solid #1d4ed8; }
.badge-atrisk    { background: #7f1d1d; color: #f87171; border: 1px solid #991b1b; }
.badge-others    { background: #1e293b; color: #94a3b8; border: 1px solid #334155; }

/* ── Characteristic chips ── */
.char-chip {
    display: inline-block;
    background: #162032;
    border: 1px solid #1e3a5f;
    border-radius: 4px;
    padding: 5px 12px;
    margin: 3px;
    font-size: 12px;
    font-weight: 500;
    color: #93c5fd;
}

/* ── Action / info box ── */
.action-box {
    background: #0f1e33;
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 6px 0;
    font-size: 13px;
    font-weight: 500;
    color: #cbd5e1;
    line-height: 1.6;
}

/* ── Rule card ── */
.rule-card {
    background: #111827;
    border: 1px solid #1e2d47;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 6px 0;
}
.rule-title {
    font-size: 14px;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 6px;
}
.rule-stat  { font-size: 11px; font-weight: 500; color: #64748b; }
.rule-highlight { color: #3b82f6; font-weight: 700; }

/* ── Insight box ── */
.insight-box {
    background: #0f1e33;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 10px 0;
    font-size: 13px;
    font-weight: 500;
    color: #93c5fd;
    line-height: 1.7;
}
.insight-box strong { color: #3b82f6; font-weight: 700; }

/* ── Profile card ── */
.profile-card {
    background: #111827;
    border: 1px solid #1e2d47;
    border-radius: 12px;
    padding: 20px;
}
.profile-id-label {
    font-size: 10px;
    font-weight: 700;
    color: #475569;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.profile-id-value {
    font-size: 26px;
    font-weight: 800;
    color: #3b82f6;
    margin-bottom: 14px;
}
.rfm-mini-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
}
.rfm-mini-cell {
    text-align: center;
    background: #0d1525;
    border-radius: 8px;
    padding: 12px 8px;
}
.rfm-mini-label {
    font-size: 10px;
    font-weight: 700;
    color: #475569;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.rfm-mini-value {
    font-size: 20px;
    font-weight: 800;
    color: #e2e8f0;
    margin: 4px 0 2px 0;
}
.rfm-mini-sub {
    font-size: 10px;
    font-weight: 500;
    color: #334155;
}

/* ── Member card (Home) ── */
.member-card {
    background: #111827;
    border: 1px solid #1e2d47;
    border-radius: 12px;
    padding: 28px 20px;
    text-align: center;
}
.member-photo {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: #1e2d47;
    margin: 0 auto 14px auto;
    object-fit: cover;
    display: block;
    border: 2px solid #3b82f6;
}
.member-photo-placeholder {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1e3a8a, #0f172a);
    border: 2px solid #3b82f6;
    margin: 0 auto 14px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 800;
    color: #3b82f6;
}
.member-name {
    font-size: 16px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 4px;
}
.member-nim {
    font-size: 12px;
    font-weight: 500;
    color: #64748b;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #1e2d47;
    margin: 20px 0;
}

/* ── Streamlit widget label override ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label,
div[data-testid="stTextInput"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    letter-spacing: 0.3px !important;
}

/* ── Button ── */
.stButton > button {
    background: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 10px 28px;
    font-weight: 700;
    font-size: 13px;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.3px;
    transition: background 0.18s;
}
.stButton > button:hover {
    background: #1d4ed8;
    color: #ffffff;
}

/* ── Tabs ── */
button[data-baseweb="tab"] {
    font-size: 13px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Expander ── */
[data-testid="stExpander"] summary {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    font-size: 13px;
    font-family: 'Inter', sans-serif;
}

/* ── General h1 h2 h3 override ── */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    color: #f1f5f9 !important;
    font-weight: 800 !important;
}
[data-testid="stMarkdownContainer"] p {
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.7;
}

/* ── About page table ── */
.about-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    color: #cbd5e1;
}
.about-table th {
    font-weight: 700;
    color: #64748b;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 10px 14px;
    border-bottom: 2px solid #1e2d47;
    text-align: left;
}
.about-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #1e2d47;
    vertical-align: top;
    line-height: 1.6;
}
.about-table td:first-child {
    font-weight: 600;
    color: #93c5fd;
    white-space: nowrap;
    width: 180px;
}
</style>
""", unsafe_allow_html=True)

# ================================================================
#  DATA & MODEL LOADING
#  Semua file dibaca sekali dan di-cache oleh Streamlit
# ================================================================
@st.cache_data
def load_data():
    rfm   = pd.read_csv("rfm_clustered.csv")
    trans = pd.read_csv("transactions_clean.csv")
    rules = pd.read_csv("association_rules.csv")
    items = pd.read_csv("frequent_itemsets.csv")
    return rfm, trans, rules, items

@st.cache_resource
def load_models():
    kmeans = joblib.load("kmeans_model.pkl")
    scaler = joblib.load("scaler.pkl")
    pca    = joblib.load("pca_model.pkl")
    return kmeans, scaler, pca

rfm, trans, rules, items = load_data()
kmeans, scaler, pca      = load_models()

# ── Parse frozenset-like strings dari association rules CSV ──────
def parse_itemset(s):
    try:
        lst = ast.literal_eval(s)
        return [x.strip() for x in lst]
    except Exception:
        return [str(s).strip()]

rules["ant_list"] = rules["antecedents"].apply(parse_itemset)
rules["con_list"] = rules["consequents"].apply(parse_itemset)

# ================================================================
#  SEGMENT CONFIG
#  Definisi karakteristik dan rekomendasi per segmen pelanggan
# ================================================================
SEGMENT_CONFIG = {
    "Champions": {
        "badge": "badge-champion",
        "chars": ["Frekuensi tinggi", "Pengeluaran tinggi", "Pelanggan aktif dan setia"],
        "actions": [
            "Berikan voucher loyalitas eksklusif",
            "Tawarkan produk premium atau pre-order",
            "Prioritaskan dalam program membership VIP",
            "Undang ke acara pelanggan spesial",
        ],
    },
    "Potential Loyalists": {
        "badge": "badge-loyalist",
        "chars": ["Frekuensi sedang", "Pengeluaran cukup tinggi", "Potensi menjadi pelanggan setia"],
        "actions": [
            "Berikan diskon untuk pembelian berikutnya",
            "Kirim newsletter produk baru",
            "Tawarkan program poin rewards",
            "Rekomendasikan produk komplementer",
        ],
    },
    "At-Risk / Churned": {
        "badge": "badge-atrisk",
        "chars": ["Lama tidak berbelanja", "Frekuensi rendah", "Memerlukan perhatian khusus"],
        "actions": [
            "Kirim promo reaktivasi dengan diskon besar",
            "Kirim email kampanye retensi pelanggan",
            "Tawarkan voucher gratis ongkos kirim",
            "Survey kepuasan untuk memahami alasan churn",
        ],
    },
}

# ── Helper: prediksi segmen dari nilai RFM ──────────────────────
def predict_segment(recency, frequency, monetary):
    arr    = np.array([[recency, frequency, monetary]])
    scaled = scaler.transform(arr)
    cluster = kmeans.predict(scaled)[0]
    label   = rfm[rfm["Cluster"] == cluster]["ClusterLabel"].mode()[0]
    return label, cluster

# ── Warna per segmen (konsisten di seluruh chart) ────────────────
COLORS_MAP = {
    "Champions":          "#22c55e",
    "Potential Loyalists": "#3b82f6",
    "At-Risk / Churned":  "#ef4444",
}

# ================================================================
#  SIDEBAR NAVIGATION
# ================================================================
with st.sidebar:
    # -- Brand --
    st.markdown("""
    <div class='sidebar-brand'>Retail Intelligence</div>
    <div class='sidebar-sub'>Data Mining Dashboard</div>
    """, unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # -- Navigasi utama (5 halaman) --
    menu = st.radio(
        "Navigasi",
        ["Home", "Dataset Overview", "Prediction", "Visualization", "About"],
        label_visibility="collapsed",
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ================================================================
#  PAGE 1 · HOME
#  Berisi: judul proyek, deskripsi, identitas anggota tim
# ================================================================
if menu == "Home":

    # -- Hero banner --
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f1e33 0%,#162032 60%,#0d1a2a 100%);
                border:1px solid #1e3a5f;border-radius:16px;padding:36px 40px;
                margin-bottom:28px;position:relative;overflow:hidden;'>
        <div style='position:absolute;top:-40px;right:-40px;width:220px;height:220px;
                    border-radius:50%;background:radial-gradient(circle,rgba(59,130,246,0.12),transparent 70%);'></div>
        <div style='position:absolute;bottom:-30px;left:30%;width:160px;height:160px;
                    border-radius:50%;background:radial-gradient(circle,rgba(34,197,94,0.08),transparent 70%);'></div>
        <div style='font-size:12px;font-weight:700;color:#3b82f6;letter-spacing:2px;
                    text-transform:uppercase;margin-bottom:10px;'>Data Mining Dashboard</div>
        <div style='font-size:32px;font-weight:800;color:#f1f5f9;letter-spacing:-0.5px;
                    margin-bottom:10px;line-height:1.2;'>
            Retail Customer<br><span style='color:#3b82f6;'>Intelligence</span>
        </div>
        <div style='font-size:14px;font-weight:400;color:#64748b;max-width:520px;line-height:1.7;'>
            Sistem analisis perilaku pelanggan berbasis Data Mining menggunakan K-Means Clustering
            dan Apriori Association Rules untuk mendukung strategi pemasaran berbasis data.
        </div>
        <div style='display:flex;gap:12px;margin-top:20px;flex-wrap:wrap;'>
            <div style='background:#1e3a8a;border:1px solid #2563eb;border-radius:6px;
                        padding:6px 16px;font-size:12px;font-weight:600;color:#93c5fd;'>
                K-Means Clustering
            </div>
            <div style='background:#14532d;border:1px solid #16a34a;border-radius:6px;
                        padding:6px 16px;font-size:12px;font-weight:600;color:#86efac;'>
                Apriori Association Rules
            </div>
            <div style='background:#3b0764;border:1px solid #7e22ce;border-radius:6px;
                        padding:6px 16px;font-size:12px;font-weight:600;color:#d8b4fe;'>
                CRISP-DM Framework
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # -- Deskripsi proyek --
    st.markdown('<div class="section-header">Tentang Proyek</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#111827;border:1px solid #1e2d47;border-radius:10px;padding:20px 24px;'>
        <p style='font-size:14px;color:#94a3b8;line-height:1.8;margin:0;'>
            Proyek ini bertujuan untuk mengidentifikasi pola pembelian pelanggan menggunakan pendekatan
            K-Means Clustering dan Apriori Association Rules Mining. Dengan memanfaatkan data transaksi
            historis dari UCI Online Retail Dataset, model ini mengelompokkan pelanggan ke dalam segmen
            yang actionable untuk mendukung strategi pemasaran berbasis data.
            <br><br>
            Dataset mencakup lebih dari 500.000 transaksi dari perusahaan retail online berbasis di UK
            selama periode Desember 2010 hingga Desember 2011, mencakup pelanggan dari berbagai negara.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- Identitas anggota tim --
    st.markdown('<div class="section-header">Anggota Tim</div>', unsafe_allow_html=True)

    col_m1, col_m2, col_spacer = st.columns([1, 1, 2])

    with col_m1:
        st.markdown("""
        <div class='member-card'>
            <img src='data:image/jpeg;base64,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xhemt+n2ent01rVC4zZat0z5fkX263M63fP8/wAnj8Gfd7/h/JgAAAAAAAAAAAAAAAAAAAAAAA33xjtZl01jfTOeefP0+36taxmEvS221MzGcJiMYyLUvTre2s994kZut9evo9Po7ej1a48OXHESJNVqznMceTPDlrp07ejr07b1dURjKW2lvl+Tz77lmczjx8/m83h7/U83wuYAAAAAAAAAAAAAAAAAAAAAAA6+rzzpvOdb1IM8+XT7Hq1cyZzd9Lda1bJnniTOcZznA1brfTrvRtliK36OnX3enff1bx5vPzxmCLq6qZ58ZZy53pvr13vfTWrbJnOYWrVz5/k8etzJmc5njw83j5/T7/neAAAAAAAAAAAAAAAAAAAAAAAA9Ho82t9c870sYmpz5dPseq3GMS9N71d61vSY588TOcYkxF0303rfSs6ZmJa69unb2+np39Gufn4c84lQutUrHPEmMXe+nTpre9aukznGY0Wms+X4/m6VZjFvPlz8/l8/r9v5/wA4AAAAAAAAAAAAAAAAAAAAAABfV24td8ctddTPHFY57+z69OfLE6dt6ut63vaY5Y5yYxiJFt303pusSSC3r069/R6vR6e948ePLHMrK71RZiTOJL0303re7qiZzmTQprPk+J5Om9azjHRy5Tj5fL6vb8HygAAAAAAAAAAAAAAAAAAAAAAGvZz59+m8c7163lw5GeW/s+2ufKN76a1re973ZjnnExjniLUu9a3Vs5Zmaq669e/ft6vR6fS5cOXLlylqS61rUVJMyRre9a30aImYkUpqeP4Xj6dejGXScOeePm4d/d8LxgAAAAAAAAAAAAAAAAAAAAAAGvY83bvc4vTrrPDjjM537PurnzS73ve+m961pjMmOfPlhq6SdGtaGOGUla1v0d+/fv6e/f0Xnw48+HGUka3dZbEELu61u3RMZhJVtaz4/hePp13nLfTPDhjhwx39vwvEAAAAAAAAAAAAAAAAAAAAAAAdvo+Pj6N6mNdelcuHHGY+x7tM8ObfS7307b1dbkWY5885Aaa1ZJx8+N0m+vo9Hfp09Pq79+rHHhz5c8zBlq6uWt2iQ1da0atTGBlbbWseL4fk69ZlvfTPn83Ll5uXs+j8DwgAAAAAAAAAAAAAAAAAAAAAAHr+l4PN177xz36NnLhy5Zy+p9Lprjw5Z32ut9Ou9b1pdazn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jOc5TW9a3vfbv23rLMk+OIiZySUnPGc5W2ySKxk1da2FBJyvXr01BJKkkZlktkloyX1fY9/q9Hf2fY+r6e3TfLxfl/wP5T52N9o3FuZcx0zZbda1vv7vf6d8+eOPLO/Z+h/Zftvv+302VZIha1z8vHp257axy48eHHnjj8b+f/ifAostuq0kkXet63nN1amcxczHDj5vNxznGdmunb0du3S26znEyz076101pjnjMxjOVut73279u20ky+LomTMizIcuczFtRIMyNXWukgoVOnQoMoQmAtkipBfR9X6Xu9Xb1/Z+p36583w/xP4r4vPSb30UisaTO7q3W9dOu/X7/R3vg81yy9n6H9x+0+19HrbERF23z8Hwdfd1nO5z48OeeXPj+c/m/wCQ4KqU0t1ZGbLreqizW7jEk8/Hz+Xz4xLdb7d+utdOurrUaznOJi67dNb1rTlzxMYmMLdb327du/WpJPi7TOYZUhJy55kW0iSpmLq73MqthrXWgisZtEzhRbJKzLZfR9b6vv8AR19v2Pf114Py/wCD/JeWDpp2stMl1I1re+vXU3vr7fp/S7/I+fxnOGfofp/3H637ns7NWVF03z+b+C+L+y/TdOWs44cpeHPzflP5h+XmjTNFt3YjWctXetM5Vz4cOPHlyxnKLr0en0dtmt2ytJnGJz3vfTerrpcc+cziY5YRrp6evXv6N2RPh1c5kKlGM454zGtRbJlZmS63dIstq9OmpCSkiKiYoqQsxautfb+17e3T3fT9nLw/C/Lfl/i85rOt3W9LUFRem+nTp21z3336Pf8AQ7+PzYzw8mN53vt+t/f/AKn63t69ITZdcfF+C/A/rf6D75nOOHM448f4z+WfDa1ISs63dW5lszbnW93PLj5/Pxxz5ESrvXX0du/Y1Lu5XUkzzxy306dNnTaTEzjGOeM4mt9e3br6O+tMz4YmYoVJnGeeMl1GqzkzIut2il6autbxiItSICZUqSKy0a19j7fu9Hb3+h874nyfD4vifMhbq62uoFTW+uumr0udduvo9fXr035OWOGEl4c/uftf2v6r7Po6y6hpx8f5v+e/Q/oP1uvLly55mcY+X/Pv5h8/pdZyol3bSoW4mt2Y8XzvNM5t3u2276dOu99tXRbFSM8sYu99Olu91MZmMZxnlzxL07d+3fv20y+GJCo0kmM4xjNqm7M5iTK73W7MrvttFziVGkggkCpBZdQ19n7vt9Xo9PL5nyPnZy+V8Hy4q3V3boFOnXrd1rcvTr17vZ6O/m8XO5meOc88ej9L/RP3H3PodqllvHyeL87j9J7/AE8ePHnMZzw+P/LfwHn2rKkXS1bC24l1Zjn8/wCbxb6dOvbew1tOnbd0WkQnPnma6dN6t1q3EzjGc558uWM669/R27+jdj4dBCqmZjOeeIuqurMZiZy1rd3pia6delzmJCFQgiCiS1F1I39j9B7vV3z8L4PLvc74/F+L5ktt1rWg0uuvXourvTW+nbr19Us8nHpnGeEnLnev0/6H/QP0v0++u2MnPz+PhfT6fTjz8eWeeefl+F/HvyeGlikWrbZFumaMy8vl/Pno9Hs6aozlZnp01q22hGpjnzmuu96lutVM4zhnnz5cea9/T379+m9T4O1ssi2JljnnGJbrS6kmYzjLW93oy313vUxmITK0SCFFZi6iXUyv1/030N8fh/DezbWt+D8/8jmVda1pV1q769mbvW9a6a6duvX09/P5eGbjlzwnnzrnj1/u/wCj/rPue+7SZ5cPP17de083DjjGOHg/GfyT428rQEtrVkVq5shlvl8/j6PT2tkM4lk1urrVVC1jHPG+u9aLdXcmc5TOOPDlyx29Hf0ejfbpPz3XVsKM3MY5cpFurbcETOML03dW76bVMQhMrUQItLZnLVlNZNfV/Vev53xPjz39fRb6Lw+J+Z4QW3etXTWt769Eurd9+++no676+3x+Ty88zn58nm5ZuOXT9j/R/wBn+j+p6dsTDG5rpnj5eTnx8nwv5Z+H89SiAU1qkmtZSWrbjEXVkJmSTarstRRjExvtbrS23RJMxOfDh5+OvR39Hp326vz3o0sirIkmOfPBbaoGcYw1vprW+mqrKRETLVQQRS2ZFzo0SfR/Tef4vi3fZ26d9+jGPn/kfnSi61rd1da10300U36evb0duu+2PHx5cuWJyxic+XO8uWd/f/o/777/ANz6XRc425yzPn4uPH5n4H+W/ItzQZFDV0ItkXVNRnlrVkJMZja20tFzJnKa7VvSLdauZJDPDjw8uevo9Hp69O3T856dLCqmZM5nLmW1RRnGMzXTp03rdDMIRmLaEGQWKIN2M9Pp+Xz9O+u/p16OvWTyfjvkZhbrWt3WtW9tbtLb36evv29HPrw4Z48OPNnniZ5csc8Y7/b/AGX6T7n6T9H9b03WbJyxpnlx8/h/M/yz8bxbkFmQKtq2RvIpvUOahJnGY1dUqhcJIm+mrdMmruzMRM8efLzcr17evvvt1/OeroqqM5zmM8sKtUKmc4L17b1aQkomZC2pLBIBqiQ3ZDtjpv099+nXfrrc5fivic8xdXW9a1dN992i61e/0PR7fZ43m4c+HDnhnliY48+XNv6f7f63f0fU/Q/p/uertqyefzb6a4ebzfnP5p+A+fcdbJLWBJTVLZGiwXc0xQM4xkutVKpEhJWumrTJdaqQzMc+fPjyxevq9fTt1/Nevrq20jOMSM8sqtVFqYzma69uuoJCWpc4irSQCAWlmVumbrrvc9Xqvr69NztnP4j8/wA5Ft1vW7dXfo0ujWtvR7vZ9P0/M4eTljlzxhjljOOPLll6/wBj+p69cb9v3/1X3vpdNL5vL06PN5vj/gP5h8jCNSS1lZIVS2FUSLbZpazZjOSa1WdFkIkLretXWcw1dUzM5xnHPny5Z6ej19+vT876+vTWtEkxjMjPLGi0RamYu+nXSCSU1DOJbVSM2xaiCxqRaNTr6dX0ezXq79NY3nP4v81zRWta1rW9a32Td1brV9Ho+h9Tv8vyeaY5uecc+eccuHHk7fpf3Xos3nn6f0P6v9J9HtWeVnPh8v8ACfzX4fj8+pNZhUqSBSqhaJKpq71MSTMRdEtWRWcjWta1rWMxNNWuec5mZMceGN9fV369fgerr13upnOZmTMzzzotICNa1rdRVZlWyTOV1YRJoWxlFRuSha7+/Wunu109PpYznH5D8xwZW6urve9610XetVWvR3930Pd5PB5Jz5658ufLnOfHjxxv6X7z7/TOby8r2fc/UfpPrd97mccPn/kP5r+afJ8+pnUgCEBdKQqgWm9sSMyZLRaBMSumm9W5iSlTEmZFxx48XT1duvb4Hq7detJjOSSYznNq1CQXpva2S21mUJmZaoQlsaRmRpLRZFrv9Ptt7+s9Huznljl+U/L+fGV3V3ve9a101vd2i9O3b0ej6mvD4uXGXny4ccOXDnzno/W/sPfGOfm82Xo+x+p/S/X9npcp4vzv86/D+vyfDzllARACtUQVRVuWt6kjOcyS0W0jWcRrppu1mWCGckkMY48cX0du3X4fo79ulJiMwmJJlq1IRJrpvV0i1UghMrULAKsjJQKW1PX9brqfQ9XPXuTHn4flfy/lwLq3e961vp11da2S9Nd/Tv6HreP5/lzJz8/DDhxzi/V/f/a7MceHDnnE39b9R+l+v9Lrz5/C/C/hfJ9f4PwslhCSQ0haq0zaLFplda3mMyTGLVVdM3fPnG+m9FqIskkysyXPPjy556+jv1+L6e3bYzmEM5zBW5JmWSXprW7aUIgSRolIoCIARpbbfX971cp7/Vzx7Nyebz/mvyPiwpq71vWtdOvXS73Zm7d/Tr1+j1eb53PlJx83n54xy58/T+u/Ze/eOPHnz5TPLD6/6P8ARfZ9mvB+I/BfP+z6PxvzNRqESTK0LQtIaRVpC3Qmc5zgbsW2Lzwu973aIipIkmZFmeXHlz6d+/b4/p79NEmY1JJnMq1pJiGTprWt2ioATMWgCCkAGVW1v2fo/Xwvt9OePq9PHPLz/nfxfgwq273vdde3XS6povb067+33+P5eJjn5vPx5Yxx5X639E+70vPjxzjnmceHO/V+99b63f8ANfivkfS/Q/J/CeXopSTLDVZXVg0plqwWlRWqmcZxJHSyLYc83W971q2IKSRM5ZSZxy5cddu/f5Pp79KSRLMs5FtsJnKRemta1alEoEmbRCog0SFVEC29PZ+k9mHq7zh29/DheH5/8P8AOwtul316Vrp01dW20vXv06e/3cfmcLPP5PPz58uc5+j9b+79ac+POc8Z6c/Hzznv9H3a+L870ff+p+E/JZ1rUlpJMTWmJrSS3Srlq5FpRGrqYxjJmb1IDOY303rVtIhahnMTOcZzjnw107d/lej07tgzLnMzFq2xGYmV6a1rVWKgIAQAkNEC1IqLXT0/p/oyerrPPj6TzTHwfwnzMNLo316bNarW+mkq77ejf0vZjw+Pi5eTz8uXPOc/U/of6PUzz44cmvfPkebjx556dOXb6v6vzfyz5NuhQkkVlbcrdVUtSFpQLpnGMxib3IExmXp13q1UINWRMkzzxlz58nTr3+X6PR0tKzlMTMXShMwmZd7u9WgFSRQhCrJCgLWRS1vf6v7HN6+l83k+l6fLwfF/A/Jy1aN73utaq76atXV7enp6u2OPPhy4eTz8sYw9H6v9t9Lec8+Uct+n7D834PPw5Y69p6P0P6P8Z/OuGrrF3EJLZkLcrdWlIZW2VaZu7nnjOGW6VGeWZvr13uixIW1GRnHPMc+OG+nb5vfv10mtMZTOc5atWpMxGM3pvWtXWslCSVlRKMtMyXQSNaTNVa1O36f7uc+n0PP5PR7+Pkz8z8B8fm3GjetW3d1prptdW3fXr6/S58/Hx83n8vGYb+x+/wD0m8xjEnDt9z6vzfzvzuHKXe9+v9P6v5l+PtpqpIimYW2DdloEWs26JLpmZxhhsaSY55z0697rVixAFImJzkY48866d/ndu3Xol0kzM5yWmqmZGWct9NXV0LbCIYtASKkLZCXVM2lNzv8Apfvs9/Q5eO+++Hh8/wDAfIznVtN60XWrq76aa1d3W9+3268vl82PH5/Nymd+/wDafsPoTNYxJj1/ovf8T8983k1a9X2PtfK/l/wpqrRCERGqsjZSgVJVoojGM5lGknPGZvt2ut0RlNINWTOZmSY48s3p2+f269uuogkxmKLqySRmZy3vWtUq1FskRQRKWSNRC0ChdTv+k/R3PTtvHl5+z0/P8Pz/AMJ8mZl1V3dJbrWrrpprV3u66e33b8ni8/Hxefjia9P6L9/9fW4mc5mfX9z0/I+L4XTbL3ff3+O/nHia0AEkUWkjaUKVYiNXVSNXPLGZBozyxG+vXe7bUmcrSTVZkZTOOPLDp28Hbr06dLIjWcZgLokzEznLfTetI0EWkAIBUiktsQCq06fov1HTG+nSefz+n3eD5/h/G/B5Zzpbd6ql1q63tu3ervfq9vXy+Ly+bx88L6/rftP1PoiJnMmd+7r4/JnXW88b+j9bw/z38Ry3qoWiSRVKiyopQthC3Vsi1z5zOZWjHLDW+u+mlasmcFKSokZzjjzxOnXw+jpvWtqjU55zC2iTKZmcunTeqNIItEAlEWyFGrlBFtNXX3f1vpl1XLz6+j5/B4Pzv5X5+c7Na1qzRbda3q73rVvTp6Pe8Hh83m8+Jv1/c/V/qfXN4iRmTPS5d97xxz6fqej8/wDzb83LqoWiSRaVFRCqGqxC3S1UNZ55zgVMcs3pvrrWqa0mc5hbTTMkmc55csTfbw+jrd60tExnIaqJmJjOM3t03bVrKoCoKgqVFLFqIlWi7z9v9j7Gi582PdfB8r535j4PHN0ut6S0tt6a1vprd1vfr9fn+d5fP5eU37fvfrf0Ptk6WJWc5jXXr1s5437ff5/xn848Dawq2SJFtqIQUStaucS1dC2wtxjOMhnPLOunTpq61ZdDEzI1V1c5kmJOXDE328Xo663qipJMwurIykzjPPOu/W6q2yKksKCojVyi21IoQtC7x9j9p77SvPx9PXxfI8nxPy3kxNLrWjVFa1vW+m961rt6evg8fn8nmmvX+j/Wfpu2tamtRWcYu+nfsxnlPV9Dr8j+e/hsXdQNEkBqkiKWENauZLSqaC6znOOchMcs76dOla6ai2JMZlustaucyZmcefnnp28Ho77uqKkiQXSZiZxMcc79HS9NAUkoKsQjVzJbdQSWhKi2bn1/2v1FznV48Ovbh8353z/yXyueNmt6NtE1rV106b6XevT6ny/J4vNz1ft/vP0fo103bpazMunXr22xx46+h7uH5z+Z/m3SiSatkSxQWFRSQtRaBoqppWeHPNTHKb6dNW63uCEzmNazLuzEiY58uOevX5/ft03qgsiZFrMRnGcccb79ddN2KpIBQQLcDVsEKgqVZt9b9v8AVrErHn125+D5vzvzXwPPNW61urdDWtXWum+t6X0+7j8jyeThjfT9X/QPd21066JrWctdu/p9fo3jn5PP39N+f+O/mnz70pBayiy6Zi0rMVUWAtBUq1WtvNywkxzz069N01shTGTVzLtnKSZxx5Z6dPB27dOmqg0SZhTMhnnnnzzrt23vdFtkBFQtSFyW0ipSRRamn1v3H14ktz5sdL4vl/O+N+b8Uzq63rRrVpra66a3evT2+rzfL8nk4zp2/SfvPoejXXpssXt6O/p9fs9XVwz5PPqeb5n4D+f+fW7EVSCy1mLSzOVurASGiiC3Rvbjy54zJzz07dNW21Cqwgk1piMxnHLlnfTxduvTpoDcJmAmYZxz5YXp36b2Rq6SBEpWkzFBbCpTJYtov0v3X2RJXn4615vmfO+f+Z+VjOmt621dUmtW63reunT3+zx/N8Xkxd9fqfvf0PXXTpvQ6e36Xv8AR07dLOXLHLjjn5vh/wAu/Lc+maJZRbLBIqXcmZVoixKVQCzWrWOXHniZz09G9W7EC0mJC2ZjJnHLlne/J37b1VpbBMixMEzy4Yrr36b1YNUkqpFGkyUKDUipKyuqub9H9z9zRnNvDk1y+f8AL8n538/wlt6dNa3dVZqmtOm9b9/0Pm/M8fnmZff/AEb9Zdb7d9536PofU9/erM5xy5ceXPj5/wAf/Lfla3i1EBqkliCXVZSasSNUgtKJE1Wqxy48sZz19PTTWwiLamMIskBjnz5TWvJ6e2tFtqQIUkxDPPhyOvo6a3qChLVQJSLcrVhazLYSS7q5v0P3P3tSzK8uWWPF8vh8f8z4OZrr06W7301YkmtTWt9fpfU+P8vyeTjx1n3f0r9d26dvo/V9mZ39Xr7BnOOfPnwxjzfP/nv8+8t0CQhrRkIIaSFqQtii1Fsy1lZV1OPDlxnb1ddNVbcyKupzwiSS0uOXPnnWvJ6O+6W1AVmUmcwznz8rOnp6aurCgq2WQQq3NS2NBFkQtti+v9v+l0ImeeHPx/M83D8x8Hia69NW66duu0zFszrt6vd1+V4vH5PPzzr6H9D/AF3s7fQ+99n1c+O+/URnPPHLHLnz8nyv5d+S46sCAlqzKiSKqQ1ZkqqKWS2CQt0nHy8M9/Z2S7s1c5I3ZzxWcyFlY58ued68vo7b0tWFhWciMozjz8zfp7at1kqoq2QsTLVVUWLRASLVHb9r+r6kE58nLy/O8s+P+U+dGuuta103vp06JEVdej19Pm+Pyebz8sdfofvv2Xq9v3fv/Q1yz066iZmc4xnlyzx8n5r+VfAdGVBZINMqJCkkXVkkq22FIWBCtVy8vmx39ffUbubZCNs881M5hRnnz543vy+jrrdWoqFZzJGsmZz4crOno77rWSqLLqZKkzNaKFgtJFQK1G/2X7HsiLOfNy4eP53Pj+S+DzXWunTe9b6dbahpnPb2erweDy+fy8XX6X7n9t6vqfpftds43vbOWcZzjOcZ5cPD+L/mPy7oUFZzFtQAqSRbTObdLYKghQSpjy+fHf1ejolFgk3M4lkzkFuefLnNa83o3rpapKhWcyJrKScuOI36O27bCmos1YhUxnehFFRoIIU3m6/XftO8BnGJjl5fmeW/n/y/jlt69enTr03elSS6mM9fV6vH4PPw8vDW/qfuP23v+5+j+jrM3tMyZxjOc5zOXn+d/O/515rpQktTMW1EFCEVUzLdVUAgULGZy8vB6PV36ayQKipnLOZBGrnHHnNa8/fe922pBFZkQkknLnzk69uvStLBSrqIUxNUhRRUpJSVqxr9T+29VImcZzz5+fw+PPyvx/z5LenXt39Pa52hZFa6+nh8/wA3HzcNX6v739n9j9F9v0XnnpZM5kziZjGePD438p/FXdzQhbJLbCBUIAEatVBFgqkssxx8fDp6fT13vKyC1LGZM5kEauefLnN3z9uuta0qQkVMohmM8ueMzr279E0qFK1qIpIpZFIpoEWItbzr9L+69tTOWZnHPHLxeLj5PzPwOGbdb7ej1d+u+hCc5vpb25/O8vDz53fp/wBE/Yfe/RfRa5NzMzjLMIxjj5vyn8j+J0XNAUkbkIoIQFCraSEUtKksuefn8eOvp79N2XSBaZkMZmZRpOfHE1rh06dNa1SSEESSEZzyxjOenb09CqIqrpAIsWLSKKgqEtm2/wBB++95M5zlM88cPN8/z9Pifj/n4LddvT6fV6vVuc8knXZnl8/y8eTp0+5/SP036L7PoM6ZzjOcwpM8uXi/n/8ALvLuGpAVCaSFUkJClqLTViSTVKVISzj5fK7d+3TbVsBqsyJJnEiqTHHnNXl0303rVIxbIhJILjnjHPOddvT2paJGlWsgqA0FQpIoFpv7f9D+jWc5mUmOfm4fO8/X4f4z5+CVrv39Xr9XbrnN1rrvOGPH4PNzw39D91+4+/8Ad9/W4zWcYyhQnDj83+XfgudmbrWYJqyyKyaUkiRbFqLS0TKqqmYsk4eThrv17dbvdzKhqsQmZMSWg5cuU1rl0303rSyM2yRCRFYxz54zm9vT22qiZaVbIWBCrRULUgBbGvs/0X6hM5zIk5ebzeDlj8x+W8fNCt77ej0er19ba6dtcuPn+f5eXPL0/sf6B9v9D9jtu4yznOZC6DPHz/n/AOS/mYka1MkapIIulJMoVFrLVFKjK2zSYKzy8/n59O3Xr01vaQi6SRJJMw0ks5cec1vj1103dUklszEQRWefPnzydfT6N2yoRRbkVECqUJbpIShBfrf0f7FZznOcyTHn8/k4fN/JfD8/ORq1d9e3p9nfWmdev0eX53j8+M4zr6P9E/Y/a+/9K6ucs5zmFurDny8X4z+SeKpFSC6QgLaRIhZFrLQUomboskDHn8/J07dOvS21LQJCJmQtzNZ48uc3vh21retLJKuc5AiW558+fKHT1ejpURagVI0QIopSNaSEoZVfo/0f7+pnOMZzJMcPP5fnfnvzvy+OYutout9u27avo7cPHz0XXb3/AKj9x+v+x31WZJM5FutRjOPl/wA0/mc0DMWtIiwKtkEhZFqLC2KJLQGU5efhL07dd9KVbUEkLJmSLrMs48cTe+He63q0znVucQIgucc+XOG/T6etSC2CkjVQBCiwtsVFJldPX/Rv0+pnGeeUmccfL8z85+e+Z4sRNdN2SpdLq66dOtz11XX1dfR9D95+3+p0tmZkzFXWqY5c/hfyH8d0oRJbalyVkttmVSSkWoRbEpRULZmZ4+bld9e2+m6GqZWsyEzJBUTly5Te+Pe63bbJm2zOSySFZxjlyi77+ntpEKCki6AJBQGhUUkW3v8A0T9buYzjlkmc8PJ+f/HfL8PHI303srNt6dN9N9O286zu69vSfR/Xf0P6U3Ukyhq26umfP4/y38d+RtENSW0tzlWZbbZmkkVFpElsS0WwltYnPh5+eunXtvptYW2Sa1c5wjEAE58eU3rl21d6UREgEklTHLGMGu/p70RagtQWxYVFZSrVUgAuun9E/Z6xmc+OMw58PD+M/M+LzYxNZ326bttvfd6710uOvbON29vTvt3+5/QvvtaZyyprda3WOHzv53/M/GQUW1BhUltVUkgslpIFgpqkllYnPz8M7317Xr0WRQl0ZxmISUsmccMta49da1tSSIEgkE5454yt6+nvskt0kWliKqC5W5y1q2S0CRrWbrr/AEr9nOWMc+fLk6XHi/N/jvj+fzzDU323vbWt+jd6buq10tXv6N318vZ+4/aemVnMlq63b00znz/H/lX4bz6SBbbUGZULaEkthJaSAKsa0kWGZw8vG9ddO16dAVBdXMzmISFsmefHF1vz9da1uiTKAksiGcYxzF6ej0bslWiW2WQUikEl1ohVBLI6dOn9P/b54cuPLnw476zHyvwf5ryY4SK313vd1rp23em7W7dXe+nfr29Pl6/qP3/v2iZWtb3rW7nnjj+f/kP5jnEkF1aCZloaISLqRJaSBFoatkBnHn8udb316b3uKUFqSZSEhbJnly5t9PN13d70kmYgISSGcYxkN9/R0sWhZbYyWAtiKl0hSktipNa7f07+h3hx8/m4cOOul5fmf5383jjlIt30101db113enTUdK3vV69+vXrM/R/oP6XohM61d73u25548n4z+R/J1EzCatFJJaKEiW1ElCAUS21CGeXl4N76dt71oVSgkZSEyKk48uTpvj03d60kkiQQkki5xjGbqZ129HWy2wo0kkupEaohZdRahLaktmV9P9H/AKd6OPLh4PHw4TtfH+C/G8OXPGVXe9701vW+mt9NnS3e+i9vR25x1/b/ALj1ga3db1prWccfD/Of5l4NQkRaS2si0RUkLUIpAKIW0jJj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hZnLOMZyTF0T0ftOP5fG9KBItugNVJUgiFzkutEiICZ58prW7MqC2tUtJTJbQgNW2nPnm25W2STEjMxMwS0G93XRIucZzmEzyws1E317dNW26klpFWoLJJbbAEQ0S3pvr6/V16Tnvn336O3n4OXDM58+fLn09HS76dOfm8fCZltmMs5zjJJS5z9l4db3KIIWraWpNVmQgWZi3SojM0SZ44ttsgU1TV0aSCFLaiDdtmbnlldRbZEznCZxJBC0ut63qQszzwyM8sKQvXt06VdEVAqhKkzbpItERaS63vt39no9Gc/Q8LfZy8+OfLMxmccde1m/R08ni4c8xq2c8ZZmMxWic8+jpd3S1EAtW20zN1nJkAhWrUjM0jPLjNKsQtTarrRakJbFtqSF1bWWMZUXVZJnjZnEkElq23fTbMNTGJJmsc8ShHTt36al1BCFKqSkytCiwFG9X0ev0+jp117fDhed48sc2pOfn11uuu9Z83l8/LM1q3HPliJMrdaM8pevbWqUgI0tNqgSAkAhdAktjHn4XdIUWy6LdKqxk1S2szK6rREzlEttuTM4pMTKVCy61d9NRksxlM5rGMSkJvr366NUkgUWyRpJJbaRVQUbTv7/AE98evq5Zs5sYzjW2PPnuno6OHn4+bjMtVM8+XLNo3pVxx5776vS1RALSXVqpJJbRmBEtpLUqTn5uOulki0WraXVqqmTWoW3MyuqEGcwq2xmTikzMxUVm63rpsshnnDGbc5xkQl69+m9VRABamZdMyN1EUULVs6e31dZ6OzdvPlw5pbZnOvR0jlx8vHHLLLTOZnjxltXe7Fxxx06autW1BSGhNLbZJJbRISItqLUsk4efHTaZloW1qi7tlGVtRq3MhpBm25xLbSxJPPGZJFRWW976al0kmMYszFkzmRLM66dunXdAIUWpnLSQ1qSAWxbU3der09NO3br0zx5efEm+mjV6+x4fL5PNjCyLnEk5cZLo30pc8Ma6ddWqsLSJrRFW1GStIzUzC2hYsmPPwdNyZFkrTWqGrRUaqRu2ZikBbnMbosTM88zMyLWSpvpvdtrJnliswsmc5Jldde/XdAsio1amcLFoICorQut9/R11jp6+/fxzPPkS76adHTHh8fHnnC1hMM554xLauumpM8p03vdUItENWs6saohdZjNRIVVIrPHzZt1ZCEluty6KtqW5bWF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' class='member-photo' />
            <div class='member-name'>Moh Fajrul Fallah</div>
            <div class='member-nim'>24051214071 · S1 Sistem Informasi</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class='member-card'>
            <img src='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD//gA7Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcgSlBFRyB2ODApLCBxdWFsaXR5ID0gOTAK/9sAQwADAgIDAgIDAwMDBAMDBAUIBQUEBAUKBwcGCAwKDAwLCgsLDQ4SEA0OEQ4LCxAWEBETFBUVFQwPFxgWFBgSFBUU/9sAQwEDBAQFBAUJBQUJFA0LDRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU/8AAEQgChQHZAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A8iooor8sP7NCiiigAooooAKKKKACiigUAFFFFABRRRQAE5ooooAKMZoooAKKKKACiiigAooooAKKKKADrRRWnoOjS61fJDGpPOTitKdOVSShHcwr14Yam6tR2SM+KCWZj5aF8cHFW7fQdUu3lEWn3BSP78jIFRfYseK9r8O+A4L4T6XpBhMkeEv9XJP7ltp/dQnoNvGWznPAqfxFbeGPDotbK00248e6yke14p2aK0jwVUkdjj6AccmvtcPw3eCdaVmfiuYeIyo1nTwtPmS7ngUltcQ3PkPbSrLt3BSuMj1/SnNZTgENEQVGWXIyBXY+MdY890C2ujWkqSYmXQLTYsR4+TKx84zzyxz7VgWnjFtHvlF3YLqWj7cv9oULNAcfwlcHj/Irapw1FR9yepjhvEabl+/pK3kY/b0P5UvtXVSaVp2tQyXVlcIY2wY5Cy5yf4XHr7965u7s5bKdopUMTg4O4Yr4/FYKrhJctRaH6zlWc4XNqfPh5fIhooorgPeuFFFFABQRiiigAooooAKKKKACjpRRQAUUUUAFFFFABRiiigAooooAKKKKACjOaKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKTOKXFArhRQeKOfQ0BcKBxRjHbjOKTgUDuLXqvwr0tzbvJDHi8lZYbZS2N0rZAx64GT+FeVqpdlUDkkCvWfAghtPFGh/a1AtdOsZ72VNwG92YxgYOMnIH5mvqeH6Cq4rmfRH5hx/jPq+V+zi/iZvfErWovBvhqLR7C8EFxJuCQdI4It/7yc45ZjnA9cn0ryfUPEdskki/bWe1e7WaWDJL3f+1IG6YJAAHCAng1xnxF+KM3iHxvd387F1kAgWPcSBGpwBz64OfrXG6hqUnmGY3OXcgmNclAMcD8OK/UeiP5hPV11LVdcuQummz02yCn97dSqJE6bj50jAZyCvyjGMVi3XihdPjuobnxLBqFxuMkcF5/pCuwIzlwQF46EZrzG4vLt8TO+5AcYByv0/SmyTRTwBIrZInzmQhR85wO/px/Ok22dEU2j0DQPGRuhdSWcsFlcjINn5mcp327uGHPA6jFdNo/ie38QWU0V+5cwgBbk4Dxn0YdSPT0rwiV2t5YlA2kAAY4INXodfNpP5iSyR3mAB02v9a83FYWGJhyTR7OWZnXyuuq1B2Z7Pf6ZLp0gEicEblYdCD3qn8232q94P8bWmt6KLG6UGEYZ4iuGt277T3Vvyq/f+GHhQzW7+ZETwjHa4HXpX5rjsrq4WV46xP6RyLinC5pTUaj5Z9jCoJApXRoz8wI7cjFN6CvCtbRn3KaauhaKKKCgooooAOlFFFABRRRQAUUUZ9hQAUUUUAFFFFAB1ooooAKKKKACiiigAooooAKKKOlABRRRQAUUUdTQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUcjoM1Nb25uLqO3XJmkICxgZJ/CtYU51XywRzV8RTw0Oes7IhCkngZ7DFWYNNuJsskb8dRtJx/nNen6D8C9bntxe6hGuiadsLma7IErqB1WPcMDORljj+VX9XtPAOkWn2S0Nz4j1AAZtFfZG+QfvJHheMeh7elfT4XIatVc1V2PzHM+PcJhpOnhVzv8Dy200QzRPJNOtuqDPzbj/IU06bBEvmG7gMS9mlVGI9g2DV/xJ49uLGyMVlZaTo0CqAYre3LEH+8dxKhuB/8AWrx/xFrl5rUjXVxPJOi5w87kAfnXsUsiw6XvanxGK4/zCTfs4qKPQLnUdO3IkfmhicDABH1zU1q2nXOUOoRwSbSRHO2xjx05rwOfxFbNIVEuwrwCgzVQ+JrZSA7ztjtgEfSuuXD+Hk7o46XH2ZQik7M+nNE8Lahq2oWws4DdBmG1o+Qwz0ql8QfELeC9Z1l4XbfIsahWwGhKMrLnty5PT05rwPRPjHP4YuUksbe2nSMEFbq0Ukn6qQe/6VkePfixP4ymWSSJrYLgiJZpHTIGP4ySOp716GW5VHASck73PF4h4lrcQQhCcOXlK3i3xKq+IbtYAypG5VQwBJwOe3fJrBn8V3av5hckg8ZPasSa6eeQuTnJyeeT71GuoPASFC4IwQVBFfRcp8bGmd1p/jh3OJImxt/h4GfcfnXXaddwaqsclv8AIdvzRu3bA+6a8htLhHmiZTtIIyM/rVuz1m40a9DxSsAjfej4I+v6VEoLoUlynsUMMF2DazkQuT8kjcjPYZqrqlhLFuhuQCVHyybccelZej+NLXxVDGmRbaqAAV4WKfH8Xs/Tn2rsbS+l1LT1g1Abmj+SK4KgOnba3t0FcMrwepotdDA0zXm0q6jcPsuVAVG/vrz8rfhXr/g3x5O2n+fGEuoCpWS2l5HGMc9sY4I6V5HrXh8s0qPG1vexAs0eflc/3lP8xWb4L8XTaDq6CUbkPyMrcDnr+dKUI1I3Kp1Z0paOx9N6ZdaB47SO1sybHVydptp8DzG/2G/i6dOvWsPWdAudEuHjni27SVJXkE5rj0vredBIYI7yBwGjlLEOmPT3FemeFvGFnq8KWPiFmeKQbfthfDoQuF3+vGOevHOa+Ux+T06ycqekj9UyDjHEYOSo4p80PyORore8SeFptFuHZNslqxJjlXBDr0/r+eKwSCD04r4GrSlRlyTWp+/4XFUsZSVWi7xYUUUVidYUUUUAFFFAoAKKXPHWkoAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKOlFFABRRRQAUAbjgcn0orp/C3hyK5t7zVdRIg0qwjDzzMdoJ7IP9o/56V04fDzxNRU4Hm5hj6WXUJYis7JDfCXgm88UTMYf3NrEwEty/CoeMAds8jivZ/Dj6N4KSaz8BaVF4i8TNxdape7RFbdQdjHhV4Hua5O/aztvDscmovNY6OqeZZ6XA3lSzZHMrn7w3AcDrg8+lcOPH6aMjzsRo+hwNvFtZgLj2UY++cdTX3OHWGy6UaSXNNn4fmLzLiSnPFTl7OhHa/U9J+INlqV1JA/i3xEbvzkMsunwyPCBj7pDt0Ax3AOAMeleJa58WJrCw/srw9ENO05Bt328e2aTrnMhyxzzyenauA+KPxTvPG2ri8lllQLxFbqxKovG0Z7txyfyrm7Sa5OGOY3K7VLcHtkV9b8SPyRLklbc1tZ8T3bxTFsD5dxBbOB2569q8y1fV5b075pfu9Ezium1KWI6PPC0hM44Zs9WA4/CvMtUvCzcnDcjn+VdFKKMqt5Mbd3a7vlYg46dBVM3cowC+cVTdyxzmlBJ/CurQagkTfaXBPJ9etNebeMHkjuaiCHvyKlWJjjAxSLtYaWOPXjFMJLdfpVpbc9P85qPyc5yuBnpQOxFG/lkHHI9KuLfbnUscEdTiqpiwM9qa3y+1AmjSSOSBDcQnGzDBkGc8/pXq/wANviFFdXcVrfpGVkUIWcDG7PH4HGD9favGbe9ltmJicjIwR2Iq7p97HHcpJjYpPzKOh4qZRUlYWq1PpPXjCb2CTeViQlYQ53FB/wA8ye4GeD6GvPfFNrFZ3u6DJtW+ZQ2Mof7v0549gKg0HxRNcwJbyy+coUFC2CRj/wDVVq+ZLuApIMlBkKehHpXJCLg7Eu8tTR8J6yYJfsU7bBJgxsTwGHau7jv3it3LYSVBtZM4Hs1eM3khFrG8bcowXHfGK7fw/wCIP7S01RK3+kxMBk90PQH6VnUhfU1p1Le6z2Twb41h+x/2ZfK9xBMVQiMZZCOAy+/TjuKTWLAWFw2xleEk7XToRXl63BhlDxyBA4O1gcbCDwOPSu38H+KV1W3n0/UArTbgUnBOT7Y7noQfds18xmuXLEUueHxI/SuEuInl2IWHrP8Ady/AtEYH0pamu7V7S5MUi7GB+gqGvzlpxdn0P6PhOM4qUXdMKKKKksKMc0YxRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUdKACgcUUUAFFFFABRRRQADiiiigApMdOaWkPtQDNHQdMbVdThtlVnBOMKMkivUF0CWdLBNQ04p4b0h5GhtVIJvLvZne5IwVUdeyjZjk1z/AMKlaHV7FobZLm8mnURLJ0GGADdemWTP4Yr2/wCKvhuSw0zT/CtjcqjvCs9yxXaLSAg/M5/vPtLMfw9K++ynDOhhXXS957H4HxbmixOaQwM5Wpx3PnHW9RuPFWuz3V1IRCzEAgfKqj+FR6Y/xrxHx34ra81CWCNz5ELEKobgY9fyrsvid43t7a2TT9MbanlmMHB6Z5kPucdCOgHrXht9ctLJ98nf1OMV6+W5aqT9vW1kz5jiDiR4uCwWE92lH8TSsJDcXSSOuEQggdjV6TUPPle6nl+SMEt6cdAKxL6+jt7COOKYA8biO4rLur1jYhAfkZ8FfXjr/KvoeW58CpaGhfXZu47g4BebLDb06VwGqEvO2cfLgV19rMJUm3AkQW7SsV4Awvyj8yK4WSRpDuJOSM5960h7pS7jQvPp26VLtx1wMHHtTokIOQCcjvWtpWiNezgMpEajJJHFaSnGO5aV9iCwsGvPuYwOuBW3B4UnnjVhuK5wSF5rsPCvgV7udNoIQjJYjCivRtN8FxQRBFAYkcKR+teNiMwUHaJ3UsLKWrR5LZeAvMXAVhngBvmP1qtqvgtLFghGZG5z2/CvpbSfhtJJFl4SgAyQF+Yj0pdV8CW62rJ5CjPAbbk59a8v+05J7nesC+XY+TLzwfeW7gqhdCoIOMisafS5MFky23qp6ivo7VfCj6arxXNuzhT+7mAz+FcD4r8CmJjNHGIwwJzH0NenRx6lpI4quFlDVHj7gqcEYIoH5c81sazpZtJMbcN0PtWRtNezCSkro856Ox0vhW+JkeD+IhmXpwAAcfzrq7a8aX5iSVjBZuhwOBn9RXm+nXBs7qKUZBU5GP8AP+cmuxtdUNhPHMEEkQOGjPGYz2/z6Upoh6GvLbrcwvGhHJDKRxznpUWlX0mm3ilhgbirKOamcxW9wvlnfaSgPGR02nt9RwPwqDU1WOUSIc7+CetZJ30MnpqjsrLUhJOVX94rnhR0rQhnazlSRH2ElTG4OOvb9BXmttqbwspRypBAz0I967XRZ08Qwi3falwTuV1PU+3/AOusJwt6G8J31W57bo+qr4v0ZI5DGmq2ke3avymVByCPcZx/+uqjKV7dOK878M6nd2dzBc2hJvrJsqT1cKRkfpXrGp+Vqmn2ms2qpHDeqXaOM5Ebdx7fSvz3OsvVOXt6ex/QPBWfvEwWBxD95bGVRRRXyJ+uhRRRQAUZHpRRQAUUUCgAooxRQAUUUUAFFFFABRRRQAAZooooAKKKKACiiigAooooAKKDRQAUUUUAFFFFABRRRQAUqjJpKWMfvBjgg/1qo6tIibtFs9v+Bi2GkahBrVzFJK2nRS3a27ICsrxAALnHALTJXG/tJfGS703Qb3RvtK/8JLr8gvdYkjIEkEX/ACxtuOnygEj/ABovvinbeCPDen2Kk+ZLFcXM7IAchHAjj98sqfQKfSvmfx3qbX94Lq6vDdavfE3F5zkQ5+5H9QAM/h6V+xYSChQhFdj+N85qTr5hWqT7s5+6ka6Z3kJYsclieTXMXt4CXKnJDYweOK2L29WOJz2A5965N5NzHPGckY9a9SETxHqS7gxzySTg8/0qC7uSQqc4Byf6UjTbADgAVTuJQQvPI7+1WtCkjXxs8NTzRsweeURHHA8sAH+YH5VzCxb9/UFe3bGK7u6t4m8JaQsXDmVw+SAD3/qK5bSLQ3U12uAeOPbmpvZXNo66FuLS5hdWCBARJGrgAdmFet+DfCaxxLJNFlgchP4TWf4T8Pi8vraZ/kigto1LMOuF7flXs/hPws2rupaIxWq8BDwX96+cxuLtoj3cJhb6sr+GvC9zqsiLbxcfxSBcKPw79K9Z8LeBLbTI0lmQzzn/AJaOOntitvw1oiW1qixps2EKARnPFdpb6Q0YUsnOOjdK+Uq15TPo6dKMEYS6SPLKhMcYGByKw9a8OgRMY4+wyOcHivQPsrqAPunPYHNNutOItyGABGM54rBSaN5K6PBNZ0lZDtwGIGCrAYI9K8/1bQkhJhlQvZy5AY9Yz6V9Ea94ZS9hISPY4+YNjGK4TWdBDRS2lzEQ5GFYYGT6130atnocU6V0fM/i3wS7QSSRxhmQY246ivJdU00WgbC4Knoe4r6w1TQn+e1kA8yMZBPG8eleOePfB8cG+cQnYB2/hr6XB4y1os+fxWGs+ZHj2w59AK6FpluLOH+8qlWPcg9ay7y1MTlcAjrmn2r7V29cV9Je54k1bQ3NM1N3tTYSfN5Lb4j0Iz1H41ctb7IEMn3CcK2ORXOrIYbpJh1GBWlBObiVyQAck4FTYysXdSgFs8RUEr69RV3w/qjW86DeUdcFGHG1gP8A61EMi3UaowXkgEdqwrmQwXrRhSmxiCOmaVuZWZK909e/tIziG9tCA+7dJtIB3dzx0zXonw31NLm/axmdfsmoZIJwAk+OPzxz714X4d1MNbOC+GJySDjOK3NM1i5065Rd+U3cMvYjvXnYjDxqwcJHtYDGVMHWjXpOzR7Zf2T2F3JA4wyNioK1LOf/AIS7w6NSUl7u3VVmB6uMfe/z6Vlng5/CvyTGYaWFquDR/WOUZjTzPCQrwe+4UUUVxHthRRRQAUUUUAFFFFABRRRQAUUUUAFFFB4oAKKKKACiiigAooooAKKKKACiiigAo60UUAFFFFABRRRQAVY063NzfQxDqzAfSq9M1S7fR/DmpXqSrDKIvLh3EAsxxkD3wT+ddeFpSr1owR5WaYuGCwdSvPojzbx74rl1HXLuW3ZfKtwLaEDqGA2k/wDfWT+XpXn1zcrI8jYJYtzn+dW7udt0rYwWbfkcc5NYmov5FuMMMtzX7NSp8kVE/jfE1HWqSm+rKd5qBdHXvnFZm70GKWZzID0znmoDJztwSM5GMV26JHPFDLmU4C5wBUB+eQIDyehpJZCzbiABT7NPMuVGG/D6Utje1kbmt3Rhs7OAHGxmP4YHFReFrd7q8eJVLlyoOOBtFM1VTMsAHuQT07/4V6H8KfCpu4vtJj43YkJ4wBXDi6ypUmzqwtJzmkep+AfCDXrJLKMW0WxUQcZOP5V7poOlpDbmKIKhDKQ20EjHauP8J2yxWyJGBtAG3vgYr0PRraOMfL85fuK/PK9Rzlqfb0aahE6nQEijiTklxwSRyef/ANVdjap5kQAGAq7gxH6Vy2kkLsIGE6DGMiukAklBYSkDABGcYrjNyKWMys4Uk4547Cn3EQeIr5m/cOdw6VGyC3IeZspnAHJP096stZRiHcVJRsAEHpWgzGltUSBvKdfNQE7VbGa57X9Ai1WwKiQGSMblkUchvSup/suFZHkaPDH5QCc4FUL+1SAYjCjLZYDPNQnZ3RLVzwjX9IkuFlaRdt/bnOO5Feb+IbCDULdwASZMrIvYV9BeMNAaVhd2oInj646uPSvG9e05Uu3lhQojHDrj7rV6NCrqcFamfMni3Qns55UxkIchsY4rlYx5cmOgzjNe5/EDQzNavdKMFCAVUcEGvGNSt/s8xU8ZPGK+3wddThZnyuJpcsivIcxbucg59sVYgkMUiODgDqaprwjAnvxipYZtsWCMgDH4V6fQ8+SsdJC6zRkhmU4ycVBfQieNbhs+b0J9xVSDfDDHPG263JCMeMCrBYYyGLA4BAIP50kjMdpU3lSgDJAIyB3Heuj02/3/ACSIWTruPBGK5G0ma1vgCMpnaSO1alldmMkBQA2c5PGaJxuSpOJ9DfAzUp7rUX0xFLy7GYMc4aL+JCPbjH410ut6eNM1Oe3yCFPykd/evAPCXiK70TUYrq1maKaN8gq2M9OP0r6Z8ZLa6jb6RrNk5lg1C2WZwSGCPj5l/CvhuIsKnTVZdD9l8PcylHEzwkno1depy9FFFfnp/QIUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFJnFLSEZFACj6dq5H4vXnk6Rp1khZi7FsA8L93t+X5V16YLjsCa84+LrNH4ntLYtmMWgYYPIZif8B+VfU8PU1PE8z6I/MePsQ6WWKEftM83vsrMyDg7exx/npWBr0/7tACMjjHtW/ejdeTvvUbRwPxrjb+RpJSOSM4ziv0+KP5qIoiMn1A6+9SSEInv2wKjiwgORTZ5N4xgDHvWl7FpalXO33FWbBT5pOcdsjgVUxn7vHertqPkUHg5x7VLdjVmzbxidocjIzgZBz1Pavpr4ZaGqeHoQq+WZhyAvUe9eE+FdEN1PpyMOTlj343YxX1b4O0vbAixKCiDaueAK+RzWttE+iy6n9o6Xw9pKwQJ8uWAA6Yrs9KRIVUbQjnjP9araLpLbMY2E9OPaux0jQxJsGwOyHJ9CB2r5SUrn0iQmn2gKAhlO0buPX0resDhAAjEtxtC54qeDRD5eY0ChQMAd60bKwMaJHnkAkgHBpFWMu90mK6KtJFuMZyo6YpLomD5NhK929TXRx2apGR1A4y3zE+9UNSiikjHA54zjAzVdCTDt0MeQfnLHPJzioLq3IkJwWOecit2HTi5VUUhtoJPpVw6S+xCVBOM9KkEebatp6hixT5B/CRgA15x4t8HJeB7izTE3UgjAb2r3bVNGMvBQFD/C3XNc9e+G2iV8KcelCk4sGlJWZ8heJNHadZIJIihJIKnuO1eE+OvDjWNyVAwiHO7HSvvLxl8O49TtzLs8ubGQQK+b/iD4AuI7KdHhJYE/MRg4r6HA4zlkjwsXhrq6PmWcHIHTAp9ucoy9MdBitDxFpL6ZOFcY3EkY4/CsqKTypcg8GvtoTU4po+XlFp2ZPYXUkCzQqcqwO5TyCPSrFpcDzlDghMYIODxzVKeNrWeOdRwwwQKtSxKUEqEOhAP0rXqYtF6+RVZHTlCgzjsR/kflSW0pglRW5RhjI5waj0y4+V4X5Dd27HFWoIkknMZ+RhwVPT/69UYyN7SmUSx8DqOR0Oa+kPh1MNU+Hd7as4JspRLGrNk4OMgfiK+Z9Jk23BjbgxEKp7YNfQ/wTm+16D4l035Tc4F0MryyjAOPxx+Zrws1pqphpp9j6zhiu8PmdGUX1L3SilIwT+tJX4+f10gooopAFFFHU+lABRRRQAUUUUAFFFFABRRRQAUUUce9ABRRRQAUUUUAFFFFABRRig4oAKKKKACiiigAoo6UUAwHFcN8ZNL+xXmk38hUi7t32r0Pynbn9T+Vdyf/ANVcb8a53uJNKLHKWtoFRcc5JJ/r+lfWcOf7y15H5Z4g2/s2L8zx++fYzd+o3A56CuRvh/pLcg84x7etdFdTbScAkZycVhTxj7Q/cg1+mpWP5vViFtvlkdTVSRMZzU0rBRioJCXcYPI4wO9U7GkRsEbS3CqozkgAD610Gm6O11c+WF2iNck1L4b0xYJHu50ISBPM2nj3x+g/Ku18IaKky3QkAMjShSzZAXgZ/mK4K9flWh106fMztPhf4bMlzFIy5SNflYjIJr6W8K2NvZwxxhw7kZwOmfWvFNBuYdIhSCAqQSoJBAAHf866iy8fRaddAjDxKcbkwTivj8TCdaVz6KjVVFWPoXT7qEeVyAw7AdK6rQtQgtVKjjBBYn9T+NfKN18V2FwWW7lWALzGEKr/ACJqG1+PF1YXyPIrBCMgxYbj68Vx/UZ7nX9dgfbUWrWSHBYNzlcjH4VImvWm4bNuR2OM5r5X07496fcsha9MZbgFwUYH0rs7D4gDUIWYujkcgxH5a5pUp090dMK8ai0PdZddtzbxgKm5epU8/wCelYtzqkcsAKv8xJ+Vl4zXndv4kMwJ8wAKO5xViHU5ZW+9wM4x0rA6EelWOoxCUqGUAnI+XFbEmt28cIOVY4xj0968qj1lo22kkknlj6VX1HxWlkhLy7AMjjrQF9DuNR1dJdoQ4Geg6YqrJqdu6kOdpAxgmvFdZ+Ka2Lzy+cpiDfK5bkiuJ1f47Lkp5qkDtuA5rqhh51Ohy1MRGB77q2rWcSSK7jIHIJHFeY+LotM1W2Lb0ycgbj29K8svvi1Lds7MwPZQzDHWsA+NJriQiRDHGxz5vBBHtn+Vd9PBOGpwTxfNojkfip8O4btJfKK7wN0bAgD6V4FqFlNp135U0bI68c46V9XNejUYZIn3XKDJBBB215t4s8DW+px+aoxMMjLLs6nge9fSYOv7L3JM8WvDn95HkLx+fb4J5XgflTLcNEvl54Y54HSt+68MX1qsyvCR5ZxkLxmsgwMqbiMMO/417sZKWzPJknHRhIghdJVy6gjNWHcPeq6kg84Palt2DI0XyopIJJ7YrLmkaKQx5PyHI9qvYytc6y2PnWzyqSHBw+2vYP2f9Vf/AIS51Ytk2UytjuuBx+oP/Aa8P0G6Mnmor/64YIz7V7p+yvaG+8c6n8wRIdFupGOAc/c/rj8hXn4u3sZ+h6OWXWMpJfzI7iX/AFsn1P8AOmU6XiV/r/Wm1+Jvc/tCHwoOlFFFIsKKKKADqaKKKACiigUAFFFFABRRRQAUUUUAFFFFAAOKDzRRQAUUUUAFFFFABRRRQAUUUUAFFFJnFAMd0H41xHxtQbdHIAKy2rfMOCrBh/8AW/M1238XtXM/FizDeGtIn2qx+0PED3AwD/n6V9JkM+TFpH51x1RVbKXL+Vo8AvnMM4jYFmYBBjgdetUNQiEMxyAT0+WrniKYx3MUykL+82/lz/Ss7UZPMZj0PXjpiv1Q/mFGa5y4PHNbPhnSW1K7QgAkEbVrDU7CDwRXv/wk8CsbayuPKyZtpB9BXPiKvsoXO2lDnlYLbwBIbC0QhhvkWSRtvJVecVu+E/B1zezyLCAkCMTJIoyzsew9B0r3IeE7U20aGPBjUIMHjpyfxqzaaZb6RFGsMQix1CgAfWvlZ4ls9mOHscfYeDYIIAPsy89cqMfnUF14FMyEJGFJ6Y65rujIRKGwuP7vOKuQsTjCL/vN2rzpV5JnoRoxaPmnxr4S1OwuHiWUpF6BfvVxM8V3ZzLG7uCowcd+a+1F0ezvYws6wMWHK7hxXmnxH+GVnK7yW0ZQ7QSqrx+Hb9K6aWMvpJGNTC9UeE6PqJSUpM7Yxw3AwfT6V3HhfxTdWl02yXCBchCeD7Vx2r6YNOvjGQAU7dKfp12Q+FABxkHuD6V1TSqRM4rkPorQPEn2pEVnGOoB6g+ld1p+oILYYYliAOOa8O8H6hLPCgGd6kdD14r1rw7bzXEIX2zk8V4NWCi9D2acm4mnqOqyQMzMdoGDivPPFXi2SQyhThSM4HHau3162kFu6sPnYYB9K8c8brJZoSVwvOCPWijFSkFWTjE5PXtekuLaeNzthzuC9s151cXTvIVI3bT8pxyPet7ULkPGVYnHTipPDfha51+9SOKLAz948V70GqcTwpwdRmNpulXV/KPKyB2yO9em+D/hzrBTDLLyePlxtH1Ner+CvBGkeGLCOS8e2ilADM07AMPwrpZfFfhu2jMY1OAHAA2sAPpXFUxsnpFHVDCR3bOR03wa1rAIJ4g+ByFGcH1yf6CpdR8GW13aOskfmptK4XOQK6SHWNNvTm2uIZeOzg8USagBCcEHnBycis4VZt3LlSilY8sg+HduLgwzxNLbfdU8Nj68dPSuM8f/AAPTT9MuJbNMKfmjIGcdzX0RaTxTOAVU7uDjpU+p6bFqFlcQkKFKso9q9KlipQlc8+eHjKNj88GtWhkljkGGjOMGsTUFxd5GMnp1r034laEdE8W30GNhJGFUcY9K861A77pUGPk4Jr6+E+eCZ89bllYm0GQi/g29Aw4719L/AAH0S5sI9b1pBJHELEwxyA4V9zqGH6CvmLSONQTjkgkEcc19seFbWTw58F9At3O2XUBJPs6DYxUj+RryM2qqjhJtn0/DOFeKzalGPR3MvOck9f8A69JRRX4+f1ukFB5oopDCiijjPtQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFHf0oAKKKCc0AFFFFABRRR39KACiiigArI8fI1z4HuRy4hlEgAHQlcZ/QVr1d0qWLzXhnTfFINu3Gee38q9LLq3sMTCbPns/wjxmW1qMd7HyFqs5nt2VxzjcAeuf8is+IefEXxjA2n3rqfH3h+58O641tcxgPHuL7QMD5jgfhiuTjyqDk7S+dtfs0ZKcVKJ/H8ouEnGW6CO281oUABLMF+Wvuf4R+H1tPDtnIUxiNRz9K+OfD9kHvLZiAR5gYEdDX3l4VjNl4ftFHdBwB7V4mZzskj1svXM22aV1iKMsR9PauautRUs+W245JJ6itrVJWeMqBkDPSvJ/HWs3NlC/lQO5YcbR0r5uNpSse49Fc1fEHxCtNGXMk8aHGFLHkn0xXEX/xRs2JkutRnRB97zHMKD6KOT+NeP8AiPUdee5Z4LJ3lPAYxkn8CelT+D/DNpqG+fxIlzFeOSEhkhYRj8elenHDU7e8zidep9lHpFv+0D4I04yefZXGoy8gYR8Z9c76rf8ADRHhy6dxFJqOkFhiNC5niA9MPyPzrwHXvD11a6rPbWlncTRrIRG8MRII/Cn6F4O1a71S3t7nTLuCIyKXMsBXCjtyK6Xg8Mo3uYrE1m9j3HUNZtPFClre5huHA/5YNkkY7r2rlZTcWF8pKkITg5GKxvEfgDWluzcaJp18QhynkKR+Vet/B/RdW8ZaTdWPifR7iyu7WPfHeyxbRKoHT0yOK43yUo6M6YOU3Zo6r4YwrdwxgcEkEev0r6Q8F+Ht88WRkAAjPevHfhxoI0xxGEGxXyGI5Fe9+GJzGY+MY4HYYr5vEVLy0PoaELR1E8ZeGY0BIVc7QQB/n3r5r+Ldi1nbT4BC7cjPavqrxfJ5zpIoONuG3cf56V4L8UvD/wDbNm4QfPtx7UYepyz1CvC8dD5Xs4JtTuCyj9ynLN2AqzefFy08LBrXSZcuow90FyR7L712nxN+H3iDW9J0jQfB9kiQFd15d7thZj/Dx24rmdN/Zp8S6NY3Av7O3uXkU/Mr5I/+vX09KVCSvN/I+dqRqx0gjnrT9orUNMffaWC3L8lp7xiWP48n8jVuP9pPVtXl23eiW0xbnMLMrH6ViS/s2eOmZjFYQTKoDAiQDI+vStXwD8I/FGh6wk2o6I0qxhgse4fer0PZ4Llucn+0tmzpXxc067kjkhUWl2gwY5zsIP8Avr/UV6joHjxb0xRXKSI7DOWYMuOOQwrzbxV8D9c8ZXsEkNpYaNtyS3mfO+fXFaHhn4JeM9BlRJZ1khHIkik38fT8q4qkcNy3jI6Ye3vqj3bQdSVp1VvXhvSuzVg6hh90gZ6V5/4Q0G+tIo1vQfMU9SuAa76xi2BUIIGO9eNzrm5Udrg7XPlP9pPSBa+NfPVMCaAN/Svny7QLMRjDg5Jz/n0r60/ao0nZLpt4oOfKZenbNfJl+Nt1KOM5IzX22DlzUYnydePLVZp+DtJbXNbitUXc7AsBzngdP0NfbXjtxavpGkxpsj06xigUdwQgz/Wvm79l/wAOf2t498+SNvs9vEWL44yo3Y/T9a921rUH1PVLm7kYuzuTk9a+W4lrqMI0Ufrvh3gvaV6mKey0KNFFFfnh+/BRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABR1oooAKKOM+1FABQrbSrDqDkH0opOg9qe2opJNWex5X+0XpyLeaZq4jw95EVlkAzvYdc/gF/MV4jIQQoB78Yr628T+D4PHXh6exnY7reN3iCg53EdfwxXyTrumXPhzWJdPvY2huISNyNxjIyP5iv1zKMSq+Ei76rQ/lDivLngc1qK2ktUd38P0Fxb22Rz5yqDjOOa+7dItB/ZtoF6eUv4cCvg74bOwuEUH90ZUYevWv0E0mLbZ2+BgmMdPp/9auXNOh5GXq1yodOE/Cgg9hWde+BLe+dTMrE5ztUDFdhFCMAjrWjDZk/P0HoK+SqVJQeh9RTpqSPNZPh5aW2WhsYy+Mc9RWDqPh6+twVj0qN35O5lTH5GvcJNKaVM42A9cd6gPh8TkOwL+mazWJfU2+rrojwWz8PeIjKPs+l6dBJ0DGOPI/ECuk0rwBrepk3OpXaIoYbhBHlvpyAAOPevUv8AhFjB80agvngHIAq9Z+HrlVG6UFQOg4ANae38yfYLscvp+ix6XCqWkTAgDEkpyR74GB0rA1u0eeciNcEgruC+vWvTJNFkSIl3U4HAXgA+lcxe2yxTnKgHNYuq3ojaNJR6GL4d0FLNQ2Aveut0eUpdpgYBOQo5/CspEL/dzj07V0Gh6dKCj4IOOOOaxbOiJva3GJYUYDKnqvpXmniC3SOURHDKRyT2Fen3VpcTwZJzGvXAwa4zxJYF4yxXBQfK2BkiiDFNXRw+naR5Mha3AGDyvX8a2WtpJR8yqu0jBIIb8GBGKfpJEUwzgFhjn1rq47FbpMqBluPatvaOJkqakeRa74QGoT7pIZYpwDtYLkdOuev61gQ+Cb7zMJLNgcfeYfTrmvpG28OQyrsdQO2TyP5VNH4YtSoCwhmzgMVABrT6wyfYJHz7pngi+kcbnYDOCX6/yr0DR/Cpt4kx8xAyQf516ZF4bFuf9WAPY5xUosBAoGwE9Pu4rKVaTYKilqcSdKCIA6KT/eNQT2EflqB99ehFdZqNsrDCgDjB4rn5x5bZHIHFaQm27mFSNlY+ff2ntOkl8MWk6ABopXjzkcDaT/SviextVvtetLaUHZNMsbBeuM/zr9CPj9YpqHgC5x1WWPqOmRj+tfKXhv4E2t6xu7zULiB0feskRVNvvX2+BxEYUdT47FUZSrOx6t8FfDs3wxuvGdhJYboHiEcUlwpEsROOnuQwyPYVePJPuc17Bdx2uqfBVNRluxc67AUtLxwu0zKo+SRh0LYxk14/0r43iCr7TELtY/fOAKKp5a5W1bYUUUV8ufqIUUUUAFFFFABRRRQAUUUUAFFFFABRjFFFABRRRQAUUUUAHWiiigAooooAKKKKACiiigAoooxmgAooHX2ooAKQ9KWk6kc46UxPRG54bAtpjcyMETyyCZP7pHNcD8S/APh3xXNdX9kkMs8jYkmTG7t6fQVqfFy5n0fwqiIxRmKDenHBUH+teY+Eru5i1OMwO2+MZK54I+lfc5bCVGknFn888UYj67jZcy+HQi0nwSfDNxAmWMDSqFZux3DivtvTm8u1tgAABGvI+lfN+touq6TC8UYEiTxlk7gg/wD1q+h7ecmCIAZ+QA9scV3Yqo6sE2fFYemqc3Y6S2AbHcngHiug02JXzxkj+VcjYzfMq5PGAPauu0sLEwIPBAyM9/WvmKq1Po6TTN6ztkkQgoCBxzV6K0G0YRQB0YDpVSzmAw56HtWzDMs6Aq4HAworj5bndHUprpTrkg4GfTin/YAMsxHy44xitEuqR/OcD1NZ19qCJlc4GM56Yq0huyMnWtio20gY7AelcNHaPql4wQZQnGSOpqTxZ4njWeOCOXYHYZ+Xgj0rmtV+JNl4btyzcAHAwea3hTk9jGU13OuOnRaRIXndFXHJYjiuh0HxFY2bRuwEqL0z90c18k+JP2nvD99qLQ/2xBb7TtK78Cun0b4kQzWIeG6SaNujROGGfwrZ4aaV2jBV4SfKmfV2o/EuwntXtkSMxlQpyoU7vXjtxXn+o+JbMyeUwBEmR9BXi0/xESWMqJAe2VwK4Pxd8W9J8OXCG81NLc44j3Zc/h1qoYaU3oKVaFNbn07/AMI/bajDmCQKTyrDtUmjXUljObe84dScN2Ir50+H37Sum6sRbW92sjA4wflIr1RvGsepQxN1cYIIPJqZYecNGioVoy1iz3OxeBI0JIIOOBzWvHbwyMCuAGGD6ivH9A8WN+7DSgJtxjuTXoGn+IVECspBOOa5GrHWmmjoJURBwRj0rOu/LUDoR2IOCKjm1dJUB3ZOM4HNZF7q5AICgqe47VKQm0kVdScjO3HXvXK6nOI5CCTj29a17vVdy8DFclrV4Cpxzk12Uo3Z51WWhz3jmJdS8ManCTkeXuG71GD/AEr5Z+JOq3cZt4IWMNnjPyHG9vWvqO/kEtrcREAq8bDn6V82/EfT/O8HJclRvhnVSR0wa+gw+i5WeTa87nc/B3WLvX/BupWkhLkQeYSR/cYf0NKRg4/CtL9nGyW08K6lLMmPN06cB269VrPf75Poa+bzdLnUkftnBc39VnTtsxtFGMUV8+fo4UUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFHGfaigAooooAKKKKACiiigAooooAKKKKACiiigApF5J9iKWgcEfrTE1ck+I9jc6l4OkWOITGS1SSMEDIK/L/AOyiuL+F3g177Sb3VpDsSNvKVWBHIHI/UV7JoVp/a2hRAnd5TvbkcZAYbl/VT+dQWWl+T4Zure3h2BZGLog7+v6V9fha9qSSP56z3DOnjqiZ5VeajbaTfRQvKS08irsHOPm619FW1woRMnnAwfwr5M8RCSPXYHZW3rMo5HP3q+nBckR22MYKKefpXqTjzQR8g1ySR12mXO1uQAueSa6uzvVjiBzu4zXnllf7BtyASc8c4rWt9U8lNpwQORXjVabTPTpTsd1bawYyNxGBV+LVdmJFOAcHIPANcHBqqyEjoc4PvVg6uIwFDY46E8VwuJ6EZNo72bxGWQMZRg9FArkPEfijbG+WHoME1gXmuvGPkw9c1f35vZfUZ+72rSKsVc5/xzrs9pZyXoZisZViR2XOK8Y8eeJZdZ02aKOUqWUgPuH5V7v4g0h9U0C6tAPlkTAGORxXgE3w2vb6YQqksJU4LM2FHvXrYVxtqeXiOZPQ+fl+HGpXVy4hwy5PzscfjXofw10q58Ey3Invy0UqhfI/hBBHIr2HT/hha6PamS5uXl24yYvlA9qwNS+Gl1d3EjWcy7Mbgs5Izx0zXpyrxqKzPMVJwleJnHxEWdlWVQCMKy44NeV6p8MptTvJ7oai8szsWYzckkn+Verw/CXV4JN1y8VumPlbduBrSg+F13YyqbmbcHxgovFRCrTp7MqpCdT4keL+CNGPhrXm+1lYnAChhwG96+g/C3jT7RfWVhG6zMzgHac4Fc7d/ChdRkDAh5QM7X+U+1dV4A8DSaRrVsyWphCEF5GPQDoKivUpzjc2oRcLRseqWl89rlTnkbh7V2Oj+KJUjj84rgc7x1rh9VKwyqFfjGAwHIqKzvngCIzFgM9PlrwHG57Kdj1P/hJFdRtn29welUH1+Qu6kgqP7rda8/udejtQpAMm47SFOQKkj1SOaMNA249xmkqYOojsLrxCP9Xna2fvVh3eqo7MnA9ya5+fVmWQLnjHJ71mJfs7neMjpg13Uqdjy607nQXV9stJj2EbHd+FeWfYB4h+HeqRSIC4TeowQSRj/Cu8uWxpd4+c4hbH5Gq0OnRaN4G05FVftF4Ej27euSP6A111ZciVjPDLmbuL4Z0qXRvBtx5Y2JDaqpwcYLED+h/KubPrXoOuXa6V4OlsE63M4GT1CqOP515906dK+YzGV6iR+7cJU+XA81t2FFFFeSfcBz70UHoKKACiiigAooooAKKKKA1CijrRQAUUUUAFFFFABRRRQAUUUUAFFFBoAKKKKACiiigAooxiigAooNHegApDxS0nWgR0vgvUGtrme2UgGaPKg/3lO4fy/Wuo8NXSQeK57V9ptdRUSx+gIAyted6fdfYr6C4HWN1I/Ou71Gwk1axF7pgCXVo/nwAdweo/U17mClzU3F9D8p4uwqhVhXS3OL+LXgWPTPE0N3BbmSEyBpFVSTwetdjHIJrC0lA4ZBjHbiuj0bVxr2gS3F/aNFPMjRNuXkYHvXJ6Dl9DjTO427vH+AP/ANf9K97Dyk1ys/J8SldMveds2nIB705L4lyC3fOKqT8JjOcfhVfJJyOOtTUXcdLQ3V1LZ1bHPJpkupOBkOpz03HoKyDJgAE5zVd5DMMYIwa8+UUenGRoXGqlht83I7YyKjsJnlmAXOM8eprPjhLScnG3nOOlVNc8SQaBYId6xl2wD0I4pwp82iCVTlV2dnJrcVrbkFN79gDjFc3bx3XiK5keBCka8Fz8qiuc0DUZNYWe7uXCWwOQc4AweKy9b+JIhX7FZyiC0iOCqcM5710woSvZHJKrzHd31to2lmJby989QctHEuRRJ4s8HXAWO6t7m0dWJjkiGQB7jNeP3vj+2hjOxA7H1PNcrqfjqS4mEcSBOBgjntXWsK3uJT7H0pc654KsEiun1d9Q6Yt44irH2rOf4p2F7Jtj0hUtlPyq4G7b6V83r4mu4389GUEnA6cf5/pUy+ObyRvvKuD1HTpVxwiQ3Ul0Poq21HwzqwK3DSadcMeSV+X8MVJf2l1pCCW1nF3asAwZOeK8As/iE0LYlZHA4wBgiul0f4nS6KU2HfaScNExyAPaolhWtUZup3PW9K1y11BlS5+SYk/Q1Pq2jSzWbTWknz8gD+teZ+I/ENqywX9lMNpPzr0K1s+FfHktxaoplUgHGS3auWdFxV0aQrp6Mkiu7mKSRLmMwv0welXo7ncx2ERkjnAwKl1W6GppExAY+oxVIR7IxwcdKzj5ly7kwkZirEnOMZNSKpJG3171Vjlxuz95sYrSiG+MEHBrsicMzTtLH+0LWWBn2eYNmceuP8auXcdrqOs6bZQuXXS42dwBnBwABUWkkrtKMeXRR07n/wCtXfHw3aqbi5WJbaaYAyMg+9gd6zxD1ijowkXZs8j8V3pn1ERbjiIDIPTNYIGPoelX9eYHV7ogg/PjIqj6e1fJ4uXNWkz+j8noqhgaUF2CiiiuQ9oKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiijPGKACiiigAooooAKKKKACiiigAoo7+lFABRRRQCD0ooooATrkV6R8NZBeWwTzAHhONpOMg15wDg1qaBqcml3u5ZAgPU9hXdhKnJO3c+X4hwTxmCko7x1PbL3TJJrcAbEQA8L0+led6cn2DUdVscqwD+Yv41YfxhqEduxWIyIehBBrmNFbULvxhJfyQslvLGY33cc/T8K+qw0JqWp+AYuFo2fQ6G5GBzzxVaULGuQxH1q3dAAvg4IGORWfIwcDJyOAB6VdVa2Oai9CQJlRgdcc0qwlcsBn8KWGYBU56AA1ejUSYCtxjpXntWPSgc7q961pazbeGKnHsK8T8d+KlvLuBLiQRwREk88Enj+Qr2fxFbSbJNoByuDnvXm958HP+E4xbtIbVm+bzIxk/SuzDThDWRy1U5aI4jVPijHFoqaZbysiAZKoeTx1rC0jSfEnjmZbfQ7CeZd2Gn6IPxrubL9lZdI1BZrzWZLuCI5aNIwufavUdLnj8MwLa2JSCBDwo4HTGa9J1qSX7swp05J/vNjzzwr+yN4q8VXKi+1GO35OfLYk4/zivYfDn7Afm6c89xrN3LbQNtm8rBZPQ46j8Kpx/EHUbNwbK5aIrgj5uB/nitCD4t6wWYzah945YiTBP1Geea53WkevBUYx0Re0/8AYH8MQXd9FP4mdJ4eQLifA7DB49x+VVNf/Yo8MafFhdckEzEkL5gIAwuD096k1D4r28ybxqKtcscswfk9P/r1zF98Spbx2EmqLgjH388ccfpUqdS4+akuhxPir9mQ6b5n9nays5AyEkwPwrxnxPpfiDwW5icSNEDjBGRj1FfSNt4otpTtE0lywHLKvH4V0Nnotj4hgC3tqskT8bZQCDWqxPJ8Wp5tamqr9zQ+N7Pxdrd5PHZ28EjPIwAA6GvX/COn6tp1tEbxfLcnkCvcLD4b+GtDnM9tpkSS9QeuPpWJrtukcpKIAFOQPauepilU0irGcMO6esmO0OM/ZVMgDHH0rQnjUQnAx2qpp7qI1OcccCi7vt3yqcCuRas6G7RKyY88jIwPzrUtmAQDjpWMp+bt6k1dhn+4Ack8ZPpXVFanFNmtcaiNKhsZWwu64HHbAB/+tW/q/wAQHubKREGMj72ccVzOq3Ftb20BeKOWeMfu8jO33965+e4e4YlzkZ4GMAVx4+tSotXd5dj7bhzJa+YWqyXLC/3jHYyOzN1ZiTSUnb0pa+Sbu7n7zTioRUV0CjpRRUlhRRRQAUUUUAFFFFABQOKBxRQAGiiigAooooAKKKKACiiigAooooAKKKD1oAKKMYooAKKKKACijsaKACiiigAooooAKAOfb0NFFANJ6Mek7oBtdlGOFBxipYL2W3mVvNJGRkHmq3ce1Kc8+mOK66eJqwknzHk4nLsNXpyjKmtfI7maYXMCSr91hk1lSyGMNj607Qrk3Fg0P8S8fhUF7JsBH1FfY/xIKaP5sxVGWDxM6EujGw3+WGcjHGMVoW1+FBIO30rm5LrngYPSojdNvA3YrnnBMcJ8p0t3ci4bLFR6HHStfQCkCllIBIBBA5FcRFdGRwC5xXQ6Nc5GSSGI6VzSi0rHRGSN7Ugsq5J7c+9cfrWgxTqWQbWA6AcV1UjgpuPU1EloZ9xPTPfFTGTgXKPMeIeItFuUD7WcZOAVJxXD3dlqUTlVDE44O7IxX0/c+GUu3AMYIx0A4rMuPhr9ucqsIU8YO0gfSu2niUnZnPKjI+a/7J1KVwCNm7gFmxW7pXhPUGUNIeD0A7V77bfCqKDAeEO3XOCQOn+FXovBC2rg+USR0GK0nik17oKgzz7wr4au7dEXChBwRt5Neg6XZmCEAEAA4xzzWpb6e1uv+qC9hx0qKQGMkDg59K86U3I6FBQQ6W8ypL4zjBxXIa4u+fzRggDAH+fpXQ3UqjIPVhXPargo209+1aU1qZ1H2MZL0QJg8elRfa/NbcxwPSquoRGNSxOcc1n/AGkvjnAOa7oQOCcmbyzjk7+cYrR0hBPOCeVAJzXNQy7sAEHiumsv9Csy2SGwB0rojFRTkyKcXXqxpR3ZW1Cc3F03ovAqCgZ6k8mivhcRU9rVlI/qHLsKsHhYUUtkFFFFcx6QUUCigAooooAKKKKACiiigAooooAKKOlFABRRRigAooooAKKKKACiiigAooooAKKKKACiijjPtQAUUUUAHWijpRQAUUUUAFFFFABRRRQBf0W5+z3eCeHHSr2qwnBIwAeePSsFW2Orrxgg/wD1q6Jbhbi0CnBOMrx+lfY5TV9rSdN9D8I43wDw+Kji47S/M5ieQA8HoaqS3mMKoJI6YrQ1KzKoxHAPcdqwZSYSeMelenKn0Pz+NTS6NzT5vM5IAPoa3LR2Uhs4Oc/hXGWF627ax4HI7YrorDUQy7SQTnGT24rjqU+U7KdS51dtdCQDIz7Vs2gEkalh0Ga5e3n+cNkDjoK2rW/XYFUnGMc1wSjY7oSudppk9uOqAnOAK0Q434aPEeMHb1rh7bUhbvkt82OT2rdttdijTMjNIRyMEDn0rNxN0zWeNmlJifA6AZpkqvGAGfkHHIqiddRzgFQ2cn2FVrvxDFk4XB6Y68etKxVyW7xIMde3FYN8hSTGcjGakudZG7BIAPIArKvNSLLkdMce1UkYzkkVr4ccdRXP6hOoUjHIGMCtK+vDMpYccdK5u/ugr5BHHWu+lA86pOxl37lgcn2xWJI5Eu0HjoKsXuoZY+mar29uZnDEewGK9SELHBOZuaJbl2GQDzz9K3r6QbFgXjPLf4VBolkIbYzN1QZA9frTHfzZGkIwT09q8/NK/wBXo8i3kfc8G5b9dxn1qa92H5i9ABSUUV8Mf0CgooooAKOlFFABRRRQAdaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKOlABRRRQAUUUUAFFFFABRRRnFABRRRQAUDrz0oooATouPyrR02Q+RtzgpyPpWfU1lJ5U544IxXrZZV9nXS7nxvFWCWLy2emsdTSljS6j55I6joDXMalpwydoI+tbEl21vIQPzoaVLpRuHOO1fdtXR/NavFnHvG0TdMdvwrR0+5aMHeB1yPXpVy5tY+u3jnr1rNMIiYHjHQ+9Yyp33OmM+xvQalsjHNXodbjXJJ2+wFcwHO0k8fSs66uJIHyB+Ncbw9zsjWsd0df3uOdw6fLVhdf2ghCADjqeleYnV5IhnP0A4FEOvujAkkg9fasJYZm8K56n/wkBUZMmCe2OlQtrca4OcN/eLV5mfFLo/GADyB1FV7nxA83Xj6dqhYdmjro9Lk8QJvYb+3qKg/4SLf8pcAAYyMdK84/twsu05xjb1qxazvKFx3reOHtuc0q9ztJNW++Q2F6D2rA1HUi5IXkdCaillMceCSTj0qrBAZZBwSfT0ruhSUThnU5txptmflRuOec102i6YJE3Ou0dcngCq1jZpGw3duw7VqpcYAjUnaOcf0rqSscknzF28k8q0KLxvOOPQdqo4xj9RVm/wAM8Az0QZx/n6VWHAr4XNqrqYlp9D+kOEMHHC5ZBpay1Fo60YzRXin3AUUUUAFFFFABRRRQAUUUZxQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRQaKACiiigAooyaKACiiigAooooAKKKKACiiigAp9uQkynHHTFMIxToBmeMd94AHrXTh5ONWLR52YwVTCVIvsyrqEoRjzzVFb91OKueJIXtLp4mDK8bMrKRyMe1cy0zK4+Y47e1fo/Y/lGSSk7dzbOoF8Ajgdaa7rMeCPXFYxuTnrj6Uw3hB4OPpSuJKxsSBgPlI+lU5Z1b5XTOKgi1UoBkZ7UrX0Exz90nrSLKlzbpLkAYx0rNltmjHse1askka5KniqM7hvT2zSsO9tCi8WBgfX6037MzEADj8BVg4JAyOmKciYORz9adkgbFtbAKuWbdk+grWV0hjCxqOOAaow4ZQCSAaspJHb8l/wxVpGTZcghaUZc8+taUPl26YHUjBPWsKXVC+ERfQGnJeYBP8AFTMtWdD9tjRcBxnPWn2LGWbOeOlc3HKWfPPNdDo8gOD1qXIajqa92my4ZTyQAKjqzqI26hIvfA49OKrE81+eY3/eJ+p/VOSf8i6j6IOlFFFcR7gUUUUAFFFAoAKKKKACiiigAooooAOtFFFABRRQeaACiig0AFFFFABRRRQAUUUUAFFFFABR0oooAKKKKACiiigAooooAKKKKACiiigAooooAK3fAejP4h8YaXYRDJaZSQB2BzWF0r3b9lPwodR8TXesPGDFbJ5aEj+IjOa9PLaDxGJhA+a4ixywGW1ar7fmeVfH3QJPDfxD1a3dCElb7RH2BDf5P5V5Ncc5I4HpnpX2t+1l8J7zxhpEGu6RCZ9RsARJAo+aWHPb3H+NfFUjDJ+Qq6khlYEFfY+lfolem6UvI/luhW9srvcrhicjGfTNI7EEelC4VjgmkcZxnvXMdhSupyOnSqUl66A55HtV25jGfTPXtmsy5i2qeTkDHBpoAGuvD3GPemt4jQcEKCf0rHuYCWPftWdcQPyAmcDmrsB0h8Qwg5J6nntT08SRgcZOK48QlTkg49+Ks20ZJIx9KYjql1/zCBgjHQelWo7p5yN3QVz9pCQw6D8K24RkAdB64pbEs0opN2RnGAOlSrIVGeAfbmoIv9XyBmpIk+cfNgVFxWL1vlnGRjFdt4OsDqOvadZxJ5kss8cYRRknJGePpXEGeO0QM7gIPU4r6b/ZI+Gl1qN2PF+q25gtUGLCKRSpJ7yY9OmK0pU3Ukl0MK01Thc5743+Dm8H+PLmJU2210qzxkDgZHQflXAA5FfWH7U3g06x4StNcgTM+ntiQgclDxn8MV8n5yox29eK+KznDfV8S2tmf0VwbmSx+WQT+KOgtFFFeCffBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAGMUUUUAFFFFABRRRQAUUUUAJnFLSc+lHT6DigV7bijPQDJJwor7j+AXg3/hEfh5aB12XNyPOdsc89v1r5a+Cnw8ufiF46sLRIibSFxLPJjI2qc4/Sv0CGipaQJAgCoiBVA6DAr7zhzCuF6816H4T4h5opqGBpO/VnHagFkYqOgPX8K+bPjt+znD4nNxr3hwJZaztDSWxUCO4x3/2Wr6nu9HmDEqMj+7iud1fTZoELFMKOv+Ffc1IQqxsz8OpzlTldH5d30Vxp2oTWF9BLaX0DbZIZFIYUowB+APpxX298VvgpoXxPtG+1Qiz1NAfKvoRiRD6H1HtXx38QPhp4i+GF55Gq2zT2AP7rUYVzG3sf7prwq2HlS1Wx9BRxEamj3MF1BwDx9Oaz7qLah6GrKTqY1bcCCO1RzEMB6ZrjTsdxizQ9cDn1xWbNFvz1BHHFb1wvykjg56VQMa5PbBp3YrGS9vuByOe2alt7crIvPHpVsoByck+oFSRIAevPajmsFi1aQbFyevb2rRixsHC49KpRE7OTxnoKtRyLGwLdM4HoKZJZjPzAYxUv2iOCMFiWyQoAwSfYVBAZtSvobCwt5Lu+nO2OCJcsTX1R8E/2eIfDTRa34jVb3WGAaK34MVtk9vVvetqVGVV7HNVrxpLU5P4K/s4T+I7mDXvF8LRWasHtdLBwX/2pPb/Zr7M0CBLG3SGNFiiUAKijCgDtisOyX94pHAx0retJQGG4Zx0HYV7lKnGmrI8OpUlUd2b2qaTb69oVxptwPMiuYzGV68EV8AeMPDk/hLxNqOlT/fglKg+ozwfyr9AtPk3qMEYA4x1FfPX7W3geKI2HiSCMIWbyJz03cEr/ACNeBnmE+sYfnjuj9B4Fzb6hj1Qn8M9PmfNVFIMFBg80Zr8uP6gTuLRRRQMKKKKAAcGiiigAooooAKKKKACiiigAoxRRQAUUdKKACiiigAooooAKKKKACiiigAooooAKKKKACikzSjoaACijGKME9OfagG7BQOantrG5u5BHBC0rHoFXNd14V+B/ivxarNbac6qDgl+MVtCjUqaRRxV8bQw6vVmkefbT6VPaWFxfOscETSMTgKqkmvq74f8A7E890ba61u8EUROXhWvf/B3wF8JeBS8ltp6lsAh5VDEH2r2KGU1qlnLQ+Ix/GeBwt40veZ8OeFP2dvF/ia5jT7C9nDIuRLPwo4r3LwF+x9osE9sNbu2urpiCUXIQ+3/66+lZ9s0qQWsQDHAVVrXsrCOzkSBSHuHOZZcZwMdF9q+hoZXQpb6n5nmHGOPxd403yryOe0n4faH4CgS10e0igIAMjRqAC2atGPcRxyK2NVjEd2+0AZHyjt9KxjI6kk/SvqqEY04JLY/OcRUqV6jnUd2MMIIJZahl06G6QhgB9eakd2yQScdqiExcbckEnA7Vo3bYwUbnK674FgnRnhOG6/8A1q8z8U+EIrizms9Ts1uLSVdrJIu4MPcV7rMCgCjnFUNS0qHUo2WVAcA9qFLTVD5Lao/Ov4pfsrS2TS6h4JYFMkvpk7cf9s2P8q+eb37VpV7LY6hBJZXkJw8EylWBr9U/E/gufTHMtupaPqRjt7V4x8S/hF4e+I9lJBqtkqXYGI7yIbJYj2IP9OntXPUwsZ6wOmnipQ0nsfBU83PsenpVZnBIB+lelfEr9nfxP8PElu7VxrmlhgFlt1PmgH+8grylboBijZVwcFWXBB9K8qdOUHaR6sJxqK8S11BwTQCoUfeJ+lRlyec49fao2uFjJPp09qixbdjSgnRYwxIHGTj09a6Dwb4J1v4k6mLHQbYSIpxNdscRQD39/Yc1u/CP4E678UZUubjzNK0BSC1wy4aUf9Mx/WvtHwV4G0jwPo8Gm6TarbQRjov8Z9T6130cM5+9I8+tiOTSJyPwe+Cmj/C62MsYa/1l1xPfSryfZR2A9K9ViXJB2k8/z7VFGgyeMDAx7VraZp0moTJHGOvpXqKKgrI8h3m7yJ9LspbmTakeSe9drpvhd0VDNgk8kf0rV8O+HYtNgDMMOB0HNboCAZB2kfrUymV7PQz7LRI41OVC7hjjiuR+K/giy8U+F002/LJbS3CKHTqjf5NegYJJwc1ai0+LVvLs5gCHDMBjgEA4P8qzk+aNpGlK9OanDRo+O/EX7EPii1leTRryC7tgu5Vf5Wx6cV5Pq/wL8aaLJMlxolwViPMkallP41+lmms4+wckZUxtg4GQf6Vo3DxSB47i2jlUghmK818nXyihN3jofqOC42x+Hio1bSSPyQm0m8gYpJbyKVJBBUgiqhBQ8jjpX6qaj8OPDF2k6T6PbncOWCKevpxXn8n7I/gbUpZHVGgdjkAErXjVMlnH4GfaYbj3DTX76Fj86z8o65FFfZfiD9hmKfU5m03UxFBkFVPavL/FP7InivRtQMNkgvIsYDKcc1508txEPsn1OG4oy3EWSqWPBMAd8Un4V6B4n+B3izwpGr3mlTFG4+QZrk7vw3qllEXnspYUHdkIArilQqw3ie9Sx+GrK9OaZmUU4xOD9xvypuMYzxWNmjuUk9mFFHb2oxSKCiiigAooooAKKMUUAFFFFABRRRQAUUdaKACiij2oAKKPrxTkjZyAqk54HFNa7EuSSuxtGDnpW5o3gvWNcu44LWwlkkboNpxXrngr9kvxL4jR2u0+w7TwGHUV10sJWq/DE8jFZvg8Gr1aiR4Qq56DJ9KvadoGoatcLFb2kk0p6Kqkmvt/wZ+xroemQW0+oEzzqclWPBPpXtHh/wCEHh3Q5VmtrCCNkAClUAr2KOS1JfG7Hw2N46wtH3aEeY+A/CP7NXizxWpkFqbVV/56nFe1eDf2LIUt4rjWJ2eUHLRJgA+1fX1vYW1ij+VCqf8AAR19agupvKUYyDXtUsqoU9XqfBYzjLMMVeMHyryPN/DvwE8LeHrqCa20+JJUHXAJ/Ou+j8M2em2zGGDYSR0FWNN/f3AYjNat7bZESkledx+lenClCnpFHx1fGYjEO9WbZSt4hp0ByRnGeFxisPVtQa4kWOLLsflCireu6kIsxx8kHA75P+RTtE0wRRtcSDMj8jjpW1ziJNJ0v+zrfzCFM7j5mPUewp9jjz55Odv3Rx0q5MdsL4PPrVW3XbD3BPIoQdSLWo/9XNjlX2k9gD/kVkXSYfIGBXQznzYnVgDkYI7deRWS9u3mSQuDlTjOOo7H8a7KU7KxzzjcynWohH1J4xzWhLZshII+lVniZwQvToeK2vcgqhzuG7j1q2kKFQy80xoAf/r02JmgzjkHtQi7D7m3jlTZIu5SMY9q4XxN8Ml1BWmtF2PnnHP4V6AhDpuXBwOc/wAqwviX4wi8CeDru9JzdMpjhj6AuwwPy/pVptbEuKe58qa2tz/wmJgMuLa1Yowj6Fvf8q5L4i/A3wx8QoZJLuyFpfnhb+zCpJu9WwMMPY12ei6BfttvpxI5u2LklSS5Jrv/APhErXRrEza3OyXBAMen2+N/Tqx/h7flTlyte+L3k7QPzT8b/CzxF4H8TQ6M9rJqguiRaXNqhYTY/kRXuvwV/ZaEXk6142iEkoYNDpanIU+r/wCFe+61f2FnMGtrOOKQnIb7zL757e+K1vBN/Y+JNej0qa4W0u7gbYmdiVduwPvXHCnBSudE51HCxdtrKO1to4YIlihjUKiKAoA9MCraR5U5GGHFdlefCvV9OdUKeaoGQwzgirGn/D66LgygKOp+leipxS0PPs0c1o2iSalcIu044HoK9R0Pw3BpESthTJ646VPpOgR6bCBsyB371qtyQO3biuedRvY1jC25EzFUAHUdRUZBbJxmriW3mHoeKuQaY0mwDjPXjFZ3NbFG3jIOccAZOe1a2jQN9viuGxt3GNR6n+I/y/Ko7mzdQkMXMkjbV456VrtAtpe2FtHyIgST6+9RUnZWCMNblV0FsVz0juiPTrWjcIhcjGA3Ue9V9TQtE+OSX3/rVluWQ46jNczd0b7kNqheEh+qnANOFv8AL1wVHDAcg1PGnJA6Hn6VYaPKHsKi5RSeFbvKN+7uEGARwGrNF79nuhBdxqT0DYxmtqALKSrcYbKnuBWX4utR9ijn4Do2CR/n2oQJtdSX+z7fVYBBOiuYwAu4ZyKxdX+Hmi69aPa3VhA6E4P7sA10dpHmztJyQshQHjjNWwoYDAweM1EqcJbo3p4mtS+CTR5Dcfsw+CJ4SDpcSEjqvBry/Xv2ItMupp5rO7eDJJVcZAr6sVS2cjIJqZIiAcj5eg9q5J4KhPRxPaoZ/mGHd4VWfnN4j/ZG8V6OlxPCi3EUZOMHBIryjWfAeuaGpe+06eJAcZZCBX62y28NwpVwrqc8Fa5/WvAWka1B5VxaQyxZ+6yg15dXJqcvgdj7HBcd4qlZYiPMj8k2jZWwylT6Him5xX3t8R/2QtE8RC6udMH2K7YZVUGUNfKPxF+BviH4fXDfaLYz2oOBNGCR+NeBiMtrYfW10fpeWcT4HMbRUuWXZnnFFOeNomKsCpHBB4xTQMivKatufXJqSuthc8UlFFIoKKKKACiiigAoopVjaSRUUZJ4AHenZvYTairvYQf5xVvTtIvNVmENlbSTyn+FFLGvXvhJ+zdrPjq4hnu45LWwJBORhiK+0fh/8BPDngq1g8mzieZFA3lRkmvbwuVVcR70tEfBZvxdhMufs6b5peR8b/Dv9ljxF4teCa8T7HayDJO35hX0l4D/AGRPD2hRxPfRC6nUghn5/CvoO1s4bZAkSKqDoBxj2qYkqoAAz7dq+qoZbh6K11Z+RZhxXmGObSlyx8jndO8AaJo5SS3soo3QcFVAIrejtooPuKAD3A7Uz+0Yo3EMpAZuSe45qG7keymjTgxMchuwr0VGMPhR8fUrVKrvOTZfK8j09ae8gAAAU9BTYCGTd1x0zVTUL4WOMgF2GMDtT2M0MvLnyFKkgn19DWYZDcMMHiqZna5ck8gnpW5p2n72AIBA644pNlFnTrQQxGZwQQOPrTNSumtYnaR13sMYBzgelW7qaMHaBmKEcY7muQ1i5e/m2L1JwfYUkAul2j6pcvcPkRIePQ9a6RG7bQuOBTbOzFvYxRjAIxuA6U502DjtQNkdz8y4XjjpTGykY9RTgCxyevtTJ5SAefwqhDOH+UkDjPpSXB2eXcR/O8Q2so/jX/63amKxZixOTjHWrG7ODwueDtpp2JfYne3guoQ6gSKwypAxmq0mmgEYAUAZOB1pbK4+wXgt5CPsszfJx91vT2B/xrTmT5zGFOByCfT0rdTM2jn7iyEZGACPaq/2FehXLV0D28bYB/DFQGyQEtggdsmtVImxjLbKrDA4GMntXhXjzUP+FlfEqz0FDnS9Pk/eFedxH3/5YH1Nd/8AHf4lW3w28LGK0O7W78GK1iHJHTc2PauB/Z9+GmoXOlT+Ib2aa0nuVzbn7+/n5mbvzVc1ldlRjc9W16zsZdLsk0bSEe9QCOERrlY9v8VebeN/Dssc1haT2jLqbDEkhyWcHoT+f5CvW7DRzJMYboSmQDKmyl+bPqP8asT+FLK8jltbRZDdErI99KRK6sOg9K5JS0sbWPlbx18Po7KC3itZpResrtdrtyY1zxg+4zn615ovhGXRgskYlicN5gkycl+zZ9q+2Ifhfo1jcPJrF3Jqjs29kCkBz78/T8qq+JvB2ia/4f1O3gsUgA4Q8DY2ODVU58u5LRlfBj4hyeNPDEdpfy7tUsgElz9517P+Pf3ru7m0VgHQ4JGWC9PpXyVp91qvw58SLdwJ5VxbNtkjbgOo/hNfVPgrxPY+O9Fi1GwkDqwAkjbho2/iUj27V0tW1Rk1Ym+yEkBgMnp6VJb6csrkgY56GtY28S/6xiRnAxxip44owNsacjv+NTclIqxWi7SG+XacYNWfKCKSn3sGpo4Acl14GDxzVfUHZI0hjXbczHavOcepqLmhFpaCeVrpgcISkZHfnn+n4Cp2wJg+PmAwCeuKsrCtvboi42oMDpwMVXZCW/2c54rmcr6miVhjkOctyOmKmVTgHqMDHHSiOPjOSRn0qZAUGc4/pU3GIoOPTipgQwOM5PQ+lR7Mj0NPHGMAelRsAkcWybcSvPbtWX4rk82wCjoWz/OtlgVK4AB9ulYWu5kh9FB6e9UmBftrcvp1spPDRjb7VELyXT5zFcplM8NUlsCunWjBudv5Cr0qLKhWVA2RwfQ0MCG3ljnO5GAz2z0q0SQuCATjOKyptLeBi9uWAz0xj/PSprPUfNfbMMPjGcYFAF1FHX9MUDk4IAGalMe4EhuSO1Vo5l3hPuSYyD6U0wHvECTnGR36YrD1zwxY61Ey3UMc8RBGGXIrokOYgSOg6AVRvbgWvlsRuRvl54NaJJ6MFKVN80XZnyl8Zv2TbPW1nvtBRbS7wWMAACN9K+OfE3hi+8LapLYahbtBNE2CpUg1+tt1CHwcfK2T6jFeMfGj4E6T8RLKWRYhHqOMxzqo3A+leDj8qhWTnS0Z+k8PcYVcHJYfGO8O/Y/OPH8s0V0nj3wNf+Adfn06/QxSKcBiMAj1rmwMdq+GqU5Upckj98w9eniaaq0neLCiiiszoCjI9KOpqa0tZb25jghUtK7BVUDvTSbaSIlJQTk3oh+nafPq16ltbRGSeRsKqjJP0r7B+AH7MENrbQ6r4ghElySCsTKMIK3v2ef2b7bw1o9rr+rxLJfuN4Rl+5nofwr6OtVVFAUAADGB0r7XLcrUV7WsfhfFHFsqknhME7Lqx2jaPa6TbpDbxCJVG0AKBxWvHFjt1/Sq9umHHHAGTnrWijBQMqCpxx6V9G7LRH5PdzfNJ3YxI+nGM8bRim+XjB6MOKlMgG36cH+lQl8ng4PU/TH/AOqovYZi65ZllNwnUcEYqzp7jWdKUEDKHIJ61puqTQMGXAYHI96xdCcafNqNuQR5Q3DPv/8AqqkKxdnlXT4mLHHy42+1crd3j3cxZiSc4FTatqbSzNzngik0my89xn5iT+VJlWLukae80ikjA6n0rp2QWsSRJjzH4B/ujvTLK3W0QswARR1744qpd3qW2XcgySnAUH7g7UgKusTiNjCnAHGRWPpsSzXZZhnoT7VY1iRZJsqeCoOataJCBFuYD0/CkwNdASoK8ZzimBC/LDn2qdFyBxjApvII5461IFcx+2Pp1qKa03ISMc1awFZsDr39KaUPC+lWgMsRlDgjFSp1PbBGKusobOccjP0pCq4BwBxke1O4WK1xCk9uVfnt757H8O1WdMu2ubd7adszwjBbuV7NS/LjdgbcZqjqKMqm8tk33UALCPpvX+Jfxpp3JaNXO4bhjeOoA6Vz/jbxjpngHQLnVtUl2pGuVjH3pGxwi+9aFz4m0+w8PPrcsgWxjg84t3AHavnmx0HW/wBorxPHrutrJp/hC0c/ZLMtgyqB1+pAHNbp2V2Slc4nwf4W8SfHn4iP4l1YJ/ZEcu7E4YRIgPES469s19WefNpcEUM2nRLBCAqPZEjYMentUmh6TaaPaWthYwR29nCu2OJOAB/nrW9JAspJBwdu0jjBFYyqc+hry2OKtvFH/Fa29hd+V9kvbdmt5EYEnDdGOOM5/StzV9X+xxNBaIsagn7gwAPrXmvxt8PSaRaaf4i0xDHLay4lxxgHGD+PNd94E1WLx34dtNTRQgdcSMzZCsOq4qnFWUkRfWwy00m81ORZHARDglj0IrZtfDtvYiTCGcuckSD5Rx2rTmvbWwCgOAVA5J6VkXnjGxhzmfce21c1OrKOb8XfCnSPGTy3F7blbzy9qzI2APT5eleICy8Q/A7xGZ0izYOfnVciOdM/+hele7ah8Rra1U+RE0r9h6n0rnNd0vVfiPpFza6h+6tnXMNvGP4+xJ7VtGbjoxWudT4Y8Taf4w0mLUNPlDxPwV6MhHUH3rbtxhs5XAHG2vj7QtW8TfBLxRLPdW8sVlNJ5UlqVISZB/Gv+NfU3hTxNZeK9NtdSsZlltp0PT7yN/dNa+hi9DpAwbG75QoySP8APtVKwcXVxLeMM4/dRYHYdT+PH5VQ1q9khSK0iP8ApN44jjx/Dx8x/AA/5NaCKkEIijwFRQo9gOhrnqOxpFdS2TvHAAz1GOlRMnIOOM/TiiJSADzyOKkyWAyuNoxWJYyPDSYY8evSpdy9RyOntURTzOnB6U5flXgDGMYGcUAPHzHg05DsznjBpAFwMU/GcYxnrzQAMCE447Vk6upMPXAJ6VrlSAPm4GB07+tZ96mYzk5yM0gI7XK6faHdxypFaU2QgcnPGcD0rLtV3aQ38RjbIx6VpRv5ttnocdfSgBYZ1m+U5BHzY/GoLuzBG5R0HBx2qGWbYMDAcdx/KrtpcrNFsc8+tFuoXsylZ3r20gVsMAeQatX1sJo/MjOHXkEY61W1C02SbugJ4I6CmQXDD5S2VzgimBd069/tCBudsiDkHjmsrWPOvdWtrKIYEcfmyEdhngH8qlBFtdean8ZGcdDVklYb6e4Aw8saL9QM007CaEUGCELkEAY5qpdDoc9e/Q1LNc45yCO3HSq0kwZVFbRd2ZyR418d/gja/E3T8whYtTiGY5cdR6V8DeKvDF74S1m5029iaKWJipypFfqbeSNCxP8AFGc8eleEftUfBWPxhoy+ItMgUX0abpAo+/714OaZdGvF1Ka94/SuE+JKmBqRwmIfuP8AA+EaTbU1xbyW1w8Uq7HQ4IIxiq3PtXwLTTsz+hYyUoqUdh+MflX0Z+x58LE8Z+Lm1S8g32tmNybhkbs188QQtcXEcUYyzEKABmv0U/Z68Nj4efDHTnZNk92wLNjB6V7uUYb29bmeyPgeMc0+oYH2cH709D25IIQk23mBVFuoHGOaTTNPZImaUcozKTjGcd6ji+S2sIl43sHYd61r7/Q8PnCPzgL39K+9b5VY/m5e+7sptKolCggEkDFSvLsfZ/D0+nvWRBL/AMThieg6Ac84q9OxIBIwcc1k0aWHtJiMsD8oGQe9JkMBuOCSDxVT7QWjCrgAcYpHnxwDnBCilYZowXHmOVbAFVNXWOC2uJgQHfClvXrSwNtA3cFsACs/xLJuWOEcgcnFVYDn44RPN0z3rrtDtAo3AAc84FYOmWn7wYP3uOldiqf2fagqf3pGFBHHTrUsZBqd6sMXzH5I+GHT8P5Vy9rOdTunuXOUBwoPQ0zxVqhGy1jJJY4YjHPFX9LsxFZwRYI7njqapoRU1p9lzbIo2jYAVra06IKiE/lWLeZuNdVP7oxkc10tvDsj5HIxipYFoMQMA47dKY7+uMYxmkDnPOBxnjioZJi5woHHJz3oQD8AL8w5xjNMkPQ9+9J5o2jGB+tMZnbgAEdAfSmA4kg5/hHb1qGZ2wu3p0INKz7GKArnHB7CoiWVRwOcAn0PrSsBMzgoSQRhRxioGYq5OSAMYx1pZGEmF7E4JB5xTC5llHPGQOaewHmviT4aarq+vfZI9SKeDruUXdzYknIYHmNf9lsfqa9DhjigiihijVLeNQqxqNoUDoMVLcEkhlyo4G0dBUDqCTtOC3GapybCxY08uHkXGChxWssmSAAeef8A69ZVqfLu0ZiuXTBx6j/9f6Vt2u2NWYtuOeNuOlPTcW5Uv9Nt9asZrG7jE8MylWVu+f8ADtXmulQv8OYbvRbCUy2/nvISOgyf8MZ+leqSupVmjfY2OGIwAfWsaL4fwF3kuLqSd3bccAKKcZW0YmefXeqz3RJdsZGCD3p1h4c1bWiDFCUiJ/1kvyjFeoW3hrSdMwyWqPIOjN8xq8s2FIGAB0A4A/Cm532Ecno3w5tLBxNdyfarg9c4CrXQulrYofIjXfjjinzyYGT09BUcqqFycCs3dlnJeKvBtl41sJbPVoBJG2SjqMNG395fSvHvDOn6p8CfFZt7uU3HhfUG2JdBcIj9sjsexr3y7vFtonKk/KOB/Ss3UdMtdY0k6VqVut1azL+8Q8gsep9uvH0raEmiZJdTN8M3y+INUv8AWEdZLKL/AEWzZTkN0MjD9B+FdKoG0jAGetZ2k6VbaFpltpthHstLddsankjn1/E1oGMICFOR3rObuxpWLMK7cbjwOB7GpBKAO4OcEHioY920gAAD19PSrBZPLGTlhxgioGQ/NkbeCD+VSCMABc+/401mMWcYIJ5OM55oWErhj0I+6KAJSoDBuBnqKcB0OMcelJwcEnAxg5pwHy4BGOwzQAEFgcHAwTVaUDy/mAyOKuxDIx2HAHpVab5gRjoOKAKemlVFxE33W45+lTaezIZrZj82MCqsDbblxwBj9asTfJcLOODjaTTtoBWvMxAtwPX1qhDqIilAB24rYvYRIScnay5rntX0typeI8r2UVNmPc6q3u47qJVOGOCfUCqtza+SxPb2xXGaVr0lhceRMSpBzk8DFdzbXUd/AHyBlcimIpM2wopB68e1N1aYRCJicEqR+R/+vSvmOcRsOnBNUvEBZIIGPI3FR2H+eKEBWkucryR9BUJuixA7juKzJ7vC8Ailspd7Due2OKtOxLRs3xEk8QPymaIgj3FXLG2j1Pw4VkG4ISrK3TFZ+suYxp/PIbafXp61seE/9VfwMcgvwMetXzXViPhd1ufC/wC1R8Ef+EYuz4j02P8A4l8zDzFQZCsa+btv1r9VfG/gWLxr4G1fRLlFJkVpAx6j5jt49iK+IP8Ahm68r5HHZa6lXmprQ/cOHOKoUsEqWKlqvyOE+C/hNvFfjW0iCZiiIdq/RHWbdNM8I6dFGNvllAPQYr5b/ZS8ILaWLapIm15nCrxX1Z4zBTw2vGFyBz2r18ow/sKKb3Z8TxlmX13MJU4v3YaHUaFMLq7tWJDIY8qO4FGr+IJpLk20cQkgAzJ67faue+HGoGW0cu3KRMo7kYxWtpCF5p5X+Y4xn8K9ea94+FhsPhYJqeFwQyhgw9u9WpJi0uMcAZxVXYpWyuV+4GaIgeh5FPLnYWznnkVkzUZMhQllzt7+1NhOep3duKinkLKMHkDv0p8AOAMZ5xgcUgNKyiMs6HnC889aytSJuLp37ZwO1a9uTa2csp64wPyqlY2TXbjJ4J/Kq2AueHbEFGmbhVHU1HrOphLeS5bhcFUHfb6/jWheyrGqWseFRBmRh0IA6V5v4x1s3NwLWI5CH5sHg+1JK4hmm79W1YysSRuLEHiu7s8Rnex+5H8o9eK5vwZpxjjErDljkcdK37m6CWtz/sJ8vtQMy9FjN1qc0xycHIxXUY/dYYnOfyrF8MWu21L9Cx7elbzqrKuFwQePepYEDtlRjA+vHFRE8kjoPTrUs+NoU4IOOfQf5xVZSdx4IHSmBNhSWccZ6imvjGBkfShR1LD5eg9qR2KjOMZNAEUh8zgjAHI6flTDgJszz1wPSpXKAAYGOuP6U0qrcnAPUY7UdAIzgvlSBxzx6UhAwdoHbFGVUg5AOSCBTmQADyzuKg5Ge9ADXwoCYBGM/LVab9wpVedgxnHapSGAAxyACcdqiCM4xjBBK+xoAZbyHei4ySMlj1B9K14JQ4VWfCg4PGKzFRhcIuAEB7elXGRx90DnhaoCzfL/AMS652fI7RnBPatG3uYZbeJsk5UDcTjtWQWb7LKX5CqQSOR0rMtdVVY0RSMDg57GnYDq3kC9WymKjL7RxgnsDWL/AGn5rFFbIA5OOKtrfBY8gAkAnaaBJFw/IvPy+2M81SvX2AjcpI6VB9rmkDIMD1xzzTLiJnwWbHpx0pDKiRpeXqRkkRL+8c98DoKux7ZmcKBjOTn+VMtohapIcbnfgsR29KRrgRK2BwOoGKOa3QTVyXKq4HQdyO1OP3HGQSVHPTnNUVkdjgDjPf0q1CcDOenbtSYbEqPuyAPY+tTMAUB9sbqgR/4gCpzx71JtY44ypGSOg+lJDH8Ko6AKcDmnFjLIpw3T6c+tN8kMqggnAyT604bewAz7UAKQAcHk4zgU9RwOoOMdKbyoOMAYx+NIZM9sH19aAJlbaCCcDNRyHIPfPFIJBtHqevtTsBwMHAoAz8bLwHI+YYxiplKEmNiu2mTJi4hOR15z3qKddjE54J5HpVJ2AtQHzI/s5OCoIBqtIm04OMgc9hTRMPNWRc7gQD71PcNvIIGUI68UgOR8T6IJwZ4lIYdRxVTwz4ga1cW8vBHAzXW3KFkKnoR6c1wWvad9muvMQ4xyDRuB6U+y+gEgGWGOlYvidz/ZwJHzbwR1rK8Ma7IQI2J6AZ9K1PFMubADkDjJ9OKLAckxLEDP5c1raTZ7mXPGBms62jDvnr7V0OmQltv8JAxTAh12XF3Zg5IVg3TFbPhu/jnvphFuMkgBIA6e9YHiBGuNRtoQMEnucYFXtHu28OXJgMIKStzcDufT6UCsdLfTi0122QY8uWAxn04Oa4X+zYfauk8T32z7PcLgbDn9K87/ALYb+5WsYpoz5nHRHJfCbQf+Ef8ADek2YA3FQTnjFeweLoPO8MsFGcLxXC6coi1CzjGAqgAYr0rUwtxpLREAgxkBR0o5VTUYroVOrLEVZ1JdWcT8PbryxOAcFojj06//AFq7fR5RHBPEwyzfMGHavNvBEgttZntiQAzMgXrjrXaC+Mc7AcFCFK+x4onuEVaNjobG287SJIuh+8vsaz2cEEc57j0ra0sFLNcHr0PpWFqsJtL8PkMkvBznFZSWpSKbMdxC8sOmT2rQtJCZBkZA5wPrWZGxa5LMf3eeOORxV20YRwvJnIBzQkM2J0aaKK2RclvmYjtWhtXTLURoP37DGfQVPYz25iEy4zt/Kuc8R+II7GJ5c5YjrS6i8zM8WeII9JtHiRszOcE9wa4fQLGTWdSLvlkz8xNZ9/dS65qRY5O88Adq9L8LaJHp1qh2nJ+97027IZtWduttanAAbGBj0rK1H5LKUc5ldYx9BXQtDkYAxgY/CsC9Qs1pEMYBLH6k4qUDZs6PH5dpCBwME1aZwZCMnHt2plnmNMFBtVcCmRMUR96fKD+dTsBDeOzZXhOhyPrUUSvJnoOcjtTZRuxjKjcffg1LGpQHA3Dpn3qlYB3X5CeMZ60hffjgEj9KSSUbRsGSvDAimON77lAAHPHXNJrQBwCodxxkc/QVCiEAvyBnAFOfjczyZ3cALjgiguNwBTIwMYX3pgRcsSCOeuakVsMTgIO+3vUbFQN5JDgZI7U4cE5IYNyQO1ACtJhsYGGJJPelLKGPO3IwfY1CZBycBeeh4xg0x5wCcqNpORt5OaLAXbeIPIpPOOGxWstvEFDcZHIHtXP2UzNNkYBPzEE9/StOOUohBPyBuMcke1MCfVLYf2bP5OFYjaB2Fec6jZXOlsZcEp3Ufzru767kW12tlASDyOcVmm9sbyB0u5dpI2gnrVq6A5eDV3eJSpzkD8KvW9/cXAMZJAPIx6VQudAmgmeS2G6DPfgEUumXSQ8uMZOOvSm9QOjtLooFdlyc44NX1vg6gOACDxz0Fc5/aMUgKhuCOo4qCK4bzsb9nPB65qQOokm3HgkMBUMds0rFsEKD6jBqnBejdkkOcd61IJgysFGCDkDt9KV7IVhI4dgAznNSRREKAQMY604BTgZ5A4pqsEQY4weR7UnqCJVK+XlRnAxTusKhRweBjtzn/D8qrp8mQpwCefYcVZjlzlQVB6qRwKBjodxjBJBzgADjBpWxtbH4D3x0pqnaT2GfyNI21RuPJHPHSs3oy1qhVOVHoB3pd2SBgUyGQDPI5wMU5SMHB+Y9qsgcyhj82Mn0piMNw28Y/lQWIXI6Y4FMJ2Jjnnr04oAW6XlGxwpzj2rLvpAZCmOTg9ela5K4XjIxzWJqJRZ5N3DjkH+lNASw7beQockEYB9qtIwaMxEHA9Kz5SWjRkOTgYqW3m+XOcHPPy+1MBt7PtXGcdj7VhatALm3MmMkVp3sO1y+Rzz+FUnIljKHjjGRSA5zT5DDcrt4wa6XVpTNpy/hnNZNrYiW8fH3RVzUG2WQQ9VGMVVgIrVVDnOPlxwK6Gwji3ZOQwGQD2rCtAMgEY9eOtbtvFthByoOOSfTFSwMi7jF7re4klI05B/z9Kv2flm3licMyjlR1xVeRRYkM4Je5fdk9l7Cq9pdvLLMq4cAjJ6Y9qYuoeL7nGisQ3zYAA9Kwf7Bi9a0fFsi/ZrWI8b5EDevWof7Vg9qq9gsjndPmzqltxk5FemSP/owyMlhjjtxXlmnFVuoHJyQQDjtXoVxcbEHJ2AdPwrWtuYUUrHn9250bxor/KFmIPHAFddqtysd8ZMkJIoGe31rjPHQLXEE6nBU4z+HFdBbXC6voKbxh4QF3L2qXqkzZHpFheCC1OeflBCrVDVEfUbZwhIcfOuOx9KpaJfi40mJ92TtUHGOP84ps+ufYyPl3EnoOPwqLFFe2nWa2DA8n8AK0VTZDtxjnOKz5Y2gnDrkQTjzVUnoe4q2ZMugDfwgke9VFCZofafs1keQMcYFef8AirUWmO3IIzgg11Gr3Qgtjk8qufxriIraTVL9VA3AnJHWmHQ2fA+grI32qVMgcgV3wkO4AABR0x9KpWUK2NpHEoAIXBxViNt7EHPIzxWchmukhyQAD8vrWLMobUgv0UD04rTt3JkC4GCMc/59qowRibUZHIxjke1QBrnEduADjccfSqt7OsaGNcfL6L1NWJpBH0GSBmsa7uRLIBwCSDnv9KLASIXeRQTwfSrrPwqgABTg9siqtvkKMjLHt2qVgdnJAGMCgBFlCMUJBBGR6iowpGRu4B6Y7UudwCkAkHGcU1lBK4JAYcU7CEZRIoySdh4APb1pzzbskgcH1xgUm7e/yjC9CaicKzvzlPvZOOlIYuChX5t69CMVEYu+7jOBj+VCoW3BnCk/MCO3tSFhGQpGARxjscdaAFwNx8wggAjb2NQvbvGPLDABDwfepV3GMLgb8cZqVYMqGGc4+63ancCpHdxpIsaB55VOdsacbvc9K1/JnvNzSkwxkY8uNvmI9z3/AAxVXzMSI3ygDjAHT/OK1UuFWMZ+760wKg0+CVVjdZggPRpWIP4HNZUej6fPqoaMvBbwgM7bs7mz8o/TJrc1JRcW0ZicIzHaST29vyqNbGTTrZXtB5sW0rJGpAYjnkfnQ2BiT6RBfwSyRMLW5iyAsEm5JCP4SnY9PpxVF9BjibLlgHAYf/XrS0Kzhs7nUv7NguDPdXDSTTXWP3RIG7A79B+daMsOQY3HygYB70tQOdbRUCnaTjOchai+xRoOpxn05raZdkeOSfb0rOm+b1Cng5oYEETtEQuflznOecVbtZwpXJIbgfd/z7VV8ouBt+YnjFSRxbtpOSAe3akBrQ3O4rt55yc9qmWTIJyCOhrORWiOXOP0q7ANz9RtPG2noBY3DhQABggn/P4VNCnyYJO5SMHPpjioEILLkYA6+lSRswQKcbwc7vb/ADilewEu8FCrIvY529eKiZC4ABIx+VGQAQTz1BpgdxwpyCeh7UAOSRQuNvPXIpc7mGeg7DpUQJDEnABOBjtUmdq9eT1NADiTtwPvetM2ncH/AP1UO5zxgZ7/AMqTzMIPQ9sdKALJbKjHJPcVh6imLx88jAHP0rTWX90V67jyTxWVqTEXoUZwAoB9TTTARXWSJQASFXsQMUyCRQ7hiTkYB6AUsJEeRtG4cYqGdijBgOM8egoYD7ufcBuHUdazUmDuUAOPWrkv76F1PGBuFY9tJ/pSYyOen+fpTA29HsRunk5Py/rVPXcR25x1BxzitLTL2O3hlzwcgEHvWFrk4khJPPPQVSAksVZlLZwAMD2roLRBMoeVSYEwSV6E+n0rG0aB9Uljt4jhBy8g6AY/nXaS+VBamCFAEReB29qQHE+LL/zLlJE2ggEKpUAd6XRrb7LYIX/1spLE1meNLlIpI2Y43yIgGO5bH+Na/mDzoYVHKjkHpjFEtAMPxSjy3tkhIH7wH/gIBrM+w+9auvyb9ftAMYVWIGOOnX9RWb5/tSAwNJmP20ockZBxXpDEPFsBBG3Gce1eX6RJ/wATOLnjIJH412eu6+uk7dxIGcdMV0VTKmrIxfGEBezkJABXJ+gFVfCuoGO3jUjKycY7YNTarrMGsWOEOWIIIrnvC04e1liLYkibA/P/AOtWa1iano/h65MMc8GRwxAYdhzW7pNhC9yJZA0zDkA4xmuG0W88y4mGCCT/AE/+tXomhzFLUMoAHAHrQlcCfxDZiPRDKAA8D8AHoD2rGs5fMk3E9VGK6gOL21u4bjhJVIzngcdf5VxGmz5R2PBUYAH9Pyq4kPUh165Mzug6Zzx/KrXhrT/s7GYjkjI47VDDZtc3IYjg9a6FYTa2xG3lgADWbfQskaXByTgnFPikO/qT344qj5hyeeexNWInKkepP+RUAblo2JHbPKqWAPSpdNttiCUgHPJ+lV9MXzUnBPGAuf8AP0q/PKlrbDkYUYxxUgUNWu1iUjPOcZFZFtmZ+uTng+nNVb+9NzckcYHPFaVlF9nQFed3UUdALIJ5GMMD+FO8wcKx5zxgdKiDFssTkE4Hbj0pVYNtPU/lQA9WCt6qTjjg0Z54XpwPamBgpK5yeoPYUu8SZwd/HHYA0bASOu35cbhnqtQkqwxgcDHTGKe8gjJVXIcjjbSSY3E8YJH5UAMbHBb7w4GOBTX+ZeCcgZyR1FOO3cRyUJ/OkGXII6AEbaABcSEt/nNSyPsGwYbjkinjEY245654wKpTcrljgnjaOtCQEUkrSNgk5xk1eWQzQDHOBjbWZLGTg45Bx8xxWnZKdgOPlxntxVAR/YpG8sncQHHQ9uauPFJBGPIkIc8c9BTo5izLEMAE9RzV9IFRs9mPOaBMx9I82NnOd/y7mLKQQTj/AAqxLG7DjaQe/etHgpI20A7sYHeqpVRkMOR0xxTvcCnJGNp7DsBWXJGBIST3+7XQGNNhyueMnPasuRUZwowDuxk8UgKccA81ucHjGeDVhLdm6YBHUjvTSm13BG5OxHWrMLC3YMR3+761IyPyQuVYk8YHfFTW7BMgKORj6U6dt7navDc4HYUyLAYZOeKAHxpvHU7+69jUnm7YlB2k549qg2gSBwGzgKNvQetSlwT0yRgbcdKAHY3sckAevt6U0Dy2O05FJnbkKeO446U5TmQhhlQAAOlAEZILbQM/X1p2cEcYUEDFRv1O0ADqPXFKxBxx36ZpIBd6g4CtxkH6etR78secj37Ch2BbA6YxUPmYX5SeemaYEscg5yMkdqz9SYfbkBO0hV4HIFWBIAwUeuD7Vn6lxqCHABKrTQmPVizy5OMHj1xUc0m6Mhjg/wAqRmG6RTjr/h/hUMzFQTnK+1MSEhuP7xwB37/Ss2W3EOo+qhsjaevSpDcbZsYBBHQ9Kl2iVUdRt2mmM0DZ/wCitJyQTuPauf1iQxwqB3PP0rXbUJGj8vPGOAK57xAzLENvcj8qqIHoPh5baxtUhtz2BYkck/5J/KrN/cZBbOAB27iuf0Oby1QliG2gH8qdrd+VWQIQABz6UuozhPEupjWfHmhaUpyElN1IoHZASB+oruvJ33yMoCHABz2rzj4awHW/H2uaySWjtlWyjzjAOdzfzH5V6h5SxySyHheMlfWlLca0Rx98xuPFDgZxHAxH4n/61Q719Kr6bcHUvE+uvnKRBIl7dAaj2n1pbCOW0aZv7SiYDGD0xXfeINJg1C2Tf1xjiuA0zC3UT9DmvTL0BrWNuo/+tW9UypnCnTRpsjRgYQ8ggVz2nTCw16aEjEc4yvqD/kV3Oqjco4HHA/GuE8Qr9ivILoAfJIAD6A1kjU67TSsGoRHkLKCvtnNd9p0o8sDJKgYx0rzae8ENrZ3AKkLIpOOgzXcWt1iIHoMZ/CqiJnQ32oC20i5fnIi4zXMaMTcW52gDJFTeJbwx6NKo5LAY9MZ/+tUPhxwLbPU7gf06Vb0joTfU6Ows1T5iOozVjUZA8USKRkE0tqd/Q55wB6VXuhmQ9OOM+lYFkIQMeeMVYhI3L24qv5gTIxinJIFI54PY9qCbm/psojt5JTj7+APw/wD11i6xqpbKg9egq9ZsBpyEcDcz/wCH8q564H2i4UdEBxQUWdJt/MYOyg881trJgAYAAHaqdkixQoinBIyc9qsbcg5OFzn/AOtSYD8/MG/gBA56YpA+CABt5GSOcCony8e05JYZGOAMGpF5JGdxPehICYHCHcBtwAR60kToq/cKZ6DsKrlMKfm/HNWIPm+ZiCF6kg8ikA7dtUoozkhc8Zx/k/pQAHYJjnacHHAA7UwL5hyCcYwAeBwaeJH+VyDgHjbQBFEwf5RyAcH6U4HaNqjAXuaf5apKQowCCQKZKdihWOMngen1oAc775MDacLnnoDVeRjKw3AEbsAdMU7CphjycAEtxmo5VAkO37nULnpVAOjdYiGIJz2xmrtqsTxYkDEDjHSssuc4B5z1rUtrjMIGABjr60AaaIoUMgAAIAAHb0/SrWQowOMnP+fyqpFOqIo6gMoH61MZFcEjpjgGglgcRrjvyazxJhyd2PpzVuRiwOcDj9Kzm4ZtpAoGkSsSiE5zzisqZ9zFjtJHGBxV15yEYf5zWYQNzHGaBkiMUA5ODzjtip4ZvmGBgDpnn/PSqocE4IOCOPanxEM5XODnGaVwLYZmb5WC7jg0pTfk5Ix1Hv61CrMzOABhccHvUv2geZgdAMjNICWB2Vgy4KDjaajZgZB1GD2/z9KfAA8gJGATkDNMZxkqRgkj8KAHD5ZCFB9DkdTSNg4BGCBwc0qPgjGSCAOaa20EY7cc9PyoATd1Oehx6mm5xnIJGM49KM4zk5J4G0YphGQCOBjP6/8A1qAGGTIIAxt4qF2xjJx6AU92GzrwTkY7Cq8rYfOQR2oAlDbGGcL656n61n6mTLeoE/u96kkkLuFzzjg+lUr6Y294vIyF4qgLE0ZV3Bz0BG0daglyICdpHbjpUsd154ByATxUc7ko3HDDAql3JuZ0+CvHUHrT7eTDEZzkYANMJXBzVIXPlSqxIAz0qQNt4xsB24PYjrXM+I5sIi5zg9q6U8ruxgdq4rxbdjOQMkZwOneqTsB2+iT7gmANjbRz7Csbx3rMel6ZdzNwiqT6Vb8OZGnx9iB3rzT4xambqCDSo2/f386W6+vzMM/pmhblHafBeyktPAdvcyIVuL93u5QwwcueB+QWuq1u/Fhpc0jEKuMnPFP0uH7BZQwoFCwoEHbgD/61cP8AFjXfsmjSwKQWfj0GPX9Kjdj20KvwxU3Oj6nqLEl7i6kZST2GF/oa0ftB9Ki+HFmLXwHaLjBEIY45yWJJ/nVf7QfanqFjmbNwJIycnkdPrXqMcpm0iA4HSvLLdTGxGMYPOK9K0eVpfDsQIyVGMjtXRU1iYwVmZk3zl1wCSOBXG+JbP7XbTpgg7cj2NdlcAiXJyARWJrMeYNwyxA6AdqwW5qc1oN7/AGz4buLUMfORSoB7Hsf5V2fhXWRf6NbMX+cphvUGvMYJ/wCwfEO9TtgmbkDgA1s+Gb5bDWb+xJwhYXEP+63b88/nWqWoHoWvXn/EuKk/d2gAfWrmgSA2oVcK3DHPeuK8Qa0kFr87kbWAz68ivUfCGgrd2kFwrK6MoI/z+FOW1ibGlaBo7fzDxuGOKilBLA9PWt27tFhjwMADHFYtyVEZYcbazSuFzPnk8snP05qL7YoIyQDWbqupJCjsWKHjB61z9lrj32qW0GQS7hQ3+fam4hY9StT/AMSyFRwRGTj3ycVkxx+XNg9ev5VqKQseBwAoArLXlixJznA9hWZReRnAy3LcjIHaphKXiPGRkYA47/8A1qqRy8E9scUscpwFBwaVgLAfaQQu0eme1Sqx4OenoKhi5BJOSOme1TRfM2c4PtTAlLZU8DnpxTvM3rheADg4FRZyCAD8oz+FSD5lKgEZPJHfp/hUgA+RgqgYPTvinvjCrnAII698UwducEZ7dqRlz7legPf6UAO+0LGEIzvA5z24qPKLHuxjAz9KPXcO2Bxg0i4cne2MnBBHX0qgAR7lBPI6nPYUzG0kAfMDxntxUzyBRjORwKryuoUlsHgc+9AFZ5drNzwOMelaloiGBCSTz07YrFiUTu4Y5POMe1dJp1udqAIQcYyw4oQDorczSqOmTnI7davFMIOMEfKfepwsdvFubBIPaoJ5BtJzgEfrQQRSAFTj6Y96z3fBbj5ulXXZgDxkjg1ny/u13dSPSgq4XDAQ54Bxn6VnBgxzwPpU80+6AjoSMH2rP3McgDI6fhQMnZ8jjpjihGKEEDj0qvkqxz6cAVJExznilYC8j7hxnqSAKI+Hzjk96ii4HoCO3anhcuATwDxjj8KQFmGQMCOBjOKR3Bk3darIcAOOD0x2qVeD0wD2NADw+ewyQDilkclgwGMcZ9vWmKOrAEnpxQSo6HgdaABpOSM8YxxxmmO43YyQB0x3H+c0HC56knoeOKiYEMO2KAGM+B6eoHaq5kBBzxg9qkkYZOCCR2xVCdzuPBHNNAOnkWGPzGOAD1/pWRrF2s8qbfkJHFS3V6FmCSKCmRlSeKqavaKsqSRneCvGO3NMkotq50woXPGM81tadqi3sQHB+XPHbNclrSiaNuSMDsKy9D1p7C5AYkL0Oa2XYLHoF0gjGex6+1YGpTAE4ORjPGMitsTfa7HzEwQw6Vw+p33lEqwIwSCKlK4I9B0fVbe40qNncF8YIP0rzbxfqsM+sRQQsDulRSB9Rx+lc74w16ew8OLc2chQRy7WCnse/wCgrM8Exy6v4jsHldmwzStnnOFx/NhQ1YaPd2nWx0xewCZH1ryi3sf+Et+MumRscwaVG963+8RtT+Z/Ku/8QXwi09mJwoGB6VxHwG36pe+JfEMoyLy7+zwHp+7jGP8A0ImpeiGeySz+XbOc/SvFPiFdtrWqpaIPlyI/zNepeIdS+zWRB+XjPFeSaNGdT8QCRhkCQuetKOmoz1zT4fsughFwAqABcYwMdKwPscddYYP+JWkQ/iIHI7Yq5/Y8f92oHbueSTx+TOw444zXaeCbjztInh6vGxGPauU1SJUmPCjFaXgK/FvrEts2cSjI+orqlsZLc6C9g4HGD1yf5Vj6ja7oH28EHGDxXU3UHcgYUY5rHvIDg8gg+tc5Z494stWeMkLiSM5z6Vkf2lIk2nXwJzE32ebHUq2MH/vrH513/iWxD722YBUqfWvK9Whe2+12RYqko+Rh2PUfqB+VbRA6zxXctc6XOsJ+cIQuR0b1/QV6R8CPHR1fw1aoZTvjXDDPQeleN22rHVNEinztZgA4HZ1yD/KsL4T+OP8AhAfiLc6HcP5VjeSedbsT03DkfnVPUlq59u311v6H7wGRXL67qvlQEY24OOO9Wft260WQEY2jB/CuB8Uaowjdck9/1qbpbAkYuvaw8km0uMHvSeCGN14mth1ALN+Q4rEkb7UMsO3HH511Hw1sg2v7wSCkZ4479f5UrlHr0rqkTY52rWY0hkkByMYycVambapHqME1VCj7oDcenpWQEwYbM9AKFkGcdO//ANaojwqAjnofSmeZs27SWwc89qANK3JZwMjB9asJuU8Yz14rPt5N3PI49OlWon4HZc4oAsI7RYz83J6cVKD5aMd2QONoqBXDZIOcjOPb0qSOTcSCMEgYFSwJUwGORz61G7MHAwduNu7v+FI7BiF3YyOfrUYkRkJII3Z4B4HagBxZiSjAEKeDTGmVQO/bHelLqyjavtmo2B3Yxz0Bp7gSSknYQRkjgVXWMtv5G0cgHtQq7c/MQAce3SoHud4McZwmACfTBpAWoZEgGY8E9M4ziti3vwqfM65A4571iWaKMDgsRj5fWtCRB5Cnoy9eapAXPnknQ53Rk84zgVbcbUK4ORz07VQ06VYxtkGR2HQA1bZlkycDGcUECMxA3kcnnGelVSA2VYYXscc1b4YE4IXHpVYqGUkgk9smgDK1SPy4wVwpP8PNZ6KzAMOD0IzWvqjAwgffPGDxmswp5bA4OAelDLD7444OMZpRhnGMYzSKQ2eMk8ADtTlKgjjaR6mkgJUZgp5yO3HanLKxOeD8uKiZ8j39qDJtYIFwT37UnoBbiIVFHdgOO1DlmXbnYRyMc1Ctwx4IwB7U03O0DOcDHPGcntQBOmQ2PvHr1xU0v+pJAySfyqosw4wWII4Ixx0p7syKMPkHgn1oAN5ck8DJ4HSmMRtYMQQevHvTHkBzg5z09qY75GOAQM0AMllCplRwe/fFVJZ+ufr+FOll+YgHCnpVK4kbntjge4qgILmD7UD0UeuOayr+4NnOsLuxJXgDtV+5uTEABz61zWuTO05m25IwM98VcVcgoatfPC7YyRjO3pxWFcSRtD5hfZ6DpzWvcy/a4yQmXxnB5rktTkZHWMjaVPIFavQaPR/AerGWNYJTuXkDNUfiJpT2p86EYQ9B6VzegXUtnJBISQB0r0XUJE1vQ3BIztyDSW9xN2PGp5Tf6Ze2bjf5seACMfMOR/Ktz4Nae0t1f3pQCO3RLdS3Td94/wAxXP6j/wAS7VVGOA4yB3616B8O7YeHfCKxOR50ryTuevUn+mP09KU3oNGL8Z/FX9ieFrwq5E3l4QLwCzcAV3Xwp0CPwv4B0ey6SRwB5d3dmGT/AD/SvEPFs/8AwnnxT0Hw+vz2yS/a7lR0Cp0BHvivoe/vE07TduBnGOOOKxZaOX8f6r5cDoDkngCuf8AW7S3m8qu1vlBHHT/9f6VneKL/AO3X23OVB7Hiuk8A23lGIYIydxyOBT6Dienqhka1iXJLknHsK6b+zT7VlaNAJL4ORlEVVBx04/8A1Vs/2mlJIW54hq8f78naDWPa3Z07V7WdeNrAA98V0mtQKspxzya5TXI2FvlBlk+YGuroZbM9hLC7hEgI+dQfbNZV5DmIrjg/pUPgfVRquixIfvxrg961bmHCFcZrlloarU4PVVDK8THOOh9a8p8baf5IMqAFwM4H8q9Z8QDyWbjGPQVw2sWsd4hBGBjGapD2PKPDOqg6nqOnOQoYC6jHp/fH54/OuT+LenSyraahbnZcwHCMvB4OcVt+M7D/AIRHWLTXEyYIpAk/HVGJDf0rR8U2Meo6LMY2DjAdGB6jHWto7EHtnwR+KT+Nfhfp092MX8YaGUnoxXvVjVZ2upCCeDmvMPgUn2TwlbbMqjXMpKjp1HFenRp5zkgcE4571nLQDOjjdEOeBjqK7H4ajF/cyDjbtG73Kk/1rkNRufKbyymFHTFdl8L/AJreWQkDfISRj0Cj+tNLQZ6C7+arLznPFQgCOPeR8xOMU4PtYntmkaYSHA4Dc/SsgIZJMrzyB2FV1lBx6+o4p87Bc+mO1U/N+YnseBmgTNO2YkjnHt7VfjPyDJ+g9KzISNhweeOlXkf5V+nP1oGWgw4PTscVIzhPlz0weRxiq0i456D096ge4LcHkHiiwE0t3hi69QeQKXcRJuJ45X8ulUVkAYqTjjGRSxzjdtz8o4ye9K1gL32hQeD905yvQinYMjIwbKt1we9UjIiFR15xzwBQ10BEQCB3XbwAKEwJLu4wu0E5bqAOhrPW4WINz9484p0jmRg2eCTgjrUXkb+3FOwGnb3ccjKI8Ak/lWlJOwAOAwA5rFtIxbhWKAZxmtQgKhTB3np7DNAEMGp77vYR8uTgDtWvbXGRjr6e1UbbTvNfIUL1yR9KuW9v5bADoOKoC8EAjOQDwSBiq7MUQggEelWXYYI4C4wOKoSMBn0pMCpqDbSvIHoo7VRLchSCBjIzU944MoJxj+dVpRuxgnbjP/1qmwDmUqTuII68cY9qYD1bg55+ntShlZOuD3zTBMN3AAH6UJASFuOnze1NEu37xYk9PpULTHaWYgDsB2oMgKqQvOOfrTAmWQou7rgc89aUuGUYA6VCCD8vQcfyqPzvmAA5PP8An8qQGxYRRTZDTBBnCgfz/lVi402eBdrSxiMYxs5ZePTrWRpiLczeVKWQBSCY8Zxkf4V0Y0u2nZkYM6hQFLHPGc9fx/SiwGabCUH93+8A6kHrWfcRvHklSpXgkjFdFc6ej52k8DGASMVSNrNAX2ysQT0Y5FO1ybnNSM4yMZHTIHSqMzFFznA4HrXUum9T5sMbEnltuCaoXVnatzJA0fsjcVSTY72OXm3FQScn1rF1UrvCNxlc5JrrHsNNZgDPNGxOMFQwFZetaHaSOjJfopxj5wVFaxViLnDf2mNMv0MhzG3BGO1VvE1tFcXCSwBSjAHI7V0Wu+DXvYkMDLKUXI8sgkmsLSdMnW5ME+dgOCCOa0YILWyPkKTzgdq6HR7vyozC5KlgB+lTyaCY4wFGQBxgHFZ72r2c3I6HvUrUGeefEK2+w6k0g+7njHauq1DWk03wwkjOEYQqSx4G0AZrD+JpBEXTkfl71578YfFMh0S00yzO+e8dLOIL6MAG/wAPxqJaFrU6n9nexk8Q6trviyaPLXUpgt2bqI1x/gK9h8V3xt4tjY6cA1k/D7QoPBvhHTtOiQAQQgMR0LHk/wA/0rJ8S3zXMzliT6D2rJlWMEubu7BxneQD2AH+RXqfg+2+ziMDkgY9a800i2E2oKOwOeK9b8H2fmyRIOVAGT3pjXc77Toxa6Y8khw7c/Q1gf2vWv4hm+y2QTofLya86+3U4rQm9hNaTbNIGHA5xiuX1OMMrL2IxxXZ+IQyzBux6VyGoKS3IwMc471tF3REiD4f62dJ1iS1k4RzleeM5r151EnzqcjtjvXgmpQvbSJcxcOhyMevrXrHgfxFHrOmIGciVRg59aymjSNzO8U2vmFxjknivO72JondWBAHT0Feua9ZF0LZxivNNatXediAxIJwB0rOJTOB8XaHHrekXVm6ZWSMjdjnpXmvgXUpbjQ5NKvQwvdNZraTI6rn5f0yPwr2yQqAA/Bz0PevHvHdqvhDxpbaza5FlfHyLsds5+U/y/L3raLIZ6B8OIH0vw5p8LcZkkf0z83/ANau7gZ5JCO2cgDtXEybdMOlwiQYWJRx6kZ/rXYW5ddr5yCBjHalKwkV9WDfaCuAMDNd98PYWt9PtA3V0ZifYnj+lcBqJ8xshQDj3r03w6vkpbIBtCRAD8qa2Ezp43O09+2ahbhRgDOTTrbDxscYIHSq1wzbj2WsSglYPk8AA44rPz5bEdRngCrrLheR1GaoyL5ZPGeauK1JbNGzlwPQHGPatRMKBjt+VYNpMqsAc9uK2hIBFzwCOAOlJoSYXFzsAHHrVKS6yTg49KivLkFuuDjpWd9oO7gcg9KLFlxrkknnJzTftZxnPIOMVU3ckkjmmnk4znmk0BpC6HUcDqKf5u5V4BbHKk8VmhWVSR0HapkDHHr60gNEfMOnTg46CrKEbVXbj6VmRsYVXjORmrMFxj5h+GaAL8SYnBxyOw5rZtYgQGl5J4zjpWTZXMcgCkYYAAkdc1qsd4AQHB6YoA04IiSmwYXpildQhIIAOcn2qnptzPvbcflVCeaP7Uiu7lrbLCcLuxjAxViJWYbcZ4qpIducDA9uafJMCoIIwy4qs0ig88gDtxzUBYpXzjzV5B654quJAN3pj8BTryfLgKBnuTVWWTOV7dx2obGODkB1456ZppOVx02nn0xUFzMI1BBwRzVZbvzcJnGevrSuBbEmchlwDnmmiVlAXqxGSRUeHwWBHoc0ozw/BwMcfWi4D2kCDBJ9D61GZ/4iQWycduKhnfYxIOBjr3qg11vYEnjHbiktQOj0SQfbDkqVK85ODXUxyhrqXaFBAXBz/TtXD6VKYrgFnKfIxA2gn1rqknY3EoJHAAJAwa0SA1zJkFvug9MVDMN4HpVWK8DYU+2M1Krh/lGMD3p2a1II5QBgd6yb9SR1JHvWvNz82CD6YrJvgWBbJx7dq1hsJmBcQBnJwo7/AEriPGyyXASONiNozXc3SE9sE1x+vbHvWDcNjmrEtDgbTUrqycBZXRweNpI4rr9C8X3gP79luiP+eigkj0rmNQswt4wB2jGeetaGkQiEqCAwPUmpNT1Cz1u1vYAbi08sd2iaoJ9NsdWdxFOYWX/nstYmnvhDzgY4U1oSXSpATnB9qa0IaPOPHvg3U76G6nsjFdiONinlSDIA9jXjXgO2Pjr4wxsyGTTvD0IbG3IMzf4f0r134p+Iz4a8NarqMKrugtpJFDd+Bx+ePyrhv2bdGbSfCA1GcZvNTma5kZlxwRwP0/U1jPcuB7ZqV4IbfAxjrnoT7VxGpXJck9MdCeK3tYuw+Nwx7D0rkJJGurnnGCelZruU9Df8NxFXEpTJIr3DwLZm0sUuGGGc5AI6Adq8s8I2f2u7tbZV5JHTsBXtpT7Hp21V2Ajav0oDY57xdqJljdTwWGR7dK4DePSum8UXOZdoOVIxnv8A56VzP7ut4bGTZ1niK2O3cOAOK427TeDxjHTOK77WlzEQyZAPNcZeRBQWXkds1MCmc3eWqyp8wIPIqt4Zv5NE1TILGN2wyngVryQ7mzn1yB3rH1G2CYZAQVPFEho9bW5TVdO3D72O1cTrtviQgNt5zgfyqXwlrYhRYnOX781p+ILaKWHzoxlGFZlrscFqNnFKo3KoYHgjtXB+KvDMfiC0k0+QZSRgAxGfm7V6JeQPgkkBCcY7iskoJdQgUKDsO4np0FaQJfY5TxGipqewAFYwqjA6YH/1q6zSLnzYInVsjbgg9OlcVrc7Sag79snGO1dD4RuN1uY265yKqViUdBdxNNcxKBguVX9a9M0OPzXbngYHHavP9PUy6vbKWB2nf713ehEw3ROTtB5pL4RPc2PNewG5iApODgdKmguYpXIJBGeM9qLy6D6fIoRSTxk1kIvlgcDArJFGteXEQDHA4HArGurnk9ACfyqG8u9mMnlu3pWTd3ZIwTk54rWCIkbVhcK0ijI64JrRnvlijCc+g9hXCW2pNBc4UnYCDW99rF7iQgjjp2pyWgluXJJS5zkfWmrweOMVXVfmIOBxUqHnHYdBWWxZJtLMMYFWYoPmycZ7j0qFG3EZ6e3FXrUKOScnjk1IyaK3GB/tdQe1PeARpsA+YHtVtId4zgEE1JJbbdrYwMYIFAGaxGcYwoORSDbnC9ckgHoOn+FX5LcMhUkAHjPcVnyr9lO/k84NAE0MzZLpHj5hj1FbMGsR25VXyvqOmKyY5o5EXDYz1C+npQdIku281ZCFJ6HmgDsrHULWSFnIKgDaWbGDk1wc+var4nvLtbFF060QMsEqLmR1HVv5/nXS6XpG+28hmL4cZPYcdK4fxPBcWbfZbWYQXVuwUR7tr7c87T71Er9Bo6DwZrlxeSiw1KXzyF3RXO3BOMZU/mK39XTyDgAEHqQOlcz4escW8pVxMYgTJMnK7sDAH5/pW7DeCeAiU5OMCnHzEY0sp38HnP6UsuFiPqOpovoGRg4OPQDtVF5CevT+tUBnX90csPf8/am2MmQTnHOM96S8QuQPU1NDbrGV496ANRQpHy5+Y8g01+AFx26imLJwADgjqajkn4xzz7dKT0AgvZQse0AHH8qzY5My44xVi6kBzjg4qjg8k4yTx7U1oBp6a2NUBBJ/dNjBx3FdU0pWWZhuG7HXp0ri9MmhXU4pGZSqqVOF3Ecjmts+ILS31K7hvNXjcZVoIZE2446K3etY6AalvfmOcZwT6Vr2s3IYkgegHeuQEq3UqvbuuSTgZxxW5p11uUBwwORgnpTeoG1JINuScVRutjZycAdcUXNyAxGeFOBj0qjdXHBBxgjFUtCGUbt4ySQxznGK851+6EWrON4IHFddq90tnCzHjk9K8n1G9e91OVix2k1ZJflUXN7Id6kNggryenStCBCFCgAACsXw75l0srYOwH5Wxwf84rftFLykL09D0qUWjSM54GTwO1E8xEfJyPeqs0v2cAHr7CmyMZEwx5HQelMbPOfjTbtrHha8tAciURpg8cGRQf0NdB4XtI9O0aGKMbUijVVHTHFO8YWcVzo7AgM/mxbT6YbOP0/SoEuTb2SIDg7Rk+tYT3NI7DNVufNJJfnrn+lU9PQSTqO+ar3MzSMM+3AFb3hPSnubiJVXdNIwAOOgrO42rnqXwy0Zl3XrL6Iny8+5rudXuli+Un5EGOag0uJND06KGMllRAPx71z/AIlvnkhIBwXOMDt0/wAKozOU1XUTfXUzH5UzgAVS/Ktl9JBgVghQ4y2RVH7IP7ldS0M2rHd64u6J2HIb0rg75JMYAGD2r0W7RnUA8DGMdq4jUE8uVkYDGCcjtWELGjMMDGMDGOAahv7MG3LAHJAOO1Pd/wDSVGeM81ptF5tuB1wAaqQI4db6Szucg4PTGK7zQtYTUbXynbquOnSuH1/S5IyZFJGDzxVHQtdNpdrG5wc7eKxNLXR1mtWDxTuC4JB4HFc/Mv2WCeYg5VCowPWuxuJV1XTvNjwZkGSMcsvpXK69Kq6eyjBycHn0q47ktaHndym66J64/IitLQ7vyL2MjkfdPpiqF2j7yU6McYHpUtpC24BQAeua2smQj0rw8u/ViyqNscRO7/P0ruNAh82cgkgk7fauJ8HRslrLMTksoUjtXc6FkhyuBhh/L/8AVU7RJ+0XdR22aIiOZS5yVP8ADWfdzYhz0HHFTXCMZpJc5J4x6VUugWhJbGB6cVmWY93O2ODuPv2rPknOPmPFWLkfvAAcepqrMMj261ujNlaMFplPTD4OBjj/ACK6Sw27VyeTwK5yE4mycEE+veujsUZ40yBhFxiob0HYvqoABpGYAEYINP2YjHIPaoQjb1yMisrlXJ1bgd607UhWXjIzxWXGuxR2P0q1CNoB/AVIkdBanKDBGBwB6VZYhgcH5+4NZdrJhSCR14rQSTLIxGSQVOKChr/KTkKAeajntt4/hwBgVZLh22kZGMc06BEbAYkg8cCgDHjtJIpAoXAzgHFWpzcwx4TJQ/hW1DbCaYDPG3oa1YNMWQxhlUj9KSA5vwxqstrcXSXIwDtZe3r/APWrR8SyWd/pyyiKMzvtRXZRxyP0qXWNIP8AaKBB0jycADPt+lLPBHBYpE6KxcgfMOByM1d0BGBLbaGocKTL8xKrhRk//WFZEcRWUMxwqntjmtqeUrB5BPygHbjpj0rMIweg4pMCK9VVyDyTmudkLfaSO2K2b91yB0KjpWTcAbSckE9KQELhXK5H404jaQM5qopYHvj09KuxyCQYPGPUUANDMO4681FNK3Y1LlV3EdDVKTJ9Qc9RQBA7lmPHGO9V5flXIHvmp3BBPpVeZjkjPGcD24oAXSbWG4u7mOSN3EkDA4O0EZGK057KG3iEYiRxHwu5QdtUtEVBcSjAyYjnI6DitPUyUlPGR0/GrAxJbISlichv7wPSrOj6rc2M/ltMxwARnkUr535zxjpVaVWRgwABz1/GgDq11OSQ5cK46Yxio5r0MDmLAHPBqnZSBoBjqoHNMuJwuVXHPBBrSOpLPL/id8R7HStRFiY5tnlE7g3RvSvO4fF9veWxKJLg9MDk89K774u+FLDUoYHJVZ2IHHBIrkNO8MW8RhEK8RgMT7Vb0JWx2GieLtNXTkheNrSUhQAV4AyOK6nQRZairzwzxsQBiMcMa4zT9Ato5VcgkkcfWumj8O2xt/MWTymzgFeKEaF28DSXJzEyIg6sMAis+4vVHKdDxmo3+229s0JvGkQEAB+RjNZM1zKZMGMHnhV6UiWyTXoG/sJJ2OA90ie4wGP+FYVxeZYAHjGBzW94jjmPhFJPL2xx3Klyx5UkED+VcnARIRyME8DHQZrnm9TSGxp2FsJf3rgnngV6x8M9CA3ajKuAPljHv6159oljLd3MEEYB3sFGB0Fe76fZLp9lBCCNka4GO59alFNk93Ogi2gEk9/SspNOa9uwzICkYyPSr7GMElgCPTNOmvZXiESbUGOqjmtDM5zWbpYpDADkdPl6dKofYo6valFHb75AATnknrWN/aC1tHYzZ6HcS/uxkZA7VyuqWMc08iE8OMcdjXW3MYaIgDpxxXNa3GYiknqAPl9a5o7mxwOpWhsJjGxJHJBq7p96WhC7gQBipdUmW8BQqOBxntWVbjyoyB2OM1rInY0tZSGWAnkHb0ry3XI/s87MDgjkbeK7zU70mDrlTwK4TW7ZrglhuGBisjSJq+EvFnkSrGSxI6Z7e1afiRIDEZVbakhDbfQ/5FeSpqEmmXvXnOf/AK1d0s0uu6LbOgyWBBxWkNyZmHNeIkzIhyAetWrXDNlRkD0qzaeEpmm+ZQFPXNbkXhtLVSScgDIzxkVsZ3sdB4XDR6NGy8b2JP4HFdj4eJaCfB5U5Yn0xXPaXGLPTrYLjbsPGPWt7w8CVuXBxggEevFKWiIT1NCUjd9TzVO5G6EjG4entVyVQc+lVLtxFbsxOQBg4rFampzt4nznnnn8qqSZ2/L6dKs3LBpSQcD3qm8gOcE56cVtexFiBHQzFQewBOOldJp0uEfB4GOK5VP3dxhl+8eceldLpmGfjhT096h6jRrjJxx+FKeTj09KIzuOc4Ap5XABBH4VBQv93AANPQqRjkEdPeoh94Dt61H5gRxnoMAH3pMTNi0kD89zWjC2xR0I6AA1g2shAxkjsK14iGjUZLemRjBpAi4XyAcc57U5ZQqbjwDwR/WoEJxyME8DFV7icAEdeopDN2wugkgU8hQRz15rdtNRUsEXjjkHpXEWUxLd8tit61JQbs+3NKwHQXK+bcFxjhQBg5xVC8w+ASAQenXHFN/tB9vPK4xnGO1QPIWLdCegzVxAHw2AcdMAelUbnbhyvTH5VauE3KTkA8VRaPAIzn1ptWAyr05YHaMnofSs24fOBjArQu32yEE8LwMVnyrvBPSoArIB6GnICoGQMnsaXGBn0PSoX6k9T2oAV5GbjoKid8LxUrkbR69qrScZGKAI5ACfbHIJqjMSWII2jtzVhjyTjmoHHzZ6/WgCxoYC6k7lmA8ojaB05Fa14C8h7gc1kaOw+3FcBT5ZBOeOv/161LyXYcZySMcVYGbMrxSnAHToTTZJM4zyCKmmkxJ2GQM+9QycgcAHGcUAXNLkBOwn5e3brUeqZ2uUHzDpiobWTy5V6ba1XUXUedvBHXpVRdmJo8s8faXNq2nCdJWWS3XaVHU5715poviW9sLgwTqfk4JYdq9u1u28uSaI/dkUj9K8tv8ASFuHd8gtg845BrVko3U1yVYV8lB844J5xWnB4glWJFlO3jAIFcpo6yWimKbDjGAR2rYe3LoGBwvoazb7Fms+qJKPmkOBSC6h8zh+cCsZl3gjOPwp6Ao69wTgH0FUKx1F8Fu/AWvxsRlFSVVHP3XH+JridCshJgsOcZ+bv6V0k919n8M6hBnJeIocdwR/9f8ASsXw7Z/aGtoFGSxA6dM1lPc0hsel/D3Sg2++kHEfyxZ459a7t9SgiTDvznAHHSuchkTSdOS3BARFG0j1ridc1uYzsY3OQe1QOx67FEt6cRkE+1TyxiGP96CpFePeGPH0llqCJcsQGOAQeBXrTakmp2Cybgw24z2oIOZ164aVygyRn0xXO+U3tWvrEht3cpg46571g/bT6V0R2Mmev+aGjOD2rB1giW32oCScge1b0UKwsd5AUDA96y9VRYWZtqsAc88VzrRmvQ8x1o3NjOQ68HoQOMVSs7wmQ7hzjAGODXeatPaXtuodFO3161w9xOlre/IAiHnOMge1aPuI0YdPjvIA7gJ6gisDW9LiRSUGAK2odQ3fLng9RxzWLrpdoXy2Bg8VBVjyPxLEoumwAoH+Ndr8ObgJocBOCgkdRnPGCa4rxUmyVsc9evpXY/DVQfB0T4z++kx+dXDcmWx6Q1xbG2PyDd1rOuZ0mJQAHHGBWQs7AnJ4xxVvT0aWZOOrDpW5kdIoCRIqjgLjHpWv4dbbHdDOM7T+lYsjjcSCQAa2vD4V4ZXB5JA/T/61TLYUfiL+SI/XHaql+P3DAcHParqkbAAvGMZqDUFPk7uBisFozY5WVDuGQDVe5j8sbk4B47Val2iY4yT2xVa/YQbFJGWJHHQVsQZkX+tVm5we9dLYzhfKOMY424rmxhSTknJ64rfsZhLCoxz14pPYDbizgdhjNPXG3JBqOBg8IPNSw9BnOKzLH4Gwds9R6VDcDaM4z1NTYDY749abLOAWQjAPBOKSAk05sRrk5I4JznmtWI8A+h6Vh2jBLo4GBjAxW3bD5Rn17U5ISLhf5O+Rzn2qjK3zEDB/Q4q3IARkZUEVnSsBlc59/aoGaNi68gDDA5zW2lq4iSUsMdcZrnLAbTkEYxjmrAu7iKQ7mPlnt6e1MDqLKLzRuYYU8YpZkVJODmobC9U6bExIDfWmecXl6fjVAWbiElOuBjJxWW5KEj8/etWQgr14xzWZdDDHHXsPWhsDEuhumJ7A1VmOEYj+VWrkgPnJOao3EhKhAep/SoAqjO0455zTCo4HYcZqbaQvQjPtTSADyOKAI8fKCevYVDJ15GasS/dB7+lVZW3dxxxQBWkwG6nNRSLx04HenMWCsD1FRmTjB4z0oAfpKodQkGQB5RJz0HStK4AJyOmeD3rN0hg9/KQxUrET8o47cVemPOcYA6e1aJAVZU2kDHSk+bHHPYZ7U2Qkk5zjtwaUYZMnjHSkOwJtRssO3StKB8xgbiAMcdqz1/eLyF64HNWYP9WVPT09KFoDKGu6c80i3EZ3oRggV5hcgx3EsW3GGIGa9hspQm9HGRkgCvLfEkPk65dgLwJCQM+orfoZJalW2SNsE5DA+lacMKtgdRWZCcADkZrSRmSJSCMmpNCSW0BHAAP07VUZVRiCMjGc+lE106jJOTjA56VYtLuJlxIgOeMigDE1e5cWUpUkgKASOgJPSui+HdofKe9bGCAqAjn61U8U+HE/4RYT25ZZJ7qNSg/u4PP6Cuh07y9P0uBQQBGgUAccisZblQ2L+sajiEr3H5Vz8kiTbieT2wOlQ31+bqR+eM1WMhABBA+nSpLNax02zvSPNjAHY9Oa7vTw1rYiFV4xwOwrzywuGJUBs5I4OK9CsTutVZiQSu3/AD+VMhrUpXyiQlicgHGPSqPl29Lqd3sYKMkNz05qjz7VvHVGTsex7FuoPmGMdMdqytRHyMjfMNuOaKK5yzzrViba62qeAehrA1D7yt1BP3e1FFWNElsSR6benFUPERKWrsGOcUUVAI8g1aZ5JHLNmvQvh2gj8HQ4/wCe0v8A6FRRWsNxS2NWSPdIOcZre0y3EO1gTnr+lFFbGRdbmTZ2rb0A7LV9vHzf0ooqZbBDc0hmP5QeMD+dRag+2IjAIx3oorHqjU5uSMJP65rP1ONeQw3Dt7UUVqQUYzuX/PrW5pkYVBjjv+NFFDKR0FvGQEGePpUyj5wO1FFY9RknSqN6/BGAc0UVS6AQ2sx9B049q6S0k/dpwOaKKcthItOcRnAxxWSxxKy44GMe1FFZDLdqTI+M4HXAqPUZWwMEiiiqQG7YDNnACc/LmtGAfKB79aKKYEmdr8e1Vb4HGQcEd8UUUnuBgXTYYjFZpGDn3ooqQJGTIHT8qrucHNFFAEfSNj3qo4xnHFFFAFSR/mximyKGjBI6UUUAGjjyrycg8LFkD8RV/dvZhjA9qKKuIFF5CWPPenMMAHvRRQWIr7XwAK0Lc7+tFFAmRMczqo4HoK4bxdADr0ig43IGJAoorV/CZ9TBUlGIB49KsCYmHbjjNFFJbFFS4frTbWVjPGoOFz0ooqGB1ssjNpMKk5UyKMfnVTVTm3jx8vy9qKKmW5cdjDjctJzzViY7bWRvTtRRUlGZpmuzW2oW42K6SHDKa9kCYt0VSVAUYA7UUVSJZjagmWZs/MvANUt7epooreOxg9z/2Q==' class='member-photo' />
            <div class='member-name'>Moh Viko Nur Huda</div>
            <div class='member-nim'>24051214076 · S1 Sistem Informasi</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- Quick stats ringkasan --
    st.markdown('<div class="section-header">Ringkasan Dataset</div>', unsafe_allow_html=True)
    total_customers = rfm["CustomerID"].nunique()
    total_invoices  = trans["InvoiceNo"].nunique()
    total_revenue   = trans["TotalPrice"].sum()
    avg_order_value = trans.groupby("InvoiceNo")["TotalPrice"].sum().mean()

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, sub in [
        (c1, "Total Pelanggan",  f"{total_customers:,}",       "pelanggan unik"),
        (c2, "Total Transaksi",  f"{total_invoices:,}",        "invoice"),
        (c3, "Total Penjualan",  f"£{total_revenue/1e6:.1f}M", "gross revenue"),
        (c4, "Rata-rata Order",  f"£{avg_order_value:,.2f}", "per transaksi"),
    ]:
        col.markdown(f"""
        <div class='metric-card'>
            <div class='m-label'>{label}</div>
            <div class='m-value'>{value}</div>
            <div class='m-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- Segmen overview --
    st.markdown('<div class="section-header">Segmen Pelanggan</div>', unsafe_allow_html=True)
    seg_col1, seg_col2, seg_col3 = st.columns(3)
    seg_counts = rfm["ClusterLabel"].value_counts()

    seg_defs = [
        ("Champions", "#22c55e", "#14532d", "#166534",
         "Pelanggan paling aktif & loyal dengan pengeluaran tertinggi."),
        ("Potential Loyalists", "#60a5fa", "#1e3a8a", "#1d4ed8",
         "Pelanggan berpotensi tinggi yang perlu didorong menjadi Champions."),
        ("At-Risk / Churned", "#f87171", "#7f1d1d", "#991b1b",
         "Pelanggan yang lama tidak aktif dan butuh kampanye reaktivasi."),
    ]
    for scol, (seg_name, color, bg, border, desc) in zip([seg_col1, seg_col2, seg_col3], seg_defs):
        count = seg_counts.get(seg_name, 0)
        pct = count / seg_counts.sum() * 100
        scol.markdown(f"""
        <div style='background:{bg};border:1px solid {border};border-radius:12px;
                    padding:20px 18px;height:100%;'>
            <div style='font-size:11px;font-weight:700;color:{color};letter-spacing:1.5px;
                        text-transform:uppercase;margin-bottom:8px;'>{seg_name}</div>
            <div style='font-size:28px;font-weight:800;color:#f1f5f9;'>{count:,}</div>
            <div style='font-size:12px;color:{color};margin-bottom:10px;'>{pct:.1f}% pelanggan</div>
            <div style='font-size:12px;color:#94a3b8;line-height:1.6;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- Fitur dashboard --
    st.markdown('<div class="section-header">Fitur Dashboard</div>', unsafe_allow_html=True)
    feat_cols = st.columns(4)
    features = [
        ("Dataset Overview", "#3b82f6", "Eksplorasi statistik deskriptif, distribusi RFM, dan sampel data transaksi."),
        ("Prediction", "#22c55e", "Prediksi segmen pelanggan baru via ID atau input manual nilai RFM."),
        ("Visualization", "#a78bfa", "Visualisasi interaktif klaster, association rules, dan tren penjualan."),
        ("About", "#f59e0b", "Penjelasan metode K-Means, Apriori, dan kerangka CRISP-DM yang digunakan."),
    ]
    for fcol, (title, color, desc) in zip(feat_cols, features):
        fcol.markdown(f"""
        <div style='background:#111827;border:1px solid #1e2d47;border-radius:10px;
                    padding:18px 16px;height:100%;'>
            <div style='width:32px;height:4px;background:{color};border-radius:2px;margin-bottom:12px;'></div>
            <div style='font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:8px;'>{title}</div>
            <div style='font-size:12px;color:#64748b;line-height:1.6;'>{desc}</div>
        </div>""", unsafe_allow_html=True)


# ================================================================
#  PAGE 2 · DATASET OVERVIEW
#  Berisi: informasi dataset, jumlah data, statistik, visualisasi
# ================================================================
elif menu == "Dataset Overview":

    st.markdown("""
    <div class='page-title'>Dataset Overview</div>
    <div class='page-subtitle'>Informasi, statistik, dan distribusi data yang digunakan</div>
    """, unsafe_allow_html=True)

    # -- Informasi dataset --
    st.markdown('<div class="section-header">Informasi Dataset</div>', unsafe_allow_html=True)

    col_info, col_shape = st.columns([2, 1])

    with col_info:
        # TODO: sesuaikan nama dataset, sumber, dan keterangan
        st.markdown("""
        <table class='about-table'>
            <tr><td>Nama Dataset</td><td>Online Retail Dataset (UCI Machine Learning Repository)</td></tr>
            <tr><td>Sumber</td><td><a href="https://archive.ics.uci.edu/dataset/352/online+retail" style="color:#3b82f6;" target="_blank">https://archive.ics.uci.edu/dataset/352/online+retail</a></td></tr>
            <tr><td>Periode Data</td><td>1 Desember 2010 — 9 Desember 2011</td></tr>
            <tr><td>Negara Asal</td><td>United Kingdom</td></tr>
            <tr><td>Format</td><td>CSV / Excel (.xlsx)</td></tr>
            <tr><td>Lisensi</td><td>Open Access — UCI Repository</td></tr>
        </table>
        """, unsafe_allow_html=True)

    with col_shape:
        rows, cols_count = trans.shape
        st.markdown(f"""
        <div class='metric-card' style='margin-bottom:10px;'>
            <div class='m-label'>Jumlah Baris</div>
            <div class='m-value'>{rows:,}</div>
            <div class='m-sub'>records transaksi</div>
        </div>
        <div class='metric-card'>
            <div class='m-label'>Jumlah Kolom</div>
            <div class='m-value'>{cols_count}</div>
            <div class='m-sub'>fitur/atribut</div>
        </div>
        """, unsafe_allow_html=True)

    # -- Statistik sederhana tabel RFM --
    st.markdown('<div class="section-header">Statistik Deskriptif (RFM)</div>', unsafe_allow_html=True)
    rfm_desc = rfm[["Recency", "Frequency", "Monetary"]].describe().round(2)
    st.dataframe(rfm_desc, use_container_width=True)

    # -- Pratinjau data transaksi --
    with st.expander("Lihat Sampel Data Transaksi (10 baris pertama)"):
        st.dataframe(trans.head(10), use_container_width=True, hide_index=True)

    # -- Visualisasi distribusi data --
    st.markdown('<div class="section-header">Distribusi Data</div>', unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        # Distribusi Recency
        fig_rec = px.histogram(
            rfm, x="Recency", nbins=40,
            labels={"Recency": "Recency (hari)", "count": "Jumlah Pelanggan"},
            title="Distribusi Recency",
            color_discrete_sequence=["#3b82f6"],
        )
        fig_rec.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=12),
            title_font=dict(size=14, weight=700, color="#e2e8f0"),
            margin=dict(t=40, b=10),
            xaxis=dict(gridcolor="#1e2d47"),
            yaxis=dict(gridcolor="#1e2d47"),
        )
        st.plotly_chart(fig_rec, use_container_width=True)

    with col_v2:
        # Distribusi Monetary (log scale lebih informatif)
        fig_mon = px.histogram(
            rfm, x="Monetary", nbins=40,
            labels={"Monetary": "Monetary (£)", "count": "Jumlah Pelanggan"},
            title="Distribusi Monetary",
            color_discrete_sequence=["#22c55e"],
            log_y=True,
        )
        fig_mon.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=12),
            title_font=dict(size=14, weight=700, color="#e2e8f0"),
            margin=dict(t=40, b=10),
            xaxis=dict(gridcolor="#1e2d47"),
            yaxis=dict(gridcolor="#1e2d47"),
        )
        st.plotly_chart(fig_mon, use_container_width=True)

    col_v3, col_v4 = st.columns(2)

    with col_v3:
        # Distribusi Frequency
        fig_freq = px.histogram(
            rfm, x="Frequency", nbins=30,
            labels={"Frequency": "Frekuensi Transaksi", "count": "Jumlah Pelanggan"},
            title="Distribusi Frequency",
            color_discrete_sequence=["#a78bfa"],
        )
        fig_freq.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=12),
            title_font=dict(size=14, weight=700, color="#e2e8f0"),
            margin=dict(t=40, b=10),
            xaxis=dict(gridcolor="#1e2d47"),
            yaxis=dict(gridcolor="#1e2d47"),
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    with col_v4:
        # Distribusi segmen pelanggan
        seg_counts = rfm["ClusterLabel"].value_counts().reset_index()
        seg_counts.columns = ["Segmen", "Jumlah"]
        fig_seg = px.bar(
            seg_counts, x="Segmen", y="Jumlah",
            title="Jumlah Pelanggan per Segmen",
            color="Segmen", color_discrete_map=COLORS_MAP,
            text="Jumlah",
        )
        fig_seg.update_traces(textposition="outside", textfont_size=12)
        fig_seg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=12),
            title_font=dict(size=14, weight=700, color="#e2e8f0"),
            margin=dict(t=40, b=10),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(gridcolor="#1e2d47"),
            showlegend=False,
        )
        st.plotly_chart(fig_seg, use_container_width=True)


# ================================================================
#  PAGE 3 · PREDICTION
#  Berisi: form input, tombol proses, hasil prediksi segmen
#  Dua tab: cari by Customer ID | input manual
# ================================================================
elif menu == "Prediction":

    st.markdown("""
    <div class='page-title'>Prediksi Segmen Pelanggan</div>
    <div class='page-subtitle'>Identifikasi segmen pelanggan menggunakan model K-Means (RFM)</div>
    """, unsafe_allow_html=True)

    # -- Dua tab input --
    tab1, tab2 = st.tabs(["Cari Berdasarkan Customer ID", "Input Data Manual"])

    # ── Tab 1: Lookup by Customer ID ──────────────────────────────
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        customer_ids = sorted(rfm["CustomerID"].dropna().astype(int).tolist())

        col_sel, col_btn = st.columns([3, 1])
        with col_sel:
            selected_id = st.selectbox("Customer ID", customer_ids, key="cid_select")
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            run_id = st.button("Analisis Pelanggan", key="btn_id")

        if run_id:
            row      = rfm[rfm["CustomerID"] == selected_id].iloc[0]
            recency  = row["Recency"]
            frequency = row["Frequency"]
            monetary  = row["Monetary"]
            label     = row["ClusterLabel"]

            cfg = SEGMENT_CONFIG.get(label, {
                "badge": "badge-others",
                "chars": ["Data tersedia"],
                "actions": ["Lakukan analisis lebih lanjut"],
            })

            col_left, col_right = st.columns(2)

            with col_left:
                # -- Profil pelanggan --
                st.markdown('<div class="section-header">Profil Pelanggan</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class='profile-card'>
                    <div class='profile-id-label'>Customer ID</div>
                    <div class='profile-id-value'>{int(selected_id)}</div>
                    <div class='rfm-mini-grid'>
                        <div class='rfm-mini-cell'>
                            <div class='rfm-mini-label'>Recency</div>
                            <div class='rfm-mini-value'>{int(recency)}</div>
                            <div class='rfm-mini-sub'>hari lalu</div>
                        </div>
                        <div class='rfm-mini-cell'>
                            <div class='rfm-mini-label'>Frequency</div>
                            <div class='rfm-mini-value'>{int(frequency)}</div>
                            <div class='rfm-mini-sub'>transaksi</div>
                        </div>
                        <div class='rfm-mini-cell'>
                            <div class='rfm-mini-label'>Monetary</div>
                            <div class='rfm-mini-value'>£{monetary:,.0f}</div>
                            <div class='rfm-mini-sub'>total belanja</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_right:
                # -- Hasil segmentasi --
                st.markdown('<div class="section-header">Hasil Segmentasi</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background:#111827;border:1px solid #1e2d47;border-radius:12px;
                            padding:20px;text-align:center;'>
                    <div style='font-size:11px;font-weight:700;color:#475569;
                                letter-spacing:1.5px;text-transform:uppercase;
                                margin-bottom:8px;'>Segmen</div>
                    <span class='segment-badge {cfg["badge"]}'>{label.upper()}</span>
                    <div style='margin-top:14px;text-align:left;'>
                        <div style='font-size:10px;font-weight:700;color:#475569;
                                    letter-spacing:1px;text-transform:uppercase;
                                    margin-bottom:8px;'>Karakteristik</div>
                        {''.join([f"<span class='char-chip'>{c}</span>" for c in cfg['chars']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # -- Rekomendasi aksi bisnis --
            st.markdown('<div class="section-header">Rekomendasi Aksi Bisnis</div>', unsafe_allow_html=True)
            for i, action in enumerate(cfg["actions"], 1):
                st.markdown(
                    f'<div class="action-box"><strong>{i}.</strong> {action}</div>',
                    unsafe_allow_html=True,
                )

    # ── Tab 2: Input manual ────────────────────────────────────────
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <p style='font-size:13px;color:#64748b;'>
            Masukkan nilai RFM pelanggan baru untuk memprediksi segmennya secara langsung.
        </p>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            inp_monetary  = st.number_input(
                "Total Belanja (£)", min_value=0, value=500, step=50, format="%d"
            )
        with col2:
            inp_frequency = st.number_input(
                "Frekuensi Belanja (transaksi)", min_value=1, value=5, step=1
            )
        with col3:
            inp_recency   = st.number_input(
                "Terakhir Belanja (hari lalu)", min_value=0, value=30, step=1
            )

        run_manual = st.button("Proses Prediksi", key="btn_manual")

        if run_manual:
            label, cluster_num = predict_segment(inp_recency, inp_frequency, inp_monetary)
            cfg = SEGMENT_CONFIG.get(label, {
                "badge": "badge-others",
                "chars": ["Pelanggan baru"],
                "actions": ["Pantau aktivitas pembelian"],
            })

            col_l, col_r = st.columns(2)

            with col_l:
                # -- Input summary --
                st.markdown(f"""
                <div class='profile-card'>
                    <div style='font-size:10px;font-weight:700;color:#475569;
                                letter-spacing:1.5px;text-transform:uppercase;
                                margin-bottom:12px;'>Data yang Dimasukkan</div>
                    <table style='width:100%;font-size:13px;font-weight:500;color:#94a3b8;border-collapse:collapse;'>
                        <tr style='border-bottom:1px solid #1e2d47;'>
                            <td style='padding:8px 0;'>Total Belanja</td>
                            <td style='text-align:right;color:#3b82f6;font-weight:700;'>
                                £{inp_monetary:,.2f}
                            </td>
                        </tr>
                        <tr style='border-bottom:1px solid #1e2d47;'>
                            <td style='padding:8px 0;'>Frekuensi</td>
                            <td style='text-align:right;color:#3b82f6;font-weight:700;'>
                                {inp_frequency} kali
                            </td>
                        </tr>
                        <tr style='border-bottom:1px solid #1e2d47;'>
                            <td style='padding:8px 0;'>Terakhir Belanja</td>
                            <td style='text-align:right;color:#3b82f6;font-weight:700;'>
                                {inp_recency} hari lalu
                            </td>
                        </tr>
                        <tr>
                            <td style='padding:8px 0;'>Cluster</td>
                            <td style='text-align:right;color:#64748b;font-weight:700;'>
                                {cluster_num}
                            </td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

            with col_r:
                st.markdown(f"""
                <div style='background:#111827;border:1px solid #1e2d47;border-radius:12px;
                            padding:20px;text-align:center;'>
                    <div style='font-size:10px;font-weight:700;color:#475569;
                                letter-spacing:1.5px;text-transform:uppercase;
                                margin-bottom:8px;'>Prediksi Segmen</div>
                    <span class='segment-badge {cfg["badge"]}'>{label.upper()}</span>
                    <div style='margin-top:14px;text-align:left;'>
                        {''.join([f"<span class='char-chip'>{c}</span>" for c in cfg['chars']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-header">Rekomendasi Aksi Bisnis</div>', unsafe_allow_html=True)
            for i, action in enumerate(cfg["actions"], 1):
                st.markdown(
                    f'<div class="action-box"><strong>{i}.</strong> {action}</div>',
                    unsafe_allow_html=True,
                )


# ================================================================
#  PAGE 4 · VISUALIZATION
#  Berisi: grafik pendukung & visualisasi hasil analisis lengkap
# ================================================================
elif menu == "Visualization":

    st.markdown("""
    <div class='page-title'>Visualization</div>
    <div class='page-subtitle'>Grafik pendukung dan visualisasi hasil analisis data</div>
    """, unsafe_allow_html=True)

    # -- Sub-navigasi visualisasi --
    viz_tab1, viz_tab2, viz_tab3 = st.tabs([
        "Segmentasi Pelanggan",
        "Pola Pembelian (Apriori)",
        "Tren Penjualan",
    ])

    # ── Tab 1: Segmentasi ──────────────────────────────────────────
    with viz_tab1:
        col_a, col_b = st.columns(2)

        with col_a:
            # Pie chart distribusi segmen
            st.markdown('<div class="section-header">Distribusi Segmen Pelanggan</div>', unsafe_allow_html=True)
            seg_counts = rfm["ClusterLabel"].value_counts().reset_index()
            seg_counts.columns = ["Segmen", "Jumlah"]
            fig_pie = px.pie(
                seg_counts, values="Jumlah", names="Segmen",
                color="Segmen", color_discrete_map=COLORS_MAP,
                hole=0.48,
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8", size=12),
                margin=dict(t=20, b=20),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
            )
            fig_pie.update_traces(textposition="outside", textinfo="percent+label",
                                  textfont=dict(family="Inter", size=12))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            # Scatter PCA klaster
            st.markdown('<div class="section-header">Klaster Pelanggan — Proyeksi PCA</div>', unsafe_allow_html=True)
            fig_pca = px.scatter(
                rfm, x="PCA1", y="PCA2", color="ClusterLabel",
                color_discrete_map=COLORS_MAP,
                hover_data={
                    "CustomerID": True, "Recency": True,
                    "Frequency": True, "Monetary": ":.0f",
                },
                labels={
                    "PCA1": "Komponen Utama 1",
                    "PCA2": "Komponen Utama 2",
                    "ClusterLabel": "Segmen",
                },
            )
            fig_pca.update_traces(marker=dict(size=5, opacity=0.65))
            fig_pca.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8", size=12),
                margin=dict(t=20, b=20),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
                xaxis=dict(gridcolor="#1e2d47"),
                yaxis=dict(gridcolor="#1e2d47"),
            )
            st.plotly_chart(fig_pca, use_container_width=True)

        # Profil RFM rata-rata per segmen
        st.markdown('<div class="section-header">Profil RFM Rata-rata per Segmen</div>', unsafe_allow_html=True)
        rfm_summary = (
            rfm.groupby("ClusterLabel")[["Recency", "Frequency", "Monetary"]]
            .mean().round(1).reset_index()
        )
        rfm_summary.columns = ["Segmen", "Avg Recency (hari)", "Avg Frekuensi", "Avg Monetary (£)"]
        rfm_summary["Avg Monetary (£)"] = rfm_summary["Avg Monetary (£)"].apply(
            lambda x: f"£{x:,.2f}"
        )
        st.dataframe(rfm_summary, use_container_width=True, hide_index=True)

        # Box plot RFM per segmen
        col_c, col_d = st.columns(2)
        with col_c:
            fig_box_r = px.box(
                rfm, x="ClusterLabel", y="Recency",
                color="ClusterLabel", color_discrete_map=COLORS_MAP,
                title="Sebaran Recency per Segmen",
                labels={"ClusterLabel": "Segmen", "Recency": "Recency (hari)"},
            )
            fig_box_r.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8", size=12),
                title_font=dict(size=14, weight=700, color="#e2e8f0"),
                showlegend=False, margin=dict(t=40, b=10),
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="#1e2d47"),
            )
            st.plotly_chart(fig_box_r, use_container_width=True)

        with col_d:
            fig_box_m = px.box(
                rfm, x="ClusterLabel", y="Monetary",
                color="ClusterLabel", color_discrete_map=COLORS_MAP,
                title="Sebaran Monetary per Segmen",
                labels={"ClusterLabel": "Segmen", "Monetary": "Monetary (£)"},
                log_y=True,
            )
            fig_box_m.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8", size=12),
                title_font=dict(size=14, weight=700, color="#e2e8f0"),
                showlegend=False, margin=dict(t=40, b=10),
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="#1e2d47"),
            )
            st.plotly_chart(fig_box_m, use_container_width=True)

    # ── Tab 2: Pola Pembelian (Apriori) ───────────────────────────
    with viz_tab2:

        st.markdown('<div class="section-header">Pencarian Pola Pembelian</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style='font-size:13px;color:#64748b;'>
            Pilih produk antecedent untuk menemukan produk yang sering dibeli bersamaan.
        </p>
        """, unsafe_allow_html=True)

        all_products = sorted(set(
            p for lst in rules["ant_list"] + rules["con_list"] for p in lst
        ))

        col_sel2, col_filt = st.columns(2)
        with col_sel2:
            selected_products = st.multiselect(
                "Produk Antecedent (maks. 3)",
                all_products, max_selections=3,
                placeholder="Ketik atau pilih produk...",
            )
        with col_filt:
            col_conf, col_sort = st.columns(2)
            with col_conf:
                min_conf = st.slider("Min. Confidence", 0.0, 1.0, 0.3, 0.05, format="%.2f")
            with col_sort:
                sort_by = st.selectbox("Urutkan", ["confidence", "lift", "support"])

        run_rules = st.button("Cari Pola Pembelian", key="btn_rules")

        if run_rules:
            if not selected_products:
                st.warning("Pilih minimal 1 produk terlebih dahulu.")
            else:
                def match_rule(ant_list):
                    return all(p in ant_list for p in selected_products)

                filtered = (
                    rules[
                        rules["ant_list"].apply(match_rule) &
                        (rules["confidence"] >= min_conf)
                    ]
                    .sort_values(sort_by, ascending=False)
                    .head(15)
                )

                if filtered.empty:
                    st.info("Tidak ditemukan aturan asosiasi untuk kombinasi produk dan filter ini.")
                else:
                    ant_label  = " + ".join(selected_products)
                    top_rule   = filtered.iloc[0]
                    conseq_label = ", ".join(top_rule["con_list"])

                    st.markdown(f"""
                    <div class='insight-box'>
                        Ditemukan <strong>{len(filtered)} aturan asosiasi</strong> untuk
                        <strong>{ant_label}</strong>.<br>
                        Aturan terbaik: pelanggan yang membeli <strong>{ant_label}</strong>
                        juga cenderung membeli <strong>{conseq_label}</strong>
                        dengan confidence <strong>{top_rule['confidence']*100:.1f}%</strong>
                        dan lift <strong>{top_rule['lift']:.2f}x</strong>.
                    </div>
                    """, unsafe_allow_html=True)

                    # Rekomendasi toko
                    st.markdown('<div class="section-header">Rekomendasi Penempatan Toko</div>', unsafe_allow_html=True)
                    for rec_text in [
                        f"<strong>Penempatan Produk:</strong> Letakkan <em>{conseq_label}</em> di dekat rak <em>{ant_label}</em>.",
                        f"<strong>Bundle Promo:</strong> Buat paket bundling <em>{ant_label}</em> + <em>{conseq_label}</em> dengan diskon khusus.",
                        f"<strong>Cross-Sell:</strong> Tampilkan <em>{conseq_label}</em> sebagai rekomendasi saat pelanggan melihat <em>{ant_label}</em>.",
                    ]:
                        st.markdown(f'<div class="action-box">{rec_text}</div>', unsafe_allow_html=True)

                    # Bar chart confidence
                    st.markdown('<div class="section-header">Confidence per Aturan Asosiasi</div>', unsafe_allow_html=True)
                    chart_data = filtered.copy()
                    chart_data["label"] = chart_data["con_list"].apply(
                        lambda x: ", ".join(x)[:40]
                    )
                    fig_bar = px.bar(
                        chart_data.sort_values("confidence"),
                        x="confidence", y="label", orientation="h",
                        color="lift",
                        color_continuous_scale=[[0, "#1e3a8a"], [0.5, "#3b82f6"], [1, "#22c55e"]],
                        labels={"confidence": "Confidence", "label": "Consequent", "lift": "Lift"},
                        text=chart_data.sort_values("confidence")["confidence"].apply(
                            lambda x: f"{x*100:.1f}%"
                        ),
                    )
                    fig_bar.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Inter", color="#94a3b8", size=12),
                        margin=dict(t=10, b=10),
                        xaxis=dict(gridcolor="#1e2d47", tickformat=".0%"),
                        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                    )
                    fig_bar.update_traces(textposition="outside")
                    st.plotly_chart(fig_bar, use_container_width=True)

                    # Detail aturan
                    st.markdown('<div class="section-header">Detail Aturan Asosiasi</div>', unsafe_allow_html=True)
                    for _, row_r in filtered.iterrows():
                        ant_str  = " + ".join(row_r["ant_list"])
                        con_str  = " + ".join(row_r["con_list"])
                        conf_pct = row_r["confidence"] * 100
                        lift_v   = row_r["lift"]
                        sup_pct  = row_r["support"] * 100

                        conf_color = "#22c55e" if conf_pct >= 70 else "#f59e0b" if conf_pct >= 50 else "#ef4444"
                        lift_color = "#22c55e" if lift_v >= 2 else "#f59e0b" if lift_v >= 1.5 else "#94a3b8"

                        st.markdown(f"""
                        <div class='rule-card'>
                            <div class='rule-title'>{ant_str} &rarr; {con_str}</div>
                            <div style='display:flex;gap:24px;margin-top:10px;flex-wrap:wrap;'>
                                <div>
                                    <div class='rule-stat'>CONFIDENCE</div>
                                    <div style='font-size:20px;font-weight:800;color:{conf_color};'>
                                        {conf_pct:.1f}%
                                    </div>
                                    <div class='rule-stat'>pelanggan membeli keduanya</div>
                                </div>
                                <div>
                                    <div class='rule-stat'>LIFT</div>
                                    <div style='font-size:20px;font-weight:800;color:{lift_color};'>
                                        {lift_v:.2f}x
                                    </div>
                                    <div class='rule-stat'>lebih sering dari peluang acak</div>
                                </div>
                                <div>
                                    <div class='rule-stat'>SUPPORT</div>
                                    <div style='font-size:20px;font-weight:800;color:#94a3b8;'>
                                        {sup_pct:.1f}%
                                    </div>
                                    <div class='rule-stat'>frekuensi kemunculan bersama</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        # Semua aturan (expander)
        with st.expander("Lihat Semua Aturan Asosiasi — Top 30 berdasarkan Lift"):
            top_rules_display = rules.sort_values("lift", ascending=False).head(30).copy()
            top_rules_display["Antecedents"] = top_rules_display["ant_list"].apply(
                lambda x: " + ".join(x)
            )
            top_rules_display["Consequents"] = top_rules_display["con_list"].apply(
                lambda x: " + ".join(x)
            )
            top_rules_display["Confidence"] = (
                top_rules_display["confidence"] * 100
            ).round(1).astype(str) + "%"
            top_rules_display["Lift"]    = top_rules_display["lift"].round(2)
            top_rules_display["Support"] = (
                top_rules_display["support"] * 100
            ).round(2).astype(str) + "%"
            st.dataframe(
                top_rules_display[["Antecedents", "Consequents", "Confidence", "Lift", "Support"]],
                use_container_width=True, hide_index=True,
            )

    # ── Tab 3: Tren Penjualan ──────────────────────────────────────
    with viz_tab3:

        col_e, col_f = st.columns(2)

        with col_e:
            # Tren revenue bulanan
            st.markdown('<div class="section-header">Tren Pendapatan Bulanan</div>', unsafe_allow_html=True)
            monthly = trans.groupby("YearMonth")["TotalPrice"].sum().reset_index()
            monthly.columns = ["Bulan", "Revenue"]
            fig_line = px.line(
                monthly, x="Bulan", y="Revenue",
                markers=True, line_shape="spline",
                labels={"Bulan": "Bulan", "Revenue": "Revenue (£)"},
            )
            fig_line.update_traces(
                line=dict(color="#3b82f6", width=2.5),
                marker=dict(size=6, color="#3b82f6"),
            )
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8", size=12),
                margin=dict(t=10, b=10),
                xaxis=dict(gridcolor="#1e2d47", tickangle=-45),
                yaxis=dict(gridcolor="#1e2d47", tickformat=",.0f"),
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with col_f:
            # Top 10 produk terlaris
            st.markdown('<div class="section-header">Top 10 Produk Terlaris</div>', unsafe_allow_html=True)
            top_prod = (
                trans.groupby("Description")["Quantity"]
                .sum().sort_values(ascending=False).head(10).reset_index()
            )
            top_prod.columns = ["Produk", "Qty"]
            top_prod["Produk"] = top_prod["Produk"].str[:40]
            fig_top = px.bar(
                top_prod.sort_values("Qty"), x="Qty", y="Produk",
                orientation="h", color="Qty",
                color_continuous_scale=[[0, "#1e3a8a"], [1, "#3b82f6"]],
                labels={"Qty": "Total Terjual", "Produk": ""},
            )
            fig_top.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8", size=12),
                margin=dict(t=10, b=10),
                showlegend=False, coloraxis_showscale=False,
                xaxis=dict(gridcolor="#1e2d47"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_top, use_container_width=True)


# ================================================================
#  PAGE 5 · ABOUT
#  Berisi: penjelasan metode, dataset, informasi proyek
# ================================================================
elif menu == "About":

    st.markdown("""
    <div class='page-title'>About</div>
    <div class='page-subtitle'>Penjelasan metode, dataset, dan informasi proyek</div>
    """, unsafe_allow_html=True)

    # -- Penjelasan metode --
    st.markdown('<div class="section-header">Metode yang Digunakan</div>', unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        # K-Means Clustering
        st.markdown("""
        <div style='background:#111827;border:1px solid #1e2d47;border-radius:10px;
                    padding:20px;height:100%;'>
            <div style='font-size:13px;font-weight:800;color:#3b82f6;
                        letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>
                K-Means Clustering
            </div>
            <p style='font-size:13px;color:#94a3b8;line-height:1.8;'>
                K-Means adalah algoritma unsupervised learning yang mengelompokkan data ke
                dalam K klaster berdasarkan jarak Euclidean terhadap centroid. Pada proyek ini,
                fitur yang digunakan adalah nilai RFM (Recency, Frequency, Monetary) yang
                sebelumnya dinormalisasi menggunakan StandardScaler dan direduksi dimensinya
                menggunakan PCA untuk keperluan visualisasi.
                <br><br>
                <!-- TODO: tambahkan detail eksperimen, nilai K optimal, dan metrik evaluasi -->
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nilai K optimal
                ditentukan menggunakan metode Elbow dan Silhouette Score.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        # Apriori Association Rules
        st.markdown("""
        <div style='background:#111827;border:1px solid #1e2d47;border-radius:10px;
                    padding:20px;height:100%;'>
            <div style='font-size:13px;font-weight:800;color:#22c55e;
                        letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>
                Apriori — Association Rule Mining
            </div>
            <p style='font-size:13px;color:#94a3b8;line-height:1.8;'>
                Algoritma Apriori digunakan untuk menemukan frequent itemsets dan menghasilkan
                aturan asosiasi dari data transaksi pelanggan. Tiga metrik utama yang digunakan
                adalah Support (frekuensi kemunculan bersama), Confidence (probabilitas
                kondisional), dan Lift (kekuatan asosiasi relatif terhadap peluang acak).
                <br><br>
                <!-- TODO: tambahkan nilai min_support dan min_confidence yang digunakan -->
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Min support yang
                digunakan adalah 0.02 dan min confidence 0.3.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    # -- Informasi dataset --
    st.markdown('<div class="section-header">Dataset</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#111827;border:1px solid #1e2d47;border-radius:10px;padding:20px;'>
        <table class='about-table'>
            <tr>
                <td>Nama</td>
                <td>
                    <!-- TODO: ganti dengan nama dataset yang sebenarnya -->
                    Online Retail Dataset
                </td>
            </tr>
            <tr>
                <td>Sumber</td>
                <td><a href="https://archive.ics.uci.edu/dataset/352/online+retail" style="color:#3b82f6;" target="_blank">UCI Machine Learning Repository — Online Retail</a></td>
            </tr>
            <tr>
                <td>Deskripsi</td>
                <td>
                    <!-- TODO: ganti dengan deskripsi dataset yang sebenarnya -->
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Dataset berisi
                    transaksi dari perusahaan retail online yang berbasis di UK, mencakup
                    periode Desember 2010 hingga Desember 2011.
                </td>
            </tr>
            <tr>
                <td>Jumlah Atribut</td>
                <td>8 kolom (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)</td>
            </tr>
            <tr>
                <td>Preprocessing</td>
                <td>
                    Penghapusan transaksi pembatalan (InvoiceNo awalan C), penanganan missing
                    CustomerID, filter Quantity dan UnitPrice negatif, pembuatan fitur TotalPrice
                    dan YearMonth.
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- Informasi proyek --
    st.markdown('<div class="section-header">Informasi Proyek</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#111827;border:1px solid #1e2d47;border-radius:10px;padding:20px;'>
        <table class='about-table'>
            <tr>
                <td>Nama Proyek</td>
                <td>
                    <!-- TODO: ganti dengan nama proyek yang sebenarnya -->
                    Analisis Pola Belanja E-Commerce Menggunakan Association Rule Mining dan K-Means Clustering
                </td>
            </tr>
            <tr>
                <td>Mata Kuliah</td>
                <td>
                    <!-- TODO: ganti dengan nama mata kuliah -->
                    Data Mining
                </td>
            </tr>
            <tr>
                <td>Dosen Pembimbing</td>
                <td>
                    <!-- TODO: ganti dengan nama dosen -->
                    Dr. Wiyli Yustanti, S.Si., M.Kom.
                </td>
            </tr>
            <tr>
                <td>Teknologi</td>
                <td>Python · Streamlit · Scikit-learn · MLxtend · Plotly · Pandas</td>
            </tr>
            <tr>
                <td>Repositori</td>
                <td>
                    <!-- TODO: isi link GitHub jika ada -->
                    https://github.com/username/repo-name
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
