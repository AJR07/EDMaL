from flask import Flask, render_template, request, jsonify 
from src.prune import prune
from src.tokenization import tokenize
from src.regenerate import regenerate

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
        return jsonify(error=str(e)), 500

@app.route("/api/regenerate", methods=["POST"])
def api_regenerate():
    try:
        data = request.get_json()
        input_data = data['input_data']

        result = regenerate(input_data)
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 500
    
@app.route("/api/tokenization", methods=["POST"])
def api_tokenization():
    try:
        data = request.get_json()
        input_data = data['input_data']

        result = tokenize(input_data)
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 500


#! Actual Routes
@app.route("/home")
@app.route("/")
def hello_world():
    return render_template("./main.html", functions={
        "prune": prune,
    })

app.run(port=8000, debug=True)