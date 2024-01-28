from sentence_transformers import SentenceTransformer, util
from nltk.stem.porter import PorterStemmer
import re
import six

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
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
    embedding_original = model.encode(tokens, convert_to_tensor=True)

    return [tokens, {k: v.item() for k, v in embedding_original.items()}]
