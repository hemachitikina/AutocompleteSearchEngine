# from flask import Flask, render_template, request
# from trie_mongodb import Trie

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize Trie instance
# trie = Trie()

# # Load existing words from MongoDB into Trie
# # from pymongo import MongoClient
# # from urllib.parse import quote_plus

# # username = "hemauser"
# # password = "Hemadb@123"
# # password_encoded = quote_plus(password)
# # connection_string = f"mongodb+srv://{username}:{password_encoded}@autocompletesearchengin.30cwosr.mongodb.net/?retryWrites=true&w=majority&appName=autocompletesearchengine"
# # client = MongoClient(connection_string)
# # db = client['AutocompleteDB']
# # collection = db['words']

# # existing_words = collection.find()
# # for doc in existing_words:
# #     word = doc['word']
# #     freq = doc['frequency']
# #     for _ in range(freq):
# #         trie.insert(word)

# # ===============================
# # 🔥 Routes
# # ===============================

# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         word = request.form["word"]
#         trie.insert(word)
#         message = f"✅ '{word}' inserted successfully!"
#         return render_template("home.html", message=message)
#     return render_template("home.html", message="")

# @app.route("/suggestions", methods=["POST"])
# def suggestions():
#     prefix = request.form["prefix"]
#     k = int(request.form["k"])
#     suggestions = trie.get_top_k_suggestions(prefix, k)
#     return render_template("suggestions.html", prefix=prefix, suggestions=suggestions)

# # ===============================
# # 🔥 Run app
# # ===============================

# if __name__ == "__main__":
#     from os import environ
#     port = int(environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

from flask import Flask, render_template, request
from trie_mongodb import Trie

# Initialize Flask app
app = Flask(__name__)

# Initialize Trie instance
trie = Trie()

# ===============================
# 🔥 Routes
# ===============================

@app.route("/", methods=["GET", "POST"])
def home():
    from pymongo import MongoClient
    from urllib.parse import quote_plus

    username = "hemauser"
    password = "Hemadb@123"
    password_encoded = quote_plus(password)
    connection_string = f"mongodb+srv://{username}:{password_encoded}@autocompletesearchengin.30cwosr.mongodb.net/?retryWrites=true&w=majority&appName=autocompletesearchengine"
    client = MongoClient(connection_string)
    db = client['AutocompleteDB']
    collection = db['words']

    # Load existing words into Trie
    existing_words = collection.find()
    for doc in existing_words:
        word = doc['word']
        freq = doc['frequency']
        for _ in range(freq):
            trie.insert(word)

    if request.method == "POST":
        word = request.form["word"]
        trie.insert(word)
        message = f"✅ '{word}' inserted successfully!"
        return render_template("home.html", message=message)
    return render_template("home.html", message="")

@app.route("/suggestions", methods=["POST"])
def suggestions():
    prefix = request.form["prefix"]
    k = int(request.form["k"])
    suggestions = trie.get_top_k_suggestions(prefix, k)
    return render_template("suggestions.html", prefix=prefix, suggestions=suggestions)

# ===============================
# 🔥 Run app
# ===============================

if __name__ == "__main__":
    from os import environ
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
