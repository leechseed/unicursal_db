**Data Model Overview for wiki-app**

---

### **Entities and Relationships**

#### **Users**

- user_id (PK)
- username
- email
- password_hash
- role

#### **Articles**

- article_id (PK)
- title
- is_redirect
- created_by (FK to Users)
- created_at

#### **Revisions**

- revision_id (PK)
- article_id (FK to Articles)
- content
- edited_by (FK to Users)
- edited_at
- summary

#### **Categories**

- category_id (PK)
- name
- parent_id (FK to Categories)

#### **Domains**

- domain_id (PK)
- name
- description

#### **Category_Domains** (join table)

- category_id (FK to Categories)
- domain_id (FK to Domains)

#### **Article_Categories** (join table)

- article_id (FK to Articles)
- category_id (FK to Categories)

#### **Media**

- media_id (PK)
- filename
- url
- uploaded_by (FK to Users)
- uploaded_at
- article_id (FK to Articles)

#### **Talk_Pages**

- talk_id (PK)
- article_id (FK to Articles)
- created_by (FK to Users)
- content
- created_at

---

### **Notes**

- Category hierarchy is supported via `parent_id`.
- Domains group categories by higher-order purpose.
- Articles support multiple categories and revisions.
- Revisions enable full edit history for each article.
- Media and Talk pages enrich article context.
