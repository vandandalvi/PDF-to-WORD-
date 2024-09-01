from flask import Flask, request, render_template, send_file
import os
from pdf2docx import Converter
import pdfplumber
import io
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/tools', methods=['GET', 'POST'])
def tools():
    return render_template('tools.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup form submission here
        username = request.form['username']
        password = request.form['password']
        # Process the data or save it to a database
        
        # Redirect the user to another page after signup
    else:
        # Handle GET request for the signup page
        return render_template('signup.html')
@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    input_pdf = file.filename
    file.save(input_pdf)

    output_word = input_pdf.replace('.pdf', '.docx')
    output_text = input_pdf.replace('.pdf', '.txt')

    # Convert PDF to Word
    cv = Converter(input_pdf)
    cv.convert(output_word)
    cv.close()

    # Convert PDF to Text
    pdf = pdfplumber.open(input_pdf)
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
    pdf.close()

    with open(output_text, 'w') as f:
        f.write(text)

    return send_file(output_word, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)