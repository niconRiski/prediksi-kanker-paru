# File: main_lung_app.py
# PERUBAHAN FINAL: Dikonfigurasi ulang untuk menjadi server web yang menyajikan semua file proyek.

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import os
import json
import numpy as np

# --- [DIUBAH] Inisialisasi Aplikasi Flask dengan cara standar ---
# 'template_folder' akan memberitahu Flask untuk mencari index.html di dalam folder 'templates'
# 'static_folder' akan memberitahu Flask untuk mencari file lain (video, json) di folder 'static'
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# --- Variabel Global ---
MODEL_PATH = os.path.join('models', 'lung_risk_classifier.pkl')
INFO_PATH = os.path.join('models', 'model_info.json')
CONFIG_PATH = 'features_config.json' # Path ke file config
model = None
model_info = None

# --- Fungsi untuk Memuat Model dan Info ---
def load_resources():
    """Memuat model dan informasi kolom fitur saat server dimulai."""
    global model, model_info
    try:
        model = joblib.load(MODEL_PATH)
        with open(INFO_PATH, 'r') as f:
            model_info = json.load(f)
        print("[*] Model dan informasi pendukung berhasil dimuat.")
    except Exception as e:
        print(f"[!!!] KESALAHAN KRITIS: Gagal memuat model. Pastikan 'train_lung_model.py' sudah dijalankan. Error: {e}")
        model = None

# --- [DIUBAH] Route Utama untuk Menyajikan Halaman Web ---
@app.route('/')
def root():
    """Menyajikan file index.html dari folder 'templates'."""
    return render_template('index.html')

# --- [BARU] Route untuk menyajikan file features_config.json ---
@app.route('/features_config.json')
def features_config():
    """Menyajikan file konfigurasi JSON dari folder utama."""
    return send_from_directory('.', 'features_config.json')


# --- Fungsi untuk mengubah data dari formulir menjadi format yang benar ---
def form_data_to_features(data, columns):
    """Mengubah data JSON dari form menjadi array numerik yang siap untuk model."""
    features_encoded = []
    
    input_data = {key.upper(): int(value) for key, value in data.items()}
    print("\n--- Menerima data dari formulir ---")
    print(input_data)

    for col in columns:
        value = input_data.get(col, 0)
        features_encoded.append(value)
    
    print(f"[*] Array fitur yang dikirim ke model: {features_encoded}")
    return np.array(features_encoded).reshape(1, -1)

# --- Route API untuk Analisis ---
@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Menerima data dari formulir, melakukan prediksi, dan mengirimkan hasil."""
    if not model or not model_info:
        return jsonify({"error": "Model tidak siap. Periksa log server."}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request tidak valid. Tidak ada data yang diterima."}), 400

        feature_columns = model_info['columns']
        features = form_data_to_features(data, feature_columns)
        
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        
        high_risk_index = np.where(model.classes_ == 1)[0][0]
        risk_score_percent = prediction_proba[high_risk_index] * 100

        response_data = {
            "riskLevel": "Berisiko Tinggi" if prediction == 1 else "Berisiko Rendah",
            "riskScore": f"{risk_score_percent:.0f}%",
            "suggestions": (
                "Berdasarkan analisis, Anda memiliki risiko tinggi terhadap penyakit paru-paru. Sangat disarankan untuk segera berkonsultasi dengan dokter spesialis."
                if prediction == 1 else
                "Berdasarkan analisis, risiko Anda tergolong rendah. Tetap pertahankan gaya hidup sehat dan hindari merokok."
            )
        }
        return jsonify(response_data)
    except Exception as e:
        print(f"[!!!] Error kritis saat prediksi: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Terjadi kesalahan internal saat melakukan analisis."}), 500

# --- Menjalankan Aplikasi ---
if __name__ == '__main__':
    load_resources()
    app.run(host='127.0.0.1', port=5000, debug=True)
