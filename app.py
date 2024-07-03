from flask import Flask, request, render_template, redirect, url_for
import os
import webbrowser
from threading import Timer

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
    elif 'text' in request.form and request.form['text'] != '':
        text = request.form['text']
        result = process_text(text)
    else:
        return 'No file or text provided'
    
    return render_template('index.html', result=result)

def process_file(filepath):
    processed_lines = []
    with open(filepath, 'r') as f:
        for line in f:
            processed_lines.append(process_line(line))
    return ''.join(processed_lines)

def process_text(text):
    processed_lines = []
    for line in text.split('\n'):
        processed_lines.append(process_line(line))
    return '\n'.join(processed_lines)

def process_line(line):
    # Replace non-standard protocols
    line = line.replace('hxsp', 'http').replace('hxxp', 'http')
    # Remove defanging by replacing '[.]' with '.'
    line = line.replace('[.]', '.')
    return line

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Start the browser only if this is the main process
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
