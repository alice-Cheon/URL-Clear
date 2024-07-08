from flask import Flask, request, render_template
from markupsafe import Markup
import os
from threading import Timer
import webbrowser
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    result = ''
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        result = process_file(filepath)
        os.remove(filepath)  # Clean up the uploaded file after processing
    elif 'content' in request.form and request.form['content'] != '':
        content = request.form['content']
        result = process_text(content)
    else:
        return 'No file or text provided'
    
    return render_template('index.html', result=Markup(result))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    return process_text(content)

def process_text(text):
    # Check if text contains a table
    if '<table' in text:
        soup = BeautifulSoup(text, 'html.parser')
        for td in soup.find_all('td'):
            lines = td.decode_contents().split('<br>')
            processed_lines = [process_line(line) for line in lines]
            td.clear()
            for i, line in enumerate(processed_lines):
                td.append(BeautifulSoup(line, 'html.parser'))
                if i < len(processed_lines) - 1:
                    td.append('<br>')
        return str(soup)
    else:
        lines = text.split('\n')
        processed_lines = [process_line(line) for line in lines]
        processed_text = '<br>'.join(processed_lines)
        return processed_text

def process_line(line):
    # Replace non-standard protocols
    line = line.replace('hxsp', 'http').replace('hxxp', 'http')
    line = re.sub(r'http\[:\]', 'http:', line)
    line = re.sub(r'https\[:\]', 'https:', line)
    # Remove defanging by replacing '[.]' with '.'
    line = line.replace('[.]', '.')
    # Remove port from IP address
    line = re.sub(r'(\d+\.\d+\.\d+\.\d+):\d+', r'\1', line)
    return line

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)