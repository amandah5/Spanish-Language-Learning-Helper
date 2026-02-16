
import re


def normalized(sentence):
    """Lowercase, scrap punctuation, and get rid of any extra whitespace/newline characters."""
    sentence = sentence.lower()
    sentence = re.sub(r"[.,':;!?]", "", sentence)
    sentence = sentence.strip()
    return sentence


def no_diacritics(sentence):
    """Replace Spanish diacritic characters."""
    for char in sentence:
        destroy_me = ["ü", "ñ", "é", "á", "í", "ó", "ú"]
        add_me = ["u", "n", "e", "a", "i", "o", "u"]
        if char in destroy_me:
            for i in range(len(destroy_me)):
                if destroy_me[i] == char:
                    sentence = sentence.replace(char, add_me[i])
    return sentence