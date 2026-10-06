# 🚀 Kartikey Gupta — 3D Portfolio Website

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Framework-red?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Three.js-3D-black?style=for-the-badge&logo=three.js" alt="Three.js">
  <img src="https://img.shields.io/badge/JSON-Data%20Storage-orange?style=for-the-badge&logo=json" alt="JSON">
</p>

<p align="center">
  <b>Modern • Futuristic • Interactive • Responsive</b>
</p>

---

## 🌐 Live Portfolio

### 🚀 [Visit My Portfolio](https://kartikey-gupta-portfolio.streamlit.app/)

A modern and interactive personal portfolio website built using **Python and Streamlit**, featuring a futuristic UI, glassmorphism design, animated 3D background, project showcase, certificates, experience, skills, resume and contact functionality.

---

## 📸 Portfolio Preview

> Add your portfolio screenshot here.

```text
assets/
└── portfolio-preview.png
```

After adding the image, use:

```markdown
![Portfolio Preview](assets/portfolio-preview.png)
```

---

## ✨ Features

- 🎨 Modern futuristic dark UI
- 🪟 Glassmorphism interface
- 🌐 Animated Three.js 3D background
- 📱 Responsive portfolio design
- 👨‍💻 Interactive hero section
- 📖 About Me section
- 🛠️ Skills showcase
- 🚀 Project showcase
- 🏆 Certificates section
- 💼 Experience and internship section
- 📄 Resume download
- 📬 Contact form
- 🔐 Secure admin panel
- 📝 Dynamic content management
- 💾 JSON-based data storage
- 🖼️ Project and certificate image support
- ⚡ Lightweight architecture
- ☁️ Easy deployment using Streamlit Community Cloud

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Application logic |
| 🎈 Streamlit | Web application framework |
| 🌐 Three.js | 3D background animation |
| 🎨 HTML/CSS | UI structure and styling |
| ⚡ JavaScript | Interactive 3D elements |
| 📦 JSON | Data storage |
| 🖼️ Pillow | Image processing |
| ☁️ Streamlit Cloud | Deployment |

---

# 📁 Project Structure

```text
portfolio/
│
├── app.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
│
├── data/
│   ├── profile.json
│   ├── skills.json
│   ├── projects.json
│   ├── certificates.json
│   ├── experience.json
│   └── messages.json
│
├── assets/
│   ├── profile/
│   ├── projects/
│   ├── certificates/
│   └── resume/
│
├── components/
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
    ├── data_manager.py
    └── helpers.py
```

---

# 💻 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Move into the project directory:

```bash
cd YOUR_REPOSITORY
```

---

## 2. Install Python

Make sure Python **3.10 or newer** is installed.

Check your Python version:

```bash
python --version
```

If Python is not installed, download it from:

[Python Official Website](https://www.python.org/downloads/)

> During Windows installation, make sure **Add Python to PATH** is checked.

---

## 3. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

You should see:

```text
(venv)
```

in your terminal.

---

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 5. Run the Portfolio

```powershell
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

# 🔐 Admin Panel

The portfolio includes an admin panel that allows the portfolio owner to update content without manually editing every JSON file.

## Access Admin Panel

Open:

```text
http://localhost:8501/?admin=true
```

Then enter your admin password.

---

## ⚙️ Admin Features

The admin panel can be used to manage:

- 👤 Profile information
- 🛠️ Skills
- 🚀 Projects
- 🏆 Certificates
- 💼 Experience
- 📄 Resume
- 🖼️ Profile image
- 📬 Contact messages

---

# 🔑 Admin Password

For local development, the password can be configured inside:

```text
.streamlit/secrets.toml
```

Example:

```toml
ADMIN_PASSWORD = "your_secure_password"
```

> ⚠️ **IMPORTANT:** Never upload `secrets.toml` containing your real password to GitHub.

Add it to `.gitignore`:

```text
.streamlit/secrets.toml
```

---

# 📝 Managing Portfolio Data

The portfolio stores dynamic information using JSON files.

## Profile

```text
data/profile.json
```

Contains:

- Name
- Bio
- Education
- Email
- GitHub
- LinkedIn
- Social links

---

## Skills

```text
data/skills.json
```

Used to manage skill categories and individual technologies.

Example:

```json
{
  "category": "Programming",
  "skills": [
    "Python",
    "Java",
    "SQL"
  ]
}
```

---

## Projects

```text
data/projects.json
```

Each project can contain:

- Project name
- Description
- Technologies
- Category
- GitHub URL
- Demo URL
- Project image
- Featured status

Example:

```json
{
  "id": 1,
  "name": "AI Diabetes Prediction System",
  "description": "AI-based diabetes prediction and recommendation system.",
  "technologies": [
    "Python",
    "Machine Learning",
    "Flask"
  ],
  "category": "AI/ML",
  "github": "https://github.com/YOUR_USERNAME/project",
  "demo": "",
  "image": "",
  "featured": true
}
```

---

# 🏆 Certificates

Certificates are managed through:

```text
data/certificates.json
```

Each certificate can contain:

- Certificate title
- Issuer
- Date
- Credential ID
- Verification URL
- Certificate image

---

# 💼 Experience

Experience and internship information is stored in:

```text
data/experience.json
```

This section can contain:

- Company
- Position
- Duration
- Description
- Technologies
- Responsibilities

---

# 📄 Resume

Place your resume inside:

```text
assets/resume/
```

Example:

```text
assets/resume/resume.pdf
```

The portfolio can then provide visitors with a resume download option.

---

# 🖼️ Adding Images

## Profile Image

Place your profile image inside:

```text
assets/profile/
```

Example:

```text
assets/profile/profile.jpg
```

Supported formats:

- JPG
- JPEG
- PNG

---

## Project Images

Place project screenshots inside:

```text
assets/projects/
```

Example:

```text
assets/projects/project1.png
assets/projects/project2.png
```

---

## Certificate Images

Place certificate images inside:

```text
assets/certificates/
```

---

# 🚀 Adding a New Project

Projects can be added through the Admin Panel.

### Steps

1. Open the Admin Panel
2. Go to **Projects**
3. Select **Add New Project**
4. Enter project name
5. Add description
6. Select category
7. Add technologies
8. Add GitHub URL
9. Add live demo URL
10. Upload project image
11. Save the project

---

# 🌐 Deployment

## Streamlit Community Cloud

The easiest way to deploy this portfolio is using Streamlit Community Cloud.

### Step 1 — Push Project to GitHub

Make sure your repository contains:

```text
app.py
requirements.txt
components/
data/
assets/
utils/
```

Do not upload:

```text
.streamlit/secrets.toml
```

---

### Step 2 — Open Streamlit Community Cloud

Visit:

https://streamlit.io/cloud

Sign in using GitHub.

---

### Step 3 — Create a New App

Select:

```text
New App
```

Choose your GitHub repository.

Set the main file to:

```text
app.py
```

Then deploy the application.

---

### Step 4 — Configure Secrets

Open the application's **Secrets** section and add:

```toml
ADMIN_PASSWORD = "your_secure_password"
```

Save the configuration.

Your portfolio will then be available through a Streamlit URL such as:

```text
https://your-portfolio.streamlit.app
```

---

# 🔒 Security

For production deployment:

- 🔐 Use a strong admin password
- 🚫 Never expose `secrets.toml`
- 🚫 Never commit passwords or API keys
- 🔑 Store sensitive credentials using Streamlit Secrets
- 🛡️ Keep private company information out of public project screenshots
- 📁 Add sensitive files to `.gitignore`

---

# 📄 Recommended `.gitignore`

```text
venv/
__pycache__/
*.pyc

.streamlit/secrets.toml

.env
.env.*

.DS_Store
Thumbs.db
```

---

# 🧩 Configuration

Streamlit configuration can be customized using:

```text
.streamlit/config.toml
```

Example:

```toml
[theme]
base = "dark"

[server]
headless = true
```

---

# ⚡ Run Locally

After installation, simply run:

```powershell
streamlit run app.py
```

That's it.

---

# 🎯 Why I Built This

I built this portfolio to create a **personal digital presence** where I can showcase my:

- 💻 Technical skills
- 🚀 Projects
- 🏆 Certifications
- 💼 Internship experience
- 📄 Resume
- 📬 Contact information

Instead of using a static HTML-only portfolio, this project uses **Python + Streamlit** with JSON-based content management and an admin panel.

---

# 📚 What I Learned

While building this project, I gained practical experience with:

- Python application development
- Streamlit
- UI/UX design
- Responsive layouts
- Custom CSS
- JavaScript integration
- Three.js
- JSON data management
- File handling
- Image processing
- Admin panel development
- Git & GitHub
- Streamlit deployment

---

# 🚀 Future Improvements

Planned improvements include:

- 🌙 Advanced theme customization
- 🤖 AI-powered portfolio assistant
- 📊 Portfolio analytics
- 📧 Email notification system
- 🗄️ Database integration
- 🔐 Improved authentication
- 🌍 Custom domain
- 📱 Further mobile optimization
- ⚡ Performance improvements

---

# 👨‍💻 About Me

**Kartikey Gupta**

B.Tech Computer Science & Engineering Student  
AI/ML & Data Analytics Enthusiast

I enjoy building practical projects using **Python, Data Analytics, AI/ML and modern web technologies**.

### 🔗 Connect With Me

- 💼 LinkedIn: https://www.linkedin.com/in/kartikey-gupta-988206372/
- 🐙 GitHub: https://github.com/guptaKartikey
- 🌐 Portfolio: https://kartikey-gupta-portfolio.streamlit.app/

---

# ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ **Star**.

---

<p align="center">
  Built with ❤️ using Python + Streamlit
</p>

<p align="center">
  © 2026 Kartikey Gupta
</p>
