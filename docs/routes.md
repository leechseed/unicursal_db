**API and HTMX Routes Overview for wiki-app**

---

### **Auth Routes**

- `POST /auth/register`: Create a new user
- `POST /auth/login`: Get JWT token
- `GET /auth/me`: Get current user info

---

### **Article Routes**

- `GET /`: Homepage, list recent articles
- `GET /articles/{id}`: View article
- `GET /articles/{id}/edit`: Get article edit form
- `POST /articles/{id}/edit`: Submit edit (new revision)
- `GET /articles/new`: New article form
- `POST /articles/new`: Create new article
- `GET /articles/{id}/history`: View revision list
- `GET /articles/{id}/history/{rev_id}`: View specific revision

---

### **Category Routes**

- `GET /categories`: List categories
- `GET /categories/{id}`: View all articles in category

---

### **HTMX-Specific Routes** (return partials)

- `GET /hx/articles/list`: Fragment for homepage/articles list
- `GET /hx/article/{id}/summary`: Small preview card
- `GET /hx/article/{id}/edit-form`: Inline edit form

---

### **Admin/Media (Optional)**

- `POST /media/upload`: Upload media asset
- `GET /media/{filename}`: Serve static file

---

### **Talk Pages (Optional)**

- `GET /talk/{article_id}`: View talk thread
- `POST /talk/{article_id}`: Add message to thread
