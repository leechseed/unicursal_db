**Project Setup Guide for wiki-app**

---

### **1. System Requirements**

- Python 3.10+
- Node.js + npm
- PostgreSQL
- Git

---

### **2. Project Folder Structure**

```plaintext
wiki-app/
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── templates/
│   └── static/
├── docs/
├── .env
├── requirements.txt
├── tailwind.config.js
├── postcss.config.js
├── package.json
├── README.md
└── run.sh / run.bat
```

---

### **3. Initial Setup Commands**

```bash
# Clone repo and enter directory
git clone <repo-url>
cd wiki-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Tailwind
npm install -D tailwindcss
npx tailwindcss init
```

---

### **4. PostgreSQL Setup**

```bash
createdb wiki_dev
```

Add `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/wiki_dev
SECRET_KEY=your-secret-key
```

---

### **5. Run the App**

```bash
uvicorn app.main:app --reload
```

---

### **6. Optional Tools**

- pgAdmin / TablePlus for DB GUI
- Postman or HTTPie for API testing
- Docker for containerization later
