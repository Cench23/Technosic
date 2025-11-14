🎵 Tecnosic - Analisis Fitur & Pemisah Vokal AI

Ini adalah proyek Ujian Akhir Semester (UAS) untuk mata kuliah Aplikasi Web, dibuat dengan Streamlit dan Python.

Tecnosic adalah aplikasi web berbasis AI yang bisa "membedah" file audio menjadi bagian-bagian utamanya (Vokal, Bass, Drum, Instrumen Lain) dan menganalisis fitur-fiturnya (BPM, Tangga Nada, Durasi).

**🚀 Fitur Utama**

**Analisis Fitur (Backend: librosa)**

Deteksi Tempo (BPM)

Deteksi Estimasi Tangga Nada (Key)

Kalkulasi Durasi (Detik)

Visualisasi Waveform

**Pemisahan AI (Backend: demucs)**

Mengekstrak Vokal (vocals.mp3)

Mengekstrak Bass (bass.mp3)

Mengekstrak Drums (drums.mp3)

Mengekstrak Instrumen Lain (other.mp3)

**⚠️ PENTING:**

Aplikasi ini TIDAK BISA di-deploy di hosting gratis (Streamlit Cloud, Heroku) karena 2 alasan utama:

Kebutuhan RAM Tinggi: Model AI Demucs + PyTorch membutuhkan > 2GB RAM, sementara hosting gratis hanya menyediakan 1GB.

Ketergantungan Rumit (FFmpeg): Aplikasi ini bergantung pada FFmpeg v7.0 (Shared Build) yang harus diinstal secara manual.

Untuk menjalankan proyek ini di laptop Windows Anda, ikuti langkah-langkah environment setup berikut:

**1. Fondasi (Python 3.11):**

Download dan install Python 3.11 (Pastikan centang Add to PATH).

**2. Buat "Garasi" (VENV):**

# Buat folder proyek
mkdir ProyekTecnosic
cd ProyekTecnosic

# Buat venv menggunakan Python 3.11
py -3.11 -m venv venv

# Aktifkan venv
.\venv\Scripts\activate


**3. Install "Alat-Alat" (Libraries):**

# (Pastikan (venv) sudah aktif)
pip install streamlit
pip install librosa
pip install torch torchaudio --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)
pip install demucs
pip install torchcodec
pip install soundfile

# (Kita uninstall torchcodec untuk mem-bypass error FFmpeg saat load)
pip uninstall torchcodec


**4. Install "Alat Berat" (FFmpeg v7.0 Manual):**

Download: ffmpeg-7.0-full_build-shared.7z (HARUS yang -shared) dari link ini.

Ekstrak file tersebut.

Masuk ke folder bin di dalamnya.

Copy SEMUA file (termasuk ffmpeg.exe dan semua file .dll).

Paste semua file tersebut ke dalam folder venv Anda di: .\venv\Scripts\

**5. Jalankan Aplikasi:**

(Pastikan venv aktif dan FFmpeg sudah di-copy)

Restart VS Code Anda.

Jalankan:

streamlit run app.py
