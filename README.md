# CampRent API - Sistem Manajemen Sewa Alat Camping

## 1. Deskripsi Proyek
**CampRent API** adalah sebuah layanan *microservice* berbasis RESTful API yang dirancang untuk mengelola inventaris peralatan *outdoor* dan camping. Proyek ini dikembangkan sebagai bagian dari tugas **Ujian Tengah Semester (UTS)** mata kuliah **Pemrograman Web Lanjutan (PWL)**.

Sistem ini berfokus pada manajemen data dari sisi administrator, memungkinkan pengelola untuk mengatur kategori peralatan serta detail alat yang tersedia untuk disewakan secara efisien melalui platform digital.

---

## 2. Fitur Utama
Sesuai dengan spesifikasi teknis proyek, sistem ini memiliki fitur-fitur berikut:

* **Manajemen Kategori (CRUD)**: Mengelola pengelompokan alat (seperti Tenda, Carrier, atau alat masak) dengan operasi Create, Read, Update, dan Delete.
* **Manajemen Alat (CRUD)**: Mengelola detail inventaris meliputi nama alat, harga sewa harian, dan stok.
* **Relasi Database (ORM)**: Implementasi relasi *One-to-Many* antara Kategori dan Alat menggunakan SQLAlchemy `relationship()`.
* **Keamanan dengan JWT**: Proteksi *endpoint* kritikal menggunakan *JSON Web Token* untuk memastikan hanya admin terautentikasi yang dapat melakukan perubahan data.
* **Validasi Data**: Memastikan input data (seperti harga dan stok) sesuai dengan tipe data dan batasan nilai menggunakan **Pydantic**.
* **Dokumentasi API Otomatis**: Integrasi dengan **Swagger UI** (`/docs`) untuk pengujian *endpoint* yang interaktif.

---

## 3. Stack Teknologi
Proyek ini dibangun menggunakan teknologi berikut sesuai dengan ketentuan:

* **Framework**: FastAPI (Python 3.9+).
* **Database**: SQLite dengan SQLAlchemy sebagai ORM.
* **Autentikasi**: JWT (JSON Web Token).
* **Server**: Uvicorn (Localhost deployment).
* **Testing**: Postman.

---

## 4. Struktur Proyek
Kode diorganisir secara modular agar lebih terorganisir dan mudah di-review:

```text
CampRent_API/
├── main.py          # Entry point aplikasi FastAPI
├── database.py      # Koneksi & session database
├── models/          # Definisi tabel SQLAlchemy (Category & Item)
├── schemas/         # Validasi data menggunakan Pydantic
├── routers/         # Logika endpoint per domain
├── auth/            # Logika keamanan dan JWT
├── requirements.txt # Daftar dependensi Python
└── README.md        # Dokumentasi proyek
