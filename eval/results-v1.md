# Evaluation

30 questions, generator `qwen2.5:7b`, embeddings `bge-m3`, 2026-10-23.

- Right article retrieved (top 6): **25/25**
- Right article cited in the answer: **21/25**
- Key facts correct in the answer: **23/25**
- Out-of-scope questions refused: **4/5**
- Answerable questions wrongly refused: 0
- Citations to something not retrieved: 4
- Average time per question: 54.9 s (laptop, local model)

| Question | Retrieved | Cited | Facts | Answer |
|---|:-:|:-:|:-:|---|
| Berapa lama maksimal jangka waktu PKWT? | ✓ | ✓ | ✓ | PKWT berdasarkan jangka waktu dapat dibuat untuk paling lama 5 (lima) tahun [PP 35/2021 Pasal 8(1)]. |
| Apakah PKWT boleh mensyaratkan masa percobaan kerja? | ✓ | ✓ | ✓ | PKWT tidak dapat mensyaratkan adanya masa percobaan kerja. [PP 35/2021 Pasal 12(1)] |
| Berapa uang kompensasi untuk PKWT selama 12 bulan terus menerus? | ✓ | ✓ | ✓ | [PP 35/2021 Pasal 16(1)a] Besaran uang kompensasi untuk PKWT selama 12 bulan terus menerus diberikan sebesar 1 bulan Upah. |
| Berapa masa kerja minimal agar pekerja PKWT berhak atas uang kompensasi? | ✓ | ✗ | ✓ | Pekerja/Buruh yang telah mempunyai masa kerja paling sedikit 1 (satu) bulan secara terus menerus berhak atas uang kompensasi. [PP 35/2021 Pasal 3] |
| Berapa jam kerja per hari untuk perusahaan dengan 5 hari kerja seminggu? | ✓ | ✓ | ✗ | [PP 35/2021 Pasal 21(2)b] Waktu kerja untuk perusahaan dengan 5 hari kerja seminggu adalah 8 (delapan) jam per hari. |
| Berapa batas maksimal waktu kerja lembur? | ✓ | ✓ | ✓ | Batas maksimal waktu kerja lembur adalah 4 jam dalam 1 hari dan 18 jam dalam 1 minggu, sebagaimana dimaksud dalam [PP 35/2021 Pasal 26(1)]. |
| Berapa upah lembur untuk jam lembur pertama? | ✓ | ✓ | ✓ | Upah lembur untuk jam lembur pertama sebesar 1,5 (satu koma lima) kali Upah sejam. [PP 35/2021 Pasal 31(1)a] |
| Berapa upah untuk jam lembur kedua dan seterusnya? | ✓ | ✓ | ✓ | Upah untuk jam lembur kedua dan seterusnya sebesar 2 (dua) kali Upah sejam. [PP 35/2021 Pasal 31(1)b] |
| Berapa istirahat mingguan bagi pekerja dengan 5 hari kerja? | ✓ | ✓ | ✓ | Istirahat mingguan bagi pekerja dengan 5 hari kerja adalah 2 hari, sebagaimana dimaksud dalam [PP 35/2021 Pasal 22 a]. |
| Berapa uang pesangon untuk masa kerja 3 tahun lebih tetapi kurang dari 4 tahun? | ✓ | ✓ | ✓ | [PP 35/2021 Pasal 40(2)d] Uang pesangon untuk masa kerja 3 tahun atau lebih tetapi kurang dari 4 tahun sebesar 4 bulan Upah. |
| Berapa uang penghargaan masa kerja untuk masa kerja 3 sampai kurang dari 6 tahun? | ✓ | ✓ | ✓ | [PP 35/2021 Pasal 40(3)a] Uang penghargaan masa kerja untuk masa kerja 3 (tiga) tahun atau lebih tetapi kurang dari 6 (enam) tahun adalah 2 (dua) bulan Upah. |
| Hubungan kerja di perusahaan alih daya didasarkan pada perjanjian apa? | ✓ | ✓ | ✓ | Hubungan kerja di perusahaan alih daya didasarkan pada Perjanjian Kerja Tempat Kerja (PKWT) atau Perjanjian Kerja Tempat Kerja Tetap (PKWTT) [PP 35/2021 Pasal 1 |
| Berapa persen minimal upah pokok dari jumlah upah pokok dan tunjangan tetap? | ✓ | ✗ | ✗ | [PP 36/2021 Pasal 2(2)] |
| Kapan paling lambat THR keagamaan wajib dibayarkan? | ✓ | ✓ | ✓ | Paling lambat THR keagamaan wajib dibayarkan 7 (tujuh) hari sebelum hari raya keagamaan [PP 36/2021 Pasal 9(2)]. |
| Berapa denda jika pengusaha terlambat membayar THR? | ✓ | ✓ | ✓ | [PP 36/2021 Pasal 62] Pengusaha yang terlambat membayar tunjangan hari raya keagamaan kepada Pekerja/Buruh dikenai denda sebesar 5% (lima persen) dari total tun |
| Berapa denda keterlambatan upah mulai hari keempat? | ✓ | ✓ | ✓ | [PP 36/2021 Pasal 61(1)a] Denda keterlambatan upah mulai hari keempat sebesar 5% (lima persen) untuk setiap hari keterlambatan dari upah yang seharusnya dibayar |
| Berapa lama jangka waktu pembayaran upah paling lama? | ✓ | ✗ | ✓ | Jangka waktu pembayaran upah oleh Pengusaha tidak boleh lebih dari 1 (satu) bulan [PP 36/2021 Pasal 5(3)]. |
| Siapa yang wajib menetapkan upah minimum provinsi? | ✓ | ✓ | ✓ | Gubernur wajib menetapkan upah minimum provinsi [PP 36/2021 Pasal 27(1)]. |
| Siapa yang menetapkan upah minimum Ibu Kota Nusantara? | ✓ | ✓ | ✓ | Upah minimum Ibu Kota Nusantara ditetapkan oleh Kepala Otorita Ibu Kota Nusantara [PP 36/2021 Pasal 81A]. |
| Apakah gubernur wajib menetapkan upah minimum sektoral provinsi? | ✓ | ✓ | ✓ | Ya, gubernur wajib menetapkan Upah minimum sektoral provinsi. Hal ini disebutkan dalam [PP 36/2021 Pasal 35A]. |
| What is the maximum duration of a fixed-term employment contract (PKWT)? | ✓ | ✓ | ✓ | The maximum duration of a fixed-term employment contract (PKWT) is 5 years. This can be extended if the work has not been completed when the initial term ends,  |
| How many hours of overtime are allowed per week? | ✓ | ✓ | ✓ | [PP 35/2021 Pasal 26(1)] Four (4) hours of overtime are allowed per day and 18 (eighteen) hours per week. |
| What is the late payment penalty for wages from the fourth day? | ✓ | ✓ | ✓ | The late payment penalty for wages from the fourth day is 5% (five percent) of the wage for each day of delay, starting from the fourth day up to the eighth day |
| Who sets the minimum wage for the new capital city Nusantara? | ✓ | ✓ | ✓ | The minimum wage for the new capital city Nusantara is set by the Head of the Nusantara Capital Authority. [PP 36/2021 Pasal 81A] |
| Must employers prepare a wage structure and scale? | ✓ | ✗ | ✓ | Yes, employers must prepare a wage structure and scale. According to [PP 36/2025 Pasal 21(1)], employers are required to prepare and implement a wage structure  |
| Berapa hari cuti tahunan yang berhak didapat pekerja? | – | – | refused ✓ | Jawaban tidak ditemukan dalam peraturan yang diberikan. |
| Berapa lama cuti melahirkan bagi pekerja perempuan? | – | – | **answered ✗** | Cuti melahirkan bagi pekerja perempuan sepanjang 2 (dua) hari, sebagaimana dimaksud dalam [PP 36/2021 Pasal 40(2)]. |
| Berapa persen iuran BPJS Kesehatan yang ditanggung pekerja? | – | – | refused ✓ | Jawaban tidak ditemukan dalam peraturan yang diberikan. |
| What is the income tax (PPh 21) rate for employees? | – | – | refused ✓ | The answer is not in these regulations. |
| Berapa nilai upah minimum provinsi DKI Jakarta tahun 2026? | – | – | refused ✓ | Jawaban tidak ditemukan dalam peraturan yang diberikan. |
