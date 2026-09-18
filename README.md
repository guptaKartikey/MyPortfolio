# 🚀 Kartikey Gupta — 3D Portfolio Website

A complete, modern, premium-looking personal portfolio website built with **Python + Streamlit**.

- 🎨 Dark futuristic theme with glassmorphism UI
- 🌐 Three.js animated 3D background
- ⚡ Runs with a single command
- 🔐 Secure admin panel
- 📦 No database required — all data saved in JSON files

---

## 📁 Project Structure

```
portfolio/
├── app.py                  ← Main entry point
├── requirements.txt
├── README.md
│
├── .streamlit/
│   ├── config.toml         ← Theme & layout settings
│   └── secrets.toml        ← Admin password (KEEP PRIVATE)
│
├── data/                   ← All your portfolio content (JSON)
│   ├── profile.json        ← Name, bio, social links, education
│   ├── skills.json         ← Skill categories and skills
│   ├── projects.json       ← Your projects
│   ├── certificates.json   ← Your certificates
│   ├── experience.json     ← Work experience / internships
│   └── messages.json       ← Contact form submissions (auto-generated)
│
├── assets/
│   ├── profile/            ← Your profile photo goes here
│   ├── projects/           ← Project images go here
│   ├── certificates/       ← Certificate images go here
│   └── resume/             ← Your resume PDF goes here
│
├── components/             ← One Python file per section
│   ├── hero.py
│   ├── about.py
│   ├── skills.py
│   ├── projects.py
│   ├── certificates.py
│   ├── experience.py
│   ├── contact.py
│   └── admin.py
│
└── utils/
    ├── data_manager.py     ← JSON read/write helpers
    └── helpers.py          ← CSS injection, image helpers
```

---

## 🛠️ Installation (Windows)

### Step 1 — Install Python

Download Python 3.10 or newer from: https://www.python.org/downloads/

During installation, **check "Add Python to PATH"**.

Verify installation:
```
python --version
```

### Step 2 — Open the portfolio folder

```powershell
cd C:\Users\Kartik\Desktop\PROFILE\portfolio
```

### Step 3 — Create a virtual environment (recommended)

```powershell
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal.

### Step 4 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 5 — Run the website

```powershell
streamlit run app.py
```

The website will open automatically at: **http://localhost:8501**

---

## 🔐 Admin Panel

### Accessing the Admin Panel

Go to: **http://localhost:8501/?admin=true**

### Default Password

The default password is: `admin123`

### Changing the Admin Password

Open the file `.streamlit/secrets.toml`:

```toml
ADMIN_PASSWORD = "your_new_strong_password_here"
```

Change `your_new_strong_password_here` to any password you want.

> **⚠️ IMPORTANT:** Never share `secrets.toml` publicly or commit it to GitHub.

---

## ✏️ How to Update Personal Information

### Method 1 — Admin Panel (Recommended for beginners)

1. Go to `http://localhost:8501/?admin=true`
2. Enter your password
3. Click the **Profile** tab
4. Edit your name, bio, college, social links, etc.
5. Click **Save Profile**

### Method 2 — Edit JSON directly

Open `data/profile.json` in any text editor (e.g., VS Code) and update the values.

Replace all `[PLACEHOLDER — ...]` values with your actual information:

```json
{
  "college": "Your College Name Here",
  "email": "your.email@example.com",
  "github": "https://github.com/yourusername",
  "linkedin": "https://linkedin.com/in/yourusername"
}
```

---

## 🖼️ How to Add Your Profile Photo

### Via Admin Panel:
1. Go to Admin → **Profile** tab
2. Scroll to "Profile Photo"
3. Upload your photo (JPG or PNG)
4. Click Save

### Manual method:
1. Copy your photo to: `assets/profile/`
2. Name it `profile.jpg`

---

## 🚀 How to Add a Project

### Via Admin Panel:
1. Admin Panel → **Projects** tab
2. Click "➕ Add New Project"
3. Fill in: Name, Category, Description, Technologies, GitHub URL, Demo URL
4. Upload a project image (optional)
5. Submit

### Manual method:
Open `data/projects.json` and add an entry to the `"projects"` array:

```json
{
  "id": 9,
  "name": "My New Project",
  "description": "What this project does...",
  "technologies": ["Python", "TensorFlow"],
  "category": "AI/ML",
  "github": "https://github.com/yourusername/project",
  "demo": "https://project-demo.com",
  "image": "",
  "featured": false
}
```

**Valid categories:** `AI/ML`, `Web Development`, `Java`, `Python`, `Other`

---

## 🏆 How to Add a Certificate

### Via Admin Panel:
1. Admin Panel → **Certificates** tab
2. Click "➕ Add New Certificate"
3. Fill in: Title, Issuer, Date, Credential ID, Verify URL
4. Upload certificate image (optional)
5. Submit

---

## 📄 How to Replace the Resume

### Via Admin Panel:
1. Admin Panel → **Resume** tab
2. Upload your PDF file
3. Done — visitors can now download it

### Manual method:
Copy your PDF to: `assets/resume/resume.pdf`

---

## 🌐 How to Deploy Online (Free)

### Option 1 — Streamlit Community Cloud (Easiest)

1. Push your project to a **GitHub repository**
   - ⚠️ Add `.streamlit/secrets.toml` to your `.gitignore` file!
2. Go to: https://streamlit.io/cloud
3. Sign in with GitHub
4. Click "New app" → select your repo → set main file to `app.py`
5. In the "Secrets" section, add:
   ```toml
   ADMIN_PASSWORD = "your_secure_password"
   ```
6. Click Deploy

Your portfolio will be live at: `https://yourapp.streamlit.app`

### Option 2 — Railway / Render

Both platforms support Python web apps and are free for small projects.
Follow their documentation and set the start command to: `streamlit run app.py --server.port $PORT`

---

## 🔒 Security Notes for Production

1. **Change the default password** before deploying
2. **Never commit `secrets.toml` to GitHub** — add it to `.gitignore`
3. For production, use Streamlit Cloud's built-in secrets management
4. Consider adding HTTPS when deploying on a custom domain

---

## ❓ Troubleshooting

**App doesn't start:**
- Make sure `(venv)` is active: run `venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

**"streamlit is not recognized":**
- Activate venv: `venv\Scripts\activate`
- Or install globally: `pip install streamlit`

**Profile photo not showing:**
- Make sure it's named exactly `profile.jpg` and placed in `assets/profile/`
- Or upload it via the admin panel

**Admin panel not accessible:**
- Make sure to add `?admin=true` at the END of the URL
- Example: `http://localhost:8501/?admin=true`

**Changes not persisting:**
- Make sure you click the Save button in the admin panel
- Check that the `data/` folder exists and you have write permission

---

## 📦 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python     | Backend logic |
| Streamlit  | Web framework |
| Three.js   | 3D hero animation (CDN, no install) |
| Vanilla CSS| All styling and animations |
| JSON       | Data storage (no database needed) |
| Pillow     | Image processing |

---

## 👤 About

Built for **Kartikey Gupta** — B.Tech CSE Student & AI/ML Developer.

---

*Portfolio v1.0 · Built with ❤️ using Python + Streamlit*
