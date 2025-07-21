import heapq
from pymongo import MongoClient
from urllib.parse import quote_plus

username = "hemauser"
password = "Hemadb@123"
password_encoded = quote_plus(password)
connection_string = f"mongodb+srv://{username}:{password_encoded}@autocompletesearchengin.30cwosr.mongodb.net/?retryWrites=true&w=majority&appName=autocompletesearchengine"

client = MongoClient(connection_string)
db = client['AutocompleteDB']
collection = db['words']

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.load_from_db()

    def load_from_db(self):
        existing_words = collection.find()
        for doc in existing_words:
            word = doc['word']
            freq = doc['frequency']
            for _ in range(freq):
                self.insert(word, db_update=False)

    def insert(self, word, db_update=True):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True
        current.frequency += 1

        # Insert or update word in MongoDB
        if db_update:
            existing = collection.find_one({'word': word})
            if existing:
                collection.update_one({'word': word}, {'$inc': {'frequency': 1}})
            else:
                collection.insert_one({'word': word, 'frequency': 1})

    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word

    def startsWith(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def get_top_k_suggestions(self, prefix, k):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        suggestions = []
        self._dfs(current, prefix, suggestions)

        # Update frequencies from MongoDB to ensure latest counts
        for i in range(len(suggestions)):
            word = suggestions[i][0]
            freq_in_db = collection.find_one({'word': word})
            if freq_in_db:
                suggestions[i] = (word, freq_in_db['frequency'])

        top_k = heapq.nlargest(k, suggestions, key=lambda x: x[1])
        return [word for word, freq in top_k]

    def _dfs(self, node, path, suggestions):
        if node.is_end_of_word:
            suggestions.append((path, node.frequency))
        for char, next_node in node.children.items():
            self._dfs(next_node, path + char, suggestions)

if __name__ == "__main__":
    trie = Trie()

    while True:
        print("\n🔍 === Autocomplete Search Engine Menu ===")
        print("1. Insert a word")
        print("2. Get top k suggestions for a prefix")
        print("3. Search for a word")
        print("4. Check if any word starts with a prefix")
        print("5. Exit")
        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            word = input("Enter the word to insert: ")
            trie.insert(word)
            print(f"✅ '{word}' inserted successfully and saved to MongoDB.")

        elif choice == '2':
            prefix = input("Enter the prefix: ")
            k = int(input("Enter the number of top suggestions (k): "))
            suggestions = trie.get_top_k_suggestions(prefix, k)
            if suggestions:
                print(f"💡 Top {k} suggestions for '{prefix}': {suggestions}")
            else:
                print(f"❌ No suggestions found for '{prefix}'.")

        elif choice == '3':
            word = input("Enter the word to search: ")
            found = trie.search(word)
            print(f"🔎 Word '{word}' found: {found}")

        elif choice == '4':
            prefix = input("Enter the prefix to check: ")
            exists = trie.startsWith(prefix)
            print(f"🔎 Any word starts with '{prefix}': {exists}")

        elif choice == '5':
            print("👋 Exiting the program. Goodbye!")
            break

        else:
            print("⚠ Invalid choice. Please try again.")
