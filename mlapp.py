from flask import Flask, request, jsonify,render_template
import traceback
import pickle
import pandas as pd
import sys
import os

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        fname = f.filename
        f.save(os.path.join("", fname))
        da = pd.read_json(fname)
        if pipeline:
            pr = pipeline.predict(da)[0]
            if pr == 0:
                prediction = "not likely to churn"
            else:
                prediction = "likely to churn"
        else:
            print("no model")
            prediction = "error"
        input = da.T.to_html(header=False, bold_rows=False, justify="left", border=1)
        return render_template("ack.html", input=input, prediction= prediction)
    
if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 5000
    pipeline = pickle.load(open('pl.pkl', 'rb'))
    app.run(debug=True)