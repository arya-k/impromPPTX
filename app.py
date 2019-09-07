from flask import Flask, request, jsonify
from data.main_function import gen_element

app = Flask(__name__)


@app.route('/')
def get():
    text = request.args['text']
    event = request.args['event']
    return jsonify(gen_element(text, event == "next_slide"))


if __name__ == "__main__":
    app.run(debug=True, port=8001)
