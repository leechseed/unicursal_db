**Development Notes for wiki-app**

---

### **Initial Goals**

- Lightweight Wikipedia-style knowledge system
- Focused on article editing, revision tracking, and tagging
- Clean UX, server-rendered with dynamic HTMX interactivity

---

### **Mental Model**

- Think in systems: Articles, Categories, Revisions, Users
- Keep features tightly scoped; grow slowly and deliberately
- Prioritize completion of vertical slices over broad partials

---

### **Notes / Log**

- **[Day 1]**: Defined project scope, selected tech stack, and scaffolded folder structure.
- **[Day 2]**: Will begin FastAPI setup, define models, and create first database migrations.

---

### **Future Considerations**

- Add tagging/annotation system to articles
- Support markdown rendering (optional)
- Enable user watchlists or bookmarks
- Consider a simple WYSIWYG or markdown editor
- Build diff viewer for revision comparison

---

### **Questions To Answer Later**

- How to handle redirects elegantly?
- Should we support multi-language articles?
- What’s the long-term plan for deployment & hosting?

- **[Day 2] (continued)**: Initialized FastAPI app and verified it runs. Root route returns JSON success message.
