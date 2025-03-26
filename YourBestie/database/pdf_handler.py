# pdf_handler.py
import re
from pypdf import PdfReader

def extract_text(filename: str):
    """Extracts all text from a PDF file."""
    text = ""
    reader = PdfReader(filename)
    for page in reader.pages:
        text += page.extract_text()
    return text

def word_transformer(word: str) -> str:
    """Cleans a word by removing non-word characters and converting it to lowercase."""
    word = re.sub(r"[^\w'-]", "", word)
    return word.lower()

# Common words to ignore
skipped_words: set[str] = {
    "after", "also", "before", "chapter", "could", "during",
    "from", "have", "since", "that", "this", "while", "width", "with"
}

def word_filter(word: str) -> bool:
    """Filters out short, numeric, or commonly used words."""
    if len(word) < 4:
        return False  # Skip short words
    if re.search(r"\d", word):
        return False  # Skip words containing numbers
    if word in skipped_words:
        return False  # Skip common words
    return True

def frequency_map(filename: str):
    """Creates a frequency map of words in the given PDF file."""
    words = {}
    text = extract_text(filename)
    for word in text.split():
        cleaned_word = word_transformer(word)
        if word_filter(cleaned_word):
            words[cleaned_word] = words.get(cleaned_word, 0) + 1
    return words

def get_recommendations2(filename: str, count: int = 5):
    """Extracts the 5 most common words from a PDF file."""
    frequencies = frequency_map(filename)
    result = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    return [word for word, _ in result[:count]]

def get_recommendations(filename: str, count: int = 5):
    """Does nothing now, only returns the filename."""
    return [filename]
