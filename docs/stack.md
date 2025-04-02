**Tech Stack Overview for wiki-app**

---

### **Backend**

- **FastAPI**: High-performance async API framework with automatic docs.
- **SQLAlchemy**: ORM for relational DB access.
- **Pydantic**: Data validation and serialization.
- **Uvicorn**: ASGI server to run FastAPI.
- **python-dotenv**: Environment variable management.

### **Frontend**

- **HTMX**: Enables dynamic interactivity with server-rendered HTML.
- **Tailwind CSS**: Utility-first CSS framework.
- **Jinja2**: Template rendering engine for server-side HTML.

### **Database**

- **PostgreSQL**: Production-grade relational database.

### **Authentication**

- **JWT with FastAPI Users**: Token-based stateless authentication.

### **Tooling**

- **Node.js + npm**: Required for Tailwind CSS build process.
- **pgAdmin / TablePlus**: GUI for PostgreSQL.
- **Postman / HTTPie**: API testing.
- **Docker** (optional): Containerization.

### **Rationale**

This stack is lightweight and productive for solo development, but robust enough to support growth, advanced features, and potential deployment at scale.
