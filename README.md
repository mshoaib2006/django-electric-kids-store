# ⚡ Electric Toy Store — Django E-Commerce

A complete, production-ready Django e-commerce website for electric toy vehicles (bikes, cars, jeeps).

---

## 📁 PROJECT STRUCTURE

```
electric_toy_store/
├── electric_toy_store_project/
│   ├── settings.py          ← All configuration
│   ├── urls.py              ← Main URL routes
│   └── wsgi.py
├── store/
│   ├── models.py            ← All database models
│   ├── views.py             ← All view logic
│   ├── urls.py              ← App URL routes
│   ├── admin.py             ← Admin panel config
│   ├── forms.py             ← All forms
│   ├── cart.py              ← Session cart system
│   ├── context_processors.py
│   ├── signals.py           ← Auto user profile creation
│   └── management/commands/
│       └── load_sample_data.py
├── templates/
│   ├── base.html            ← Main layout
│   ├── store/
│   │   ├── home.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_confirmation.html
│   │   ├── profile.html
│   │   ├── dashboard.html
│   │   └── partials/product_card.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── static/                  ← CSS, JS, images
├── media/                   ← Uploaded product images
├── db.sqlite3               ← SQLite database
└── manage.py
```

---

## 🚀 SETUP & RUN INSTRUCTIONS

### Step 1: Install Requirements

```bash
pip install django pillow
```

### Step 2: Navigate to Project

```bash
cd electric_toy_store
```

### Step 3: Apply Migrations

```bash
python manage.py migrate
```

### Step 4: Load Sample Data (Products + Admin User)

```bash
python manage.py load_sample_data
```

This creates:
- 3 categories: Electric Bikes, Cars, Jeeps
- 6 sample products
- Admin user: **admin** / **admin123**

### Step 5: Run the Server

```bash
python manage.py runserver
```

### Step 6: Open in Browser

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000 | Homepage |
| http://127.0.0.1:8000/products/ | All Products |
| http://127.0.0.1:8000/cart/ | Shopping Cart |
| http://127.0.0.1:8000/checkout/ | Checkout |
| http://127.0.0.1:8000/admin/ | Admin Panel |
| http://127.0.0.1:8000/dashboard/ | Sales Dashboard |

---

## 🛠️ ADMIN PANEL — HOW TO ADD PRODUCTS & IMAGES

1. Go to http://127.0.0.1:8000/admin/
2. Login with: **admin** / **admin123**
3. Click **Products → Add Product**
4. Fill in all details
5. Scroll down to **Product Images** section
6. Upload as many images as you want (100+ supported)
7. Check **Is Primary** on the main image
8. Click **Save**

---

## 🛒 FEATURES

### Customer Features
- ✅ Homepage with featured/latest products
- ✅ Product listing with category + price filters
- ✅ Product detail with Amazon-style image gallery
- ✅ Star ratings & reviews system
- ✅ Session-based shopping cart (AJAX updates)
- ✅ Checkout with Cash on Delivery
- ✅ WhatsApp order confirmation button
- ✅ User registration & login
- ✅ User profile with order history
- ✅ Search products
- ✅ Responsive mobile design

### Admin Features
- ✅ Full Django admin panel
- ✅ Upload 100+ images per product
- ✅ Stock management
- ✅ Order status management (Pending → Delivered)
- ✅ Sales dashboard with analytics
- ✅ Top products report

---

## 📱 WHATSAPP INTEGRATION

Change the WhatsApp number in `settings.py`:

```python
WHATSAPP_NUMBER = '923001234567'  # Your number here
```

Format: Country code + number (no spaces or + sign)

---

## 🗃️ DATABASE

### Development (SQLite — default)
Already configured. No setup needed.

### Production (PostgreSQL)
Uncomment and configure in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'electric_toy_store',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run: `pip install psycopg2-binary`

---

## 🔒 SECURITY CHECKLIST (Before Going Live)

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'use-a-real-secret-key-from-env'
```

---

## 🎨 CUSTOMIZATION

| What | Where |
|------|-------|
| Store name | `base.html` navbar brand |
| WhatsApp number | `settings.py` → `WHATSAPP_NUMBER` |
| Colors/theme | `base.html` CSS variables |
| Products | Admin panel |
| Delivery areas | Checkout form dropdown |
