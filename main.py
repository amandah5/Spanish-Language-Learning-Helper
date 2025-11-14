
from word_helpers import pos_map, get_tokens_tags_lemmas, determiner_func, adjective_func, verb_form, noun_func, wrong_prep, edits_pos, synonym_func
from clean_text import normalized, no_diacritics
from set_up_models import translate
import random
import spacy
from nltk.corpus import brown
from collections import Counter

# Load a lightweight Spanish pre-trained model
nlp = spacy.load("es_core_news_sm")


# Take a random sentence from the Brown corpus
def get_random_sentence():
    sentences = brown.sents()
    sentence = " ".join(random.choice(sentences))
    return sentence.capitalize()
english_input = get_random_sentence()
correct_spanish = translate(english_input)

print("ENGLISH SENTENCE TO TRANSLATE: ", english_input)
user_attempt = input("YOUR TRANSLATION: ")


# Normalize user input & correct translation
attempt = no_diacritics(normalized(user_attempt))
accurate = no_diacritics(normalized(correct_spanish))


# Get POS tags & lemmas
accurate_tokens, accurate_tags, accurate_lemmas = get_tokens_tags_lemmas(accurate, nlp)
attempt_tokens, attempt_tags, attempt_lemmas = get_tokens_tags_lemmas(attempt, nlp)
attempt_tags = [pos_map.get(tag, tag) for tag in attempt_tags]
accurate_tags = [pos_map.get(tag, tag) for tag in accurate_tags]


#GENERATE FEEDBACK:

hint_feedback = []
giveaway_feedback = []

# boolean, true if the lists themselves are not the same but they contain the same words (including duplicate counts)
just_word_order = (Counter(attempt_tokens) == Counter(accurate_tokens) and attempt_tokens != accurate_tokens)

if attempt_tokens == accurate_tokens:
    hint_feedback.insert(0, "Wow! You got it perfect.")
    giveaway_feedback.insert(0, "NO FIXES FOR YOU!")

elif just_word_order:
    hint_feedback.append("So close! You have all the right words, but they're in the wrong order.")
    giveaway_feedback.append("The only error you made is in the order of your words.")

else:
    med_ops = edits_pos(attempt_tokens, attempt_tags, accurate_tokens, accurate_tags)
    for op in med_ops:
        kind = op[0]
        # DELETE operation
        if kind == "DELETE":
            word, tag = op[1], op[2]
            hint_feedback.append(f"~ DELETE a word. The word to delete has the tag {tag}.")
            giveaway_feedback.append(f"~ Delete \"{word}\".")
        # INSERT operation
        elif kind == "ADD":
            word, tag = op[1], op[2]
            hint_feedback.append(f"~ ADD a word. The word to add has the tag {tag}.")
            giveaway_feedback.append(f"~ Add \"{word}\".")
        # SUBSTITUTE operation
        elif kind == "SUBSTITUTE":
            _, from_word, to_word, from_tag, to_tag, from_index, to_index = op
            extra_hint_parts = []
            if synonym_func(from_word, to_word):
                hint_feedback.append(f'~ Actually, "{from_word}" and "{to_word}" mean the same thing!')
                continue
            # Run verb_form if both sides are verbs
            if from_tag in ("verb", "auxiliary") and to_tag in ("verb", "auxiliary"):
                from_lemma = attempt_lemmas[from_index]
                to_lemma = accurate_lemmas[to_index]
                extra = verb_form(from_lemma, to_lemma)
                if extra:
                    extra_hint_parts.append(extra)
            # Other POS-specific checks
            if from_tag == "determiner":
                extra = determiner_func(from_word, to_word, from_tag, to_tag)
                if extra:
                    extra_hint_parts.append(extra)
            if from_tag == "adjective":
                extra = adjective_func(from_word, to_word, from_tag, to_tag)
                if extra:
                    extra_hint_parts.append(extra)
            if from_tag == "noun":
                extra = noun_func(from_word, to_word, from_tag, to_tag)
                if extra:
                    extra_hint_parts.append(extra)
            if from_tag == "adposition":
                extra = wrong_prep(from_word, to_word, from_tag, to_tag)
                if extra:
                    extra_hint_parts.append(extra)
            main_hint = f"~ SUBSTITUTE a word. Delete a word with tag {from_tag}, and add a word with tag {to_tag}."
            if extra_hint_parts:
                main_hint += " " + " ".join(extra_hint_parts)
            hint_feedback.append(main_hint)
            giveaway_feedback.append(f'~ Replace "{from_word}" with "{to_word}".')
    hint_feedback.insert(0, "Not bad! You have a few errors.")
    hint_feedback.insert(1, "\nIn the order provided below, do the following:")


# Print feedback
for line in hint_feedback:
    print(line)
print("\nSTUMPED? Here are the fixes:")
for line in giveaway_feedback:
    print(line)

print("\nYOUR ATTEMPT: ", user_attempt)
print("THE RIGHT ANSWER: ", correct_spanish)