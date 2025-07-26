from docx import Document
import re

def normalize_word(word, keep_numbering=False):
    word = word.replace("’", "'").replace("‘", "'").replace("`", "'").strip() 
    if not keep_numbering:
        word = re.sub(r"\s\d+\.$", "", word).strip()
    return word.lower()

def load_dictionary_from_docx(file_path):
    doc = Document(file_path)
    dictionary = {}
    current_words = []
    current_definition = ""

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Regex to match words including "adv.adj."
        match = re.match(r"([\w\s’'’\-\(\).,]+)\s(adj\.|adv\.|adj\.adv\.|adj\.ij\.|conj\.|excl\.|excl\.n\.|ij\.|inf\.|interj\.|n\.|phr\.|phr\.n\.|pron\.|v\.|v\.n\.)\s(.+)", text, re.IGNORECASE)

        if match:
            if current_words and current_definition.strip():
                for word in current_words:
                    dictionary[word] = current_definition.strip()
            
            raw_words = match.group(1).strip()
            cleaned_words = [normalize_word(w, keep_numbering=True) for w in raw_words.split(" also ")]
            cleaned_words = [re.sub(r"\s*\(.*?\)", "", w).strip() for w in cleaned_words]
            
            current_words = cleaned_words
            current_definition = f"({match.group(2)}) {match.group(3).strip()}"  # Store definition
        elif current_words and not re.match(r"[\w\s’'’-]+?\s(n\.|phr\.|phr\.n\.|adj\.|adv\.adj\.|adv\.|v\.|ij\.|pron\.|conj\.)", text, re.IGNORECASE):
            current_definition += " " + text
        else:
            if current_words and current_definition.strip():
                for word in current_words:
                    dictionary[word] = current_definition.strip()
            current_words = []
            current_definition = ""

    if current_words and current_definition.strip():
        for word in current_words:
            dictionary[word] = current_definition.strip()
    
    return dictionary

def search_word(dictionary, word):
    word = re.sub(r"\s*\(.*?\)", "", word).strip()
    
    normalized_word = normalize_word(word)
    normalized_word_with_numbering = normalize_word(word, keep_numbering=True)
    
    # Exact match first
    if normalized_word_with_numbering in dictionary:
        return dictionary[normalized_word_with_numbering]
    
    # Search for base word without numbering
    numbered_matches = {key: definition for key, definition in dictionary.items() if normalize_word(key) == normalized_word}
    
    if numbered_matches:
        return "\n".join([f"{key}: {definition}" for key, definition in numbered_matches.items()])
    
    return "Word not found in dictionary."

if __name__ == "__main__":
    file_path = "/Users/agan/Desktop/Kelabit/Dic_search/kelabit-dictionary/Dic_data2.docx"  #Data file path
    print()
    print("Loading dictionary...")
    dictionary = load_dictionary_from_docx(file_path)

    while True:
        print()
        word = input("Enter a word to search (or 'exit' to quit): ").strip()
        if word.lower() == "exit":
            break
        print()
        print(search_word(dictionary, word))

