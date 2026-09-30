import io
import random
import time
import uuid
from datetime import datetime
import pandas as pd
import streamlit as st

# Konfigurasi halaman web utama
st.set_page_config(
    page_title="Super App Analyzer - LW321 & DI319",
    page_icon="🏦",
    layout="wide",
)

# ================= MODERN CUSTOM CSS & STYLING =================
st.markdown(
    """
    <style>
    /* Global Font & Background Styling */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Sticky Filter Bar Modern */
    .sticky-filter-container {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        z-index: 9999;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin-bottom: 24px;
    }

    /* Modern Card Container */
    .modern-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 16px;
    }

    /* Styling Buttons & Inputs */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Input Fields Border Radius */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        border-radius: 8px !important;
    }

    /* Metric Container Enhancement */
    [data-testid="stMetric"] {
        background: #ffffff;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
    }
    
    /* Sidebar Modernization */
    [data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ================= INISISASI GLOBAL & SESSION STATE =================
if "active_user_tokens" not in st.session_state:
  st.session_state.active_user_tokens = {}

if "authenticated" not in st.session_state:
  st.session_state["authenticated"] = False
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state["username"] = ""
if "my_session_token" not in st.session_state:
  st.session_state.my_session_token = str(uuid.uuid4())

if "nasabah_catatan" not in st.session_state:
  st.session_state.nasabah_catatan = {}
if "custom_lists" not in st.session_state:
  st.session_state.custom_lists = {}
if "pipeline_leads" not in st.session_state:
  st.session_state.pipeline_leads = []
if "tidak_potensial_list" not in st.session_state:
  st.session_state.tidak_potensial_list = {}

if "show_help" not in st.session_state:
  st.session_state["show_help"] = False
if "show_login_help" not in st.session_state:
  st.session_state["show_login_help"] = False
if "notification_read" not in st.session_state:
  st.session_state["notification_read"] = False

# Database Kredensial Pengguna
USER_CREDENTIALS = {
    "qilmi": "123",
    "arjuna": "123",
    "pras": "123",
    "adi": "123",
    "bagas": "123",
    "yoga28": "123",
    "ngurah": "123",
    "agustianprimaryap": "123",
    "bri": "123",
}

is_user_logged_in = st.session_state["authenticated"] or st.session_state.logged_in

# ================= PENGECEKAN SINGLE DEVICE LOGIN =================
if is_user_logged_in:
  current_user = st.session_state["username"] or st.session_state.username
  active_token_map = st.session_state.active_user_tokens

  if (
      current_user in active_token_map
      and active_token_map[current_user] != st.session_state.my_session_token
  ):
    st.session_state["authenticated"] = False
    st.session_state.logged_in = False
    st.session_state["username"] = ""
    st.session_state.username = ""
    st.error(
        "⚠ Akun Anda telah login di perangkat/browser lain. Sesi di sini"
        " diakhiri."
    )
    st.stop()

# ================= DAFTAR MOTIVASI RM SME =================
sme_motivations = [
    (
        "🔥 'Menjadi RM SME handal bukan hanya tentang target, tapi tentang"
        " membangun kemitraan jangka panjang dan menjadi solusi bagi"
        " pertumbuhan bisnis nasabah.'"
    ),
    (
        "💪 'Setiap kunjungan (visit) adalah peluang emas. Dengarkan kebutuhan"
        " nasabah, tawarkan solusi terbaik, dan wujudkan deal impian hari ini!'"
    ),
    (
        "🚀 'Portofolio yang sehat berawal dari ketelitian menganalisis karakter"
        " nasabah dan disiplin dalam memantau kolektibilitas.'"
    ),
    (
        "💼 'Fokus pada solusi, bukan pada hambatan. Sebagai RM SME profesional,"
        " Anda adalah penggerak utama pertumbuhan ekonomi sektor riil.'"
    ),
    (
        "⭐ 'Target tinggi bukan untuk ditakuti, tapi untuk ditaklukkan dengan"
        " strategi yang cerdas, kerja keras, dan pelayanan sepenuh hati.'"
    ),
    (
        "🎯 'Kunci sukses RM SME: Proaktif mendatangi nasabah, cepat merespons"
        " kebutuhan kredit, dan menjaga kualitas kredit tetap lancar (Kol 1).'"
    ),
]


# ================= FUNGSI BANTUAN LOGIN =================
def toggle_login_help():
  st.session_state["show_login_help"] = not st.session_state[
      "show_login_help"
  ]


# ================= FORM LOGIN =================
if not is_user_logged_in:
  col_title, col_btn_help = st.columns([5, 1])
  with col_title:
    st.markdown(
        "<div style='margin-top: 10px;'>",
        unsafe_allow_html=True,
    )
    st.title("🔐 Login Super App (LW321 & DI319)")
    st.markdown("**Developer:** Prima & Primarya")
    st.markdown("</div>", unsafe_allow_html=True)

  with col_btn_help:
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    login_help_label = (
        "❌ Tutup Bantuan"
        if st.session_state["show_login_help"]
        else "💡 Bantuan (Help)"
    )
    st.button(
        login_help_label,
        on_click=toggle_login_help,
        use_container_width=True,
        key="btn_toggle_login_help",
    )

  if st.session_state["show_login_help"]:
    st.info("""
        ### 📖 Panduan Penggunaan & Informasi Aplikasi Super App
        **Developer:** Prima & Primarya  
        Aplikasi ini dirancang khusus untuk mempermudah pekerjaan Relationship Manager (RM) dan pengelola data perbankan. Berikut adalah panduan singkat untuk memulai:

        1. **🔑 Cara Login:**
            - Masukkan **Username** dan **Password** yang telah terdaftar pada sistem (misal: `qilmi`, `arjuna`, `pras`, `bri`, dll. dengan password default `123`).
            - Setiap akun hanya dapat aktif di satu perangkat/browser dalam satu waktu untuk keamanan data.

        2. **📈 Modul LW321 (Loan Debitur):**
            - Digunakan untuk mengunggah dan menganalisis file laporan kredit/debitur (`.xlsx`).
            - Memiliki fitur filter pencarian canggih berdasarkan Nama/No Rekening, Kanca, Uker, Tipe Pinjaman, Plafon, dan Kolektibilitas.
            - Dilengkapi monitoring otomatis untuk debitur **Jatuh Tempo (5 Bulan ke Depan)** serta debitur yang sudah lunas.

        3. **🏦 Modul DI319 (Pipeline & Dana):**
            - Digunakan untuk mengelola data simpanan/dana nasabah.
            - Dilengkapi fitur pencarian saldo, pembuatan **Pipeline Kunjungan**, catatan personal nasabah, hingga penandaan nasabah tidak potensial.

        4. **📞 Bantuan & Kendala:**
            - Jika mengalami error atau kendala teknis, Anda dapat menghubungi pengembang melalui kontak WhatsApp yang tertera di bagian bawah halaman.
        """)
    st.markdown("---")

  st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
  chosen_motivation = random.choice(sme_motivations)
  st.info(f"💡 **Motivasi RM SME Hari Ini:**\n\n{chosen_motivation}")
  st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    with st.form("login_form"):
      input_user = st.text_input("Username").strip().lower()
      input_pass = st.text_input("Password", type="password")
      submit_btn = st.form_submit_button(
          "Login", use_container_width=True, type="primary"
      )

      if submit_btn:
        if (
            input_user in USER_CREDENTIALS
            and USER_CREDENTIALS[input_user] == input_pass
        ):
          st.session_state.active_user_tokens[input_user] = (
              st.session_state.my_session_token
          )
          st.session_state["authenticated"] = True
          st.session_state.logged_in = True
          st.session_state["username"] = input_user
          st.session_state.username = input_user
          st.success(f"Login berhasil! Selamat datang, {input_user}")
          st.rerun()
        else:
          st.error("Username atau Password salah! Silakan coba lagi.")
  st.stop()


# ================= SIDEBAR UTAMA & PEMILIHAN APLIKASI =================
active_uname = st.session_state["username"] or st.session_state.username
st.sidebar.markdown(f"👤 **User Login:** `{active_uname}`")
if st.sidebar.button("🚪 Logout", use_container_width=True):
  if active_uname in st.session_state.active_user_tokens:
    del st.session_state.active_user_tokens[active_uname]
  st.session_state["authenticated"] = False
  st.session_state.logged_in = False
  st.session_state["username"] = ""
  st.session_state.username = ""
  st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Pilih Modul Aplikasi")
app_mode = st.sidebar.radio(
    "Pilih Tools Analisis:",
    ["📈 LW321 Analyzer (Loan Debitur)", "🏦 DI319 Analyzer (Pipeline & Dana)"],
)


# ================= FUNGSI BANTUAN LW321 =================
def toggle_help():
  st.session_state["show_help"] = not st.session_state["show_help"]


def format_no_rekening(no_rek):
  if pd.isna(no_rek):
    return "-"
  s = "".join(filter(str.isdigit, str(no_rek)))
  return s if s else str(no_rek)


def parse_numeric(val):
  if pd.isna(val):
    return 0.0
  if isinstance(val, (int, float)):
    return float(val)
  s = str(val).strip()
  for char in ["Rp", "IDR", "rp", "idr", " ", "\xa0"]:
    s = s.replace(char, "")

  if "." in s and "," in s:
    if s.rfind(".") > s.rfind(","):
      s = s.replace(",", "")
    else:
      s = s.replace(".", "").replace(",", ".")
  elif "," in s and "." not in s:
    s = s.replace(",", ".")
  elif s.count(".") > 1:
    s = s.replace(".", "")

  try:
    return float(s)
  except:
    return 0.0


def parse_rate(val):
  if pd.isna(val):
    return "N/A"
  s = str(val).strip()
  for char in ["%", " ", "\xa0"]:
    s = s.replace(char, "")
  if not s:
    return "N/A"
  s = s.replace(",", ".")
  try:
    num = float(s)
    return f"{num:.2f}".rstrip("0").rstrip(".")
  except:
    return str(val).strip()


def get_kolektibilitas(row):
  kol_mapping = {
      "KOLEKTIBILITAS LANCAR": "Kol 1 (Lancar)",
      "KOLEKTIBILITAS DPK": "Kol 2 (DPK)",
      "KOLEKTIBILITAS KURANG LANCAR": "Kol 3 (Kurang Lancar)",
      "KOLEKTIBILITAS DIRAGUKAN": "Kol 4 (Diragukan)",
      "KOLEKTIBILITAS MACET": "Kol 5 (Macet)",
  }
  for col, label in kol_mapping.items():
    if col in row and pd.notna(row[col]):
      val = str(row[col]).strip()
      if val and val != "0" and val != "0.0":
        return label
  return "Kol 1 (Lancar)"


def find_os_column(df):
  for col in df.columns:
    if str(col).strip().upper() == "BALANCE DALAM IDR":
      return col
  possible_keywords = [
      "BALANCE DALAM IDR",
      "OS",
      "OUTSTANDING",
      "BAK SO",
      "SALDO",
      "SISA PLAFON",
      "BAK",
      "BAK_SO",
      "IDR",
      "BALANCE",
      "SISA",
      "POKOK",
  ]
  for col in df.columns:
    col_upper = str(col).upper()
    if any(keyword in col_upper for keyword in possible_keywords):
      return col
  return None


def find_rate_column(df):
  possible_keywords = ["RATE", "SUKU BUNGA", "BUNGA", "IR", "INTEREST"]
  for col in df.columns:
    col_upper = str(col).upper()
    if any(keyword in col_upper for keyword in possible_keywords):
      return col
  return None


@st.cache_data(show_spinner=False)
def process_uploaded_file_cached(file_bytes, file_name):
  df_raw = pd.read_excel(io.BytesIO(file_bytes), header=None)
  headers = df_raw.iloc[3].values
  df = df_raw.iloc[4:].copy()
  df = df.iloc[:, 1:]
  headers = headers[1:]
  df.columns = headers

  if "PLAFON" in df.columns:
    df["PLAFON"] = df["PLAFON"].apply(parse_numeric)

  os_col_name = find_os_column(df)
  if os_col_name:
    df["OS_COL_DETECTED"] = os_col_name
    df["OUTSTANDING_AMT"] = df[os_col_name].apply(parse_numeric)
  else:
    df["OUTSTANDING_AMT"] = 0.0

  rate_col_name = find_rate_column(df)
  if rate_col_name:
    df["RATE_COL_DETECTED"] = rate_col_name
    df["RATE_CLEAN"] = df[rate_col_name].apply(parse_rate)
  else:
    df["RATE_CLEAN"] = "N/A"

  if "TGL JATUH TEMPO" in df.columns:
    df["TGL_JATUH_TEMPO_DT"] = pd.to_datetime(
        df["TGL JATUH TEMPO"], format="%d/%m/%Y", errors="coerce"
    )

  if "NOMOR_REKENING" in df.columns:
    df["REK_CLEAN"] = (
        df["NOMOR_REKENING"]
        .astype(str)
        .apply(lambda x: "".join(filter(str.isdigit, x)))
    )

  df["STATUS_KOL"] = df.apply(get_kolektibilitas, axis=1)

  if "TGL_JATUH_TEMPO_DT" in df.columns:
    df["TAHUN_JATUH_TEMPO"] = df["TGL_JATUH_TEMPO_DT"].dt.year
    df["BULAN_JATUH_TEMPO"] = df["TGL_JATUH_TEMPO_DT"].dt.month

    bulan_nama_map = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember",
    }
    df["BULAN_NAMA"] = df["BULAN_JATUH_TEMPO"].map(bulan_nama_map)

  return df


def process_uploaded_file(uploaded_file):
  start_time = time.time()
  with st.spinner(
      "⏳ Sedang memproses file LW Anda... Mohon tunggu sebentar."
  ):
    file_bytes = uploaded_file.getvalue()
    df = process_uploaded_file_cached(file_bytes, uploaded_file.name)
    elapsed_time = time.time() - start_time
    st.toast(
        f"✅ File berhasil dimuat dalam waktu {elapsed_time:.2f} detik!"
        f" ({len(df):,} baris data)",
        icon="⚡",
    )
    return df


# ================= FUNGSI FORMAT RUPIAH DI319 =================
def format_rupiah(val):
  try:
    if pd.isna(val) or val == "":
      return "Rp 0"
    if isinstance(val, (int, float)):
      return f"Rp {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    val_str = str(val).replace(",", "").strip()
    val_float = float(val_str)
    return (
        f"Rp {val_float:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
  except:
    return str(val)


@st.cache_data(show_spinner="Sedang memproses file Excel DI319...")
def load_excel_data_di319(uploaded_file):
  df = pd.read_excel(uploaded_file)
  if "short name" in df.columns:
    df["short name"] = df["short name"].astype(str).str.strip()
  if "balance" in df.columns:
    df["balance"] = pd.to_numeric(
        df["balance"].astype(str).str.replace(",", ""), errors="coerce"
    ).fillna(0)
  return df


# ================= LOGIKA UTAMA BERDASARKAN PILIHAN MODUL =================
if app_mode == "📈 LW321 Analyzer (Loan Debitur)":
  st.sidebar.header("📁 Upload File LW")
  uploaded_file_lw = st.sidebar.file_uploader(
      "Pilih file Excel LW (.xlsx):", type=["xlsx"], key="lw_uploader"
  )

  if uploaded_file_lw is not None:
    df = process_uploaded_file(uploaded_file_lw)

    if df is not None:
      detected_kanca = "Kantor Cabang Tidak Terdeteksi"
      if "KANCA" in df.columns:
        valid_kanca_list = df["KANCA"].dropna().unique()
        if len(valid_kanca_list) > 0:
          detected_kanca = str(valid_kanca_list[0])

      if "TGL_JATUH_TEMPO_DT" in df.columns:
        current_date = pd.Timestamp(datetime.now().date())
        future_limit_date = current_date + pd.DateOffset(months=5)
        count_tempo = len(
            df[
                (df["TGL_JATUH_TEMPO_DT"].notna())
                & (df["TGL_JATUH_TEMPO_DT"] >= current_date)
                & (df["TGL_JATUH_TEMPO_DT"] <= future_limit_date)
            ]
        )
      else:
        count_tempo = 0

      os_col_check = find_os_column(df)
      if os_col_check:
        count_lunas = len(df[df["OUTSTANDING_AMT"] <= 1.0])
      else:
        count_lunas = 0

      col_title, col_help_btn = st.columns([5, 1])
      with col_title:
        st.title("🔍 Aplikasi Penganalisa & Pencari Data Loan Debitur (LW321)")
        st.markdown(
            f"🏢 **Kantor Cabang (Kanca):** `{detected_kanca}`"
            " &nbsp;|&nbsp; **Developer:** Prima & Primarya"
        )

      with col_help_btn:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        button_label = (
            "❌ Tutup Bantuan"
            if st.session_state["show_help"]
            else "💡 Bantuan (Help)"
        )
        st.button(
            button_label, on_click=toggle_help, use_container_width=True
        )

      if not st.session_state["notification_read"]:
        with st.chat_message("assistant", avatar="🤖"):
          st.markdown(
              f"Halo **{active_uname}**! File LW untuk **{detected_kanca}**"
              " berhasil dianalisis dengan baik."
          )
          if count_tempo > 0 or count_lunas > 0:
            st.markdown(
                f"💡 *Hei, ada informasi penting nih:* Ditemukan"
                f" **{count_tempo:,} nasabah** yang akan jatuh tempo dalam 5"
                f" bulan ke depan dan **{count_lunas:,} nasabah** yang sudah"
                " lunas. Mari kita cek terlebih dahulu pada tab dengan badge"
                " notifikasi di bawah!"
            )
          else:
            st.markdown(
                "🚀 Semua data sudah siap dieksplorasi. Silakan gunakan menu"
                " filter di sebelah kiri atau cari debitur secara instan."
            )

      if st.session_state["show_help"]:
        st.info("""
                ### 📖 Panduan Lengkap Fitur Aplikasi LW321
                **Developer:** Prima & Primarya  
                Aplikasi ini dirancang untuk memudahkan Anda menganalisis, menyaring, memantau, dan mengelola data debitur dari file laporan LW. Berikut adalah penjelasan setiap fitur yang tersedia:

                1. **📁 Upload File LW (Sidebar Kiri)**
                    - Unggah file laporan Excel (`.xlsx`) Anda melalui menu di sebelah kiri. Sistem akan otomatis mendeteksi kolom penting seperti Plafon, Outstanding/Baki Debet, Suku Bunga, Tanggal Jatuh Tempo, dan Kolektibilitas.

                2. **🔍 Tab 1: Cari & Analisis Data**
                    - **Filter Pencarian Canggih:** Cari debitur berdasarkan Nama atau Nomor Rekening secara fleksibel.
                    - **Filter Tipe Pinjaman & Wilayah:** Saring data berdasarkan Tipe Pinjaman (`DESCRIPTION`), Kantor Cabang (Kanca), dan Unit Kerja (UKER).
                    - **Filter Plafon & Kol:** Batasi nominal plafon minimum/maksimum dan pilih status kolektibilitas (Kol 1 s.d. Kol 5).
                    - **Tabel Interaktif & Rincian Debitur:** Klik salah satu baris data pada tabel untuk menampilkan **Rincian Lengkap Debitur** di bagian bawah.
                    - **Simpan ke List Kustom:** Tambahkan debitur yang dipilih ke dalam list kategori buatan Anda sendiri.

                3. **📅 Tab 2: Jatuh Tempo & Sudah Lunas**
                    - **Jatuh Tempo (5 Bulan ke Depan & Filter Kustom Bulan/Tahun):** Memantau otomatis daftar nasabah yang akan jatuh tempo berdasarkan pilihan bulan dan rentang tahun secara bebas, dilengkapi reminder pengecekan SLIK dan rekening koran.
                    - **Checkbox Rincian:** Klik/centang baris data nasabah di tabel jatuh tempo untuk melihat rincian lengkapnya secara instan.
                    - **Debitur Sudah Lunas:** Menampilkan daftar nasabah dengan sisa saldo/outstanding ($\le$ Rp 1).

                4. **📁 Tab 3: Kelola List Simpanan Nasabah**
                    - Tempat mengelola list kustom debitur yang telah Anda buat sebelumnya.
                """)

      tab1_label = "🔍 Cari & Analisis Data"
      badge_count = count_tempo + count_lunas
      if badge_count > 0 and not st.session_state["notification_read"]:
        tab2_label = f"📅 Jatuh Tempo & Sudah Lunas 🔴 {badge_count}"
      else:
        tab2_label = "📅 Jatuh Tempo & Sudah Lunas"
      tab3_label = "📁 Kelola List Simpanan Nasabah"

      tab_cari, tab_tempo_lunas, tab_list = st.tabs(
          [tab1_label, tab2_label, tab3_label]
      )

      with tab_cari:
        st.session_state["notification_read"] = True

        st.sidebar.markdown("---")
        st.sidebar.header("🎛️ Filter & Kriteria Pencarian")

        keyword = st.sidebar.text_input(
            "Cari Nama Debitur / No Rekening:",
            "",
            placeholder="Ketik nama atau no rek...",
        )

        kanca_list = (
            ["Semua Kanca"] + sorted(df["KANCA"].dropna().unique().tolist())
            if "KANCA" in df.columns
            else ["Semua Kanca"]
        )
        selected_kanca = st.sidebar.selectbox(
            "Pilih Kantor Cabang (Kanca)", kanca_list
        )

        if selected_kanca != "Semua Kanca" and "UKER" in df.columns:
          uker_list = ["Semua UKER"] + sorted(
              df[df["KANCA"] == selected_kanca]["UKER"].dropna().unique().tolist()
          )
        else:
          uker_list = (
              ["Semua UKER"]
              + sorted(df["UKER"].dropna().unique().tolist())
              if "UKER" in df.columns
              else ["Semua UKER"]
          )

        selected_uker = st.sidebar.selectbox(
            "Pilih Unit Kerja (UKER)", uker_list
        )

        if "DESCRIPTION" in df.columns:
          desc_list = ["Semua Tipe Pinjaman"] + sorted(
              df["DESCRIPTION"].dropna().unique().tolist()
          )
          selected_desc = st.sidebar.selectbox(
              "Pilih Tipe Pinjaman (Description)", desc_list
          )
        else:
          selected_desc = "Semua Tipe Pinjaman"

        st.sidebar.markdown("---")
        st.sidebar.subheader("💰 Filter Plafon (Rupiah)")
        use_plafon_filter = st.sidebar.checkbox("Aktifkan Filter Plafon")

        min_input, max_input = 0, 0
        if use_plafon_filter:
          min_input = st.sidebar.number_input(
              "Plafon Minimum (Rp):", min_value=0, value=0, step=1000000
          )
          max_input = st.sidebar.number_input(
              "Plafon Maksimum (Rp):",
              min_value=0,
              value=(
                  int(df["PLAFON"].max())
                  if "PLAFON" in df.columns
                  else 1000000000
              ),
              step=1000000,
          )

        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Status Kolektibilitas")
        kol_options = [
            "Semua Kol",
            "Kol 1 (Lancar)",
            "Kol 2 (DPK)",
            "Kol 3 (Kurang Lancar)",
            "Kol 4 (Diragukan)",
            "Kol 5 (Macet)",
        ]
        selected_kol = st.sidebar.selectbox("Pilih Kol:", kol_options)

        if "TAHUN_JATUH_TEMPO" in df.columns:
          st.sidebar.markdown("---")
          st.sidebar.subheader("📅 Tahun Jatuh Tempo")
          tahun_list = sorted([
              int(x)
              for x in df["TAHUN_JATUH_TEMPO"].dropna().unique().tolist()
              if x > 2000
          ])
          selected_tahun = st.sidebar.multiselect(
              "Pilih Tahun Jatuh Tempo:", tahun_list, default=[]
          )
        else:
          selected_tahun = []

        filtered_df = df.copy()

        if keyword.strip():
          keyword_clean = "".join(filter(str.isdigit, keyword))
          mask = (
              filtered_df["NAMA_DEBITUR"]
              .astype(str)
              .str.contains(keyword, case=False, na=False)
              | filtered_df["NOMOR_REKENING"]
              .astype(str)
              .str.contains(keyword, case=False, na=False)
          )
          if keyword_clean:
            mask = mask | filtered_df["REK_CLEAN"].str.contains(
                keyword_clean, na=False
            )
          filtered_df = filtered_df[mask]

        if selected_kanca != "Semua Kanca":
          filtered_df = filtered_df[filtered_df["KANCA"] == selected_kanca]
        if selected_uker != "Semua UKER":
          filtered_df = filtered_df[filtered_df["UKER"] == selected_uker]
        if (
            selected_desc != "Semua Tipe Pinjaman"
            and "DESCRIPTION" in filtered_df.columns
        ):
          filtered_df = filtered_df[
              filtered_df["DESCRIPTION"] == selected_desc
          ]

        if use_plafon_filter and "PLAFON" in filtered_df.columns:
          filtered_df = filtered_df[
              (filtered_df["PLAFON"] >= min_input)
              & (filtered_df["PLAFON"] <= max_input)
          ]

        if selected_kol != "Semua Kol":
          filtered_df = filtered_df[
              filtered_df["STATUS_KOL"] == selected_kol
          ]

        if selected_tahun and "TAHUN_JATUH_TEMPO" in filtered_df.columns:
          filtered_df = filtered_df[
              filtered_df["TAHUN_JATUH_TEMPO"].isin(selected_tahun)
          ]

        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        with col_info1:
          st.metric("Total Seluruh Data", f"{len(df):,} baris")
        with col_info2:
          st.metric("Data Sesuai Filter", f"{len(filtered_df):,} baris")
        with col_info3:
          total_plafon_filtered = (
              filtered_df["PLAFON"].sum() if "PLAFON" in filtered_df.columns else 0
          )
          st.metric(
              "Total Plafon (Filter)", f"Rp {total_plafon_filtered:,.0f}"
          )
        with col_info4:
          total_os_filtered = (
              filtered_df["OUTSTANDING_AMT"].sum()
              if "OUTSTANDING_AMT" in filtered_df.columns
              else 0
          )
          st.metric(
              "Total Tunggakan Pokok (Filter)", f"Rp {total_os_filtered:,.0f}"
          )

        st.markdown("---")

        if not filtered_df.empty:
          st.success(f"Ditemukan **{len(filtered_df)}** data debitur yang sesuai.")
          st.subheader(
              "📋 Daftar Debitur (Klik Baris Tabel untuk Melihat Rincian)"
          )
          table_view = filtered_df.copy()
          if "NOMOR_REKENING" in table_view.columns:
            table_view["NOMOR_REKENING"] = table_view["NOMOR_REKENING"].apply(
                format_no_rekening
            )
          if "PLAFON" in table_view.columns:
            table_view["PLAFON"] = table_view["PLAFON"].apply(
                lambda x: f"Rp {x:,.0f}"
            )

          os_col_name = find_os_column(table_view)
          if os_col_name and os_col_name in table_view.columns:
            table_view[os_col_name] = table_view["OUTSTANDING_AMT"].apply(
                lambda x: f"Rp {x:,.0f}"
            )

          display_cols = [
              col
              for col in [
                  "NOMOR_REKENING",
                  "NAMA_DEBITUR",
                  "DESCRIPTION",
                  "KANCA",
                  "UKER",
                  "PLAFON",
                  os_col_name if os_col_name else None,
                  "STATUS_KOL",
                  "TGL JATUH TEMPO",
                  "PN PENGELOLA 1",
              ]
              if col and col in table_view.columns
          ]

          event = st.dataframe(
              table_view[display_cols],
              use_container_width=True,
              on_select="rerun",
              selection_mode="single-row",
              key="table_debitur_selection",
          )

          selected_rows = event.get("selection", {}).get("rows", [])
          selected_debitur_idx = None
          if selected_rows:
            clicked_row_position = selected_rows[0]
            selected_debitur_idx = filtered_df.index[clicked_row_position]

          st.markdown("---")
          st.subheader("📥 Aksi & Rincian Debitur Terpilih")

          if (
              selected_debitur_idx is not None
              and selected_debitur_idx in filtered_df.index
          ):
            row_selected = filtered_df.loc[selected_debitur_idx]
            st.info(
                f"Debitur Terpilih dari Tabel:"
                f" **{row_selected.get('NAMA_DEBITUR')}** (Rek:"
                f" {format_no_rekening(row_selected.get('NOMOR_REKENING'))})"
            )
          else:
            st.info(
                "💡 **Tips:** Klik salah satu baris pada tabel di atas untuk"
                " melihat rincian lengkap debitur."
            )

          col_input, col_btn = st.columns([3, 1])
          with col_input:
            new_list_name = st.text_input(
                "Nama List Baru atau Pilih yang Sudah Ada:",
                placeholder=(
                    "Contoh: Debitur Macet Prioritas / Kunjungan Bulan Ini"
                ),
                key="input_nama_list",
            )

          existing_lists = list(st.session_state["custom_lists"].keys())
          chosen_existing_list = st.selectbox(
              "Atau masukkan ke list yang sudah ada:",
              ["-- Buat Baru / Pilih dari kolom teks --"] + existing_lists,
              key="select_existing_list",
          )

          target_list_name = (
              chosen_existing_list
              if chosen_existing_list
              != "-- Buat Baru / Pilih dari kolom teks --"
              else new_list_name
          )

          if st.button("➕ Tambahkan Debitur Terpilih ke List"):
            if selected_debitur_idx is None:
              st.warning(
                  "Silakan klik salah satu baris di tabel daftar debitur"
                  " terlebih dahulu!"
              )
            elif not target_list_name.strip():
              st.warning("Nama list tidak boleh kosong!")
            else:
              if (
                  target_list_name
                  not in st.session_state["custom_lists"]
              ):
                st.session_state["custom_lists"][target_list_name] = []

              row_data = filtered_df.loc[selected_debitur_idx].to_dict()
              rek_to_add = row_data.get("NOMOR_REKENING")
              already_exists = any(
                  item.get("NOMOR_REKENING") == rek_to_add
                  for item in st.session_state["custom_lists"][
                      target_list_name
                  ]
              )

              if already_exists:
                st.warning(
                    "Debitur ini sudah ada di dalam list"
                    f" '{target_list_name}'!"
                )
              else:
                st.session_state["custom_lists"][target_list_name].append(
                    row_data
                )
                st.success(
                    "Berhasil menambahkan"
                    f" **{row_data.get('NAMA_DEBITUR')}** ke dalam list"
                    f" **'{target_list_name}'**!"
                )

          if (
              selected_debitur_idx is not None
              and selected_debitur_idx in filtered_df.index
          ):
            row = filtered_df.loc[selected_debitur_idx]
            st.markdown("#### Rincian Lengkap Data Debitur")

            os_val = row.get("OUTSTANDING_AMT", 0)
            rate_val = row.get("RATE_CLEAN", "N/A")

            dcol1, dcol2, dcol3 = st.columns(3)
            with dcol1:
              st.metric("1. Nama Debitur", row.get("NAMA_DEBITUR", "N/A"))
              st.metric(
                  "2. Nomor Rekening",
                  format_no_rekening(row.get("NOMOR_REKENING", "N/A")),
              )
              st.metric("3. Plafon", f"Rp {row.get('PLAFON', 0):,.0f}")
              st.metric(
                  "4. Balance dalam IDR (Baki Debet)",
                  f"Rp {os_val:,.0f}" if pd.notna(os_val) else "Rp 0",
              )
            with dcol2:
              st.metric("5. Status Kolektibilitas", row.get("STATUS_KOL", "N/A"))
              st.metric(
                  "6. Tanggal Jatuh Tempo", row.get("TGL JATUH TEMPO", "N/A")
              )
              st.metric("7. Jangka Waktu", row.get("JANGKA WAKTU", "N/A"))
              st.metric(
                  "8. Suku Bunga",
                  f"{rate_val}%" if rate_val != "N/A" else "N/A",
              )
            with dcol3:
              st.metric("9. Unit Kerja (UKER)", row.get("UKER", "N/A"))
              st.metric("10. Jenis Pinjaman", row.get("DESCRIPTION", "N/A"))
              st.metric("11. Pengelola", row.get("PN PENGELOLA 1", "N/A"))
              st.metric("12. Segmen", row.get("DESC SEGMEN LV1", "N/A"))

        else:
          st.warning("Tidak ada data yang cocok dengan kombinasi filter tersebut.")

      with tab_tempo_lunas:
        st.session_state["notification_read"] = True
        st.header("📅 Monitoring Jatuh Tempo & Debitur Lunas")

        sub_tab_tempo, sub_tab_lunas = st.tabs(
            ["⏳ Debitur Jatuh Tempo", "✅ Debitur Sudah Lunas (OS = 0)"]
        )
        os_col_name = find_os_column(df)

        with sub_tab_tempo:
          st.subheader("Daftar Nasabah Jatuh Tempo")
          st.warning("""⚠️ **Reminder Penting untuk RM:** 
                    1. Wajib **cek SLIK** terlebih dahulu. Jika status kolektibilitas nasabah berada di **Kolek 2 sampai dengan Kolek 5 (Kol 2-5), langsung SKIP saja**!
                    2. Cek transaksi nasabah melalui **rekening koran** sebelum menawarkan penawaran kredit baru untuk memastikan apakah nasabah memenuhi syarat atau tidak.""")

          if "TGL_JATUH_TEMPO_DT" in df.columns:
            tempo_mode = st.radio(
                "Pilih Mode Filter Jatuh Tempo:",
                [
                    "Jatuh Tempo 5 Bulan ke Depan",
                    "Filter Bebas Bulan & Rentang Tahun",
                ],
                horizontal=True,
            )

            df_tempo = df[df["TGL_JATUH_TEMPO_DT"].notna()].copy()

            if tempo_mode == "Jatuh Tempo 5 Bulan ke Depan":
              current_date = pd.Timestamp(datetime.now().date())
              future_limit_date = current_date + pd.DateOffset(months=5)
              df_tempo = df_tempo[
                  (df_tempo["TGL_JATUH_TEMPO_DT"] >= current_date)
                  & (df_tempo["TGL_JATUH_TEMPO_DT"] <= future_limit_date)
              ]
            else:
              col_m, col_y1, col_y2 = st.columns(3)

              urutan_bulan = [
                  "Januari",
                  "Februari",
                  "Maret",
                  "April",
                  "Mei",
                  "Juni",
                  "Juli",
                  "Agustus",
                  "September",
                  "Oktober",
                  "November",
                  "Desember",
              ]
              available_months = [
                  b
                  for b in urutan_bulan
                  if b in df_tempo["BULAN_NAMA"].dropna().unique().tolist()
              ]
              available_years = sorted([
                  int(y)
                  for y in df_tempo["TAHUN_JATUH_TEMPO"]
                  .dropna()
                  .unique()
                  .tolist()
                  if y > 2000
              ])

              with col_m:
                selected_months = st.multiselect(
                    "Pilih Bulan:",
                    available_months,
                    default=available_months[:1] if available_months else [],
                    key="tempo_m_select",
                )
              with col_y1:
                min_year = st.selectbox(
                    "Tahun Mulai:",
                    available_years,
                    index=0 if available_years else 0,
                    key="tempo_y1_select",
                )
              with col_y2:
                max_year = st.selectbox(
                    "Tahun Selesai:",
                    available_years,
                    index=len(available_years) - 1 if available_years else 0,
                    key="tempo_y2_select",
                )

              if selected_months:
                df_tempo = df_tempo[
                    (df_tempo["BULAN_NAMA"].isin(selected_months))
                    & (df_tempo["TAHUN_JATUH_TEMPO"] >= min_year)
                    & (df_tempo["TAHUN_JATUH_TEMPO"] <= max_year)
                ]
              else:
                df_tempo = df_tempo.iloc[0:0]

            with st.expander(
                "🔍 Filter Tambahan Berdasarkan Plafon (Jatuh Tempo)",
                expanded=False,
            ):
              use_tempo_plafon = st.checkbox(
                  "Aktifkan Filter Plafon di Jatuh Tempo", key="chk_tempo_plafon"
              )
              t_min_plafon, t_max_plafon = 0.0, (
                  float(df["PLAFON"].max())
                  if "PLAFON" in df.columns
                  else 1000000000.0
              )
              if use_tempo_plafon:
                col_fp1, col_fp2 = st.columns(2)
                with col_fp1:
                  t_min_plafon = st.number_input(
                      "Plafon Minimum (Rp):",
                      min_value=0.0,
                      value=0.0,
                      step=1000000.0,
                      key="t_min",
                  )
                with col_fp2:
                  t_max_plafon = st.number_input(
                      "Plafon Maksimum (Rp):",
                      min_value=0.0,
                      value=t_max_plafon,
                      step=1000000.0,
                      key="t_max",
                  )

                if "PLAFON" in df_tempo.columns:
                  df_tempo = df_tempo[
                      (df_tempo["PLAFON"] >= t_min_plafon)
                      & (df_tempo["PLAFON"] <= t_max_plafon)
                  ]

            st.info(
                f"Ditemukan **{len(df_tempo):,}** nasabah yang memenuhi"
                " kriteria filter jatuh tempo."
            )

            if not df_tempo.empty:
              view_tempo = df_tempo.copy()
              view_tempo["NOMOR_REKENING"] = view_tempo["NOMOR_REKENING"].apply(
                  format_no_rekening
              )
              view_tempo["PLAFON"] = view_tempo["PLAFON"].apply(
                  lambda x: f"Rp {x:,.0f}"
              )
              if os_col_name and os_col_name in view_tempo.columns:
                view_tempo[os_col_name] = view_tempo["OUTSTANDING_AMT"].apply(
                    lambda x: f"Rp {x:,.0f}"
                )

              cols_t = [
                  c
                  for c in [
                      "NOMOR_REKENING",
                      "NAMA_DEBITUR",
                      "KANCA",
                      "UKER",
                      "PLAFON",
                      os_col_name if os_col_name else None,
                      "TGL JATUH TEMPO",
                      "STATUS_KOL",
                      "PN PENGELOLA 1",
                  ]
                  if c and c in view_tempo.columns
              ]

              event_tempo = st.dataframe(
                  view_tempo[cols_t],
                  use_container_width=True,
                  on_select="rerun",
                  selection_mode="single-row",
                  key="table_tempo_selection",
              )

              selected_tempo_rows = (
                  event_tempo.get("selection", {}).get("rows", [])
              )
              selected_tempo_idx = None
              if selected_tempo_rows:
                clicked_t_pos = selected_tempo_rows[0]
                selected_tempo_idx = df_tempo.index[clicked_t_pos]

              if (
                  selected_tempo_idx is not None
                  and selected_tempo_idx in df_tempo.index
              ):
                row_t = df_tempo.loc[selected_tempo_idx]
                st.markdown("---")
                st.markdown(
                    f"#### 🔍 Rincian Lengkap Debitur Jatuh Tempo:"
                    f" **{row_t.get('NAMA_DEBITUR')}**"
                )

                os_val_t = row_t.get("OUTSTANDING_AMT", 0)
                rate_val_t = row_t.get("RATE_CLEAN", "N/A")

                dtcol1, dtcol2, dtcol3 = st.columns(3)
                with dtcol1:
                  st.metric("1. Nama Debitur", row_t.get("NAMA_DEBITUR", "N/A"))
                  st.metric(
                      "2. Nomor Rekening",
                      format_no_rekening(row_t.get("NOMOR_REKENING", "N/A")),
                  )
                  st.metric(
                      "3. Plafon", f"Rp {row_t.get('PLAFON', 0):,.0f}"
                  )
                  st.metric(
                      "4. Balance (Baki Debet)",
                      f"Rp {os_val_t:,.0f}" if pd.notna(os_val_t) else "Rp 0",
                  )
                with dtcol2:
                  st.metric(
                      "5. Status Kolektibilitas",
                      row_t.get("STATUS_KOL", "N/A"),
                  )
                  st.metric(
                      "6. Tanggal Jatuh Tempo",
                      row_t.get("TGL JATUH TEMPO", "N/A"),
                  )
                  st.metric("7. Jangka Waktu", row_t.get("JANGKA WAKTU", "N/A"))
                  st.metric(
                      "8. Suku Bunga",
                      f"{rate_val_t}%" if rate_val_t != "N/A" else "N/A",
                  )
                with dtcol3:
                  st.metric("9. Unit Kerja (UKER)", row_t.get("UKER", "N/A"))
                  st.metric(
                      "10. Jenis Pinjaman", row_t.get("DESCRIPTION", "N/A")
                  )
                  st.metric("11. Pengelola", row_t.get("PN PENGELOLA 1", "N/A"))
                  st.metric("12. Segmen", row_t.get("DESC SEGMEN LV1", "N/A"))
              else:
                st.info(
                    "💡 **Tips:** Klik salah satu baris pada tabel di atas"
                    " untuk melihat rincian lengkap debitur jatuh tempo."
                )

              st.markdown("---")
              output_tempo = io.BytesIO()
              with pd.ExcelWriter(output_tempo, engine="openpyxl") as writer:
                drop_cols = [
                    col
                    for col in [
                        "REK_CLEAN",
                        "TAHUN_JATUH_TEMPO",
                        "BULAN_JATUH_TEMPO",
                        "BULAN_NAMA",
                        "TGL_JATUH_TEMPO_DT",
                        "OS_COL_DETECTED",
                        "RATE_COL_DETECTED",
                        "OUTSTANDING_AMT",
                        "RATE_CLEAN",
                    ]
                    if col in df_tempo.columns
                ]
                export_tempo_df = df_tempo.drop(columns=drop_cols)
                export_tempo_df.to_excel(
                    writer, index=False, sheet_name="Jatuh Tempo"
                )

              st.download_button(
                  label="📊 Download Daftar Jatuh Tempo (.xlsx)",
                  data=output_tempo.getvalue(),
                  file_name="Debitur_Jatuh_Tempo.xlsx",
                  mime=(
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  ),
              )
          else:
            st.warning(
                "Kolom tanggal jatuh tempo tidak ditemukan di dalam file Excel."
            )

        with sub_tab_lunas:
          st.subheader(
              "Daftar Nasabah yang Sudah Lunas (Tunggakan Pokok / Balance"
              " $\le$ 0)"
          )
          if os_col_name:
            df_lunas = df[df["OUTSTANDING_AMT"] <= 1.0].copy()
            st.success(
                f"Ditemukan **{len(df_lunas):,}** nasabah yang statusnya sudah"
                " lunas."
            )

            if not df_lunas.empty:
              view_lunas = df_lunas.copy()
              view_lunas["NOMOR_REKENING"] = view_lunas["NOMOR_REKENING"].apply(
                  format_no_rekening
              )
              view_lunas["PLAFON"] = view_lunas["PLAFON"].apply(
                  lambda x: f"Rp {x:,.0f}"
              )
              view_lunas[os_col_name] = view_lunas["OUTSTANDING_AMT"].apply(
                  lambda x: f"Rp {x:,.0f}"
              )

              cols_l = [
                  c
                  for c in [
                      "NOMOR_REKENING",
                      "NAMA_DEBITUR",
                      "KANCA",
                      "UKER",
                      "PLAFON",
                      os_col_name,
                      "TGL JATUH TEMPO",
                      "STATUS_KOL",
                      "PN PENGELOLA 1",
                  ]
                  if c and c in view_lunas.columns
              ]
              st.dataframe(view_lunas[cols_l], use_container_width=True)

              output_lunas = io.BytesIO()
              with pd.ExcelWriter(output_lunas, engine="openpyxl") as writer:
                drop_cols = [
                    col
                    for col in [
                        "REK_CLEAN",
                        "TAHUN_JATUH_TEMPO",
                        "BULAN_JATUH_TEMPO",
                        "BULAN_NAMA",
                        "TGL_JATUH_TEMPO_DT",
                        "OS_COL_DETECTED",
                        "RATE_COL_DETECTED",
                        "OUTSTANDING_AMT",
                        "RATE_CLEAN",
                    ]
                    if col in df_lunas.columns
                ]
                export_lunas_df = df_lunas.drop(columns=drop_cols)
                export_lunas_df.to_excel(
                    writer, index=False, sheet_name="Debitur Lunas"
                )

              st.download_button(
                  label="📊 Download Daftar Debitur Lunas (.xlsx)",
                  data=output_lunas.getvalue(),
                  file_name="Daftar_Debitur_Lunas.xlsx",
                  mime=(
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  ),
              )
          else:
            st.warning(
                "Kolom Sisa Saldo / Outstanding tidak terdeteksi otomatis."
            )

      with tab_list:
        st.session_state["notification_read"] = True
        st.header("📁 Kelola & Export List Simpanan Debitur")

        if not st.session_state["custom_lists"]:
          st.info(
              "Belum ada list yang Anda buat. Silakan cari debitur di tab"
              " **'Cari & Analisis Data'** lalu tambahkan ke list."
          )
        else:
          selected_manage_list = st.selectbox(
              "Pilih List yang Ingin Dikelola:",
              list(st.session_state["custom_lists"].keys()),
              key="manage_list_box",
          )

          if selected_manage_list:
            list_data = st.session_state["custom_lists"][selected_manage_list]
            st.write(
                f"Jumlah debitur dalam list **'{selected_manage_list}'**:"
                f" **{len(list_data)}** nasabah"
            )

            if list_data:
              df_list = pd.DataFrame(list_data)
              df_list_view = df_list.copy()
              if "NOMOR_REKENING" in df_list_view.columns:
                df_list_view["NOMOR_REKENING"] = df_list_view[
                    "NOMOR_REKENING"
                ].apply(format_no_rekening)
              if "PLAFON" in df_list_view.columns:
                df_list_view["PLAFON"] = df_list_view["PLAFON"].apply(
                    lambda x: f"Rp {x:,.0f}" if pd.notna(x) else "Rp 0"
                )

              os_col_name = find_os_column(df_list_view)
              if os_col_name and os_col_name in df_list_view.columns:
                df_list_view[os_col_name] = df_list_view[
                    "OUTSTANDING_AMT"
                ].apply(lambda x: f"Rp {x:,.0f}")

              list_display_cols = [
                  c
                  for c in [
                      "NOMOR_REKENING",
                      "NAMA_DEBITUR",
                      "DESCRIPTION",
                      "KANCA",
                      "UKER",
                      "PLAFON",
                      os_col_name if os_col_name else None,
                      "STATUS_KOL",
                      "TGL JATUH TEMPO",
                      "PN PENGELOLA 1",
                  ]
                  if c and c in df_list_view.columns
              ]
              st.dataframe(
                  df_list_view[list_display_cols], use_container_width=True
              )

              col_del1, col_del2 = st.columns(2)
              with col_del1:
                if st.button("🗑️ Hapus List Ini"):
                  del st.session_state["custom_lists"][selected_manage_list]
                  st.success(f"List '{selected_manage_list}' berhasil dihapus.")
                  st.rerun()

              st.markdown("---")
              st.subheader("📥 Download / Export ke File Excel")

              output = io.BytesIO()
              with pd.ExcelWriter(output, engine="openpyxl") as writer:
                drop_cols = [
                    col
                    for col in [
                        "REK_CLEAN",
                        "TAHUN_JATUH_TEMPO",
                        "BULAN_JATUH_TEMPO",
                        "BULAN_NAMA",
                        "TGL_JATUH_TEMPO_DT",
                        "OS_COL_DETECTED",
                        "RATE_COL_DETECTED",
                        "OUTSTANDING_AMT",
                        "RATE_CLEAN",
                    ]
                    if col in df_list.columns
                ]
                export_df = df_list.drop(columns=drop_cols)
                export_df.to_excel(
                    writer, index=False, sheet_name="List Debitur"
                )

              processed_data = output.getvalue()
              st.download_button(
                  label=f"📊 Download List '{selected_manage_list}' (.xlsx)",
                  data=processed_data,
                  file_name=(
                      "List_Debitur_"
                      f"{selected_manage_list.replace(' ', '_')}.xlsx"
                  ),
                  mime=(
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  ),
              )
  else:
    st.info(
        "👆 Silakan **upload file Excel LW** Anda melalui menu di sebelah kiri"
        " (sidebar) untuk mulai menggunakan aplikasi LW321."
    )

elif app_mode == "🏦 DI319 Analyzer (Pipeline & Dana)":
  st.title("🏦 DI319 Analyzer")
  st.write(
      "**Developer:** Prima & Primarya | Selamat datang,"
      f" **{active_uname.capitalize()}** | Pipeline & Kunjungan Nasabah"
  )

  uploaded_file_di319 = st.file_uploader(
      "Pilih atau Seret File Excel DI319 di sini",
      type=["xlsx", "xls"],
      key="di319_uploader",
  )

  if uploaded_file_di319 is not None:
    try:
      df_di319 = load_excel_data_di319(uploaded_file_di319)
      st.success(f"File berhasil dimuat! Total baris: {len(df_di319):,}")

      if "short name" not in df_di319.columns:
        st.error("Kolom 'short name' tidak ditemukan di dalam file.")
      else:
        st.markdown('<div class="sticky-filter-container">', unsafe_allow_html=True)
        st.markdown(
            "<p"
            " style='font-size:13px; font-weight:600; color:#374151;"
            " margin-bottom:8px;'>🎛️ FILTER DATA NASABAH</p>",
            unsafe_allow_html=True,
        )

        col_f1, col_f2, col_f3, col_f4, col_f5, col_f6 = st.columns([
            1.2,
            1.2,
            1.2,
            1.3,
            1.3,
            1.0,
        ])

        with col_f1:
          uker_list = (
              ["Semua"]
              + sorted(df_di319["uker code"].dropna().unique().tolist())
              if "uker code" in df_di319.columns
              else ["Semua"]
          )
          selected_uker = st.selectbox("Uker:", uker_list)

        with col_f2:
          prod_list = (
              ["Semua"]
              + sorted(df_di319["prod code"].dropna().unique().tolist())
              if "prod code" in df_di319.columns
              else ["Semua"]
          )
          selected_prod = st.selectbox("Produk:", prod_list)

        with col_f3:
          curr_list = (
              ["Semua"]
              + sorted(df_di319["curr code"].dropna().unique().tolist())
              if "curr code" in df_di319.columns
              else ["Semua"]
          )
          selected_curr = st.selectbox("Valuta:", curr_list)

        with col_f4:
          min_default = (
              float(df_di319["balance"].min()) if not df_di319.empty else 0.0
          )
          min_input = st.number_input(
              "Saldo Min:", value=min_default, step=100000.0
          )

        with col_f5:
          max_default = (
              float(df_di319["balance"].max())
              if not df_di319.empty
              else 100000000.0
          )
          max_input = st.number_input(
              "Saldo Maks:", value=max_default, step=100000.0
          )

        with col_f6:
          st.markdown(
              "<div style='height: 22px;'></div>", unsafe_allow_html=True
          )
          cari_ditekan = st.button(
              "🔍 Cari", type="primary", use_container_width=True
          )

        st.markdown("</div>", unsafe_allow_html=True)

        if selected_uker != "Semua":
          df_di319 = df_di319[df_di319["uker code"] == selected_uker]
        if selected_prod != "Semua":
          df_di319 = df_di319[df_di319["prod code"] == selected_prod]
        if selected_curr != "Semua":
          df_di319 = df_di319[df_di319["curr code"] == selected_curr]

        df_filtered_di319 = df_di319[
            (df_di319["balance"] >= min_input)
            & (df_di319["balance"] <= max_input)
        ]

        if "search_active" not in st.session_state:
          st.session_state.search_active = False

        if cari_ditekan:
          st.session_state.search_active = True

        tab_pencarian, tab_pipeline, tab_tidak_potensial, tab_list_kustom = (
            st.tabs([
                "🔍 Cari & Leads Database",
                "🚀 Pipeline & Kunjungan",
                "🚫 Nasabah Tidak Potensial",
                "📂 Kelola List",
            ])
        )

        with tab_pencarian:
          if st.session_state.search_active:
            st.subheader("🔍 Pencarian Nasabah")
            keyword = st.text_input(
                "Cari Nama Nasabah / No. Rekening / No. CIF:", "", key="kw_di319"
            ).strip()

            hasil = df_filtered_di319.copy()
            if keyword:
              k_upper = keyword.upper()
              mask = (
                  hasil["short name"].str.upper().str.contains(k_upper, na=False)
                  | hasil["account number"]
                  .astype(str)
                  .str.contains(k_upper, na=False)
                  | hasil["ciff no"].astype(str).str.contains(k_upper, na=False)
              )
              hasil = hasil[mask]

            rekening_tidak_potensial = [
                item["No. Rekening"]
                for item in st.session_state.tidak_potensial_list
            ]
            hasil = hasil[
                ~hasil["account number"].astype(str).isin(rekening_tidak_potensial)
            ]

            total_debitur = len(hasil)
            total_saldo_nominal = (
                hasil["balance"].sum() if not hasil.empty else 0.0
            )

            col_m1, col_m2 = st.columns(2)
            with col_m1:
              st.metric("Total Nasabah", f"{total_debitur:,} Orang")
            with col_m2:
              st.metric("Total Saldo", format_rupiah(total_saldo_nominal))

            st.markdown("---")
            st.write(
                "💡 **Klik baris pada tabel di bawah** untuk melihat rincian"
                " lengkap, menulis catatan personal, atau memindahkan nasabah."
            )

            if not hasil.empty:
              kolom_list = [
                  "short name",
                  "account number",
                  "ciff no",
                  "balance",
                  "prod code",
                  "PN PENGELOLA SINGLEPN",
              ]
              kolom_tersedia = [
                  col for col in kolom_list if col in hasil.columns
              ]
              df_list_tampil = hasil[kolom_tersedia].copy()

              if "balance" in df_list_tampil.columns:
                df_list_tampil["balance"] = df_list_tampil["balance"].apply(
                    format_rupiah
                )

              df_list_tampil = df_list_tampil.rename(columns={
                  "short name": "Nama Nasabah",
                  "account number": "No. Rekening",
                  "ciff no": "No. CIF",
                  "balance": "Saldo",
                  "prod code": "Produk",
                  "PN PENGELOLA SINGLEPN": "Pengelola Utama",
              })

              event = st.dataframe(
                  df_list_tampil,
                  use_container_width=True,
                  hide_index=True,
                  on_select="rerun",
                  selection_mode="single-row",
                  key="table_di319_select",
              )

              selected_rows = event.selection.rows
              if selected_rows:
                idx_terpilih = selected_rows[0]
                data_terpilih = hasil.iloc[idx_terpilih]
                rek_key = str(data_terpilih.get("account number", ""))

                st.markdown("---")
                st.subheader("📌 Rincian & Aksi Nasabah")
                st.info(
                    f"Terpilih: **{data_terpilih.get('short name', '-')}** (No."
                    f" Rek: {rek_key})"
                )

                st.markdown("#### 📝 Catatan Personal Nasabah")
                catatan_saat_ini = st.session_state.nasabah_catatan.get(
                    rek_key, ""
                )
                input_catatan = st.text_area(
                    "Tulis catatan khusus untuk nasabah ini (tersimpan otomatis):",
                    value=catatan_saat_ini,
                    key=f"note_{rek_key}",
                )
                if st.button("💾 Simpan Catatan Nasabah"):
                  st.session_state.nasabah_catatan[rek_key] = input_catatan
                  st.success("Catatan berhasil disimpan untuk nasabah ini!")

                st.markdown("---")

                col_aksi1, col_aksi2 = st.columns(2)

                with col_aksi1:
                  with st.form(f"form_add_pipeline_{rek_key}"):
                    st.markdown("#### 🚀 Masukkan ke Pipeline Kunjungan")
                    alasan_leads = st.text_input(
                        "Alasan / Potensi Leads:",
                        value="Potensi penempatan dana",
                    )
                    prioritas_leads = st.selectbox(
                        "Prioritas:", ["High", "Medium", "Low"]
                    )
                    rencana_tgl = st.date_input("Rencana Tanggal Kunjungan")
                    pic_rm = st.text_input(
                        "PIC / RM:",
                        value=str(
                            data_terpilih.get("PN PENGELOLA SINGLEPN", "-")
                        ),
                    )

                    if st.form_submit_button("➕ Tambah ke Pipeline"):
                      new_pipe = {
                          "Nama Nasabah": data_terpilih.get("short name", "-"),
                          "No. Rekening": rek_key,
                          "No. CIF": str(data_terpilih.get("ciff no", "-")),
                          "Uker": str(data_terpilih.get("uker code", "-")),
                          "Produk": str(data_terpilih.get("prod code", "-")),
                          "Saldo": format_rupiah(data_terpilih.get("balance", 0)),
                          "Alasan Potensi Leads": alasan_leads,
                          "Prioritas": prioritas_leads,
                          "Rencana Tanggal Kunjungan": str(rencana_tgl),
                          "Status Kunjungan": "Belum Dikunjungi",
                          "Tanggal Kunjungan": "-",
                          "Hasil Kunjungan": "-",
                          "Catatan Probing": "-",
                          "Tanggal Follow-up": "-",
                          "Status Follow-up": "-",
                          "PIC/RM": pic_rm,
                          "Keterangan": st.session_state.nasabah_catatan.get(
                              rek_key, "-"
                          ),
                      }
                      if not any(
                          p["No. Rekening"] == rek_key
                          for p in st.session_state.pipeline_leads
                      ):
                        st.session_state.pipeline_leads.append(new_pipe)
                        st.success("Berhasil masuk ke Pipeline Kunjungan!")
                      else:
                        st.warning("Nasabah ini sudah ada di dalam Pipeline.")

                with col_aksi2:
                  with st.form(f"form_tidak_potensial_{rek_key}"):
                    st.markdown("#### 🚫 Tandai Tidak Potensial")
                    alasan_tp = st.text_input(
                        "Alasan Tidak Potensial:",
                        value="Sudah pindah bank / dana tertutup",
                    )
                    if st.form_submit_button(
                        "🗑️ Pindahkan ke Daftar Tidak Potensial"
                    ):
                      item_tp = {
                          "Nama Nasabah": data_terpilih.get("short name", "-"),
                          "No. Rekening": rek_key,
                          "No. CIF": str(data_terpilih.get("ciff no", "-")),
                          "Uker": str(data_terpilih.get("uker code", "-")),
                          "Produk": str(data_terpilih.get("prod code", "-")),
                          "Saldo": format_rupiah(data_terpilih.get("balance", 0)),
                          "Alasan Tidak Potensial": alasan_tp,
                          "Catatan Terakhir": st.session_state.nasabah_catatan.get(
                              rek_key, "-"
                          ),
                      }
                      if not any(
                          t["No. Rekening"] == rek_key
                          for t in st.session_state.tidak_potensial_list
                      ):
                        st.session_state.tidak_potensial_list.append(item_tp)
                        st.session_state.pipeline_leads = [
                            p
                            for p in st.session_state.pipeline_leads
                            if p["No. Rekening"] != rek_key
                        ]
                        st.success(
                            "Nasabah dipindahkan ke 'Nasabah Tidak Potensial'"
                            " dan disembunyikan dari daftar utama!"
                        )
                        st.rerun()
                      else:
                        st.warning("Nasabah sudah ada di daftar tidak potensial.")

                mapping_lengkap = {
                    "periode": "Periode Laporan",
                    "uker code": "Kode Uker",
                    "curr code": "Kode Mata Uang",
                    "curr desc": "Keterangan Mata Uang",
                    "account number": "Nomor Rekening",
                    "ciff no": "Nomor CIF",
                    "short name": "Nama Nasabah",
                    "Open DT": "Tanggal Buka Rekening",
                    "balance": "Saldo",
                    "available balance": "Saldo Tersedia",
                    "int credit": "Kredit Bunga",
                    "accrued int": "Bunga Berjalan",
                    "average balance": "Saldo Rata-rata",
                    "prod code": "Kode Produk",
                    "PN PENGELOLA SINGLEPN": "Pengelola Utama",
                    "PN Customer Service": "Petugas CS",
                    "PN RM Dana/Mantri": "RM Dana / Mantri",
                    "PN RM Pinjaman": "RM Pinjaman",
                    "PN RM Merchant": "RM Merchant",
                    "PN Relationship Officer / RM Kredit Menangah": (
                        "RM Kredit Menengah"
                    ),
                    "PN Sales Person": "Sales Person",
                    "PN PAB": "Petugas PAB",
                    "PN RM Referral": "RM Referral",
                    "JUMLAH PN Pemasar": "Jumlah Pemasar",
                    "Balance dalam IDR": "Saldo dalam IDR",
                }

                kolom_uang = [
                    "balance",
                    "available balance",
                    "int credit",
                    "accrued int",
                    "average balance",
                    "Balance dalam IDR",
                ]
                rincian_data = []
                for k_asli, n_baru in mapping_lengkap.items():
                  if k_asli in data_terpilih:
                    val = data_terpilih[k_asli]
                    val_tamp = (
                        format_rupiah(val) if k_asli in kolom_uang else str(val)
                    )
                    if val is None or val_tamp == "nan" or not val_tamp.strip():
                      val_tamp = "-"
                    rincian_data.append(
                        {"Atribut Data": n_baru, "Nilai": val_tamp}
                    )

                st.dataframe(
                    pd.DataFrame(rincian_data),
                    use_container_width=True,
                    hide_index=True,
                )

              csv = hasil.to_csv(index=False).encode("utf-8")
              st.download_button(
                  label="📥 Download Hasil Pencarian (CSV)",
                  data=csv,
                  file_name="hasil_pencarian.csv",
                  mime="text/csv",
              )
            else:
              st.warning("Tidak ada data yang cocok.")
          else:
            st.info(
                "👉 Atur filter di atas, lalu klik **Cari** untuk mulai mencari"
                " data."
            )

        with tab_pipeline:
          st.subheader("🚀 Dashboard Pipeline & Kunjungan")

          if st.session_state.pipeline_leads:
            df_pipe = pd.DataFrame(st.session_state.pipeline_leads)

            d1, d2, d3, d4, d5 = st.columns(5)
            with d1:
              st.metric("Total Leads", len(df_pipe))
            with d2:
              st.metric(
                  "Belum Kunjung",
                  len(df_pipe[df_pipe["Status Kunjungan"] == "Belum Dikunjungi"]),
              )
            with d3:
              st.metric(
                  "Sudah Kunjung",
                  len(df_pipe[df_pipe["Status Kunjungan"] == "Sudah Dikunjungi"]),
              )
            with d4:
              st.metric(
                  "Perlu Follow-up",
                  len(df_pipe[df_pipe["Status Follow-up"] == "Perlu Follow-up"]),
              )
            with d5:
              st.metric(
                  "Closing",
                  len(df_pipe[df_pipe["Status Follow-up"] == "Closing"]),
              )

            st.markdown("---")
            c_f1, c_f2 = st.columns(2)
            with c_f1:
              f_kunjung = st.selectbox(
                  "Filter Kunjungan:",
                  ["Semua", "Belum Dikunjungi", "Sudah Dikunjungi"],
              )
            with c_f2:
              f_fu = st.selectbox(
                  "Filter Follow-up:",
                  ["Semua", "Perlu Follow-up", "Closing", "Tidak Lanjut", "-"],
              )

            df_view = df_pipe.copy()
            if f_kunjung != "Semua":
              df_view = df_view[df_view["Status Kunjungan"] == f_kunjung]
            if f_fu != "Semua":
              df_view = df_view[df_view["Status Follow-up"] == f_fu]

            st.dataframe(df_view, use_container_width=True, hide_index=True)

            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
              out_p = io.BytesIO()
              with pd.ExcelWriter(out_p, engine="xlsxwriter") as w:
                df_pipe.to_excel(w, index=False, sheet_name="Pipeline")
              out_p.seek(0)
              st.download_button(
                  "📊 Export Pipeline ke Excel",
                  out_p,
                  "Pipeline_Leads.xlsx",
                  (
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  ),
                  use_container_width=True,
              )
            with col_ex2:
              out_m = io.BytesIO()
              with pd.ExcelWriter(out_m, engine="xlsxwriter") as w:
                df_pipe.to_excel(w, index=False, sheet_name="Monitoring")
              out_m.seek(0)
              st.download_button(
                  "📈 Export Monitoring ke Excel",
                  out_m,
                  "Monitoring_Kunjungan.xlsx",
                  (
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  ),
                  use_container_width=True,
              )

            st.markdown("---")
            st.subheader("✍️ Update Progress Kunjungan & Follow-up")
            rek_opts = df_pipe["No. Rekening"].tolist()
            sel_rek = st.selectbox(
                "Pilih No. Rekening untuk Di-update:",
                rek_opts,
                key="sel_rek_di319",
            )

            if sel_rek:
              idx_t = df_pipe[df_pipe["No. Rekening"] == sel_rek].index[0]
              cur = st.session_state.pipeline_leads[idx_t]

              with st.form("form_update_di319"):
                st.write(
                    f"**Nasabah:** {cur['Nama Nasabah']} (Rek: {sel_rek})"
                )
                uc1, uc2 = st.columns(2)
                with uc1:
                  is_sudah = st.checkbox(
                      "Sudah Dikunjungi",
                      value=True
                      if cur["Status Kunjungan"] == "Sudah Dikunjungi"
                      else False,
                  )
                  tgl_k = st.date_input("Tanggal Kunjungan", key="tgl_k_di319")
                  hasil_k = st.selectbox(
                      "Hasil Kunjungan:",
                      [
                          "Potensi Prospek",
                          "Tidak Berminat",
                          "Tidak Sesuai",
                          "Berpotensi Menjadi Prospek",
                      ],
                  )
                  cat_prob = st.text_area(
                      "Catatan Probing:", value=cur["Catatan Probing"]
                  )
                with uc2:
                  stat_fu = st.selectbox(
                      "Status Follow-up:",
                      ["Perlu Follow-up", "Closing", "Tidak Lanjut", "-"],
                  )
                  tgl_fu = st.date_input(
                      "Tanggal Follow-up", key="tgl_fu_di319"
                  )
                  pic_u = st.text_input("PIC / RM:", value=cur["PIC/RM"])
                  ket_u = st.text_input("Keterangan:", value=cur["Keterangan"])

                if st.form_submit_button("💾 Simpan Update"):
                  st.session_state.pipeline_leads[idx_t]["Status Kunjungan"] = (
                      "Sudah Dikunjungi" if is_sudah else "Belum Dikunjungi"
                  )
                  st.session_state.pipeline_leads[idx_t]["Tanggal Kunjungan"] = (
                      str(tgl_k)
                  )
                  st.session_state.pipeline_leads[idx_t]["Hasil Kunjungan"] = (
                      hasil_k
                  )
                  st.session_state.pipeline_leads[idx_t]["Catatan Probing"] = (
                      cat_prob
                  )
                  st.session_state.pipeline_leads[idx_t]["Tanggal Follow-up"] = (
                      str(tgl_fu)
                  )
                  st.session_state.pipeline_leads[idx_t]["Status Follow-up"] = (
                      stat_fu
                  )
                  st.session_state.pipeline_leads[idx_t]["PIC/RM"] = pic_u
                  st.session_state.pipeline_leads[idx_t]["Keterangan"] = ket_u
                  st.success("Update berhasil disimpan!")
                  st.rerun()
          else:
            st.info(
                "Belum ada data di Pipeline. Silakan tambah dari menu"
                " pencarian."
            )

        with tab_tidak_potensial:
          st.subheader("🚫 Daftar Nasabah Tidak Potensial")
          st.write(
              "Berikut adalah daftar nasabah yang telah ditandai sebagai tidak"
              " potensial dan disembunyikan dari hasil pencarian utama."
          )

          if st.session_state.tidak_potensial_list:
            df_tp = pd.DataFrame(st.session_state.tidak_potensial_list)
            st.dataframe(df_tp, use_container_width=True, hide_index=True)

            col_tp1, col_tp2 = st.columns(2)
            with col_tp1:
              out_tp = io.BytesIO()
              with pd.ExcelWriter(out_tp, engine="xlsxwriter") as w:
                df_tp.to_excel(w, index=False, sheet_name="Tidak Potensial")
              out_tp.seek(0)
              st.download_button(
                  "📥 Export Daftar Tidak Potensial ke Excel",
                  out_tp,
                  "Nasabah_Tidak_Potensial.xlsx",
                  (
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  ),
                  use_container_width=True,
              )

            with col_tp2:
              if st.button("🗑️ Kosongkan Semua Daftar Tidak Potensial"):
                st.session_state.tidak_potensial_list = []
                st.success("Daftar berhasil dikosongkan.")
                st.rerun()
          else:
            st.info("Belum ada nasabah yang dimasukkan ke daftar tidak potensial.")

        with tab_list_kustom:
          st.subheader("📂 Kelola List Kustom DI319")
          if st.session_state.custom_lists:
            sel_l = st.selectbox(
                "Pilih List:",
                list(st.session_state["custom_lists"].keys()),
                key="sel_list_di319",
            )
            items = st.session_state["custom_lists"].get(sel_l, [])
            if items:
              df_c = pd.DataFrame(items)
              st.dataframe(df_c, use_container_width=True, hide_index=True)
              st.download_button(
                  "📥 Download List (CSV)",
                  df_c.to_csv(index=False).encode("utf-8"),
                  f"list_{sel_l}.csv",
                  "text/csv",
              )
            else:
              st.info("List masih kosong.")
          else:
            st.info("Belum ada list kustom.")

    except Exception as e:
      st.error(f"Terjadi kesalahan: {e}")
  else:
    st.info("👆 Silakan unggah file Excel DI319 Anda terlebih dahulu.")

# --- FOOTER INFO ERROR / BUG & KONTAK WHATSAPP DEVELOPER ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 14px; margin-bottom: 20px;'>
        Mengalami kendala, error, atau bug pada aplikasi? Hubungi developer via WhatsApp di: 
        <a href='https://wa.me/6289527971310' target='_blank' style='text-style: none; font-weight: bold; color: #25D366;'>
            🟢 0895-2797-1310
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)