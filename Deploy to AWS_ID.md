# Deployment using AWS EC2

Sebelum mengikuti petunjuk lebih lanjut, pastikan Anda telah mencoba menjalankan Python Bot secara lokal terlebih dahulu. Anda juga perlu memiliki akun AWS sebelum melakukan deployment.

# Table of Contents

- [Deployment using AWS EC2](#deployment-using-aws-ec2)
- [Table of Contents](#table-of-contents)
- [Mengapa AWS EC2?](#mengapa-aws-ec2)
- [Cara Menggunakan AWS EC2](#cara-menggunakan-aws-ec2)
  - [Buat EC2 Instance](#buat-ec2-instance)
  - [Akses EC2 Instance Menggunakan SSH](#akses-ec2-instance-menggunakan-ssh)
  - [Install Python dan Git di EC2 Instance](#install-python-dan-git-di-ec2-instance)
  - [Clone Source Code dari GitHub](#clone-source-code-dari-github)
  - [Membuat Virtual Environment dan Install Dependencies](#membuat-virtual-environment-dan-install-dependencies)
  - [Mengatur konfigurasi](#mengatur-konfigurasi)
  - [Menjalankan Bot Python](#menjalankan-bot-python)
  - [Tips: Menjaga Bot Tetap Berjalan](#tips-menjaga-bot-tetap-berjalan)

# Mengapa AWS EC2?

Menyediakan layanan gratis untuk penggunaan ringan selama 1 tahun (AWS Free Tier). Layanan ini sangat fleksibel dan cocok untuk proyek yang lebih kompleks. Buka [link](https://aws.amazon.com/ec2) untuk mendaftar.

# Cara Menggunakan AWS EC2

Berikut ini adalah langkah-langkah untuk menggunakan AWS EC2 dan menjalankan kode sumber Python dari GitHub di server tersebut. Pastikan Anda memiliki akun AWS dan sudah masuk.

## Buat EC2 Instance

Catatan: Kita hanya akan menggunakan Free Tier saja.

1. Buka **[AWS Management Console](https://console.aws.amazon.com/)**.

2. Pergi ke layanan **EC2** dengan mencarinya di menu **Services** (di samping logo AWS).

3. Klik **Launch Instance**.

4. **Configure Instance**:

   - Beri nama instance (misalnya `MyPythonServer`).

   - Pilih **Amazon Machine Image (AMI)**:

     - Pilih **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type**.

   - Pilih **Instance Type**:

     - Pilih **t2.micro**.

5. **Configure Key Pair**:

   - Buat key pair baru dengan menekan **Create new key pair**.

   - Beri nama, misalnya `my-key-pair`.

   - Pilih format file key:

     - Jika anda akan melakukan koneksi dengan OpenSSH, pilih `.pem`.

     - Jika anda akan melakukan koneksi dengan PuTTY (untuk Windows), pilih `.ppk`.

   - Simpan file dengan menekan **Create key pair**.

6. **Configure Network Settings**:

   - Centang **Allow SSH traffic from** dan ganti ke **My IP** (untuk keamanan) atau biarkan Anywhere `0.0.0.0/0` (agar bisa diakses dari mana saja). Hindari memilih `0.0.0.0/0` (akses dari semua IP), kecuali benar-benar diperlukan.

7. **Configure Storage**:

   - Pastikan alokasi storage cukup untuk kebutuhan proyek Anda. 8 GB biasanya cukup untuk aplikasi kecil.

8. (**Opsional**) Instal dependensi (`pip install` untuk script Python). Pada bagian **Advanced Details** cari **User Data (for bootstrapping)** dan tambahkan kode di bawah pada kolom inputan.
   ```bash
   #!/bin/bash
   sudo apt-get update
   sudo apt-get install -y python3-pip
   pip3 install -r /home/ubuntu/requirements.txt
   ```

9.  Click **Launch Instance**.

## Akses EC2 Instance Menggunakan SSH

1. Navigasi ke tab **Instances** di **EC2 Console** dan pilih instance Anda, klik tombol **Connect**, pilih menu **SSH client**. Salin contoh perintah SSH.

2. Buka terminal di komputer Anda dan akses instance menggunakan SSH, tempel perintah SSH tadi.

   - Ganti lokasi file `.pem` sesuai dengan lokasi file yang Anda simpan.

   - Jika ada error terkait izin, jalankan perintah di bawah:
     ```bash
     chmod 400 /path/to/my-key-pair.pem
     ```
     Lalu ulangi memembuat koneksi menggunakan SSH.

3. (**Opsional**) Jika saat membuat koneksi terjadi error dan anda sudah capek, gunakan **CloudShell** yang berada pada pojok kiri bawah atau pada bagian menu atas dengan ikon console di samping ikon lonceng. Perlu diingat bahwa **CloudShell** adalah **lingkungan sementara**. Semua proses yang berjalan akan **dihentikan begitu Anda menutup sesi CloudShell** atau **keluar dari AWS Console**.

## Install Python dan Git di EC2 Instance

1. Cek versi Python, Pip dan Git. Jalankan per 1 baris.
   ```bash
   python3 --version
   pip --version
   git --version
   ```

2. Jika terjadi kesalahan pada nomor 1 maka perbarui package list dan install package yang tidak ditemukan.
   ```bash
   sudo apt update -y

   # Sesuaikan dengan package yang error
   sudo apt install python3 -y
   sudo apt install python3-pip -y
   sudo apt install git -y
   ```

3. Cek kembali versi package yang telah diinstall seperti nomor 1.

## Clone Source Code dari GitHub

1. Clone repository GitHub.
   ```bash
   git clone https://github.com/syauqi-a/GetGrassMiner.git
   ```

2. Masuk ke folder project.
  ```bash
  cd GetGrassMiner
  ```

## Membuat Virtual Environment dan Install Dependencies

Direkomendasikan untuk tetap membuat **virtual environment**.

1. (**Opsional**) Jika package `virtualenv` belum ada maka install terlebih dahulu:
   ```bash
   sudo pip3 install virtualenv
   ```

2. Buat dan aktifkan **virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies dari file `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

## Mengatur konfigurasi

Lakukan pengaturan konfigurasi pada file `.env`, `config.json` dan `proxies.txt` seperti saat menjalankan di lokal, lihat di [sini](README.md#setting-up-env-file).

## Menjalankan Bot Python

Jalankan script utama untuk memulai bot.
```bash
python main.py
```

## Tips: Menjaga Bot Tetap Berjalan

Jika Anda ingin aplikasi **tetap berjalan** meskipun Anda keluar dari SSH, gunakan metode berikut:
```bash
nohup python main.py > /dev/null 2>&1 & echo $! > nohup_main.pid
```

**Note**:

- Dengan menambahkan `> /dev/null 2>&1` semua output standar (`stdout`) dan output error (`stderr`) tidak akan disimpan untuk mencegah membengkaknya penyimpanan.

- Melihat proses `main.py` yang berjalan di background.
  ```bash
  ps -ef | grep main.py
  ```

- Melihat proses secara lebih detail.
  ```bash
  htop
  ```
  Lalu tekan F4, masukkan `main.py` dan tekan ENTER. Untuk keluar tekan Q.

- Menghentikan proses `main.py` yang berjalan di background.
  ```bash
  kill $(cat nohup_main.pid)
  ```
