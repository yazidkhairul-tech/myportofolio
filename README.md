Nama : Yazid Khairul Firmansyah

NPM : 2506537064

Kelas : PBP D



### Tugas 1

1. Ya, saya pakai elemen semantik HTML5 di struktur portofolio ini — `<header>` untuk navigasi atas, `<main>` untuk konten utama tiap halaman, `<section>` untuk tiap bagian besar (`hero`/profile, `education`, `experience`, `projects`), `<article>` untuk unit konten yang berdiri sendiri dan bisa berulang (kartu pendidikan, kartu proyek, entri pengalaman), serta `<footer>` untuk info hak cipta. Saya belum memakai `<aside>` karena belum ada konten pelengkap/sekunder yang terpisah dari alur utama (semacam sidebar atau catatan tambahan) — semua informasi yang saya tampilkan masih relevan langsung dengan konten utamanya, jadi memaksakan `<aside>` justru akan mengaburkan struktur, bukan membantu.

   Elemen semantik ini membantu proses membuat *static web* dengan beberapa cara: (1) strukturnya jadi lebih mudah dibaca saat saya menulis ulang atau debug CSS, karena nama tag sudah menjelaskan fungsinya tanpa perlu buka-tutup banyak `<div class="...">`; (2) browser dan screen reader bisa memahami hierarki halaman secara otomatis (meningkatkan aksesibilitas); dan (3) mesin pencari lebih mudah mengenali bagian mana yang merupakan konten utama vs navigasi, yang berguna untuk SEO. Kalau saya hanya pakai `<div>` generik di semua tempat, halaman tetap tampil sama secara visual, tapi maknanya jadi "buta" bagi tools dan assistive technology yang membaca struktur dokumen, bukan cuma tampilannya.

2. Tantangan tata letak terbesar ada di bagian hero/profile, karena aslinya pakai grid 2 kolom (`grid-template-columns: 1fr auto`) dengan foto di kanan dan teks identitas/bio di kiri. Di layar sempit, dua kolom berdampingan itu jadi terlalu sempit dan foto ikut mengecil sampai proporsinya aneh. Solusinya saya ubah `grid-template-areas` supaya di mobile urutannya jadi 1 kolom dengan foto di paling atas, baru identitas dan detail teks di bawahnya — jadi bukan cuma menumpuk elemen apa adanya, tapi saya susun ulang urutannya (foto dulu, karena secara visual itu "penyambut" pertama) supaya tetap enak dibaca dari atas ke bawah.

   Evaluasi elemen mana yang perlu diubah posisi/ukurannya saya lakukan dengan menimbang dua hal: elemen yang punya makna visual kuat tapi kaku secara lebar (seperti foto profil dan grid kartu pendidikan/proyek 2 kolom) saya prioritaskan untuk berubah dari grid ke 1 kolom penuh; sementara elemen yang sifatnya deretan pendek (seperti search bar + tombol cari, atau baris judul + tombol tambah) saya ubah dari flex horizontal jadi flex vertikal (`flex-direction: column`) supaya tombolnya tetap mudah disentuh dengan lebar penuh di layar sentuh, bukan malah mengecil dan susah di-tap.

3. Karena situs ini murni *static web*, batasan yang paling saya rasakan adalah: semua informasi (riwayat pendidikan, pengalaman, proyek) harus saya tulis langsung di HTML, jadi setiap kali ada info baru atau ada yang perlu diubah, saya harus edit kode sumbernya langsung, lalu deploy ulang. Tidak ada cara bagi saya (atau orang lain) untuk menambah/mengubah/menghapus data lewat antarmuka web — semuanya manual lewat teks editor. Ini juga berarti tidak ada validasi data, tidak ada penyimpanan yang persisten di luar file kode, dan tidak bisa berkembang secara dinamis (misalnya highlight otomatis untuk proyek terbaru, atau pencarian data).

   Berdasarkan batasan itu, fungsionalitas dinamis yang paling ingin saya siapkan di iterasi selanjutnya adalah kemampuan CRUD berbasis database (tambah/ubah/hapus data lewat form web, bukan edit kode), supaya kontennya bisa terus diperbarui tanpa harus menyentuh source code setiap saat, plus fitur pencarian/filter data yang berjalan dari server, bukan konten yang di-hardcode.

### Tugas 2

1. Alurnya dimulai saat browser mengirim *request* (misalnya GET ke `/projects/`) ke server. Request itu pertama kali ditangkap oleh **`urls.py` di level proyek**, yang bertugas sebagai "pintu masuk" dan mencocokkan awalan path — di sini biasanya isinya cuma `path("", include("main.urls"))`, yang berarti semua path akan dilempar untuk dicocokkan lebih lanjut ke **`urls.py` di level aplikasi** (`main`). Di `urls.py` aplikasi inilah path spesifik seperti `projects/` dicocokkan dengan fungsi **view** tertentu (`views.show_projects`).

   Setelah view itu terpanggil, ia akan mengambil data lewat **model** — misalnya `Project.objects.all()` — yang berperan menerjemahkan query Python itu menjadi query SQL ke database, lalu mengembalikan hasilnya sebagai objek-objek Python (QuerySet). View lalu membungkus data itu ke dalam sebuah `context` (dictionary), dan memanggil `render(request, "projects.html", context)`. Di titik inilah **template** berperan: ia menerima context tersebut, melakukan loop lewat `{% for project in project_list %}`, dan menyusun data itu menjadi markup HTML final. HTML hasil render itu lalu dikirim balik sebagai response HTTP ke browser, yang kemudian menampilkannya ke pengguna.

2. Data sebaiknya disimpan di model, bukan ditulis langsung di template, karena model merepresentasikan struktur data yang **persisten** — tersimpan di database, bisa di-query, difilter, diurutkan, divalidasi, dan direlasikan ke model lain secara terstruktur. Kalau data ditulis langsung di template (hardcode), setiap perubahan data mengharuskan saya mengedit source code dan deploy ulang, tidak ada satu sumber data yang konsisten (kalau data yang sama dibutuhkan di dua halaman, saya harus duplikasi manual), dan tidak mungkin ada fitur seperti pencarian, filter, atau endpoint JSON, karena semuanya butuh data yang bisa di-query secara dinamis dari satu tempat.

   Dampaknya terhadap pemeliharaan: dengan data di model, saya (atau pengguna lain lewat form) bisa menambah/mengubah/menghapus data tanpa menyentuh kode template atau logic view sama sekali — cukup lewat CRUD form atau admin panel. Ini membuat aplikasi jauh lebih mudah dikembangkan lebih lanjut, karena perubahan struktur data cukup dilakukan di satu tempat (`models.py`), dan seluruh bagian aplikasi yang memakai data itu (template, JSON endpoint, search) otomatis ikut konsisten.

3. `makemigrations` dan `migrate` adalah dua tahap yang berbeda dalam proses mengubah struktur database di Django:
   - **`makemigrations`** membaca perubahan yang saya buat di `models.py` (misalnya field baru, model baru, field yang dihapus) dan **membuat file migrasi** — semacam "rencana"/instruksi perubahan struktur database dalam bentuk skrip Python. Perintah ini **belum mengubah database sama sekali**, hanya membuat catatan perubahan apa yang perlu dilakukan.
   - **`migrate`** yang benar-benar **mengeksekusi** file-file migrasi itu ke database sebenarnya — membuat tabel baru, menambah/menghapus kolom, dan seterusnya, sesuai instruksi dari file migrasi yang sudah dibuat oleh `makemigrations`.

   Contoh nyata dari proyek saya sendiri: waktu saya menambahkan field baru `is_featured` (BooleanField) ke model `Project`, saya harus menjalankan `python manage.py makemigrations` dulu supaya Django membuatkan file migrasi yang isinya instruksi "tambahkan kolom `is_featured` ke tabel `Project`", lalu baru menjalankan `python manage.py migrate` supaya kolom itu benar-benar dibuat di tabel `Project` pada database.

### Tugas 3

1. Kita menggunakan `ModelForm` alih-alih membuat form HTML manual karena `ModelForm` otomatis menghasilkan field form berdasarkan definisi model (termasuk tipe input, validasi tipe data, dan constraint seperti `max_length` atau `blank`), jadi kita tidak perlu menulis ulang logika validasi dan rendering input satu per satu. Ini membuat kode lebih singkat, konsisten dengan struktur database, dan lebih mudah dirawat — kalau ada perubahan di model, form ikut menyesuaikan tanpa perlu diedit manual. `ModelForm` juga sudah menangani proses cleaning data dan mapping ke instance model lewat `form.save()`, sehingga mengurangi risiko bug dibanding menulis parsing `request.POST` secara manual.

   Kita wajib menambahkan `{% csrf_token %}` pada form untuk melindungi aplikasi dari serangan **Cross-Site Request Forgery (CSRF)**, yaitu serangan di mana pihak ketiga yang jahat mencoba mengirim request (misalnya POST) atas nama user yang sedang login tanpa sepengetahuan/izin user tersebut. Django mewajibkan token CSRF ini pada setiap form yang mengirim data lewat method selain GET (POST, PUT, DELETE), karena middleware `CsrfViewMiddleware` akan menolak request yang tidak menyertakan token valid tersebut, sehingga hanya request yang benar-benar berasal dari form yang di-render oleh server kita sendiri yang bisa diproses.

2. JSON lebih disukai dibanding XML dalam pengembangan aplikasi web modern karena beberapa alasan:
   - **Lebih ringkas** — JSON tidak memerlukan closing tag seperti XML, sehingga ukuran datanya lebih kecil dan lebih hemat bandwidth.
   - **Native di JavaScript** — JSON pada dasarnya adalah representasi object JavaScript, sehingga bisa langsung di-parse (`JSON.parse()`) dan digunakan tanpa parser tambahan, sangat cocok untuk aplikasi web yang banyak memakai JavaScript/AJAX di sisi client.
   - **Lebih mudah dibaca manusia** — strukturnya lebih sederhana (key-value dan array) dibanding XML yang penuh tag pembuka/penutup.
   - **Parsing lebih cepat dan ringan** — karena strukturnya lebih sederhana, proses parsing JSON umumnya lebih cepat dan menggunakan resource lebih sedikit dibanding parsing XML yang butuh DOM parser/SAX parser.
   - **Didukung luas** oleh hampir semua bahasa pemrograman dan framework modern sebagai format pertukaran data standar untuk REST API.

3. Alur yang terjadi saat fungsi *view* mengembalikan data portofolio dalam bentuk JSON:
   1. Request masuk ke fungsi *view* (misalnya lewat URL `/projects/json/`).
   2. View mengambil data dari database melalui Django ORM, contohnya `Project.objects.all()`, yang hasilnya berupa **QuerySet** berisi objek-objek model Python (bukan format yang bisa langsung dikirim lewat HTTP sebagai teks).
   3. QuerySet tersebut di-*serialize* menggunakan `django.core.serializers.serialize("json", queryset)`, yang mengubah objek-objek model Python itu menjadi string berformat JSON.
   4. String JSON hasil serialisasi itu dibungkus dalam `HttpResponse` dengan `content_type="application/json"`, lalu dikirim sebagai response ke client.

   Kita perlu melakukan proses **serialization** pada model Django sebelum datanya dikembalikan karena objek model Django adalah objek Python (instance class) yang kompleks — punya method, relasi ke model lain, koneksi ke database, dan tipe data Python native (seperti `datetime`, `Decimal`, dsb.) yang **tidak bisa langsung dikonversi menjadi teks/JSON** oleh protokol HTTP. HTTP hanya bisa mengirim data dalam bentuk teks (string byte), sehingga objek model tersebut harus diubah dulu (diserialisasi) menjadi format teks terstruktur seperti JSON, agar bisa dikirim melalui jaringan dan nantinya dapat dibaca/di-parse kembali (deserialisasi) oleh pihak yang menerimanya, baik itu browser, aplikasi mobile, maupun sistem lain.

