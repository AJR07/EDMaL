from rouge_score.rouge_scorer import _create_ngrams
import six
from src.utils import tokenize

#! N-Gram Score Generation
def get_score_ngrams(target_ngrams, prediction_ngrams):
    intersection_ngrams_count = 0
    ngram_dict = {}
    for ngram in six.iterkeys(target_ngrams):
        intersection_ngrams_count += min(target_ngrams[ngram],
                                        prediction_ngrams[ngram])
        ngram_dict[ngram] = min(target_ngrams[ngram], prediction_ngrams[ngram])
    target_ngrams_count = sum(target_ngrams.values()) # prediction_ngrams
    return intersection_ngrams_count / max(target_ngrams_count, 1), ngram_dict


def get_ngram_info(article_tokens, summary_tokens, _ngram):
    article_ngram = _create_ngrams( article_tokens , _ngram)
    summary_ngram = _create_ngrams( summary_tokens , _ngram)
    ngram_score, ngram_dict = get_score_ngrams( article_ngram, summary_ngram) 
    return ngram_score, ngram_dict, sum( ngram_dict.values() )

def ngram(masked, regenerated):
    masked_tokenized = tokenize(masked)

    # going through each generation
    ngram_scores = []
    generated_tokenized = tokenize(regenerated)
    
    # go through each possible n gram from 1 to 25
    for _ngram in range(1, 25):
        ngram_score, _, _ = get_ngram_info(masked_tokenized, generated_tokenized, _ngram)
        ngram_scores.append(ngram_score / len(generated_tokenized))

    return [masked_tokenized, generated_tokenized, ngram_scores]