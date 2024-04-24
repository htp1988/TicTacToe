from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Define the root route '/' that renders and returns the 'index.html' template when accessed
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
