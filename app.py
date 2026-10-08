# ==============================================================================
# SISTEM PENGURUSAN PETAK JADUAL WAKTU SEKOLAH (KPM)
# Hakcipta Terpelihara © 2026 Sazahlie S. (sazahlie.sapar@moe.edu.my)
# 
# VERSI KOD       : v2.1 (Auto-Serial Hash, Memory Cleanup, Fit-to-Page)
# TARIKH KEMASKINI: 08 Oktober 2026
# ==============================================================================

import streamlit as st
import pandas as pd
import base64
import os
import io
import hashlib
from datetime import datetime, timedelta

# Import Pustaka ReportLab untuk Penjanaan PDF
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Pemalar Versi Kod & Sistem
VERSI_KOD = "v2.1"
TARIKH_KEMASKINI = "08 Oktober 2026"

# Tetapan Halaman Streamlit
st.set_page_config(
    page_title="Sistem Pengurusan Petak Jadual Waktu Sekolah (KPM)",
    page_icon="🏫",
    layout="wide"
)

# ==============================================================================
# SCRIPT KESELAMATAN (DISABLE RIGHT CLICK, DEVTOOLS & VIEW SOURCE)
# ==============================================================================
st.components.v1.html("""
    <script>
    // 1. Sekat Klik Kanan (Context Menu) secara menyeluruh
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }, true);

    // 2. Sekat Kekunci Pintasan Developer Tools & View Source
    document.addEventListener('keydown', function(e) {
        if (e.key === 'F12' || e.keyCode === 123) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && 
            (e.key === 'I' || e.key === 'i' || e.keyCode === 73 ||
             e.key === 'J' || e.key === 'j' || e.keyCode === 74 ||
             e.key === 'C' || e.key === 'c' || e.keyCode === 67)) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }

        if ((e.ctrlKey || e.metaKey) && (e.key === 'U' || e.key === 'u' || e.keyCode === 85)) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        
        if ((e.ctrlKey || e.metaKey) && (e.key === 'S' || e.key === 's' || e.keyCode === 83)) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
    }, true);

    try {
        window.parent.document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        });
        window.parent.document.addEventListener('keydown', function(e) {
            if (e.key === 'F12' || e.keyCode === 123 ||
                ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) ||
                ((e.ctrlKey || e.metaKey) && (e.keyCode === 85 || e.keyCode === 83))) {
                e.preventDefault();
                return false;
            }
        });
    } catch (err) {}
    </script>
""", height=0, width=0)

# --- SUNTIKAN CSS UNTUK SOLEKAN PENGEPALA RASMI & PERLINDUNGAN SKRIN ---
st.markdown("""
    <style>
    /* Halang Penyorotan Teks & Pergerakan Elemen (Security CSS) */
    body, html, [data-testid="stAppViewContainer"] {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
    }

    /* Format Pengepala Rasmi Sekolah (Center-Aligned) */
    .header-rasmi-container {
        text-align: center;
        padding-top: 5px;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    .header-rasmi-line1 {
        font-size: 22px;
        font-weight: 800;
        color: #1e3a8a;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
        text-transform: uppercase;
    }
    .header-rasmi-line2 {
        font-size: 15px;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 4px;
        text-transform: uppercase;
    }
    .header-rasmi-line3 {
        font-size: 12px;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
    }

    /* Wrap Text dan kemaskan header dalam Streamlit Data Editor */
    [data-testid="stDataFrame"] div[role="gridcell"], 
    [data-testid="stDataFrame"] div[role="columnheader"] {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        line-height: 1.2 !important;
        text-align: center !important;
    }

    /* Reka Bentuk Kad Hakcipta & Badge Versi */
    .copyright-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 10px 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .copyright-title {
        font-size: 12px;
        font-weight: 600;
        color: #333;
        margin-bottom: 3px;
    }
    .copyright-author {
        font-size: 14px;
        font-weight: bold;
        color: #1c64f2;
        margin-bottom: 4px;
    }
    .version-badge {
        font-size: 10px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .email-badge {
        background-color: #0066ff;
        color: white !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: bold;
        text-decoration: none !important;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0,102,255,0.2);
    }
    .disclaimer-box {
        background-color: #fffbebfb;
        border: 1px solid #fef3c7;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 11px;
        color: #92400e;
        line-height: 1.4;
        margin-top: 15px;
    }
    .logo-img {
        width: 55px;
        height: auto;
        object-fit: contain;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi Dapatkan Base64 Imej Logo jika fail logo.png wujud
def get_image_base64(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    return None

# Fungsi untuk memaparkan Kad Hakcipta atas kanan
def paparkan_kad_hakcipta():
    img_b64 = get_image_base64("logo.png")
    
    if img_b64:
        logo_html = f'<img src="{img_b64}" class="logo-img" alt="Logo">'
    else:
        logo_html = '''
        <svg class="logo-img" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#ff4500;stop-opacity:1" />
                    <stop offset="50%" style="stop-color:#00d2ff;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#9900ff;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M 20 20 L 80 20 Q 50 50 80 80 L 20 80 Q 50 50 20 20 Z" fill="url(#grad)" />
        </svg>
        '''

    st.markdown(f"""
        <div class="copyright-card">
            <div class="copyright-text">
                <div class="copyright-title">🔒 Hakcipta Terpelihara</div>
                <div class="copyright-author">© Sazahlie S.</div>
                <div class="version-badge">Versi {VERSI_KOD} ({TARIKH_KEMASKINI})</div>
                <a href="mailto:sazahlie.sapar@moe.edu.my" class="email-badge">📩 sazahlie.sapar@moe.edu.my</a>
            </div>
            <div>
                {logo_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Fungsi Paparan Header Rasmi 3 Baris
def paparkan_header_rasmi(jumlah_z=0):
    sekolah = st.session_state.get("nama_sekolah", "SK BANDAR SANDAKAN").upper()
    kod = st.session_state.get("kod_sekolah", "XBA2004").upper()
    tahun = st.session_state.get("tahun_sesi", "2027")
    minggu = st.session_state.get("minggu_akademik", 39)
    pengetua = st.session_state.get("nama_pengetua", "EN. SAZAHLIE BIN SAPAR").upper()
    negeri = st.session_state.get("negeri", "SABAH").upper()
    kumpulan = st.session_state.get("kumpulan", "Kumpulan B (Isnin - Jumaat)").upper()

    st.markdown(f"""
        <div class="header-rasmi-container">
            <div class="header-rasmi-line1">{sekolah} ({kod})</div>
            <div class="header-rasmi-line2">SISTEM PENGURUSAN PETAK JADUAL WAKTU TAHUN {tahun}</div>
            <div class="header-rasmi-line3">MINGGU AKADEMIK: {minggu} MINGGU | JUMLAH PETAK JADUAL WAKTU: {jumlah_z}</div>
            <div class="header-rasmi-line3" style="margin-top:2px;">PENGETUA / GURU BESAR: {pengetua} | NEGERI: {negeri} ({kumpulan})</div>
        </div>
    """, unsafe_allow_html=True)

# Inisialisasi Session State
if "page" not in st.session_state:
    st.session_state.page = 1

# Data Lalai Subjek
DATA_LALAI = {
    "Tahap 1": [
        {"Subjek": "Bahasa Melayu", "Jam_Tahun": 192},
        {"Subjek": "Bahasa Inggeris", "Jam_Tahun": 160},
        {"Subjek": "Matematik", "Jam_Tahun": 96},
        {"Subjek": "Pendidikan Islam / Pendidikan Moral", "Jam_Tahun": 96},
        {"Subjek": "Sains", "Jam_Tahun": 48},
        {"Subjek": "Pendidikan Jasmani & Pendidikan Kesihatan", "Jam_Tahun": 48},
        {"Subjek": "Pendidikan Seni Visual", "Jam_Tahun": 32},
        {"Subjek": "Pendidikan Muzik", "Jam_Tahun": 16},
        {"Subjek": "Tasmik", "Jam_Tahun": 32},
        {"Subjek": "B. Tambahan", "Jam_Tahun": 48},
        {"Subjek": "Perhimpunan", "Jam_Tahun": 16},
    ],
    "Tahap 2": [
        {"Subjek": "Bahasa Melayu", "Jam_Tahun": 160},
        {"Subjek": "Bahasa Inggeris", "Jam_Tahun": 160},
        {"Subjek": "Matematik", "Jam_Tahun": 96},
        {"Subjek": "Sains", "Jam_Tahun": 64},
        {"Subjek": "Pendidikan Islam / Pendidikan Moral", "Jam_Tahun": 96},
        {"Subjek": "Pendidikan Jasmani & Pendidikan Kesihatan", "Jam_Tahun": 48},
        {"Subjek": "Sejarah", "Jam_Tahun": 32},
        {"Subjek": "Pendidikan Seni Visual", "Jam_Tahun": 32},
        {"Subjek": "Pendidikan Muzik", "Jam_Tahun": 16},
        {"Subjek": "Reka Bentuk dan Teknologi", "Jam_Tahun": 32},
        {"Subjek": "Tasmik", "Jam_Tahun": 32},
        {"Subjek": "B. Tambahan", "Jam_Tahun": 48},
        {"Subjek": "Perhimpunan", "Jam_Tahun": 16},
    ]
}

def pergi_muka_2():
    st.session_state.page = 2

def pergi_muka_1():
    st.session_state.page = 1

def jana_slot_masa(masa_mula_str, tempoh_petak, masa_rehat_str, tempoh_rehat, bil_petak):
    try:
        cur_time = datetime.strptime(masa_mula_str.strip(), "%H:%M")
        rehat_time = datetime.strptime(masa_rehat_str.strip(), "%H:%M")
    except ValueError:
        cur_time = datetime.strptime("12:05", "%H:%M")
        rehat_time = datetime.strptime("14:35", "%H:%M")

    slots = []
    p_num = 1
    rehat_inserted = False

    for _ in range(bil_petak):
        if not rehat_inserted and cur_time >= rehat_time:
            end_rehat = cur_time + timedelta(minutes=tempoh_rehat)
            time_str = f"{cur_time.strftime('%H:%M')} - {end_rehat.strftime('%H:%M')}"
            slots.append({
                "label": f"REHAT\n({time_str})",
                "is_rehat": True,
                "key": "slot_rehat"
            })
            cur_time = end_rehat
            rehat_inserted = True

        end_time = cur_time + timedelta(minutes=tempoh_petak)
        time_str = f"{cur_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        slots.append({
            "label": f"P{p_num}\n({time_str})",
            "is_rehat": False,
            "key": f"slot_P{p_num}"
        })
        p_num += 1
        cur_time = end_time

    return slots

# FUNGSI PENJANAAN PDF COMPACT, JUSTIFIED, AUTO-SERIAL HASH & MEMORY CLEANUP
def jana_pdf_laporan(sekolah, kod, tahun, pengetua, negeri, kumpulan, tahap, minggu, df_analisis, df_grid, jumlah_z):
    # Penjanaan ID Unik Penentusahan (Serial Hash)
    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_raw = f"{sekolah}_{kod}_{tahun}_{time_now}".encode('utf-8')
    serial_hash = f"DOC-{datetime.now().strftime('%Y%m%d')}-{hashlib.md5(hash_raw).hexdigest()[:6].upper()}"

    buffer = io.BytesIO()
    try:
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=18,
            leftMargin=18,
            topMargin=15,
            bottomMargin=15
        )
        elements = []
        styles = getSampleStyleSheet()

        header_line1 = ParagraphStyle(
            'HeaderLine1', parent=styles['Heading1'],
            fontSize=12, leading=14, alignment=1,
            textColor=colors.HexColor('#1e3a8a'), fontName="Helvetica-Bold"
        )
        header_line2 = ParagraphStyle(
            'HeaderLine2', parent=styles['Heading2'],
            fontSize=10, leading=12, alignment=1,
            textColor=colors.HexColor('#1e3a8a'), fontName="Helvetica-Bold"
        )
        header_line3 = ParagraphStyle(
            'HeaderLine3', parent=styles['Normal'],
            fontSize=8, leading=10, alignment=1,
            textColor=colors.HexColor('#475569')
        )

        section_style = ParagraphStyle(
            'SectionHeader', parent=styles['Heading2'],
            fontSize=9, leading=11, textColor=colors.HexColor('#1e293b'),
            spaceBefore=4, spaceAfter=2, fontName="Helvetica-Bold"
        )
        cell_style = ParagraphStyle(
            'GridCell', parent=styles['Normal'],
            fontSize=7, leading=10, alignment=1
        )
        cell_header = ParagraphStyle(
            'GridHeader', parent=styles['Normal'],
            fontSize=7, leading=10, alignment=1, fontName="Helvetica-Bold"
        )
        
        style_guna = ParagraphStyle('GunaStyle', parent=cell_style, textColor=colors.HexColor('#854D0E'), fontName="Helvetica-Bold")
        style_tidak = ParagraphStyle('TidakStyle', parent=cell_style, textColor=colors.HexColor('#F8FAFC'), fontName="Helvetica-Bold")

        # Header Dokumen
        elements.append(Paragraph(f"{sekolah.upper()} ({kod.upper()})", header_line1))
        elements.append(Paragraph(f"SISTEM PENGURUSAN PETAK JADUAL WAKTU TAHUN {tahun}", header_line2))
        elements.append(Paragraph(f"MINGGU AKADEMIK: {minggu} MINGGU | JUMLAH PETAK JADUAL WAKTU: {jumlah_z}", header_line3))
        elements.append(Paragraph(f"PENGETUA / GURU BESAR: {pengetua.upper()} | NEGERI: {negeri.upper()} ({kumpulan.upper()}) | TAHAP: {tahap.upper()}", header_line3))
        elements.append(Paragraph(f"<font size=7 color='#0284c7'><b>[ ID DOKUMEN: {serial_hash} ]</b></font>", header_line3))
        elements.append(Spacer(1, 4))

        # 1. Jadual Analisis
        elements.append(Paragraph("1. Analisis Pengiraan Petak Jadual Waktu", section_style))
        
        mapping_label = {
            "Subjek": "Subjek",
            "Jam_Tahun": "Jam Setahun",
            "Jam/Minggu": "Jam Seminggu",
            "Waktu/Petak": "Waktu/Petak Seminggu",
            "Janaan Sistem": "Janaan Sistem",
            "Tetapan_Z": "Tetapan Sekolah",
            "Jam Operasi/Tahun": "Jam Operasi/Tahun",
            "Beza Jam": "Beza Jam",
            "Status": "Status"
        }
        
        df_analisis_pdf = df_analisis.rename(columns=mapping_label)
        headers_analisis = list(df_analisis_pdf.columns)
        data_analisis = [[Paragraph(h, cell_header) for h in headers_analisis]]
        
        for _, row in df_analisis_pdf.iterrows():
            row_data = [Paragraph(str(val), cell_style) for val in row.values]
            data_analisis.append(row_data)

        t_analisis = Table(data_analisis, repeatRows=1)
        t_analisis.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(t_analisis)
        elements.append(Spacer(1, 6))

        # 2. Kerangka Jadual Seminggu
        elements.append(Paragraph("2. Kerangka Jadual Waktu Seminggu", section_style))
        
        headers_grid = list(df_grid.columns)
        data_grid = [[Paragraph(str(h).replace('\n', '<br/>'), cell_header) for h in headers_grid]]
        
        grid_style = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]

        for r_idx, row in df_grid.iterrows():
            row_data = []
            row_num = r_idx + 1
            for c_idx, (col_name, val) in enumerate(row.items()):
                val_str = str(val).strip()
                if val_str == "Guna":
                    p_text = Paragraph(val_str, style_guna)
                    grid_style.append(('BACKGROUND', (c_idx, row_num), (c_idx, row_num), colors.HexColor('#FEF08A')))
                elif val_str == "Tidak":
                    p_text = Paragraph(val_str, style_tidak)
                    grid_style.append(('BACKGROUND', (c_idx, row_num), (c_idx, row_num), colors.HexColor('#334155')))
                elif val_str == "REHAT":
                    p_text = Paragraph(val_str, cell_style)
                    grid_style.append(('BACKGROUND', (c_idx, row_num), (c_idx, row_num), colors.HexColor('#E2E8F0')))
                else:
                    p_text = Paragraph(val_str, cell_style)
                
                row_data.append(p_text)
            data_grid.append(row_data)

        t_grid = Table(data_grid, repeatRows=1)
        t_grid.setStyle(TableStyle(grid_style))
        elements.append(t_grid)
        
        # Footer PDF dengan Klausa Penafian & Hak Cipta
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"<font size=6 color='#64748b'>🔒 Hakcipta Terpelihara © Sazahlie S. (sazahlie.sapar@moe.edu.my) — Sistem Pengurusan Petak Jadual Waktu KPM [{VERSI_KOD}]<br/>PENAFIAN: Laporan ini adalah janaan pengiraan automatik sebagai kerangka panduan sekolah. Pihak sekolah hendaklah memastikan keselarasan penuh dengan Pekeliling Ikhtisas KPM semasa.</font>", header_line3))

        doc.build(elements)
        buffer.seek(0)
        return buffer
    finally:
        pass # Buffer dikembalikan ke Streamlit untuk muat turun


# ==============================================================================
# TETAPAN PARAMETER & PENDAFTARAN SUBJEK
# ==============================================================================
if st.session_state.page == 1:
    col_tajuk, col_hakcipta = st.columns([3, 1.2])
    with col_tajuk:
        st.title("🏫 Sistem Pengurusan Petak Jadual Waktu Sekolah (KPM)")
        st.subheader("Tetapan Parameter Asas & Pendaftaran Subjek")
        st.markdown("Isikan maklumat parameter sekolah serta daftarkan mata pelajaran yang ditawarkan di sekolah anda.")
    with col_hakcipta:
        paparkan_kad_hakcipta()

    st.divider()

    col_kiri, col_tengah, col_kanan = st.columns([1, 1, 2.2])

    with col_kiri:
        st.markdown("##### 📌 Maklumat Sekolah & Sesi")
        nama_sekolah = st.text_input("Nama Sekolah", st.session_state.get("nama_sekolah", "SK BANDAR SANDAKAN"))
        kod_sekolah = st.text_input("Kod Sekolah", st.session_state.get("kod_sekolah", "XBA2004"))
        tahun_sesi = st.text_input("Tahun Jadual Waktu", st.session_state.get("tahun_sesi", "2027"))
        nama_pengetua = st.text_input("Pengetua / Guru Besar", st.session_state.get("nama_pengetua", "EN. SAZAHLIE BIN SAPAR"))
        negeri = st.selectbox("Negeri", ["SABAH", "SARAWAK", "JOHOR", "KEDAH", "KELANTAN", "MELAKA", "NEGERI SEMBILAN", "PAHANG", "PERAK", "PERLIS", "PULAU PINANG", "SELANGOR", "TERENGGANU", "WP KUALA LUMPUR", "WP LABUAN", "WP PUTRAJAYA"], index=0)
        kumpulan = st.selectbox(
            "Kumpulan Kalender KPM", 
            ["Kumpulan B (Isnin - Jumaat)", "Kumpulan A (Ahad - Khamis)"],
            index=0 if st.session_state.get("kumpulan") != "Kumpulan A (Ahad - Khamis)" else 1
        )
        tahap = st.selectbox(
            "Tahap Jadual Waktu", 
            ["Tahap 1", "Tahap 2"],
            index=0 if st.session_state.get("tahap") != "Tahap 2" else 1
        )

    with col_tengah:
        st.markdown("##### ⏰ Masa & Minggu Akademik")
        minggu_akademik = st.number_input("Minggu Akademik (Contoh: 39)", min_value=1, max_value=52, value=st.session_state.get("minggu_akademik", 39))
        masa_mula = st.text_input("Masa Mula (Contoh: 12:05 atau 06:40)", st.session_state.get("masa_mula", "12:05"))
        tempoh_petak = st.number_input("Tempoh Masa Setiap Petak (Minit)", min_value=15, max_value=60, value=st.session_state.get("tempoh_petak", 30))
        masa_rehat = st.text_input("Masa Rehat (Contoh: 14:35 atau 09:10)", st.session_state.get("masa_rehat", "14:35"))
        tempoh_rehat = st.number_input("Tempoh Rehat (Minit)", min_value=10, max_value=40, value=st.session_state.get("tempoh_rehat", 20))

    with col_kanan:
        st.markdown("##### 📚 Pendaftaran Mata Pelajaran")
        st.caption("Ubah, tambah, atau padam subjek di bawah.")

        if "subjek_df_raw" not in st.session_state or st.session_state.get("last_tahap") != tahap:
            subjek_default = DATA_LALAI[tahap]
            st.session_state["subjek_df_raw"] = pd.DataFrame(subjek_default)
            st.session_state["last_tahap"] = tahap

        raw_df = st.session_state["subjek_df_raw"]

        display_df = raw_df.copy()
        display_df["Janaan_Sistem"] = display_df["Jam_Tahun"].apply(
            lambda a: round((a / minggu_akademik) * 2) if minggu_akademik > 0 else 0
        )

        edited_df = st.data_editor(
            display_df,
            column_config={
                "Subjek": st.column_config.TextColumn("Mata Pelajaran", required=True, width="medium"),
                "Jam_Tahun": st.column_config.NumberColumn("Jam Setahun", min_value=1, required=True, width="small"),
                "Janaan_Sistem": st.column_config.NumberColumn("Janaan Sistem", disabled=True, width="small")
            },
            num_rows="dynamic",
            use_container_width=True,
            height=380,
            key="data_editor_muka1"
        )

        st.session_state["subjek_df_raw"] = edited_df[["Subjek", "Jam_Tahun"]]

    st.session_state["nama_sekolah"] = nama_sekolah
    st.session_state["kod_sekolah"] = kod_sekolah
    st.session_state["tahun_sesi"] = tahun_sesi
    st.session_state["nama_pengetua"] = nama_pengetua
    st.session_state["negeri"] = negeri
    st.session_state["kumpulan"] = kumpulan
    st.session_state["tahap"] = tahap
    st.session_state["minggu_akademik"] = minggu_akademik
    st.session_state["masa_mula"] = masa_mula
    st.session_state["tempoh_petak"] = tempoh_petak
    st.session_state["masa_rehat"] = masa_rehat
    st.session_state["tempoh_rehat"] = tempoh_rehat

    st.divider()

    st.button("➡️ Seterusnya: Pergi ke Muka Pengiraan & Jadual", on_click=pergi_muka_2, type="primary", use_container_width=True)


# ==============================================================================
# PENGIRAAN, ANALISIS & KERANGKA JADUAL
# ==============================================================================
elif st.session_state.page == 2:
    nama_sekolah = st.session_state.get("nama_sekolah", "SK BANDAR SANDAKAN")
    kod_sekolah = st.session_state.get("kod_sekolah", "XBA2004")
    tahun_sesi = st.session_state.get("tahun_sesi", "2027")
    nama_pengetua = st.session_state.get("nama_pengetua", "EN. SAZAHLIE BIN SAPAR")
    negeri = st.session_state.get("negeri", "SABAH")
    kumpulan = st.session_state.get("kumpulan", "Kumpulan B (Isnin - Jumaat)")
    tahap = st.session_state.get("tahap", "Tahap 1")
    minggu_akademik = st.session_state.get("minggu_akademik", 39)
    masa_mula = st.session_state.get("masa_mula", "12:05")
    tempoh_petak = st.session_state.get("tempoh_petak", 30)
    masa_rehat = st.session_state.get("masa_rehat", "14:35")
    tempoh_rehat = st.session_state.get("tempoh_rehat", 20)
    subjek_raw = st.session_state.get("subjek_df_raw", pd.DataFrame(DATA_LALAI["Tahap 1"]))

    col_nav1, col_nav2, col_hakcipta2 = st.columns([1, 3, 1.2])
    with col_nav1:
        st.button("⬅️ Kembali ke Tetapan", on_click=pergi_muka_1)
    with col_nav2:
        pass
    with col_hakcipta2:
        paparkan_kad_hakcipta()

    # --- JADUAL ANALISIS SEMENTARA UNTUK DAPATKAN JUMLAH Z ---
    df_muka2_temp = subjek_raw.copy()
    if "z_values" not in st.session_state or len(st.session_state["z_values"]) != len(df_muka2_temp):
        st.session_state["z_values"] = df_muka2_temp["Jam_Tahun"].apply(
            lambda a: round((a / minggu_akademik) * 2) if minggu_akademik > 0 else 0
        ).tolist()
    jumlah_z_semasa = sum(st.session_state["z_values"])

    # PAPARAN PENGEPALA RASMI
    paparkan_header_rasmi(jumlah_z=jumlah_z_semasa)

    st.divider()

    # --- BAHAGIAN JADUAL ANALISIS TUNGGAL ---
    st.write("### Analisis Pengiraan Petak Jadual Waktu")
    st.caption("Anda boleh terus menyunting nilai di kolum **Tetapan Sekolah** di bawah. Kolum analisis lain akan dikemaskini secara automatik.")

    df_muka2 = subjek_raw.copy()
    df_muka2["Tetapan_Z"] = st.session_state["z_values"]

    df_muka2["Jam/Minggu"] = df_muka2["Jam_Tahun"].apply(lambda a: round(a / minggu_akademik, 1))
    df_muka2["Waktu/Petak"] = df_muka2["Jam/Minggu"].apply(lambda w: round(w * 2, 1))
    df_muka2["Janaan Sistem"] = df_muka2["Waktu/Petak"].apply(lambda x: round(x))
    df_muka2["Jam Operasi/Tahun"] = df_muka2["Tetapan_Z"].apply(lambda z: round((z * minggu_akademik) / 2, 1))
    df_muka2["Beza Jam"] = (df_muka2["Jam Operasi/Tahun"] - df_muka2["Jam_Tahun"]).abs().round(1)
    df_muka2["Status"] = df_muka2.apply(lambda r: "LEBIH" if r["Jam Operasi/Tahun"] >= r["Jam_Tahun"] else "KURANG", axis=1)

    columns_order = [
        "Subjek", "Jam_Tahun", "Jam/Minggu", "Waktu/Petak", 
        "Janaan Sistem", "Tetapan_Z", "Jam Operasi/Tahun", "Beza Jam", "Status"
    ]
    df_muka2 = df_muka2[columns_order]

    edited_df_muka2 = st.data_editor(
        df_muka2,
        column_config={
            "Subjek": st.column_config.TextColumn("Mata Pelajaran", disabled=True),
            "Jam_Tahun": st.column_config.NumberColumn("Jam Setahun", disabled=True),
            "Jam/Minggu": st.column_config.NumberColumn("Jam Seminggu", disabled=True),
            "Waktu/Petak": st.column_config.NumberColumn("Waktu/Petak Seminggu", disabled=True),
            "Janaan Sistem": st.column_config.NumberColumn("Janaan Sistem", disabled=True),
            "Tetapan_Z": st.column_config.NumberColumn("Tetapan Sekolah", min_value=1, required=True),
            "Jam Operasi/Tahun": st.column_config.NumberColumn("Jam Operasi/Tahun", disabled=True),
            "Beza Jam": st.column_config.NumberColumn("Beza Jam", disabled=True),
            "Status": st.column_config.TextColumn("Status", disabled=True),
        },
        use_container_width=True,
        key="editor_tunggal_muka2"
    )

    st.session_state["z_values"] = edited_df_muka2["Tetapan_Z"].tolist()
    jumlah_z = int(edited_df_muka2["Tetapan_Z"].sum())

    # --- BAHAGIAN KERANGKA JADUAL WAKTU MINGGUAN ---
    st.divider()
    st.write("### 📅 Kerangka Jadual Waktu Seminggu")
    st.caption("Pilih status petak pada jadual di bawah kepada **Guna** atau **Tidak** untuk menyusun kerangka seminggu.")

    num_petak = st.slider("Jumlah Petak Disediakan Per Hari", min_value=8, max_value=12, value=9)

    st.divider()

    slots = jana_slot_masa(masa_mula, tempoh_petak, masa_rehat, tempoh_rehat, num_petak)
    hari_list = ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat"] if "Kumpulan B" in kumpulan else ["Ahad", "Isnin", "Selasa", "Rabu", "Khamis"]

    grid_data = {"Hari": hari_list}
    column_config_grid = {"Hari": st.column_config.TextColumn("Hari", disabled=True, width="small")}

    for slot in slots:
        col_label = slot["label"]
        if slot["is_rehat"]:
            grid_data[col_label] = ["REHAT"] * len(hari_list)
            column_config_grid[col_label] = st.column_config.TextColumn(
                col_label,
                disabled=True,
                width="small"
            )
        else:
            grid_data[col_label] = ["Guna"] * len(hari_list)
            column_config_grid[col_label] = st.column_config.SelectboxColumn(
                col_label,
                options=["Guna", "Tidak"],
                required=True,
                width="small"
            )

    df_grid_init = pd.DataFrame(grid_data)

    edited_grid = st.data_editor(
        df_grid_init,
        column_config=column_config_grid,
        use_container_width=True,
        hide_index=True,
        key="editor_jadual_grid_simple"
    )

    total_petak_diguna = 0
    for col in edited_grid.columns:
        if col != "Hari" and "REHAT" not in col:
            total_petak_diguna += (edited_grid[col] == "Guna").sum()

    # --- RUMUSAN & ANALISIS AKHIR ---
    st.divider()
    st.write("### 📊 Rumusan & Status Analisis Petak")

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("JUMLAH BESAR (Sasaran Sekolah)", jumlah_z)
    col_m2.metric("Petak Diguna Dalam Jadual", total_petak_diguna)

    status_padan = "✅ SEPADAN (OK)" if total_petak_diguna == jumlah_z else ("⚠️ LEBIH" if total_petak_diguna > jumlah_z else "⚠️ KURANG")
    col_m3.metric("Status Jadual", status_padan)

    if total_petak_diguna == jumlah_z:
        st.success("Tahniah! Jumlah petak diguna sepadan sepenuhnya dengan sasaran Tetapan Sekolah. Jadual sedia untuk digunapakai oleh guru.")
    else:
        st.warning(f"Jumlah petak diguna ({total_petak_diguna}) tidak sepadan dengan sasaran Tetapan Sekolah ({jumlah_z}). Sila laraskan penandaan petak hari anda.")

    # --- BAHAGIAN EKSPORT / CETAKAN PDF KEMAS ---
    st.divider()
    st.write("### 🖨️ Mod Eksport PDF / Cetakan Kemas")
    st.caption("Muat turun laporan lengkap jadual waktu ini dalam format PDF sedia cetak 1 muka surat.")

    pdf_buffer = jana_pdf_laporan(
        sekolah=nama_sekolah,
        kod=kod_sekolah,
        tahun=tahun_sesi,
        pengetua=nama_pengetua,
        negeri=negeri,
        kumpulan=kumpulan,
        tahap=tahap,
        minggu=minggu_akademik,
        df_analisis=edited_df_muka2,
        df_grid=edited_grid,
        jumlah_z=jumlah_z
    )

    st.download_button(
        label="📥 Muat Turun Laporan Jadual Waktu (PDF)",
        data=pdf_buffer,
        file_name=f"Laporan_Jadual_{nama_sekolah.replace(' ', '_')}_{tahun_sesi}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )

    # KLAUSA PENAFIAN UNDANG-UNDANG (DISCLAIMER)
    st.markdown("""
        <div class="disclaimer-box">
            <b>⚠️ PENAFIAN PENGGUNAAN (DISCLAIMER):</b><br/>
            Sistem ini dibangunkan secara bebas sebagai alat bantu pemudah cara bagi perancangan dan pengiraan kerangka petak jadual waktu sekolah KPM. 
            Segala hasil analisis dan laporan janaan sistem hendaklah disemak dan disahkan oleh Pengurusan Sekolah mengikut Surat Pekeliling Ikhtisas (SPI) Kementerian Pendidikan Malaysia yang berkuat kuasa. 
            Pembangun sistem tidak bertanggungjawab atas sebarang ralat pengisian data oleh pihak pengguna.
        </div>
    """, unsafe_allow_html=True)