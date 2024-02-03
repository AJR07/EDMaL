from src.utils import tokenize
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def editDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def edit_distance(text1, text2):
    # Tokenize the text.
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    editDistanceScore = -editDistance(' '.join(tokens1), ' '.join(tokens2))

    return [tokens1, tokens2, editDistanceScore, "AI Generated" if editDistanceScore > -729.1 else "Human Written"]