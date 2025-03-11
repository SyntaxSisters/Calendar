from multiprocessing import Pool

from pypdf import PdfReader
import regex

def extract_text(filename: str):
    text: str = ""
    reader: PdfReader = PdfReader(filename)
    for page in reader.pages:
        text += page.extract_text()

    return text

def word_transformer(word: str)->str:
    #remove non-word characters like commas or periods
    word = regex.sub(r"[^\w'-]", "", word)
    return word.lower()

skipped_words: set[str] = {"after",
                           "also",
                           "before",
                           "chapter",
                           "could",
                           "during",
                           "from",
                           "have",
                           "since",
                           "that",
                           "this",
                           "while",
                           "width",
                           "with"}


def word_filter(word: str):
    if len(word) < 4:
        # skip short words that likely show up too frequently to be a useful indicator of content
        return False
    if regex.search(r"\d", word):
        # contains number and is therefore not a valid word
        return False
    if word in skipped_words:
        # skip words that provide no context
        return False
    return True


def frequency_map(filename: str):
    words: dict[str, int] = {}
    reader: PdfReader = PdfReader(filename)
    with Pool() as P:
        try:
            for page in reader.pages:
                for word in filter(word_filter, P.map(word_transformer, page.extract_text().split(" "))):
                    words[word] = words.get(word, 0) + 1
        finally:
            P.close()
    return words


def get_recommendations(filename: str, count:int = 5):
    frequencies = frequency_map(filename)
    result = list(map(lambda item: item[0], sorted(frequencies.items(), key=lambda item: item[1], reverse=True)))
    return result[0:count]