// File: static/js/script.js

// Tunggu hingga semua elemen halaman dimuat
document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const symptomInput = document.getElementById('symptom-input');
    const resultsContainer = document.getElementById('results-container');
    const severityLevel = document.getElementById('severity-level');
    const chartCanvas = document.getElementById('symptom-chart');
    const keywordChartCanvas = document.getElementById('keyword-chart');
    const loadingSpinner = document.getElementById('loading');
    const treatmentSuggestionsDiv = document.getElementById('treatment-suggestions');
    const messageBox = document.getElementById('message-box');

    // Voice Input (SpeechRecognition) elements
    const startVoiceInputBtn = document.getElementById('start-voice-input-btn');
    const stopVoiceInputBtn = document.getElementById('stop-voice-input-btn');

    // Voice Output (SpeechSynthesis) elements
    const readResultsBtn = document.getElementById('read-results-btn');

    let symptomChart = null;
    let keywordFreqChart = null;

    // --- Speech Recognition (Voice Input) setup ---
    let recognition = null;
    let isListening = false; // NEW: Status untuk melacak apakah sedang mendengarkan

    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true; // NEW: Terus mendengarkan
        recognition.interimResults = true; // NEW: Menampilkan hasil sementara
        recognition.lang = 'id-ID'; // Bahasa Indonesia

        recognition.onstart = () => {
            isListening = true;
            displayMessage('Mendengarkan... Ucapkan gejala Anda.', 'info');
            startVoiceInputBtn.classList.add('hidden');
            stopVoiceInputBtn.classList.remove('hidden');
            symptomInput.placeholder = 'Sedang mendengarkan dan mengetik...'; // Umpan balik yang lebih jelas
            symptomInput.classList.add('bg-blue-50', 'placeholder-blue-600'); // Indikator visual
            symptomInput.focus(); // Fokus pada input
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            // Tampilkan hasil final jika ada, jika tidak, tampilkan interim
            symptomInput.value = finalTranscript || interimTranscript;
            // Jika ada interim, berikan umpan balik visual bahwa ini belum final
            if (interimTranscript && !finalTranscript) {
                symptomInput.placeholder = `Sedang mendengarkan: "${interimTranscript}"`;
            } else {
                symptomInput.placeholder = 'Tekan Stop Bicara jika sudah selesai.';
            }
        };

        recognition.onend = () => {
            isListening = false;
            // Hanya tampilkan pesan onend jika tidak ada error yang memicu penghentian
            // dan jika ini bukan hasil dari penghentian manual oleh pengguna setelah continuous
            if (!symptomInput.classList.contains('bg-red-100')) { // Cek jika bukan error state
                displayMessage('Pengenalan suara selesai. Klik Analisis Gejala.', 'info');
            }
            startVoiceInputBtn.classList.remove('hidden');
            stopVoiceInputBtn.classList.add('hidden');
            symptomInput.classList.remove('bg-blue-50', 'placeholder-blue-600');
            symptomInput.placeholder = 'Contoh: Saya merasa pusing, demam tinggi sejak kemarin...';
        };

        recognition.onerror = (event) => {
            isListening = false;
            console.error('Speech Recognition Error:', event.error);
            let errorMessage = 'Terjadi kesalahan pada pengenalan suara.';
            if (event.error === 'not-allowed') {
                errorMessage = 'Izin mikrofon ditolak. Mohon izinkan akses mikrofon di browser Anda.';
            } else if (event.error === 'no-speech') {
                errorMessage = 'Tidak ada ucapan terdeteksi. Pastikan mikrofon Anda berfungsi dan coba lagi.';
            } else if (event.error === 'network') {
                errorMessage = 'Kesalahan jaringan saat pengenalan suara. Pastikan koneksi internet stabil.';
            } else if (event.error === 'aborted') {
                 errorMessage = 'Pengenalan suara dibatalkan.'; // Saat stop secara manual
            }
            displayMessage(errorMessage, 'error');
            startVoiceInputBtn.classList.remove('hidden');
            stopVoiceInputBtn.classList.add('hidden');
            symptomInput.classList.remove('bg-blue-50', 'placeholder-blue-600');
            symptomInput.placeholder = 'Contoh: Saya merasa pusing, demam tinggi sejak kemarin...';
        };

        startVoiceInputBtn.addEventListener('click', () => {
            if (!isListening) { // Only start if not already listening
                symptomInput.value = ''; // Bersihkan input sebelumnya sebelum mendengarkan
                recognition.start();
            } else {
                displayMessage('Pengenalan suara sudah aktif.', 'info');
            }
        });
        stopVoiceInputBtn.addEventListener('click', () => {
            if (isListening) { // Only stop if currently listening
                recognition.stop();
            }
        });
    } else {
        displayMessage('API Pengenalan Suara tidak didukung oleh browser Anda. Mohon gunakan Chrome atau Edge terbaru.', 'error');
        startVoiceInputBtn.classList.add('hidden'); // Sembunyikan tombol jika tidak didukung
        stopVoiceInputBtn.classList.add('hidden');
    }

    // --- Speech Synthesis (Voice Output) setup ---
    const synth = window.speechSynthesis;
    let doctorVoice = null;

    const getIndonesianDoctorVoice = () => {
        const voices = synth.getVoices();
        let selectedVoice = voices.find(voice => voice.lang === 'id-ID' && voice.name.includes('Google') && !voice.name.includes('Wavenet')) ||
                           voices.find(voice => voice.lang === 'id-ID' && (voice.name.includes('Male') || voice.name.includes('Female'))) ||
                           voices.find(voice => voice.lang.startsWith('id'));
        return selectedVoice;
    };

    synth.onvoiceschanged = () => {
        doctorVoice = getIndonesianDoctorVoice();
        if (!doctorVoice) {
            console.warn('Tidak dapat menemukan suara Bahasa Indonesia yang cocok. Menggunakan suara default.');
        }
    };
    if (synth.getVoices().length > 0) {
        doctorVoice = getIndonesianDoctorVoice();
    }

    const speakText = (text) => {
        if (synth.speaking) {
            synth.cancel();
        }
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'id-ID';
        if (doctorVoice) {
            utterance.voice = doctorVoice;
        } else {
            console.warn("Menggunakan suara default untuk Text-to-Speech karena suara dokter tidak ditemukan.");
        }
        
        utterance.onerror = (event) => {
            console.error('Speech Synthesis Error:', event.error);
            displayMessage('Terjadi kesalahan saat membacakan hasil.', 'error');
        };

        synth.speak(utterance);
    };

    const displayMessage = (message, type = 'info') => {
        messageBox.textContent = message;
        messageBox.classList.remove('hidden', 'bg-red-100', 'text-red-700', 'bg-green-100', 'text-green-700', 'bg-blue-100', 'text-blue-700');
        
        if (type === 'error') {
            messageBox.classList.add('bg-red-100', 'text-red-700');
        } else if (type === 'success') {
            messageBox.classList.add('bg-green-100', 'text-green-700');
        } else {
            messageBox.classList.add('bg-blue-100', 'text-blue-700');
        }
        messageBox.classList.remove('hidden');
        
        setTimeout(() => {
            messageBox.classList.add('hidden');
            messageBox.textContent = '';
        }, 5000);
    };

    const analyzeSymptoms = async () => {
        const symptomsText = symptomInput.value.trim();
        if (symptomsText === '') {
            displayMessage('Mohon masukkan deskripsi gejala Anda.', 'error');
            return;
        }

        if (synth.speaking) {
            synth.cancel();
        }
        if (isListening) { // Stop listening if still active when analysis button is clicked
            recognition.stop(); 
        }

        loadingSpinner.style.display = 'block';
        resultsContainer.style.display = 'none';
        treatmentSuggestionsDiv.textContent = '';
        if (symptomChart) symptomChart.destroy();
        if (keywordFreqChart) keywordChart.destroy();

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms: symptomsText }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Gagal mendapatkan respons dari server.');
            }

            const data = await response.json();
            displayResults(data);
            displayMessage('Analisis berhasil!', 'success');

        } catch (error) {
            console.error('Error:', error);
            displayMessage(`Terjadi kesalahan: ${error.message}`, 'error');
        } finally {
            loadingSpinner.style.display = 'none';
        }
    };

    const displayResults = (data) => {
        resultsContainer.style.display = 'block';

        severityLevel.textContent = data.severity;
        severityLevel.className = `badge ${data.severity}`;

        const vizData = data.visualization;
        if (symptomChart) {
            symptomChart.destroy();
        }
        
        symptomChart = new Chart(chartCanvas, {
            type: 'radar',
            data: {
                labels: vizData.labels,
                datasets: [{
                    label: 'Skor Faktor Keparahan',
                    data: vizData.scores,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                }]
            },
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                },
                scales: {
                    r: {
                        angleLines: { display: false },
                        suggestedMin: 0,
                        suggestedMax: 1
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        const keywordData = data.keyword_frequencies;
        if (keywordFreqChart) {
            keywordFreqChart.destroy();
        }

        if (keywordData && keywordData.labels.length > 0) {
            keywordFreqChart = new Chart(keywordChartCanvas, {
                type: 'bar',
                data: {
                    labels: keywordData.labels,
                    datasets: [{
                        label: 'Frekuensi Kata Kunci',
                        data: keywordData.counts,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Jumlah Kemunculan'
                            },
                            ticks: {
                                precision: 0
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Kata Kunci'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        } else {
            if (keywordChartCanvas) {
                const ctx = keywordChartCanvas.getContext('2d');
                ctx.clearRect(0, 0, keywordChartCanvas.width, keywordChartCanvas.height);
            }
        }

        if (data.suggestions) {
            treatmentSuggestionsDiv.textContent = data.suggestions;
        } else {
            treatmentSuggestionsDiv.textContent = 'Tidak ada saran yang tersedia.';
        }
    };

    const clearInputAndResults = () => {
        symptomInput.value = '';
        resultsContainer.style.display = 'none';
        treatmentSuggestionsDiv.textContent = '';
        
        if (symptomChart) {
            symptomChart.destroy();
            symptomChart = null;
        }
        if (keywordFreqChart) {
            keywordFreqChart.destroy();
            keywordFreqChart = null;
        }
        if (synth.speaking) {
            synth.cancel();
        }
        if (isListening) { // Stop listening if active
            recognition.stop(); 
        }
        displayMessage('Input dan hasil telah dibersihkan.', 'info');
    };

    // Tambahkan event listener ke tombol
    analyzeBtn.addEventListener('click', analyzeSymptoms);
    clearBtn.addEventListener('click', clearInputAndResults);

    readResultsBtn.addEventListener('click', () => {
        const severityText = `Tingkat keparahan: ${severityLevel.textContent}.`;
        const suggestionsText = treatmentSuggestionsDiv.textContent;
        
        // **START MODIFICATION**
        let severityFactorsText = "Berikut adalah faktor-faktor keparahan: ";
        if (symptomChart && symptomChart.data.labels && symptomChart.data.scores) {
            symptomChart.data.labels.forEach((label, index) => {
                const score = (symptomChart.data.datasets[0].data[index] * 100).toFixed(0); // Convert to percentage
                severityFactorsText += `${label} dengan skor ${score} persen; `;
            });
        } else {
            severityFactorsText += "Data faktor keparahan tidak tersedia. ";
        }
        // **END MODIFICATION**

        const fullTextToSpeak = `${severityText} ${severityFactorsText} ${suggestionsText}`;
        speakText(fullTextToSpeak);
    });

    const observer = new MutationObserver((mutationsList) => {
        for(let mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                if (resultsContainer.style.display === 'block') {
                    readResultsBtn.classList.remove('hidden');
                } else {
                    readResultsBtn.classList.add('hidden');
                    if (synth.speaking) {
                        synth.cancel();
                    }
                }
            }
        }
    });
    observer.observe(resultsContainer, { attributes: true });
    if (resultsContainer.style.display === 'block') {
        readResultsBtn.classList.remove('hidden');
    } else {
        readResultsBtn.classList.add('hidden');
    }
});