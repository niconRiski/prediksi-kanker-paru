# 🫁 Prediksi Risiko Kanker Paru-Paru (Lung Cancer Risk Prediction)

Aplikasi sistem berbasis pengetahuan (Machine Learning) yang dirancang untuk melakukan skrining awal dan memprediksi tingkat risiko kanker paru-paru berdasarkan data medis, gaya hidup, serta gejala klinis pengguna.

## 📌 Fungsi Utama
Sistem ini berfungsi sebagai alat deteksi dini mandiri (*self-screening tool*). Pengguna cukup mengisi formulir interaktif yang berisi 26 pertanyaan seputar kebiasaan sehari-hari (seperti merokok, paparan polusi) serta riwayat kesehatan. Sistem kemudian akan memproses data tersebut dan menampilkan hasil berupa **Tingkat Risiko** ("Berisiko Tinggi" atau "Berisiko Rendah") beserta **Persentase Skor Risiko** dan saran medis awal.

## ✨ Fitur Unggulan
1. **Analisis Sangat Komprehensif (26 Faktor):** Mempertimbangkan berbagai variabel mendetail yang diatur di dalam `features_config.json`, mulai dari faktor lingkungan hingga gejala spesifik seperti kuku jari membulat (*clubbing*) dan batuk berdarah.
2. **Peta Fasilitas Kesehatan Terdekat (Otomatis):** Jika pengguna terdeteksi memiliki risiko lebih dari 50%, sistem akan mengaktifkan GPS dan memunculkan peta interaktif (Leaflet.js) yang melacak Rumah Sakit atau Klinik terdekat dalam radius 5 km.
3. **Formulir yang Dinamis (JSON-Driven):** Seluruh input formulir di-*generate* secara otomatis dari file JSON, membuat sistem ini sangat fleksibel untuk diperbarui di masa depan tanpa harus merombak kode utama.
4. **Antarmuka Modern (Responsive UI):** Menggunakan Tailwind CSS untuk menghasilkan antarmuka yang ramah pengguna, lengkap dengan *splash screen*, animasi loading, dan desain yang memanjakan mata di PC maupun ponsel.

## 🛠️ Detail Sistem & Teknologi
Proyek ini mengadopsi arsitektur *Client-Server* yang dipadukan dengan kecerdasan buatan:
*   **Algoritma Machine Learning:** Menggunakan `Random Forest Classifier` (via *scikit-learn*). Model ini sangat akurat dalam menemukan pola tersembunyi dari berbagai kombinasi gejala medis.
*   **Penanganan Data Bias (SMOTE):** Karena data medis seringkali tidak seimbang, sistem ini menggunakan teknik *Synthetic Minority Over-sampling Technique* (SMOTE) saat pelatihan agar model tidak menebak secara "bias".
*   **Dataset Gabungan:** Model dilatih dengan mengkombinasikan dua dataset berbeda untuk menghasilkan wawasan prediksi yang lebih luas dan akurat.
*   **Backend:** Python + Flask Framework.
*   **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS, dan Leaflet.js.

## 📊 Hasil Pelatihan Model (Training Log)
Sistem ini dilatih menggunakan gabungan dataset sebanyak 1.309 data pasien dan berhasil mencapai tingkat **Akurasi 98%**. Berikut adalah log terminal proses *training*-nya:

```text
[*] Konfigurasi fitur berhasil dimuat. Model akan dilatih dengan fitur berikut: ['AGE', 'GENDER', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH', 'SWALLOWING_DIFFICULTY', 'CHEST_PAIN', 'AIR_POLLUTION', 'OCCUPATIONAL_HAZARDS', 'GENETIC_RISK', 'BALANCED_DIET', 'OBESITY', 'PASSIVE_SMOKER', 'WEIGHT_LOSS', 'CLUBBING_OF_FINGER_NAILS', 'FREQUENT_COLD', 'DRY_COUGH', 'SNORING']

[*] Dataset 1 'survey lung cancer.csv' berhasil dimuat.
[*] Memulai pra-pemrosesan data 1...
[*] Pra-pemrosesan data 1 selesai.

[*] Dataset 2 'cancer patient data sets.csv' berhasil dimuat.
[*] Memulai pra-pemrosesan data 2...
[*] Pra-pemrosesan data 2 selesai.

[*] Menggabungkan dan menyelaraskan dataset...
[*] Total data setelah digabung dan diselaraskan: 1309 baris.

--- Menyeimbangkan Data Latih dengan SMOTE ---
Distribusi kelas sebelum SMOTE:
LUNG_CANCER
1    773
0    274
Name: count, dtype: int64

Distribusi kelas setelah SMOTE:
LUNG_CANCER
1    773
0    773
Name: count, dtype: int64

[*] Memulai pelatihan model dengan data gabungan...
[*] Pelatihan model selesai.

[*] Akurasi final model: 0.98

[*] Laporan Klasifikasi Final:
                  precision    recall  f1-score   support

Berisiko Rendah       0.97      0.97      0.97        68
Berisiko Tinggi       0.99      0.99      0.99       194

       accuracy                           0.98       262
      macro avg       0.98      0.98      0.98       262
   weighted avg       0.98      0.98      0.98       262


[*] Grafik Feature Importance disimpan di: models\feature_importance.png
[*] Model terbaik disimpan di: models\lung_risk_classifier.pkl
[*] Informasi kolom disimpan di: models\model_info.json
```
<img width="1278" height="977" alt="image" src="https://github.com/user-attachments/assets/ae0b53fb-45d0-4b65-a2f4-f1132f19fb17" />
<img width="1271" height="980" alt="image" src="https://github.com/user-attachments/assets/0b80a45d-feb7-4333-ba22-52126d1fb5bc" />
<img width="1267" height="917" alt="image" src="https://github.com/user-attachments/assets/9859044b-898e-4e72-91d2-4549dbc973c5" />
<img width="1274" height="980" alt="image" src="https://github.com/user-attachments/assets/ea42a609-6864-4754-bd76-a62a7f63017b" />
