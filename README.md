Deskripsi
Repo ini berisi kode Python untuk mengimplementasikan autocropping dan warping pada gambar KTP (Kartu Tanda Penduduk) Indonesia dengan tujuan meningkatkan akurasi OCR (Optical Character Recognition) pada gambar KTP. Autocropping dan warping digunakan untuk mengambil area yang relevan dari gambar KTP dan mengubahnya menjadi format yang lebih sesuai untuk proses OCR.

Cara Kerja
1. Membaca gambar KTP yang akan diproses.
2. Menggunakan pemisahan kanal untuk membagi gambar menjadi kanal biru (blue) dan merah (red).
3. Melakukan Gaussian Blur pada kedua kanal untuk mengurangi noise.
4. Melakukan thresholding untuk menghasilkan gambar biner pada kedua kanal.
5. Menggabungkan hasil thresholding biru dan merah menggunakan operasi bitwise OR.
6. Menghilangkan area yang sama antara thresholding biru dan merah.
7. Melakukan operasi erosi untuk membersihkan gambar biner.
8. Mencari kontur pada gambar erosi.
9. Mengidentifikasi kontur terbesar yang merupakan area gambar KTP.
10. Mengambil area gambar KTP dengan memotong gambar asli menggunakan koordinat dari kontur terbesar.
11. Melakukan rotasi gambar jika diperlukan berdasarkan orientasi.
12. Mengganti ukuran gambar ke ukuran yang ditentukan (900x600 piksel).
13. Melakukan Gaussian Blur pada kanal biru berdasarkan nilai mean value B.
14. Melakukan thresholding pada kanal biru berdasarkan nilai threshold yang dihitung berdasarkan mean value B.
15. Menghasilkan gambar akhir setelah proses autocropping dan warping.

Prasyarat
- Python 3.x
- OpenCV (pip install opencv-python)
- NumPy (pip install numpy)

Cara Menggunakan
Pastikan Anda telah menginstal prasyarat yang disebutkan di atas.
Simpan gambar KTP yang ingin Anda proses dalam repositori ini atau ubah path gambar di kode sesuai dengan lokasi gambar Anda.
Jalankan kode Python untuk melakukan autocropping dan warping dengan menjalankan Autocrop and Warp for Indonesia ID Card
.py.
