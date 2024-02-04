
import re
import six
from nltk.stem.porter import PorterStemmer


stemmer = PorterStemmer()

def tokenize(text, stopwords = []):
    # Convert everything to lowercase.
    text = text.lower()
    # Replace any non-alpha-numeric characters with spaces.
    text = re.sub(r"[^a-z0-9]+", " ", six.ensure_str(text))

    tokens = re.split(r"\s+", text)
    if stemmer:
        # Only stem words more than 3 characters long.
        tokens = [stemmer.stem(x) if len(x) > 3 else x for x in tokens if x not in stopwords]

    # One final check to drop any empty or invalid tokens.
    tokens = ' '.join([x for x in tokens if re.match(r"^[a-z0-9]+$", six.ensure_str(x))])

    return tokens