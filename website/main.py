from flask import Flask, render_template

app = Flask(__name__, template_folder="static")

@app.route("/home")
@app.route("/")
def hello_world():
    return render_template("./main.html")

app.run(port=8000, debug=True)