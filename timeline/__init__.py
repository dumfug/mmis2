import json
from flask import Flask, render_template, request, Response


app = Flask(__name__)

@app.route('/get_dummy_data')
def dummy_data():
    data = [{"date":"2014-01-01", "value":190000000},
            {"date":"2014-01-02", "value":190379978},
            {"date":"2014-01-03", "value":90493749},
            {"date":"2014-01-04", "value":190785250}]

    return Response(json.dumps(data), mimetype='application/json')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
