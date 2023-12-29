# backend/app.py
import os
import uuid
import time
import logging
from flask import Flask, render_template, request, jsonify
from pylint.lint import Run
from pylint.reporters.text import ParseableTextReporter
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
CORS(app, resources={r"/analyze": {"origins": "http://localhost:5000"}})  # Allow requests only from your frontend origin

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    try:
        code_file = request.files['codeFile']

        # Generate a unique temporary file name
        temp_files_dir = 'temp_files'
        os.makedirs(temp_files_dir, exist_ok=True)  # Ensure the directory exists

        temp_file_name = f'temp_file_{uuid.uuid4()}_{int(time.time())}.py'
        temp_file_path = os.path.join(temp_files_dir, temp_file_name)

        # Save the code to the temporary file using Flask's save method
        code_file.save(temp_file_path)

        # Log the content of the file for debugging
        with open(temp_file_path, 'r', encoding='utf-8') as temp_file:
            file_content = temp_file.read()
            logging.debug("File Content:\n%s" % file_content)

        # Run pylint without 'do_exit'
        pylint_result = Run([temp_file_path], exit=False)

        # Check if 'global_note' is present in pylint_result.linter.stats
        pylint_output = getattr(pylint_result.linter.stats, 'global_note', 'N/A')

        # Extract linting comments
        linting_comments = extract_comments_from_reporter(pylint_result.linter.reporter)

        result = {
            'message': f'Pylint Output: {pylint_output}',
            'linting_comments': linting_comments
        }

        return jsonify(result)  # Explicitly set the content type to JSON
    except Exception as e:
        result = {
            'error': f'An error occurred during analysis: {str(e)}'
        }
        logging.error('Error during analysis:', exc_info=True)  # Log the exception details
        return jsonify(result), 500

def extract_comments_from_reporter(reporter):
    if isinstance(reporter, ParseableTextReporter):
        return [msg.message for msg in reporter.data]
    return []

if __name__ == '__main__':
    app.run(debug=True)
