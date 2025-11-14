import streamlit as st
import os
import librosa
import numpy as np
import subprocess
import glob
import sys

# --- 1. Konfigurasi Halaman (Lebih Profesional) ---
st.set_page_config(
    page_title="Technosic - Analisis Audio AI",
    page_icon="🎵",
    layout="wide"
)

# --- 2. Bagian Landing Page (Hero Section) ---
st.title("🎵 Selamat Datang di Technosic")
st.header("Analisis Fitur & Pemisah Vokal Berbasis AI")

st.markdown("""
Selamat datang di **Technosic**!
Platform ini adalah alat bantu berbasis AI untuk "membedah" file audio Anda. Cukup unggah lagu, dan biarkan AI menganalisis serta memisahkan vokal dan instrumen untuk Anda.


""")

# --- 3. Bagian Fitur (Yang Akan Dibuat) ---
st.subheader("Fitur Utama")

col1, col2 = st.columns(2)

with col1:
    st.info("Analisis Fitur Audio")
    st.write("- Deteksi Tempo (BPM)")
    st.write("- Deteksi Tangga Nada (Key)") # <-- Fitur baru sudah ada
    st.write("- Visualisasi Waveform")

with col2:
    st.success("Pemisah Vokal AI")
    st.write("- Memisahkan Vokal (Acappella)")
    st.write("- Memisahkan Instrumen (Minus One)")
    st.write("- Ditenagai oleh model AI Demucs")

st.divider()

# --- 4. Aplikasi Inti (Alatnya) ---
st.header("Mulai Coba Aplikasinya")

uploaded_file = st.file_uploader(
    "Pilih file audio (.mp3, .wav, .flac) untuk dianalisis",
    type=["mp3", "wav", "flac"]
)

# --- Area Kerja Utama ---
if uploaded_file is not None:
    
    # Tampilkan pemutar audio untuk file asli
    st.subheader("Audio Asli yang Diunggah:")
    st.audio(uploaded_file, format=uploaded_file.type)

    # --- Bagian Fase 4 (Analisis) ---
    st.divider()
    st.subheader("Analisis Fitur")

    # Saya ganti nama tombolnya agar tidak sama dengan tombol AI
    if st.button("Mulai Analisis Audio", key="analisis_button"):
        
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Simpan file ke folder 'temp'
        with st.spinner("Menyimpan file temporer..."):
            file_path = os.path.join(temp_dir, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        st.success(f"File disimpan di {file_path}")

        # Proses file dengan Librosa
        with st.spinner("Menganalisis audio..."):
            try:
                # Muat file audio
                y, sr = librosa.load(file_path, sr=None)
                
                # --- PERBAIKAN (KEMBALIKAN KE KODE LAMA YANG BERHASIL) ---
                # Kita biarkan saja ada "FutureWarning" di terminal,
                # yang penting aplikasinya JALAN.
                bpm = librosa.beat.tempo(y=y, sr=sr)[0] 
                # --- AKHIR PERBAIKAN ---
                
                # Hitung Durasi
                duration = librosa.get_duration(y=y, sr=sr)
                
                # --- FITUR TANGGA NADA (INI KITA TETAPKAN) ---
                notes_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                chroma = librosa.feature.chroma_stft(y=y, sr=sr)
                chroma_mean = np.mean(chroma, axis=1)
                key_index = np.argmax(chroma_mean)
                estimated_key = notes_list[key_index]
                # --- AKHIR FITUR ---
                
                
                # Tampilkan Hasil Analisis
                st.subheader("Hasil Analisis:")
                
                col_res1, col_res2, col_res3 = st.columns(3)
                col_res1.metric("Tempo (BPM)", f"{bpm:.1f}")
                col_res2.metric("Durasi (Detik)", f"{duration:.1f} s")
                col_res3.metric("Estimasi Tangga Nada", estimated_key) # <-- Tampilkan Key
                
                st.subheader("Bentuk Gelombang (Waveform)")
                waveform_data = np.interp(np.linspace(0, len(y), 1000), 
                                        np.arange(len(y)), y)
                st.line_chart(waveform_data)

            except Exception as e:
                st.error(f"Terjadi error saat analisis: {e}")
                st.warning("Pastikan file audio tidak corrupt.")

    # --- BAGIAN FASE 5 (PEMISAHAN AI) ---
    st.divider()
    st.subheader("Pemisah Vokal AI")
    
    # Saya ganti nama tombolnya agar tidak sama
    if st.button("Mulai Pemisahan Vokal (Proses AI)", key="pemisah_button"):
        
        temp_dir = "temp"
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        if not os.path.exists(file_path):
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.info("File temporer disimpan untuk AI.")

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        st.info("AI (Demucs) sedang bekerja... Ini SANGAT lambat (bisa 30+ menit). Harap tunggu dan jangan refresh halaman.")
        
        # Pesan loading
        with st.spinner(f"Memproses {uploaded_file.name}... Ini akan memakan waktu SANGAT LAMA..."):
            
            model_name = "htdemucs_ft"
            
            cmd = [
                sys.executable, "-m", "demucs",
                "-n", model_name,
                "-o", output_dir,
                "--mp3",            # Perintah Simpan sebagai MP3 (Rencana C)
                file_path
            ]
            
            try:
                # Jalankan perintah AI
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                
                st.success("Pemisahan AI Selesai!")
                
                file_name_without_ext = os.path.splitext(uploaded_file.name)[0]
                model_output_dir = os.path.join(output_dir, model_name)

                # --- PERBAIKAN FINAL (SESUAI SCREENSHOT ANDA) ---
                # Kita cari file .mp3 (karena kita pakai --mp3)
                # dengan nama-nama yang ada di screenshot Anda
                
                vocal_path = os.path.join(model_output_dir, file_name_without_ext, "vocals.mp3")
                bass_path = os.path.join(model_output_dir, file_name_without_ext, "bass.mp3")
                drums_path = os.path.join(model_output_dir, file_name_without_ext, "drums.mp3")
                other_path = os.path.join(model_output_dir, file_name_without_ext, "other.mp3")
                
                # Kita Cek file Vokal dulu
                if os.path.exists(vocal_path):
                    st.subheader("Hasil Pemisahan:")
                    
                    st.write("Vokal (ACappella):")
                    st.audio(vocal_path, format='audio/mp3')
                    
                    # Tampilkan sisanya (Musik Saja)
                    if os.path.exists(bass_path):
                        st.write("Bass:")
                        st.audio(bass_path, format='audio/mp3')
                    
                    if os.path.exists(drums_path):
                        st.write("Drums:")
                        st.audio(drums_path, format='audio/mp3')
                        
                    if os.path.exists(other_path):
                        st.write("Instrumen Lain:")
                        st.audio(other_path, format='audio/mp3')
                
                else:
                    # Ini jika --mp3 gagal dan dia simpan sbg .wav (Jaga-jaga)
                    vocal_path_wav = os.path.join(model_output_dir, file_name_without_ext, "vocals.wav")
                    if os.path.exists(vocal_path_wav):
                        st.subheader("Hasil Pemisahan:")
                        st.write("Vokal Saja (ACappella):")
                        st.audio(vocal_path_wav)
                        st.warning("Disimpan sebagai .wav karena --mp3 mungkin gagal.")
                    else:
                        st.error("Gagal menemukan file hasil pemisahan (vocals.mp3 atau vocals.wav).")
                        st.write(f"Mencari di: {vocal_path}")
                # --- AKHIR PERBAIKAN ---

            except subprocess.CalledProcessError as e:
                st.error("Gagal menjalankan AI Demucs.")
                st.subheader("Error Detail (stderr):")
                st.code(e.stderr, language="log")
                st.subheader("Error Output (stdout):")
                st.code(e.stdout, language="log")
            except Exception as e:
                st.error(f"Terjadi error yang tidak diketahui: {e}")
                st.warning("Mungkin file hasil tidak ditemukan. Cek folder 'output' Anda.")

else:
    st.info("Silakan unggah file audio di atas untuk memulai.")