from flask import Flask, request, jsonify
from Search_code2 import load_dictionary_from_docx, normalize_word

app = Flask(__name__)
dictionary = None  # Lazy-load to prevent memory crash on Render free plan

@app.route("/define", methods=["GET"])
def define():
    global dictionary
    if dictionary is None:
        dictionary = load_dictionary_from_docx("Dic_data2.docx")

    word = request.args.get("word", "").strip().lower()
    word = normalize_word(word)
    definition = dictionary.get(word, "Word not found.")
    return jsonify({"word": word, "definition": definition})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
