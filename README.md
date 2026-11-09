Nama : Yazid Khairul Firmansyah

NPM : 2506537064

Kelas : PBP D

## Tentang Proyek

Website portofolio pribadi berbasis Django. Bagian yang saya kerjakan sendiri adalah **Education** (riwayat pendidikan): CRUD, pencarian, star, peran Editor/pemilik, dan sejak Tugas 6 dilayani lewat REST API (`/api/v1/education/`) dengan Django REST Framework.

## Cara Menjalankan

```bash
python -m venv env
env\Scripts\activate          # Windows (Linux/macOS: source env/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test main    # menjalankan seluruh test
```

Endpoint API: `GET/POST /api/v1/education/?search=<kata>`, `GET/PUT/PATCH/DELETE /api/v1/education/<uuid>/`, `POST /api/v1/education/<uuid>/star/`. Browsable API dapat dibuka langsung di browser.

## Progres Mingguan

| Tugas | Fokus |
|---|---|
| 1 | Halaman statis HTML/CSS semantik dan responsif |
| 2 | Model, view, template Django (MVT) |
| 3 | ModelForm, CSRF, endpoint JSON |
| 4 | Autentikasi, peran Editor/pemilik, fitur star |
| 5 | AJAX, debounced search, toast, pencegahan XSS |
| 6 | REST API dengan DRF, permission class, APITestCase, modal edit via PATCH |



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

### Tugas 5

1. **Pengertian debouncing dan kepentingannya pada fitur pencarian berbasis AJAX:**
   *Debouncing* adalah teknik optimasi pemrograman yang menunda pemanggilan suatu fungsi hingga jeda waktu tertentu (*delay*) telah berlalu sejak event terakhir kali dipicu. Jika event baru terjadi kembali sebelum jeda waktu tersebut berakhir (misalnya pengguna masih terus menekan tombol keyboard untuk mengetik), penghitung waktu (*timer*) yang lama akan dibatalkan (`clearTimeout`) dan digantikan oleh penghitung waktu yang baru.
   
   Teknik ini sangat penting diterapkan pada fitur pencarian AJAX karena:
   - **Mencegah beban berlebih pada server dan database:** Tanpa debouncing, setiap ketukan tombol (*keystroke*) akan mengirim satu permintaan HTTP ke server. Mengetik kata "Universitas" akan memicu 11 permintaan sekaligus dalam hitungan detik. Dengan debouncing, hanya 1 permintaan yang dikirimkan setelah pengguna berhenti mengetik sejenak.
   - **Mencegah *race condition* (inkonsistensi data):** Karena kecepatan transmisi jaringan bersifat asinkron, respons dari permintaan pertama (misalnya kata kunci "Uni") bisa saja sampai lebih lambat daripada respons dari permintaan kedua ("Universitas"). Tanpa debouncing dan pembatalan permintaan (*AbortController*), respons yang sudah usang dapat menimpa hasil pencarian terbaru.
   - **Menghemat bandwidth dan meningkatkan responsivitas antarmuka (UI):** Mengurangi jumlah request secara drastis membuat konsumsi bandwidth hemat dan browser tidak terbebani oleh render ulang yang tidak perlu secara terus-menerus.

2. **Fungsi kata kunci `await` saat menggunakan `fetch()` dan konsekuensi jika tidak digunakan:**
   Fungsi utama kata kunci `await` adalah untuk menunda (*pause*) eksekusi kode di dalam fungsi `async` sampai objek `Promise` yang dihasilkan oleh `fetch()` selesai diproses (*resolved* atau *rejected*), kemudian langsung mengekstrak nilai hasil (*resolved value*) dari Promise tersebut (yaitu objek `Response` HTTP).
   
   Jika kita **tidak menggunakan `await`**:
   - Pemanggilan `const response = fetch(url);` tidak akan menghasilkan objek `Response`, melainkan objek `Promise {<pending>}`.
   - Saat kode selanjutnya mencoba membaca properti atau metode dari objek tersebut, seperti `if (!response.ok)` atau `response.json()`, kode akan menghasilkan error atau perilaku yang tidak terduga karena objek `Promise` tidak memiliki properti `ok` (bernilai `undefined`).
   - Jika kita memanggil `response.json()` tanpa `await`, hasilnya pun kembali berupa `Promise` kedua, bukan array/data JSON sebenarnya. Mencoba mengakses data seperti `data.length` atau `data.forEach(...)` akan langsung melempar error `TypeError: data.forEach is not a function`.
   - Kode di bawahnya akan berjalan secara sinkron mendahului selesainya proses pengambilan data dari jaringan, sehingga data belum siap ditampilkan ke DOM dan antarmuka web menjadi kosong atau rusak (*broken state*).

3. **Pengertian serangan XSS (Cross-Site Scripting) dan alasan kerentanan data via AJAX/JavaScript dibanding template Django:**
   *Cross-Site Scripting* (XSS) adalah kerentanan keamanan web di mana penyerang berhasil menyisipkan skrip berbahaya (biasanya berupa kode JavaScript jahat) ke dalam aplikasi web terpercaya, yang kemudian dieksekusi di peramban (*browser*) pengguna lain yang mengakses halaman tersebut. Melalui XSS, penyerang dapat mencuri cookie sesi atau kredensial, melakukan pembajakan akun (*session hijacking*), merekam ketukan tombol (*keylogging*), hingga memanipulasi tampilan dan fungsi halaman secara tidak sah.
   
   Data yang ditampilkan melalui **AJAX/JavaScript jauh lebih rentan terhadap serangan XSS** dibandingkan data yang ditampilkan langsung melalui template Django karena:
   - **Template Django memiliki perlindungan otomatis (*Auto-escaping*):** Secara bawaan (*by default*), mesin template Django menerapkan *contextual HTML escaping* pada semua variabel yang dirender (`{{ variable }}`). Karakter-karakter khusus HTML yang berpotensi mengeksekusi skrip (seperti `<`, `>`, `&`, `"`, `'`) secara otomatis diubah menjadi *HTML entities* (seperti `&lt;`, `&gt;`). Skrip berbahaya yang tersimpan di database hanya akan ditampilkan sebagai teks polos di layar tanpa dieksekusi oleh browser.
   - **Penyisipan manual di JavaScript/DOM tidak memiliki auto-escaping bawaan:** Ketika data diambil lewat AJAX (format JSON), data tersebut murni berupa string teks mentah. Jika pengembang menyisipkannya ke halaman menggunakan properti manipulasi DOM seperti `innerHTML` atau interpolasi template literal (misalnya `element.innerHTML = '<h2>' + data.title + '</h2>'`), browser akan langsung mem-parsing string tersebut sebagai kode HTML murni. Jika data tersebut mengandung payload berbahaya seperti `<img src="x" onerror="alert('XSS!')">`, skrip jahat akan langsung dieksekusi oleh browser. Oleh sebab itu, saat menggunakan AJAX/JavaScript, pengembang wajib secara eksplisit melakukan sanitasi di sisi server (misal dengan `strip_tags` pada ModelForm) serta melakukan *escaping* manual (misal fungsi `escapeHtml()`) atau menggunakan `textContent` di sisi client.



### Tugas 6

1. **Pengertian REST, mengapa JSON saja belum cukup, serta perbedaan PUT dan PATCH:**
   - **REST (Representational State Transfer)** adalah gaya arsitektur perangkat lunak (*architectural style*) yang diperkenalkan oleh Roy Fielding untuk merancang sistem terdistribusi dan komunikasi antar-layanan berbasis web. REST menekankan interaksi berbasis *resource* (sumber daya), di mana setiap sumber daya diidentifikasi secara unik melalui URI (seperti `/api/v1/education/`), dimanipulasi melalui representasinya menggunakan metode standar HTTP (GET, POST, PUT, PATCH, DELETE), bersifat nirkeadaan (*stateless*), dapat di-*cache* (*cacheable*), serta memiliki antarmuka yang seragam (*uniform interface*).
   - **Mengapa mengembalikan JSON saja belum cukup untuk disebut RESTful:** Mengembalikan format JSON hanyalah salah satu pilihan format serialisasi data (*content-type: application/json*). Sebuah API baru dapat disebut RESTful jika mematuhi batasan-batasan arsitektural REST. Sebagai contoh, jika sebuah endpoint URL berupa `/api/delete_education_by_id?id=1` dan dipanggil menggunakan metode `GET` atau `POST` generik lalu mengembalikan `{ "status": "deleted" }`, API tersebut **bukanlah RESTful** meskipun formatnya JSON, karena melanggar prinsip *Uniform Interface* (menggunakan URL berbasis aksi/RPC (*Remote Procedure Call*), bukan sumber daya nomina), menyalahgunakan semantik metode HTTP (GET tidak boleh menimbulkan efek samping mutasi), serta tidak mengembalikan kode status HTTP semantik (seperti `204 No Content` atau `404 Not Found`). RESTful menuntut konsistensi semantik kata kerja HTTP, representasi status yang akurat melalui HTTP Status Codes, dan manipulasi *resource* yang independen.
   - Perbedaan PUT dan PATCH beserta contoh kasus penggunaannya:
     - `PUT` (Full Replacement / Penggantian Menyeluruh): Bersifat idempoten. Klien mengirimkan representasi sumber daya secara lengkap dan utuh. Jika ada atribut atau field yang tidak disertakan dalam *payload*, field tersebut akan dianggap dikosongkan (*null*) atau diatur ke nilai *default*-nya, bahkan bisa gagal divalidasi jika field tersebut berstatus *required*.
       - *Contoh kasus:* Fitur sinkronisasi data formulir profil atau form riwayat pendidikan menyeluruh dari aplikasi eksternal, di mana seluruh field (nama institusi, program, tanggal mulai, tanggal selesai, deskripsi, nilai) dikirimkan ulang secara lengkap untuk menggantikan seluruh baris record yang sudah ada.
     - `PATCH` (Partial Update / Pembaruan Sebagian): Digunakan untuk memperbarui satu atau beberapa field tertentu saja dari suatu sumber daya tanpa harus mengirimkan kembali seluruh field lainnya. Field yang tidak disertakan dalam *payload* akan tetap mempertahankan nilai aslinya di database.
       - *Contoh kasus:* Pengguna hanya ingin memperbarui field `score` (nilai akhir) atau mengubah tanggal selesai `ended_at` pada riwayat pendidikan tanpa perlu mengirimkan ulang teks `description`, `institution_name`, dan `started_at` yang panjang.

2. **Peran Serializer pada Django REST Framework dan Keuntungannya dibanding Dictionary Manual `JsonResponse`:**
   - **Peran Serializer di DRF:**
     Serializer bertindak sebagai jembatan dua arah (*two-way bridge*) yang sangat krusial dalam DRF:
     1. **Serialisasi (Output):** Mengonversi struktur data Python kompleks dari Django ORM (objek Model atau QuerySet) menjadi tipe data Python primitif (dictionary, list, string, number) yang dapat dengan mudah dirender ke format JSON/XML via HTTP. Termasuk menyediakan field turunan komputasi dinamis lewat `SerializerMethodField` (seperti `star_count`, status relasi `is_starred`, dan `is_ongoing`).
     2. **Deserialisasi dan Validasi (Input):** Mengonversi *payload* teks mentah (JSON) dari permintaan HTTP klien kembali menjadi tipe data Python, melakukan sanitasi teks (*strip_tags* terhadap serangan XSS), validasi tipe data dan batasan model (`min_value`, `max_value`, format ISO datetime), validasi tingkat field tunggal (`validate_<field>`), validasi silang antar-field (`validate()`, misalnya memastikan tanggal selesai tidak mendahului tanggal mulai), dan secara otomatis menyimpannya ke database melalui metode `.save()`, `.create()`, atau `.update()`.
   - **Keuntungan Serializer dibanding merakit dictionary manual dengan `JsonResponse`:**
     - **Validasi Terstruktur dan Deklaratif:** Pada pendekatan manual `JsonResponse`, pengembang harus menulis puluhan baris validasi manual (`if not request.POST.get('name'): return JsonResponse(...)`), pengecekan tipe data, dan parsing manual yang rentan terlewat. Serializer menangani seluruh aturan validasi deklaratif dan otomatis mengembalikan dictionary error yang terstruktur dengan kode status `400 Bad Request`.
     - **Reusabilitas dan Modularitas (DRY):** `ModelSerializer` secara otomatis membaca metadata dari model Django (`fields`, tipe kolom, `blank`, `null`), sehingga mengurangi duplikasi kode secara drastis dibanding merakit dictionary manual setiap kali membuat endpoint baru.
     - **Sanitasi Terpusat:** Logika pembersihan data (seperti pembersihan tag HTML jahat) diletakkan di satu tempat di dalam serializer, menjamin konsistensi baik saat data dibuat (`POST`) maupun diperbarui (`PUT`/`PATCH`).
     - **Dukungan Built-in DRF:** Terintegrasi langsung dengan fitur canggih DRF seperti Browsable API, pagination, nested relationship, partial updates, dan context request (misalnya mendeteksi user yang sedang login untuk `is_starred`).

3. **Perbedaan Autentikasi vs Otorisasi di DRF dan Alasan Hak Akses Wajib Diperiksa di Server:**
   - **Perbedaan Autentikasi dan Otorisasi:**
     - **Autentikasi (*Authentication*):** Proses untuk membuktikan dan mengidentifikasi **siapa pengguna yang mengirim permintaan** (*Who are you?*). DRF memeriksa kredensial (misalnya cookie sesi via `SessionAuthentication` atau Bearer Token) untuk mencocokkan identitas pengguna ke instance `request.user`. Jika kredensial salah atau tidak ada, pengguna dikategorikan sebagai *anonymous/unauthenticated*.
     - **Otorisasi (*Authorization / Permissions*):** Proses untuk menentukan **apakah pengguna yang identitasnya telah teridentifikasi tersebut memiliki izin untuk melakukan tindakan tertentu pada sumber daya yang diminta** (*What are you allowed to do?*). Misalnya, apakah pengguna tersebut berhak mengubah data (anggota grup *Editor*), menghapus data (*Superuser/Portfolio Owner*), atau hanya boleh membaca data (*Visitor*).
   - **Mengapa hak akses wajib diperiksa dengan Permission Class di Server, bukan hanya menyembunyikan tombol di Template:**
     - **Antarmuka Klien (Template/HTML/JS) Berada di Luar Kendali Server:** Menyembunyikan elemen visual tombol (misalnya tombol *Hapus* atau modal *Edit*) di HTML/template hanyalah kemudahan pengalaman pengguna (*UI convenience / security through obscurity*), **bukan mekanisme keamanan sama sekali**.
     - **Akses Langsung ke Endpoint HTTP:** Penyerang atau pengguna biasa yang paham teknis dapat dengan mudah mengabaikan tampilan HTML dan mengirimkan permintaan HTTP secara langsung ke endpoint API (misalnya menggunakan `curl`, Postman, terminal, skrip Python, atau konsol Fetch di Developer Tools browser).
     - **Prinsip *Zero Trust* & Validasi Sisi Server:** Jika server tidak memvalidasi hak akses melalui *permission class* (seperti `IsPortfolioOwnerOrEditorOrReadOnly`), siapa pun yang mengirimkan `DELETE /api/v1/education/<uuid>/` akan berhasil menghapus data penting meskipun tombol hapus tidak ditampilkan di antarmuka web mereka. Oleh sebab itu, server harus selalu menjadi benteng pertahanan utama dan terakhir yang memverifikasi setiap hak akses pada setiap transaksi HTTP.

4. **Alasan Permintaan Mutasi Memerlukan Token CSRF saat Memakai `SessionAuthentication` dan Mengapa `force_authenticate` Tidak Cukup:**
   - **Alasan Permintaan Mutasi Memerlukan Token CSRF pada `SessionAuthentication`:**
     `SessionAuthentication` di Django mengandalkan *cookie* sesi (`sessionid`) yang disimpan oleh peramban pengguna. Masalah keamanan fundamental dari *cookie* berbasis peramban adalah sifatnya yang otomatis disertakan oleh browser (*ambient authority*) pada setiap permintaan yang ditujukan ke domain server tersebut, bahkan jika permintaan tersebut dipicu dari situs web jahat pihak ketiga (*cross-site*), misalnya melalui form tersembunyi atau skrip JavaScript jahat di situs lain saat pengguna masih dalam keadaan login di aplikasi portofolio. Ini adalah celah serangan **Cross-Site Request Forgery (CSRF)**.
     
     Untuk menggagalkan serangan ini, Django dan DRF mewajibkan *token rahasia yang tidak dapat diprediksi* (*CSRF Token*) yang dikirimkan melalui header kustom `X-CSRFToken` pada setiap permintaan yang melakukan mutasi data (POST, PUT, PATCH, DELETE). Karena situs web pihak ketiga tidak dapat membaca nilai cookie domain lain (akibat *Same-Origin Policy*), penyerang tidak dapat menyertakan header `X-CSRFToken` yang valid, sehingga peramban dan server berhasil menggagalkan upaya eksploitasi tersebut.
   - **Mengapa Test dengan `force_authenticate` Tidak Cukup untuk Membuktikan Perlindungan CSRF:**
     `force_authenticate(user=...)` pada DRF `APITestCase` dirancang sebagai alat bantu pengujian unit untuk *mocking* atau memintas (*bypass*) seluruh lapisan autentikasi HTTP, *middleware*, dan pengecekan CSRF standar demi menguji logika bisnis izin (*permissions*) secara terisolasi dan cepat.
     
     Saat kita menggunakan `force_authenticate`, objek `request.user` langsung disuntikkan secara artifisial ke dalam request tanpa melalui pipeline autentikasi Django biasa, dan secara default DRF mematikan verifikasi CSRF. Akibatnya, pengujian yang memakai `force_authenticate` **sama sekali tidak memverifikasi apakah middleware CSRF aktif, apakah token CSRF divalidasi dengan benar, atau apakah permintaan tanpa token akan ditolak**.
     
     Oleh karena itu, untuk membuktikan secara empiris bahwa pertahanan CSRF benar-benar berfungsi, kita wajib menggunakan `APIClient(enforce_csrf_checks=True)` dan melakukan autentikasi nyata melalui `client.login()`. Pengujian ini memastikan bahwa permintaan sesi tanpa header `HTTP_X_CSRFTOKEN` akan ditolak mentah-mentah dengan status `403 Forbidden`, sedangkan permintaan yang menyertakan token yang valid akan berhasil diproses.


---

### AI Disclosure (Tugas 6)

**Tools:** Google Antigravity (agent AI di IDE) dengan model Gemini dan Claude.

**Strategi prompting:** Saya memberikan dokumen soal Tugas 6 beserta rubriknya ke agent, lalu meminta pengerjaan dibagi per tahap (backend API → integrasi halaman → test → dokumentasi) supaya setiap tahap bisa saya review dan commit terpisah. Untuk setiap tahap saya meminta agent menjalankan `python manage.py test main` sampai semuanya lulus sebelum lanjut.

**Bagian yang dibantu AI:**
- Penulisan `EducationSerializer`, permission class `IsPortfolioOwnerOrEditorOrReadOnly`, dan API view `education_list` / `education_detail` / `education_star`.
- Migrasi `templates/education.html` ke `/api/v1/education/` dan modal edit `templates/components/education_edit_modal.html`.
- Perluasan test di `main/tests_api.py` (`EducationAPITest`).
- Draf awal jawaban pertanyaan reflektif, yang kemudian saya baca ulang dan sesuaikan.

**Keterbatasan AI yang ditemukan selama pengerjaan:**
1. **Asumsi keliru soal `strip_tags`.** Test validasi awal memakai payload `<script>alert(1)</script>` dengan harapan ditolak (400). Ternyata test gagal (201), karena `strip_tags` hanya membuang tag dan menyisakan teks `alert(1)`, sehingga input dianggap valid. Payload diganti menjadi tag kosong (`<i></i>`) yang memang menjadi string kosong setelah disanitasi. Ini menunjukkan output AI tetap harus diverifikasi dengan benar-benar menjalankan test, bukan diasumsikan benar.
2. **View lama terlewat.** Saat audit akhir terhadap checklist, ditemukan bahwa view lama `create_education` dan `delete_education` sama sekali tidak memeriksa hak akses (pengunjung tanpa login pun bisa menghapus data lewat `POST /education/<id>/delete/`), padahal soal meminta view lama disesuaikan dengan aturan API. Kedua view kemudian dibatasi hanya untuk superuser dan ditambahkan test `test_legacy_views_follow_api_rules`. AI cenderung fokus pada file yang sedang dikerjakan dan tidak otomatis memeriksa jalur lain yang mengakses model yang sama.

**Verifikasi yang saya lakukan:** menjalankan seluruh test (`python manage.py test main`), mencoba halaman Education dengan akun pengunjung, pengguna biasa, Editor, dan superuser, serta membuka Browsable API di `/api/v1/education/`.
