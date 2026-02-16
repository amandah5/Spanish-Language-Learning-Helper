
import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)


def get_tokens_tags_lemmas(text, nlp):
    """Get tokens, POS tags, & lemmas for a text using the SpaCy model."""
    doc = nlp(text)
    tokens = [token.text for token in doc if token.pos_ != "PUNCT"]
    tags = [token.pos_ for token in doc if token.pos_ != "PUNCT"]
    lemmas = [token.lemma_ for token in doc if token.pos_ != "PUNCT"]
    return tokens, tags, lemmas


def determiner_func(word1, word2, tag1, tag2):
  """Generates a message if a determiner error likely comes from gender or plurality mismatch."""
  if tag1 == "determiner" and tag2 == "determiner":
    if ("s" in word1 and "s" not in word2) or ("s" in word2 and "s" not in word1): # "s" indicates the plural determiners: los & las
      addition = " (make sure your determiner matches the plurality of the noun)"
      return addition
    if ("a" in word1 and "a" not in word2) or ("a" in word2 and "a" not in word1): # "a" indicates the feminine determiners: la & las
      addition = " (make sure your determiner matches the gender of the noun)"
      return addition
    else:
      addition = " (this error does NOT seem to be plurality or gender)" # catchall for other determiner typos/errors
      return addition
  else:
    return None


def adjective_func(word1, word2, tag1, tag2):
  """Generates a message if an adjective error likely comes from gender or plurality mismatch."""
  if tag1 == "adjective" and tag2 == "adjective":
    addition = ""
    if (word1[-1] == "s" and word2[-1] != "s") or (word2[-1] == "s" and word1[-1] != "s"): #because if "s" is the last index, it signifies plural
      addition = " (make sure your adjective matches the plurality of the noun)"
    if ((word1[-1] == "a" or word1[-2:] == "as") and (word2[-1] != "a" or word2[-2:] != "as")) or (
          (word2[-1] == "a" or word2[-2:] == "as") and (word1[-1] != "a" or word1[-2:] != "as")):
      addition = " (make sure your adjective matches the gender of the noun)"
    return addition
  else:
    return None


def verb_form(lemma1, lemma2):
  """Generates a message if a verb error likely comes from a "to be" error or an otherwise incorrect conjugation."""
  if (lemma1 == "ser" and lemma2 == "estar") or (lemma1 == "estar" and lemma2 == "ser"):
    return ' (you used the wrong verb for "to be")'
  if lemma1 == lemma2:
    return " (right verb, wrong conjugation!)"
  else:
    return None


def noun_func(word1, word2, tag1, tag2):
  """Generates a message if a noun error likely comes from gender or plurality mismatch."""
  if tag1 == "noun" and tag2 == "noun":
    if (word1[-1] == "s" and word2[-1] != "s") or (word2[-1] == "s" and word1[-1] != "s"): #because if "s" is the last index, it signifies plural
      addition = " (make sure your noun has the correct plurality)"
      return addition
    if ((word1[-1] == "a" or word1[-2:] == "as") and (word2[-1] != "a" or word2[-2:] != "as")) or (
       (word2[-1] == "a" or word2[-2:] == "as") and (word1[-1] != "a" or word1[-2:] != "as")):
      addition = " (make sure your noun has the correct gender agreement)"
      return addition
  return None


def wrong_prep(word1, word2, tag1, tag2):
  """Generates a message if the attempted translation uses a different preposition than the correct translation."""
  if tag1 == "adposition" and tag2 == "adposition" and word1 != word2:
    addition = " (wrong preposition errors are common; think about how they're used differently in Spanish)"
    return addition
  else:
    return None


def synonym_func(word1, word2):
  """Returns true if the two words passed in are synonyms, according to NLTK's WordNet interface."""
  synsets = wn.synsets(word1, lang = 'spa') #synsets = sets of synonyms
  synonyms = []
  for synset in synsets:
    for lemma in synset.lemmas(lang = 'spa'):
      if lemma.name() not in synonyms:
        synonyms.append(lemma.name())
  if word2 in synonyms:
    return True
  else:
    return False


def edits_pos(guess_tokens, guess_tags, target_tokens, target_tags):
    """
    Performs Minimum Edit Distance (MED) for hints based on POS.
    A correct POS but wrong word will not affect the edit cost at all. POS tags are included as a simple
    addition to make feedback more informative.
    """
    m, n = len(guess_tokens), len(target_tokens)
    # Build DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if guess_tokens[i - 1] == target_tokens[j - 1] else 1
            # Choose whichever operation (deletion, insertion, substitution/match) costs the lowest
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    # Backtrack
    operations = []
    i, j = m, n
    while i > 0 or j > 0:
        # 1. Match (no cost)
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] and guess_tokens[i - 1] == target_tokens[j - 1]:
            i -= 1
            j -= 1
            continue
        # 2. Substitute (different words, diagonal move)
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(("SUBSTITUTE", guess_tokens[i - 1], target_tokens[j - 1], guess_tags[i - 1], target_tags[j - 1], i - 1, j - 1))
            i -= 1
            j -= 1
            continue
        # 3. Delete (move up)
        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(("DELETE", guess_tokens[i - 1], guess_tags[i - 1]))
            i -= 1
            continue
        # 4. Insert (move left)
        if j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            operations.append(("ADD", target_tokens[j - 1], target_tags[j - 1]))
            j -= 1
            continue
        break
    return operations[::-1]
