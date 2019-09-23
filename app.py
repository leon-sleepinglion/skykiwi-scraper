from flask import Flask, Markup, request, jsonify, render_template
from tinydb import TinyDB


app = Flask(__name__)
db = TinyDB('./entry.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/room')
def room():
    return jsonify(result=db.all())

if __name__ == '__main__':
    app.run(debug=True)