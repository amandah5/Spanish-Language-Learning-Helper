***SPANISH LANGUAGE LEARNING HELPER***

**OVERVIEW**
* This is a beginner project that was created in an effort to become familiar with widely-used tools and libraries in NLP tasks.
* The purpose of the program is to help English-speaking users practice their Spanish language skills. It does so by providing English sentences, allowing the user to input their translation, and provides customized feedback generated using minimum edit distance and part of speech cues.

**REQUIREMENTS**
* See requirements.txt. This project uses SpaCy (Spanish model for tokenization, POS, lemmatization) and NLTK (sentence generation, synonym search), which both must be installed. NLTK necessary downloads include wordnet, omw-1.4 (Open Multilingual WordNet), and the Brown corpus for sentences.

**PROGRAM FEATURES**
* Generate a random (English) sentence, using the Brown corpus.
* Print the sentence to the console and allow user to input a Spanish translation. (NOTE: this will not penalize the user for lack of diacritics or punctuation differences.)
* On both the correct translation and the user's input, do the following, using a SpaCy pipeline:
  * Tokenize
  * POS tag
  * Lemmatize
* Generate 2 sets of feedback: one with "hints" that cue the user as to what errors they made with extra info on POS, and one with "giveaways" that explicitly lists the incorrect tokens.
* If the user's input matches the accurate translation perfectly (after normalizing, which has taken away diacritics and punctuation), the only thing that will be in the feedback string is an indication of success.
* If the user has all the right tokens (including the correct number of duplicates for words/tokens that appear more than once in the sentence), but they are scrambled in some way, the only feedback for the user will be that the word order is incorrect.
* Otherwise, to address actual errors:
  * Minimum edit distance (MED) generates a list of edits that the user would need to make to correct their translation.
  * Indicate which token(s) require deletion, insertion, or substitution.
  * For substitutions, additional functions address common errors like gender agreement, wrong verb form, wrong preposition, etc.

**EXAMPLE (This is what would print to the console):**

ENGLISH SENTENCE TO TRANSLATE:  His boss told him that he wanted to write another report.

YOUR TRANSLATION: su jefe lo dijo que queria a escribir esta informa
Not bad! You have a few errors.

In the order provided below, do the following:

~ SUBSTITUTE a word. Delete a word with tag pronoun, and add a word with tag pronoun.

~ DELETE a word. The word to delete has the tag adposition.

~ SUBSTITUTE a word. Delete a word with tag determiner, and add a word with tag determiner.  (make sure your determiner matches the plurality of the noun)

~ SUBSTITUTE a word. Delete a word with tag noun, and add a word with tag noun.  (make sure your noun has the correct gender agreement)

STUMPED? Here are the fixes:

~ Replace "lo" with "le".

~ Delete "a".

~ Replace "esta" with "otro".

~ Replace "informa" with "informe".

YOUR ATTEMPT:  su jefe lo dijo que queria a escribir esta informa

THE RIGHT ANSWER:  Su jefe le dijo que quería escribir otro informe.



**LIMITATIONS**
* This is just an introductory project and will not successfully address complex errors in user input.
* Substitutions, as indicated by MED, are often problematic, because the program may not accurately match up words that should actually correspond.
* MED is at the token level, not character level. So if a user types "juggo" instead of "juego", they will be punished exactly the same as if they were to type something like "manzana" instead of "juego".

