from flask import Flask, render_template, request
from trie_mongodb import Trie

app = Flask(__name__)
trie = Trie()

@app.route("/", methods=["GET", "POST"])
def home():
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

if __name__ == "__main__":
    from os import environ
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


