from flask import Flask, request, jsonify
from Search_code2 import load_dictionary_from_docx, normalize_word
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
dictionary = None  # Lazy-load to prevent memory crash on startup

@app.route("/")
def home():
    return "<h2>Kelabit Dictionary API is running.</h2><p>Use /define?word=yourword</p>"

@app.route("/define")
def define():
    global dictionary
    try:
        logging.info("Accessed /define route")
        if dictionary is None:
            logging.info("Loading dictionary from Dic_data2.docx...")
            dictionary = load_dictionary_from_docx("Dic_data2.docx")

        word_raw = request.args.get("word", "")
        word = normalize_word(word_raw)
        logging.info(f"Normalized word: '{word_raw}' → '{word}'")
        definition = dictionary.get(word, "Word not found.")
        logging.info(f"Result: {definition}")
        return jsonify({"word": word, "definition": definition})
    except Exception as e:
        logging.error(f"Error in /define route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
