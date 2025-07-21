# 🔍 Autocomplete Search Engine

This project implements an **Autocomplete Search Engine** using:

- **Flask** (Python web framework)
- **MongoDB Atlas** (cloud database)
- **Trie data structure** for efficient suggestions.

---

## 💡 **Features**

✅ Insert new words  
✅ Get top-k suggestions based on prefix and frequency  
✅ Stores data persistently in MongoDB Atlas

---

## 🚀 **Deployment**

- Previously deployed on **Render** using `render.yaml`.
- Due to Render free-tier sleep policy, public URL is inactive currently.
- Can be re-deployed on Render, Railway, or AWS EC2 anytime using the existing structure.

---

## ⚙ **How to Run Locally**

1. Clone the repo:

```bash
git clone https://github.com/hemachitikina/AutocompleteSearchEngine
cd AutocompleteSearchEngine


Install dependencies
Ensure you have Python installed. Then run:
pip install -r requirements.txt

Run the Flask app:
python app.py

Open browser and go to http://localhost:5000

🛠 Folder Structure

.
├── static/
├── templates/
│   ├── home.html
│   └── suggestions.html
├── app.py
├── trie_mongodb.py
├── requirements.txt
└── render.yaml

app.py – Main Flask application

trie_mongodb.py – Trie implementation integrated with MongoDB

templates/ – HTML templates for user interface

render.yaml – Deployment configuration for Render platform

📝 Notes
The MongoDB connection uses MongoDB Atlas with a username and password.

Ensure your IP whitelist and connection string are properly configured on MongoDB Atlas to run this project locally or in production.

✨ Contact
🔗 LinkedIn: https://www.linkedin.com/in/hema-sri-chitikina-226686250/
📧 Email: hemasrichitikina123@gmail.com
