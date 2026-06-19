# File: train_lung_model.py
# VERSI FINAL (SINKRONISASI): Menggunakan features_config.json sebagai sumber kebenaran tunggal.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import joblib
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

def load_config(config_path='features_config.json'):
    """Memuat file konfigurasi JSON."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File konfigurasi '{config_path}' tidak ditemukan.")
        return None

def train():
    """Fungsi lengkap untuk melatih model berdasarkan konfigurasi fitur."""
    
    # --- 1. Memuat Konfigurasi Fitur sebagai "Sumber Kebenaran" ---
    feature_config = load_config()
    if not feature_config:
        return
        
    # Dapatkan daftar semua ID fitur dari konfigurasi
    # Ini adalah daftar kolom final yang harus dimiliki oleh model
    master_feature_list = [feature['id'] for feature in feature_config]
    print(f"[*] Konfigurasi fitur berhasil dimuat. Model akan dilatih dengan fitur berikut: {master_feature_list}")

    # --- 2. Memuat dan Memproses Dataset Pertama (survey lung cancer.csv) ---
    try:
        df1 = pd.read_csv('survey lung cancer.csv')
        print("\n[*] Dataset 1 'survey lung cancer.csv' berhasil dimuat.")
    except FileNotFoundError:
        print("[ERROR] File 'survey lung cancer.csv' tidak ditemukan.")
        return

    print("[*] Memulai pra-pemrosesan data 1...")
    df1['LUNG_CANCER'] = df1['LUNG_CANCER'].apply(lambda x: 1 if str(x).strip().upper() == 'YES' else 0)
    df1['GENDER'] = df1['GENDER'].apply(lambda x: 1 if str(x).strip().upper() == 'M' else 0)
    for col in df1.columns:
        if col not in ['AGE', 'GENDER', 'LUNG_CANCER']:
            df1[col] = df1[col].apply(lambda x: 1 if x == 2 else 0)
    
    df1.rename(columns={'FATIGUE ': 'FATIGUE', 'ALLERGY ': 'ALLERGY'}, inplace=True)
    print("[*] Pra-pemrosesan data 1 selesai.")

    # --- 3. Memuat dan Memproses Dataset Kedua (cancer patient data sets.csv) ---
    try:
        df2 = pd.read_csv('cancer patient data sets.csv')
        print("\n[*] Dataset 2 'cancer patient data sets.csv' berhasil dimuat.")
    except FileNotFoundError:
        print("[ERROR] File 'cancer patient data sets.csv' tidak ditemukan.")
        return
        
    print("[*] Memulai pra-pemrosesan data 2...")
    df2_rename_map = {
        'Age': 'AGE', 'Gender': 'GENDER', 'Air Pollution': 'AIR_POLLUTION', 'Alcohol use': 'ALCOHOL_CONSUMING',
        'Dust Allergy': 'ALLERGY', 'OccuPational Hazards': 'OCCUPATIONAL_HAZARDS', 'Genetic Risk': 'GENETIC_RISK',
        'chronic Lung Disease': 'CHRONIC_DISEASE', 'Balanced Diet': 'BALANCED_DIET', 'Obesity': 'OBESITY',
        'Smoking': 'SMOKING', 'Passive Smoker': 'PASSIVE_SMOKER', 'Chest Pain': 'CHEST_PAIN',
        'Coughing of Blood': 'COUGHING', 'Fatigue': 'FATIGUE', 'Weight Loss': 'WEIGHT_LOSS',
        'Shortness of Breath': 'SHORTNESS_OF_BREATH', 'Wheezing': 'WHEEZING', 'Swallowing Difficulty': 'SWALLOWING_DIFFICULTY',
        'Clubbing of Finger Nails': 'CLUBBING_OF_FINGER_NAILS', 'Frequent Cold': 'FREQUENT_COLD',
        'Dry Cough': 'DRY_COUGH', 'Snoring': 'SNORING', 'Level': 'LUNG_CANCER'
    }
    df2.rename(columns=df2_rename_map, inplace=True)
    df2.drop(['Patient Id', 'index'], axis=1, inplace=True, errors='ignore')

    df2['GENDER'] = df2['GENDER'].apply(lambda x: 1 if x == 1 else 0) 
    df2['LUNG_CANCER'] = df2['LUNG_CANCER'].apply(lambda x: 1 if str(x).strip().upper() in ['HIGH', 'MEDIUM'] else 0)
    
    for col in df2.columns:
        if col not in ['AGE', 'GENDER', 'LUNG_CANCER']:
            df2[col] = pd.to_numeric(df2[col], errors='coerce').fillna(0).apply(lambda x: 1 if x > 3 else 0)
    print("[*] Pra-pemrosesan data 2 selesai.")

    # --- 4. Menggabungkan dan Menyelaraskan Dataset dengan Konfigurasi ---
    print("\n[*] Menggabungkan dan menyelaraskan dataset...")
    df_combined = pd.concat([df1, df2], ignore_index=True, sort=False)
    
    # Buat dataframe final dengan SEMUA kolom dari master list, isi data yang ada, dan sisanya 0
    final_cols = master_feature_list + ['LUNG_CANCER']
    df_final = pd.DataFrame(columns=final_cols)

    for col in final_cols:
        if col in df_combined.columns:
            df_final[col] = df_combined[col]
        else:
            df_final[col] = 0 # Jika kolom tidak ada di data gabungan, isi dengan 0
            
    df_final.fillna(0, inplace=True)
    
    # Pastikan tipe data benar
    for col in df_final.columns:
        if col != 'LUNG_CANCER':
             df_final[col] = df_final[col].astype(int)
    df_final['LUNG_CANCER'] = df_final['LUNG_CANCER'].astype(int)

    print(f"[*] Total data setelah digabung dan diselaraskan: {len(df_final)} baris.")
    
    # --- 5. Melatih Model dengan Data yang Sudah Selaras ---
    X = df_final[master_feature_list] # Gunakan master list untuk memastikan urutan dan kelengkapan kolom
    y = df_final['LUNG_CANCER']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("\n--- Menyeimbangkan Data Latih dengan SMOTE ---")
    print(f"Distribusi kelas sebelum SMOTE: \n{y_train.value_counts()}")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    print(f"\nDistribusi kelas setelah SMOTE: \n{y_train_resampled.value_counts()}")
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    print("\n[*] Memulai pelatihan model dengan data gabungan...")
    model.fit(X_train_resampled, y_train_resampled)
    print("[*] Pelatihan model selesai.")
    
    # --- 6. Evaluasi dan Penyimpanan ---
    y_pred = model.predict(X_test)
    print(f"\n[*] Akurasi final model: {accuracy_score(y_test, y_pred):.2f}")
    print("\n[*] Laporan Klasifikasi Final:\n", classification_report(y_test, y_pred, target_names=['Berisiko Rendah', 'Berisiko Tinggi']))

    # Visualisasi dan penyimpanan model
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': importances}).sort_values(by='importance', ascending=False)
    
    plt.figure(figsize=(12, 10))
    sns.barplot(x='importance', y='feature', data=feature_importance_df, palette='viridis', hue='feature', legend=False)
    plt.title('Pentingnya Faktor Risiko Menurut Model (Data Gabungan & Selaras)', fontsize=16)
    plt.tight_layout()
    
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    plt.savefig(os.path.join(models_dir, 'feature_importance.png'))
    print(f"\n[*] Grafik Feature Importance disimpan di: {os.path.join(models_dir, 'feature_importance.png')}")

    joblib.dump(model, os.path.join(models_dir, 'lung_risk_classifier.pkl'))
    print(f"[*] Model terbaik disimpan di: {os.path.join(models_dir, 'lung_risk_classifier.pkl')}")
    
    # Simpan informasi kolom berdasarkan master list dari JSON
    with open(os.path.join(models_dir, 'model_info.json'), 'w') as f:
        json.dump({'columns': master_feature_list}, f, indent=4)
    print(f"[*] Informasi kolom disimpan di: {os.path.join(models_dir, 'model_info.json')}")

    print("\n--- Proses Selesai ---")

if __name__ == '__main__':
    train()
