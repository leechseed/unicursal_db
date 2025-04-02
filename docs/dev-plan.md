**Development Plan for wiki-app MVP**

---

### **Phase 1: Environment Setup**

- [x] Install Python, PostgreSQL, Node.js
- [x] Create virtualenv and install dependencies
- [x] Set up Tailwind and HTMX
- [x] Initialize Git repo

---

### **Phase 2: Scaffolding**

- [ ] Create FastAPI project structure
- [ ] Add SQLAlchemy models and base database config
- [ ] Add .env and configuration loading
- [ ] Set up Jinja2 templating engine

---

### **Phase 3: Authentication**

- [ ] Implement registration, login, logout routes
- [ ] Secure article editing with JWT or session auth

---

### **Phase 4: Article Core**

- [ ] Create article model and route
- [ ] Add article creation form
- [ ] Implement revision tracking
- [ ] Add edit/view history feature

---

### **Phase 5: Categories & Domains**

- [ ] Add category and domain models
- [ ] Implement category browser
- [ ] Tag articles with multiple categories

---

### **Phase 6: HTMX Interactions**

- [ ] Add HTMX fragment routes (e.g., article cards, edit forms)
- [ ] Enable inline edits and dynamic updates

---

### **Phase 7: Styling & UI**

- [ ] Implement Tailwind layout for homepage, articles
- [ ] Add mobile responsiveness
- [ ] Add basic navigation/header/footer

---

### **Phase 8: Finalization**

- [ ] Write tests for core routes
- [ ] Dockerize the app (optional)
- [ ] Deploy to Render, Fly.io, or local server

---

**Milestone Goal**: End-to-end demo: login → create → edit → view history → browse by category
