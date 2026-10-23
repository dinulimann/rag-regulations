# Evaluation

30 questions, generator `qwen2.5:7b`, embeddings `bge-m3`, 2026-10-23.

- Right article retrieved (top 6): **25/25**
- Right article cited in the answer: **23/25**
- Key facts correct in the answer: **25/25**
- Out-of-scope questions refused: **5/5**
- Answerable questions wrongly refused: 0
- Citations to something not retrieved: 0
- Average time per question: 51.5 s (laptop, local model)

| Question | Retrieved | Cited | Facts | Answer |
|---|:-:|:-:|:-:|---|
| Berapa lama maksimal jangka waktu PKWT? | ✓ | ✓ | ✓ | PKWT berdasarkan jangka waktu dapat dibuat untuk paling lama 5 (lima) tahun. [PP 35/2021 Pasal 8] |
| Apakah PKWT boleh mensyaratkan masa percobaan kerja? | ✓ | ✓ | ✓ | PKWT tidak dapat mensyaratkan adanya masa percobaan kerja. [PP 35/2021 Pasal 12] |
| Berapa uang kompensasi untuk PKWT selama 12 bulan terus menerus? | ✓ | ✓ | ✓ | Uang kompensasi untuk PKWT selama 12 bulan terus menerus diberikan sebesar 1 bulan Upah. [PP 35/2021 Pasal 16] |
| Berapa masa kerja minimal agar pekerja PKWT berhak atas uang kompensasi? | ✓ | ✓ | ✓ | Pekerja/Buruh yang telah mempunyai masa kerja paling sedikit 1 (satu) bulan secara terus menerus berhak atas uang kompensasi. [PP 35/2021 Pasal 15][PP 35/2021 P |
| Berapa jam kerja per hari untuk perusahaan dengan 5 hari kerja seminggu? | ✓ | ✓ | ✓ | 8 jam per hari untuk perusahaan dengan 5 hari kerja seminggu [PP 35/2021 Pasal 21]. |
| Berapa batas maksimal waktu kerja lembur? | ✓ | ✓ | ✓ | Batas maksimal waktu kerja lembur adalah 4 jam dalam 1 hari dan 18 jam dalam 1 minggu, tidak termasuk kerja lembur pada waktu istirahat mingguan dan/atau hari l |
| Berapa upah lembur untuk jam lembur pertama? | ✓ | ✓ | ✓ | Upah lembur untuk jam lembur pertama sebesar 1,5 (satu koma lima) kali Upah sejam. [PP 35/2021 Pasal 31] |
| Berapa upah untuk jam lembur kedua dan seterusnya? | ✓ | ✓ | ✓ | Upah untuk jam lembur kedua dan seterusnya sebesar 2 (dua) kali Upah sejam. [PP 35/2021 Pasal 31][PP 35/2021 Pasal 31] |
| Berapa istirahat mingguan bagi pekerja dengan 5 hari kerja? | ✓ | ✓ | ✓ | Istirahat mingguan bagi pekerja dengan 5 hari kerja adalah 2 hari [PP 35/2021 Pasal 22]. |
| Berapa uang pesangon untuk masa kerja 3 tahun lebih tetapi kurang dari 4 tahun? | ✓ | ✓ | ✓ | 9 (sembilan) bulan Upah [PP 35/2021 Pasal 40] |
| Berapa uang penghargaan masa kerja untuk masa kerja 3 sampai kurang dari 6 tahun? | ✓ | ✓ | ✓ | 2 (dua) bulan Upah [PP 35/2021 Pasal 40] |
| Hubungan kerja di perusahaan alih daya didasarkan pada perjanjian apa? | ✓ | ✓ | ✓ | Hubungan kerja di perusahaan alih daya didasarkan pada PKWT atau PKWTT [PP 35/2021 Pasal 18]. |
| Berapa persen minimal upah pokok dari jumlah upah pokok dan tunjangan tetap? | ✓ | ✗ | ✓ | [2][3] Minimal upah pokok dari jumlah upah pokok dan tunjangan tetap adalah 75%. |
| Kapan paling lambat THR keagamaan wajib dibayarkan? | ✓ | ✓ | ✓ | Paling lambat, THR keagamaan wajib dibayarkan 7 (tujuh) hari sebelum hari raya keagamaan. [PP 36/2021 Pasal 9] |
| Berapa denda jika pengusaha terlambat membayar THR? | ✓ | ✓ | ✓ | Denda jika pengusaha terlambat membayar tunjangan hari raya keagamaan sebesar 5% dari total tunjangan yang harus dibayar sejak berakhirnya batas waktu kewajiban |
| Berapa denda keterlambatan upah mulai hari keempat? | ✓ | ✓ | ✓ | Denda keterlambatan upah mulai hari keempat sebesar 5% (lima persen) dari upah yang seharusnya dibayarkan untuk setiap hari keterlambatan dari hari keempat hing |
| Berapa lama jangka waktu pembayaran upah paling lama? | ✓ | ✗ | ✓ | [1] Jangka waktu pembayaran upah oleh Pengusaha tidak boleh lebih dari 1 (satu) bulan. |
| Siapa yang wajib menetapkan upah minimum provinsi? | ✓ | ✓ | ✓ | Gubernur wajib menetapkan upah minimum provinsi. [PP 36/2021 Pasal 27][PP 36/2021 Pasal 28A][PP 36/2021 Pasal 29][PP 36/2021 Pasal 35A] |
| Siapa yang menetapkan upah minimum Ibu Kota Nusantara? | ✓ | ✓ | ✓ | Upah minimum Ibu Kota Nusantara ditetapkan oleh Kepala Otorita Ibu Kota Nusantara setelah penetapan pemindahan Ibu Kota Negara. [PP 36/2021 Pasal 81A] |
| Apakah gubernur wajib menetapkan upah minimum sektoral provinsi? | ✓ | ✓ | ✓ | Ya, gubernur wajib menetapkan upah minimum sektoral provinsi. Menurut [PP 36/2021 Pasal 35A] dan [PP 36/2021 Pasal 35D], pasal 35A dan 35D PP 36/2021 menyatakan |
| What is the maximum duration of a fixed-term employment contract (PKWT)? | ✓ | ✓ | ✓ | The maximum duration of a fixed-term employment contract (PKWT) is 5 years. [PP 35/2021 Pasal 8] |
| How many hours of overtime are allowed per week? | ✓ | ✓ | ✓ | According to [PP 35/2021 Pasal 26], the maximum allowed overtime per week is 18 hours. |
| What is the late payment penalty for wages from the fourth day? | ✓ | ✓ | ✓ | The late payment penalty for wages from the fourth day is 5% (five percent) of the wage for each day of delay from the date the wage was due, up to a maximum of |
| Who sets the minimum wage for the new capital city Nusantara? | ✓ | ✓ | ✓ | The minimum wage for the new capital city Nusantara is set by the Head of the Nusantara Capital Authority. [PP 36/2021 Pasal 81A] |
| Must employers prepare a wage structure and scale? | ✓ | ✓ | ✓ | Yes, employers must prepare a wage structure and scale. According to [PP 36/2021 Pasal 21], employers are required to compile and implement a wage structure and |
| Berapa hari cuti tahunan yang berhak didapat pekerja? | – | – | refused ✓ | [PP 35/2021 Pasal 22][PP 35/2021 Pasal 26][PP 35/2021 Pasal 21][PP 35/2021 Pasal 40][PP 36/2021 Pasal 40][PP 35/2021 Pasal 11] |
| Berapa lama cuti melahirkan bagi pekerja perempuan? | – | – | refused ✓ | [PP 36/2021 Pasal 41][PP 35/2021 Pasal 22][PP 36/2021 Pasal 40][PP 35/2021 Pasal 21][PP 35/2021 Pasal 26][PP 35/2021 Pasal 40] |
| Berapa persen iuran BPJS Kesehatan yang ditanggung pekerja? | – | – | refused ✓ | Answer is not in these regulations. |
| What is the income tax (PPh 21) rate for employees? | – | – | refused ✓ | The answer is not in these regulations. |
| Berapa nilai upah minimum provinsi DKI Jakarta tahun 2026? | – | – | refused ✓ | Jawaban tidak ditemukan dalam peraturan yang diberikan. |
