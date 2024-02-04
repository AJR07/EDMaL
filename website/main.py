from flask import Flask, render_template, request, jsonify 
from src.prune import prune
from src.cosine_similarity import cosine_similarity
from src.regenerate import regenerate
from src.edit_distance import edit_distance
from src.ngram import ngram
from src.rfcsvm import rfc, svm

import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')

app = Flask(__name__, template_folder="static")

#! APIs
@app.route("/api/prune", methods=["POST"])
def api_prune():
    try:
        data = request.get_json()
        input_data = data['input_data']
    
        result = prune(input_data)
        return jsonify(result=result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500

@app.route("/api/regenerate", methods=["POST"])
def api_regenerate():
    try:
        data = request.get_json()
        input_data = data['input_data']

        result = regenerate(input_data)
        return jsonify(result=result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500
    
@app.route("/api/cosine-similarity", methods=["POST"])
def api_cos_similarity():
    try:
        data = request.get_json()
        text1 = data['text1']
        text2 = data['text2']

        result = cosine_similarity(text1, text2)
        return jsonify(result=result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500

@app.route("/api/edit-distance", methods=["POST"])
def api_edit_distance():
    try:
        data = request.get_json()
        text1 = data['text1']
        text2 = data['text2']

        result = edit_distance(text1, text2)
        return jsonify(result=result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500
    
@app.route("/api/ngram", methods=["POST"])
def api_ngram():
    try:
        data = request.get_json()
        text1 = data['text1']
        text2 = data['text2']

        result = ngram(text1, text2)
        return jsonify(result=result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500
    
@app.route("/api/rfc", methods=["POST"])
def api_rfc():
    try:
        data = request.get_json()
        ngram = data['ngram']

        result = rfc(ngram)
        return jsonify(result=result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500
    
@app.route("/api/svm", methods=["POST"])
def api_svm():
    try:
        data = request.get_json()
        ngram = data['ngram']

        result = svm(ngram)
        return jsonify(result=result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500

#! Actual Routes
@app.route("/home")
@app.route("/")
def hello_world():
    return render_template("./main.html", functions={
        "prune": prune,
    })

app.run(port=8000, debug=True)