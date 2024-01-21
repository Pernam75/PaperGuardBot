# create an API with Flask
# run with: python simple_api.py

from flask import Flask, jsonify, request

app = Flask(__name__)

# create a simple test route on the default URL
@app.route("/")
def test():
    # return Hello World! to the caller
    return jsonify(response="Hello World!", status=200)

# create a route that gets "input" in the query string and returns it to the caller
@app.route("/echo", methods=["GET"])
def echo():
    # get the input parameter from the query string
    input = request.args.get("input")
    # return the input parameter, with a message to the caller
    return jsonify(response=f"{input} from API", status=200)

# run the app
if __name__ == "__main__":
    app.run(debug=True)