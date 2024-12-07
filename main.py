import requests, json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    else:
        print(request.form['city_start'])
        print(request.form['city_end'])

if __name__ == '__main__':
    app.run(debug=True)



