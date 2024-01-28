from src.utils import tokenize
from sentence_transformers import util
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def cosine_similarity(text1, text2):
    # Tokenize the text.
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    embedding1 = model.encode(tokens1, convert_to_tensor=True)
    embedding2 = model.encode(tokens2, convert_to_tensor=True)


    # Compute the cosine similarity.
    cosine_similarity_score = util.pytorch_cos_sim(embedding1, embedding2)

    return [tokens1, [x.item() for x in embedding1], tokens2, [x.item() for x in embedding2], cosine_similarity_score[0].item()]