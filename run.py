from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1>Aviad Azriel Say Hello</h1>"

if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')


