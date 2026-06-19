/* File: static/css/style.css */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f4f7f6;
    color: #333;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
}

.container {
    width: 90%;
    max-width: 800px;
    background: #fff;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

header {
    text-align: center;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
    margin-bottom: 20px;
}

h1 {
    color: #0056b3;
}

textarea {
    width: 100%;
    height: 120px;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
    margin-bottom: 15px;
    box-sizing: border-box;
}

button {
    display: block;
    width: 100%;
    padding: 15px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #0056b3;
}

.results-area {
    margin-top: 30px;
}

.result-summary {
    font-size: 1.2em;
    margin-bottom: 20px;
}

.badge {
    padding: 5px 15px;
    border-radius: 15px;
    color: white;
    font-weight: bold;
}

.badge.Rendah { background-color: #28a745; }
.badge.Sedang { background-color: #ffc107; color: #333; }
.badge.Tinggi { background-color: #dc3545; }

.visualization {
    max-width: 500px;
    margin: auto;
}