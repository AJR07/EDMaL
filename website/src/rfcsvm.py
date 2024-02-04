import joblib
rfc_model = joblib.load('./src/models/rfc.pkl')
svm_model = joblib.load('./src/models/svm.pkl')

def rfc(ngrams):
	return int(rfc_model.predict([ngrams])[0])
def svm(ngrams):
	return int(svm_model.predict([ngrams])[0])