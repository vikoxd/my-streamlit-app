#  Pengembangan Aplikasi Analisis Pola Belanja E-Commerce Menggunakan Association Rule Mining dan K-Means Clustering Berbasis Data Mining

##  Deskripsi Project

Project ini merupakan tugas akhir mata kuliah Data Mining yang bertujuan untuk menganalisis pola perilaku pelanggan pada bisnis e-commerce menggunakan metode **RFM (Recency, Frequency, Monetary)** dan membangun model **Machine Learning** untuk melakukan prediksi segmentasi pelanggan.

Analisis dilakukan menggunakan dataset **Online Retail** dari UCI Machine Learning Repository yang berisi data transaksi pelanggan sebuah toko retail online. Hasil analisis diharapkan dapat membantu perusahaan memahami karakteristik pelanggan sehingga strategi pemasaran dapat dilakukan secara lebih efektif dan tepat sasaran.



##  Tujuan Project

* Menganalisis perilaku pelanggan berdasarkan metode RFM.
* Mengelompokkan pelanggan ke dalam beberapa segmen berdasarkan karakteristik pembeliannya.
* Membangun model machine learning untuk memprediksi segmen pelanggan baru.
* Menyediakan dashboard interaktif berbasis Streamlit untuk memudahkan visualisasi dan prediksi.



##  Dataset

Dataset yang digunakan adalah **Online Retail Dataset** dari UCI Machine Learning Repository.

### Informasi Dataset

* Jumlah data: ±541.909 transaksi
* Periode transaksi: Desember 2010 – Desember 2011
* Negara dominan: United Kingdom

### Atribut Utama

| Kolom       | Deskripsi         |
| ----------- | ----------------- |
| InvoiceNo   | Nomor transaksi   |
| StockCode   | Kode produk       |
| Description | Nama produk       |
| Quantity    | Jumlah produk     |
| InvoiceDate | Tanggal transaksi |
| UnitPrice   | Harga satuan      |
| CustomerID  | ID pelanggan      |
| Country     | Negara pelanggan  |

---

##  Metodologi

### 1. Data Preprocessing

Tahapan preprocessing meliputi:

* Menghapus data kosong (missing value)
* Menghapus transaksi pembatalan (cancelled transaction)
* Menghapus data duplikat
* Konversi tipe data tanggal

### 2. Perhitungan RFM

Setiap pelanggan dihitung berdasarkan:

* **Recency (R)** : Jarak waktu sejak transaksi terakhir
* **Frequency (F)** : Frekuensi transaksi pelanggan
* **Monetary (M)** : Total nilai pembelian pelanggan

### 3. Feature Engineering

* Normalisasi data
* Pembuatan fitur RFM Score
* Labeling segment pelanggan

### 4. Machine Learning

Model machine learning digunakan untuk memprediksi segmen pelanggan berdasarkan nilai RFM yang dimiliki pelanggan.

### 5. Deployment

Model diimplementasikan menggunakan **Streamlit** sehingga pengguna dapat melakukan prediksi secara langsung melalui antarmuka web.



##  Fitur Aplikasi

### Home

Menampilkan informasi umum mengenai project, tujuan analisis, serta gambaran sistem.

### Dataset Overview

Menampilkan informasi dataset, statistik deskriptif, dan hasil preprocessing data.

### Prediction

Memungkinkan pengguna memasukkan nilai Recency, Frequency, dan Monetary untuk memprediksi segmen pelanggan.

### Visualization

Menampilkan berbagai visualisasi data seperti:

* Distribusi pelanggan
* Distribusi RFM
* Segmentasi pelanggan
* Insight hasil analisis

### About

Berisi informasi mengenai project, teknologi yang digunakan, serta pengembang aplikasi.



##  Teknologi yang Digunakan

* Python
* Pandas
* NumPy
* Scikit-Learn
* Matplotlib
* Seaborn
* Plotly
* Streamlit
* GitHub

---

##  Struktur Project

```text
UAS_DataMining_vikofalah/
│
├── data/
│   └── Online Retail.xlsx
│
├── models/
│   └── model.pkl
│
├── pages/
│   ├── Dataset_Overview.py
│   ├── Prediction.py
│   ├── Visualization.py
│   └── About.py
│
├── Home.py
├── requirements.txt
├── README.md
└── assets/
```

---

##  Cara Menjalankan Project

### Clone Repository

```bash
git clone https://github.com/vikoxd/UAS_DataMining_vikofalah.git
```

### Masuk ke Folder Project

```bash
cd UAS_DataMining_vikofalah
```

### Install Dependency

```bash
pip install -r requirements.txt
```

### Jalankan Streamlit

```bash
streamlit run app.py
```

---

## Deployment

Aplikasi telah di-deploy menggunakan Streamlit Community Cloud dan terhubung dengan repository GitHub sehingga setiap pembaruan pada branch utama dapat langsung diterapkan ke aplikasi.

---

##  Mata Kuliah

Data Mining

Program Studi Sistem Informasi

Universitas Negeri Surabaya (UNESA)

---

##  Pengembang

**Moh Viko Nur Huda | 24051214076

Moh Fajrul Falah    | 24051214076**

Project Akhir Mata Kuliah Data Mining

2026
