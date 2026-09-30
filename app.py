import io
import pandas as pd
import streamlit as st

# Konfigurasi halaman web (layout wide agar area utama lebih lebar)
st.set_page_config(
    page_title="DI319 Analyzer - Pipeline & Kunjungan Nasabah",
    page_icon="🏦",
    layout="wide",
)

# Custom CSS untuk Sticky Filter Bar & Login Card
st.markdown(
    """
    <style>
    .sticky-filter-container {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        z-index: 9999;
        background-color: #ffffff;
        padding: 12px 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }
    .stSelectbox, .stNumberInput {
        margin-bottom: 0px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ================= INISISASI SESSION STATE =================
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "nasabah_catatan" not in st.session_state:
  st.session_state.nasabah_catatan = {}
if "custom_lists" not in st.session_state:
  st.session_state.custom_lists = {}
if "pipeline_leads" not in st.session_state:
  st.session_state.pipeline_leads = []
if "tidak_potensial_list" not in st.session_state:
  st.session_state.tidak_potensial_list = []

# Database Kredensial Pengguna
USER_CREDENTIALS = {"bagas": "123", "bri": "123"}


# ================= FORM LOGIN =================
if not st.session_state.logged_in:
  st.title("🏦 DI319 Analyzer")
  st.write("**Developer:** Prima | Silakan Login Terlebih Dahulu")
  st.markdown("---")

  col1, col2, col3 = st.columns([1, 1.5, 1])
  with col2:
    st.subheader("🔐 Login Pengguna")
    with st.form("login_form"):
      input_user = st.text_input("Username").strip().lower()
      input_pass = st.text_input("Password", type="password")
      submit_login = st.form_submit_button(
          "Masuk", type="primary", use_container_width=True
      )

      if submit_login:
        if (
            input_user in USER_CREDENTIALS
            and USER_CREDENTIALS[input_user] == input_pass
        ):
          st.session_state.logged_in = True
          st.session_state.username = input_user
          st.success("Login berhasil! Memuat aplikasi...")
          st.rerun()
        else:
          st.error("Username atau Password salah!")

  st.stop()  # Menghentikan eksekusi kode di bawah jika belum login

# ================= KODE UTAMA SETELAH LOGIN =================
st.title("🏦 DI319 Analyzer")
col_title_1, col_title_2 = st.columns([4, 1])
with col_title_1:
  st.write(
      f"**Developer:** Prima | Selamat datang, **{st.session_state.username.capitalize()}**"
      " | Pipeline & Kunjungan Nasabah"
  )
with col_title_2:
  if st.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()


# Fungsi untuk memformat angka menjadi format Rupiah Indonesia
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


# ================= SISTEM CACHE UNTUK MEMPERCEPAT LOAD FILE =================
@st.cache_data(show_spinner="Sedang memproses file Excel...")
def load_excel_data(uploaded_file):
  df = pd.read_excel(uploaded_file)
  if "short name" in df.columns:
    df["short name"] = df["short name"].astype(str).str.strip()
  if "balance" in df.columns:
    df["balance"] = pd.to_numeric(
        df["balance"].astype(str).str.replace(",", ""), errors="coerce"
    ).fillna(0)
  return df


# Fitur Upload File
uploaded_file = st.file_uploader(
    "Pilih atau Seret File Excel DI319 di sini", type=["xlsx", "xls"]
)

if uploaded_file is not None:
  try:
    df = load_excel_data(uploaded_file)
    st.success(f"File berhasil dimuat! Total baris: {len(df):,}")

    if "short name" not in df.columns:
      st.error("Kolom 'short name' tidak ditemukan di dalam file.")
    else:
      # ================= TOP STICKY FILTER BAR =================
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
            ["Semua"] + sorted(df["uker code"].dropna().unique().tolist())
            if "uker code" in df.columns
            else ["Semua"]
        )
        selected_uker = st.selectbox("Uker:", uker_list)

      with col_f2:
        prod_list = (
            ["Semua"] + sorted(df["prod code"].dropna().unique().tolist())
            if "prod code" in df.columns
            else ["Semua"]
        )
        selected_prod = st.selectbox("Produk:", prod_list)

      with col_f3:
        curr_list = (
            ["Semua"] + sorted(df["curr code"].dropna().unique().tolist())
            if "curr code" in df.columns
            else ["Semua"]
        )
        selected_curr = st.selectbox("Valuta:", curr_list)

      with col_f4:
        min_default = float(df["balance"].min()) if not df.empty else 0.0
        min_input = st.number_input("Saldo Min:", value=min_default, step=100000.0)

      with col_f5:
        max_default = (
            float(df["balance"].max()) if not df.empty else 100000000.0
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

      # Terapkan Filter
      if selected_uker != "Semua":
        df = df[df["uker code"] == selected_uker]
      if selected_prod != "Semua":
        df = df[df["prod code"] == selected_prod]
      if selected_curr != "Semua":
        df = df[df["curr code"] == selected_curr]

      df_filtered = df[
          (df["balance"] >= min_input) & (df["balance"] <= max_input)
      ]

      if "search_active" not in st.session_state:
        st.session_state.search_active = False

      if cari_ditekan:
        st.session_state.search_active = True

      # --- TAB UTAMA ---
      tab_pencarian, tab_pipeline, tab_tidak_potensial, tab_list_kustom = (
          st.tabs([
              "🔍 Cari & Leads Database",
              "🚀 Pipeline & Kunjungan",
              "🚫 Nasabah Tidak Potensial",
              "📂 Kelola List",
          ])
      )

      # ================= TAB 1: PENCARIAN & LEADS =================
      with tab_pencarian:
        if st.session_state.search_active:
          st.subheader("🔍 Pencarian Nasabah")
          keyword = st.text_input(
              "Cari Nama Nasabah / No. Rekening / No. CIF:", ""
          ).strip()

          hasil = df_filtered.copy()
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

          # Sembunyikan nasabah yang ada di daftar tidak potensial
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
            kolom_tersedia = [col for col in kolom_list if col in hasil.columns]
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

              # --- CATATAN PERSONAL NASABAH ---
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

              # --- TOMBOL AKSI: TAMBAH PIPELINE ATAU TIDAK POTENSIAL ---
              col_aksi1, col_aksi2 = st.columns(2)

              with col_aksi1:
                with st.form(f"form_add_pipeline_{rek_key}"):
                  st.markdown("#### 🚀 Masukkan ke Pipeline Kunjungan")
                  alasan_leads = st.text_input(
                      "Alasan / Potensi Leads:", value="Potensi penempatan dana"
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
                          "Nasabah dipindahkan ke 'Nasabah Tidak Potensial' dan"
                          " disembunyikan dari daftar utama!"
                      )
                      st.rerun()
                    else:
                      st.warning("Nasabah sudah ada di daftar tidak potensial.")

              # Tampilkan Tabel Rincian Atribut Lengkap
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

      # ================= TAB 2: PIPELINE & KUNJUNGAN =================
      with tab_pipeline:
        st.subheader("🚀 Dashboard Pipeline & Kunjungan")

        if st.session_state.pipeline_leads:
          df_pipe = pd.DataFrame(st.session_state.pipeline_leads)

          # Dashboard Metrik Ringkas
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
                "Filter Kunjungan:", ["Semua", "Belum Dikunjungi", "Sudah Dikunjungi"]
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

          # Tombol Export Excel
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
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
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
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

          st.markdown("---")
          st.subheader("✍️ Update Progress Kunjungan & Follow-up")
          rek_opts = df_pipe["No. Rekening"].tolist()
          sel_rek = st.selectbox(
              "Pilih No. Rekening untuk Di-update:", rek_opts
          )

          if sel_rek:
            idx_t = df_pipe[df_pipe["No. Rekening"] == sel_rek].index[0]
            cur = st.session_state.pipeline_leads[idx_t]

            with st.form("form_update"):
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
                tgl_k = st.date_input("Tanggal Kunjungan")
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
                tgl_fu = st.date_input("Tanggal Follow-up")
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
          st.info("Belum ada data di Pipeline. Silakan tambah dari menu pencarian.")

      # ================= TAB 3: NASABAH TIDAK POTENSIAL =================
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
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

          with col_tp2:
            if st.button("🗑️ Kosongkan Semua Daftar Tidak Potensial"):
              st.session_state.tidak_potensial_list = []
              st.success("Daftar berhasil dikosongkan.")
              st.rerun()
        else:
          st.info("Belum ada nasabah yang dimasukkan ke daftar tidak potensial.")

      # ================= TAB 4: KELOLA LIST KUSTOM =================
      with tab_list_kustom:
        st.subheader("📂 Kelola List Kustom")
        cl1, cl2 = st.columns(2)
        with cl1:
          new_ln = st.text_input("Nama List Baru:")
          if st.button("➕ Buat List", use_container_width=True):
            if new_ln.strip() and new_ln.strip() not in st.session_state.custom_lists:
              st.session_state.custom_lists[new_ln.strip()] = []
              st.success("List berhasil dibuat!")
            else:
              st.warning("Nama list tidak valid atau sudah ada.")
        with cl2:
          if st.session_state.custom_lists:
            sel_l = st.selectbox(
                "Pilih List:", list(st.session_state.custom_lists.keys())
            )
            if st.button("🗑️ Kosongkan List", use_container_width=True):
              st.session_state.custom_lists[sel_l] = []
              st.success("List dikosongkan.")
              st.rerun()

            items = st.session_state.custom_lists.get(sel_l, [])
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