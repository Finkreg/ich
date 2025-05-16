from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Flask"

@app.route("/handle_url_params")
def handle_params():
    if "greeting" in request.args.keys() and "name" in request.args.keys():
        greeting = request.args["greeting"]
        name = request.args.get("name")
        return f"{greeting}, {name}"
    else:
        return "Some parameters are missing"


@app.route("/user/<name>")
def greet(name):
    return f"Hello, {name}"

if __name__ == "__main__":
    app.run(debug=True)

