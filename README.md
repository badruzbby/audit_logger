# 📊 Audit Trail & Change Logger API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Audit Logger adalah solusi backend yang tangguh untuk mencatat aktivitas pengguna dan perubahan data penting yang dapat diintegrasikan secara mulus dengan berbagai aplikasi. Dengan pendekatan modular dan API yang jelas, Audit Logger memberikan kemampuan audit yang komprehensif dan dapat disesuaikan.

## ✨ Fitur Utama

- 🔄 **REST API** lengkap untuk mencatat dan mengambil log aktivitas
- ⚡ **gRPC endpoint** untuk integrasi yang lebih efisien dan berperforma tinggi
- 🔍 **Filter dan pagination** untuk pencarian log yang mudah dan efisien
- 🔒 **Autentikasi JWT** untuk keamanan API
- 🛡️ **Rate limiting** untuk perlindungan dari penyalahgunaan
- 📊 **Export log** ke format CSV dan JSON
- 🔔 **Webhook triggers** untuk notifikasi perubahan real-time
- 👨‍💼 **Admin panel** yang intuitif untuk visualisasi dan pengelolaan log

## 🛠️ Teknologi

<p align="center">
  <img src="https://www.python.org/static/community_logos/python-logo.png" alt="Python" height="40" />
  <img src="https://static.djangoproject.com/img/logos/django-logo-positive.png" alt="Django" height="40" />
  <img src="https://grpc.io/img/logos/grpc-logo.png" alt="gRPC" height="40" />
  <img src="https://wiki.postgresql.org/images/3/30/PostgreSQL_logo.3colors.120x120.png" alt="PostgreSQL" height="40" />
</p>

- **Python 3.11+**
- **Django & Django REST Framework**
- **gRPC** untuk komunikasi antar layanan yang efisien
- **PostgreSQL** (atau SQLite untuk development)
- **JWT Authentication**

## 🚀 Memulai

### Prasyarat

- Python 3.11 atau yang lebih baru
- pip (Python package installer)
- (Opsional) PostgreSQL untuk lingkungan produksi

### Instalasi

1. **Clone repository**

```bash
git clone https://github.com/badruzbby/audit_logger.git
cd audit_logger
```

2. **Buat virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Siapkan konfigurasi**

```bash
cp .env.example .env
# Edit file .env sesuai kebutuhan
```

5. **Generate kode gRPC**

```bash
python grpc_server/generate_proto.py
```

6. **Jalankan database migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Buat superuser (admin)**

```bash
python manage.py createsuperuser
```

## 🏃‍♂️ Menjalankan Aplikasi

### REST API Server

```bash
python manage.py runserver
```

### gRPC Server

```bash
python grpc_server/server.py
```

## 📝 API Documentation

### REST API

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/api/log/` | POST | Mencatat log aktivitas baru |
| `/api/log/` | GET | Menampilkan log dengan filter dan pagination |
| `/api/log/export/csv/` | GET | Export log ke CSV |
| `/api/log/export/json/` | GET | Export log ke JSON |

### Authentication

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/api/auth/register/` | POST | Register pengguna baru |
| `/api/auth/login/` | POST | Login pengguna |
| `/api/auth/token/refresh/` | POST | Refresh token JWT |
| `/api/auth/api-keys/` | POST | Membuat API key baru |

## 📋 Struktur Log

```json
{
  "user_id": 1,
  "action": "UPDATE",
  "entity": "Product",
  "entity_id": "123",
  "changes": {
    "price": {"old": 10.99, "new": 12.99},
    "stock": {"old": 50, "new": 45}
  },
  "timestamp": "2025-04-21T08:30:45Z",
  "log_level": "INFO"
}
```

## 📊 Contoh Penggunaan

### Mencatat Perubahan Data

```python
import requests

api_url = "https://auditlogger.badruz.com/api/log/"
token = "your_jwt_token"

log_data = {
    "user_id": 1,
    "action": "UPDATE",
    "entity": "Product",
    "entity_id": "123",
    "changes": {
        "price": {"old": 10.99, "new": 12.99},
        "stock": {"old": 50, "new": 45}
    },
    "log_level": "INFO"
}

response = requests.post(
    api_url,
    json=log_data,
    headers={"Authorization": f"Bearer {token}"}
)

print(response.json())
```

## 📈 Performa

Audit Logger dirancang untuk menangani volume catatan log yang besar dengan tetap mempertahankan performa yang baik.

- ⚡ **gRPC Service**: Lebih dari 10.000 catatan per detik
- 🔄 **REST API**: Lebih dari 5.000 catatan per detik
- 🛠️ **Database Indexed**: Optimasi kueri untuk pencarian cepat

## 🤝 Kontribusi

Kontribusi selalu disambut dengan baik! Jika Anda tertarik untuk berkontribusi, silakan:

1. Fork repository
2. Buat branch baru (`git checkout -b feature/amazing-feature`)
3. Commit perubahan Anda (`git commit -m 'Add some amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buka Pull Request

Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk informasi lebih lanjut.

## 🔒 Keamanan

Jika Anda menemukan masalah keamanan, mohon jangan membuka issue publik. Silakan kirim email ke security@example.com.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail.

---

<p align="center">
  Dibuat dengan ❤️ oleh Muhammad Badruz Zaman
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/muhammad-badruz-zaman-6a2262227?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app">Linkedin</a> •
  <a href="https://github.com/badruzbby/audit_logger">GitHub</a> •
  <a href="https://auditlogger.badruz.com">Website</a>
</p> 