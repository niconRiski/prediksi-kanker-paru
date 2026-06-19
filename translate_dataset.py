# File: translate_dataset.py
# PERUBAHAN: Sekarang bisa melanjutkan proses (resume) dan menangani teks panjang.

import pandas as pd
from deep_translator import GoogleTranslator
import time
import os

# --- Konfigurasi ---
INPUT_FILENAME = 'Disease and symptoms dataset.csv'
OUTPUT_FILENAME = 'dataset_indonesia.csv'
COLUMN_TO_TRANSLATE = 'gejala_lengkap'
SAVE_EVERY_N_ROWS = 500 # Simpan kemajuan setiap 500 baris
CHAR_LIMIT = 4500 # Batas aman karakter untuk API terjemahan

# --- Fungsi Pra-pemrosesan ---
def create_symptom_sentence(df):
    """Membaca dataset asli dan membuat kolom 'gejala_lengkap'."""
    print("Memuat dataset asli...")
    df.columns = df.columns.str.strip()
    if 'diseases' in df.columns:
        df.rename(columns={'diseases': 'Disease'}, inplace=True)
    
    symptom_columns = df.columns.drop('Disease')
    
    print("Menggabungkan gejala menjadi kalimat deskriptif...")
    symptom_data = df[symptom_columns]
    df[COLUMN_TO_TRANSLATE] = symptom_data.dot(symptom_columns + ' ').str.strip()
    
    return df[['Disease', COLUMN_TO_TRANSLATE]]

# --- [FUNGSI BARU] Untuk menerjemahkan teks panjang dengan aman ---
def translate_with_chunks(translator, text):
    """Menerjemahkan teks dengan memecahnya jika terlalu panjang."""
    if len(text) <= CHAR_LIMIT:
        return translator.translate(text)
    
    print(f"    -> Teks terlalu panjang ({len(text)} karakter), memecah menjadi beberapa bagian...")
    chunks = []
    current_chunk = ""
    for sentence in text.split('. '):
        if len(current_chunk) + len(sentence) + 1 > CHAR_LIMIT:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += ('. ' if current_chunk else '') + sentence
    chunks.append(current_chunk)
    
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"        -> Menerjemahkan bagian {i+1}/{len(chunks)}...")
        translated_chunks.append(translator.translate(chunk))
        time.sleep(1) # Beri jeda antar permintaan untuk menghindari blokir
        
    return '. '.join(translated_chunks)


# --- Fungsi Utama ---
def main():
    """Fungsi utama untuk menerjemahkan dataset dengan fitur checkpoint/resume."""
    
    # 1. Siapkan DataFrame Sumber
    if not os.path.exists(INPUT_FILENAME):
        print(f"[ERROR] File input '{INPUT_FILENAME}' tidak ditemukan.")
        return

    source_df = create_symptom_sentence(pd.read_csv(INPUT_FILENAME))
    source_df = source_df[source_df[COLUMN_TO_TRANSLATE] != ''].copy().reset_index(drop=True)

    # 2. Siapkan atau Muat DataFrame Hasil
    start_index = 0
    if os.path.exists(OUTPUT_FILENAME):
        print(f"File output '{OUTPUT_FILENAME}' ditemukan. Mencoba melanjutkan proses.")
        try:
            result_df = pd.read_csv(OUTPUT_FILENAME)
            if not result_df.empty:
                start_index = len(result_df)
                print(f"Proses akan dilanjutkan dari baris ke-{start_index + 1}.")
            else:
                print("File output kosong. Memulai dari awal.")
        except pd.errors.EmptyDataError:
            print("File output kosong. Memulai dari awal.")
            result_df = pd.DataFrame(columns=['Disease', 'gejala_indonesia'])
    else:
        print(f"File output '{OUTPUT_FILENAME}' tidak ditemukan. Memulai dari awal.")
        result_df = pd.DataFrame(columns=['Disease', 'gejala_indonesia'])

    # Jika sudah selesai, keluar.
    if start_index >= len(source_df):
        print("Selamat! Seluruh dataset sudah selesai diterjemahkan.")
        return
        
    # 3. Proses Penerjemahan
    translator = GoogleTranslator(source='en', target='id')
    
    print(f"\nMemulai proses penerjemahan dari baris {start_index + 1} hingga {len(source_df)}...")

    # Loop hanya pada sisa data yang belum diterjemahkan
    for index in range(start_index, len(source_df)):
        row = source_df.iloc[index]
        text_to_translate = row[COLUMN_TO_TRANSLATE]
        translated_text = ""
        
        for attempt in range(5): # Coba hingga 5 kali jika gagal
            try:
                # [PERUBAHAN] Gunakan fungsi baru yang lebih tangguh
                translated_text = translate_with_chunks(translator, text_to_translate)
                if translated_text: # Pastikan hasil tidak kosong
                    break
            except Exception as e:
                print(f"\n[WARNING] Gagal menerjemahkan baris #{index + 1}. Percobaan ke-{attempt + 1}. Error: {e}")
                print("Menunggu 20 detik sebelum mencoba lagi...")
                time.sleep(20)
        
        # Tambahkan hasil ke DataFrame sementara
        new_row = pd.DataFrame([{'Disease': row['Disease'], 'gejala_indonesia': translated_text}])
        result_df = pd.concat([result_df, new_row], ignore_index=True)
        
        # Tampilkan progres dan simpan secara berkala
        if (index + 1) % 100 == 0:
            print(f"Selesai menerjemahkan {index + 1} / {len(source_df)} baris...")
        
        if (index + 1) % SAVE_EVERY_N_ROWS == 0:
            print(f"\n--- MENYIMPAN KEMAJUAN ({index + 1} baris) ---")
            result_df.to_csv(OUTPUT_FILENAME, index=False)
            print(f"--- Kemajuan berhasil disimpan ke '{OUTPUT_FILENAME}' ---\n")

    # 4. Simpan hasil akhir
    result_df.to_csv(OUTPUT_FILENAME, index=False)
    print(f"\nPROSES SELESAI! Dataset berhasil diterjemahkan dan disimpan sebagai '{OUTPUT_FILENAME}'.")

if __name__ == '__main__':
    main()
