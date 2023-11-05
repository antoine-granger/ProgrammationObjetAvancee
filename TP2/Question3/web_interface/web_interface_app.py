from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
app.debug = True

API_GATEWAY_URL = "http://api-gateway:5000"


@app.route('/')
def index():
    books = requests.get(f"{API_GATEWAY_URL}/books").json()
    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
