from flask import Flask, request, jsonify
import zipfile
import os
import pandas as pd

app = Flask(__name__)

@app.route('/api/', methods=['POST'])
def answer_question():
    question = request.form.get('question')
    file = request.files.get('file')

    if file:
        file.save(file.filename)
        with zipfile.ZipFile(file.filename, 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(file.filename)

        csv_file = [f for f in os.listdir() if f.endswith('.csv')][0]
        df = pd.read_csv(csv_file)
        answer = df['answer'].iloc[0]
        os.remove(csv_file)
    else:
        answer = 'No file provided'

    return jsonify({'answer': str(answer)})

if __name__ == '__main__':
    app.run(debug=True)