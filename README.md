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

<img width="1278" height="977" alt="image" src="https://github.com/user-attachments/assets/ae0b53fb-45d0-4b65-a2f4-f1132f19fb17" />
<img width="1271" height="980" alt="image" src="https://github.com/user-attachments/assets/0b80a45d-feb7-4333-ba22-52126d1fb5bc" />
<img width="1267" height="917" alt="image" src="https://github.com/user-attachments/assets/9859044b-898e-4e72-91d2-4549dbc973c5" />
<img width="1274" height="980" alt="image" src="https://github.com/user-attachments/assets/ea42a609-6864-4754-bd76-a62a7f63017b" />
