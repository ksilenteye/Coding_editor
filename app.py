from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
from io import StringIO
import contextlib
import traceback
import threading
import queue
import concurrent.futures
import time
import ast
import re

app = Flask(__name__)
CORS(app)

class TimeoutException(Exception):
    pass

class InputManager:
    def __init__(self):
        self.input_queue = queue.Queue()
        self.current_input = None
    
    def mock_input(self, prompt=''):
        # In a real implementation, this would wait for user input
        # For now, we'll return a default value
        return "Test User"

def create_safe_globals():
    safe_globals = {
        '__builtins__': {
            'print': print,
            'len': len,
            'range': range,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'sum': sum,
            'min': min,
            'max': max,
            'enumerate': enumerate,
            'zip': zip,
            'type': type,
            'input': InputManager().mock_input,
            'chr': chr,
            'ord': ord,
        }
    }
    return safe_globals

def analyze_syntax_error(error_msg, code):
    """Analyze syntax errors and provide specific feedback."""
    if "invalid syntax" in error_msg:
        # Check for common syntax issues
        if ":" not in code:
            return "Missing colon (:) after control statement"
        if code.count("(") != code.count(")"):
            return "Mismatched parentheses"
        if code.count("[") != code.count("]"):
            return "Mismatched square brackets"
        if code.count("{") != code.count("}"):
            return "Mismatched curly braces"
    elif "unexpected indent" in error_msg:
        return "Incorrect indentation. Check your code's indentation level"
    elif "expected an indented block" in error_msg:
        return "Missing indentation after control statement"
    return error_msg

def analyze_name_error(error_msg):
    """Analyze name errors and provide specific feedback."""
    match = re.search(r"name '(\w+)' is not defined", error_msg)
    if match:
        var_name = match.group(1)
        if var_name in ['print', 'input', 'len', 'range']:
            return f"The function '{var_name}' needs to be imported or defined"
        return f"The variable or function '{var_name}' hasn't been defined before using it"
    return error_msg

def analyze_type_error(error_msg):
    """Analyze type errors and provide specific feedback."""
    if "unsupported operand type(s)" in error_msg:
        return "You're trying to perform an operation on incompatible types. Check the types of your variables"
    if "object is not callable" in error_msg:
        return "You're trying to call something that isn't a function"
    return error_msg

def get_error_context(error_msg, code):
    """Get the context around the error."""
    try:
        line_match = re.search(r"line (\d+)", error_msg)
        if line_match:
            line_num = int(line_match.group(1))
            lines = code.split('\n')
            start = max(0, line_num - 2)
            end = min(len(lines), line_num + 1)
            context = '\n'.join(f"{i+1}: {line}" for i, line in enumerate(lines[start:end]))
            return {
                'line_number': line_num,
                'context': context
            }
    except Exception:
        pass
    return None

def analyze_error(error_msg, code):
    """Analyze the error and provide helpful feedback."""
    if "SyntaxError" in error_msg:
        return analyze_syntax_error(error_msg, code)
    elif "NameError" in error_msg:
        return analyze_name_error(error_msg)
    elif "TypeError" in error_msg:
        return analyze_type_error(error_msg)
    elif "IndentationError" in error_msg:
        return "Check your indentation. Python uses indentation to define code blocks"
    elif "ZeroDivisionError" in error_msg:
        return "You're trying to divide by zero"
    return error_msg

def execute_with_timeout(code, timeout=5):
    output = StringIO()
    result = None
    error = None
    error_analysis = None
    error_context = None
    
    def run_code():
        nonlocal result, error, error_analysis, error_context
        try:
            # First, try to parse the code to catch syntax errors
            ast.parse(code)
            
            safe_globals = create_safe_globals()
            local_env = {}
            with contextlib.redirect_stdout(output):
                exec(code, safe_globals, local_env)
            result = output.getvalue()
        except Exception as e:
            error = f"{type(e).__name__}: {str(e)}"
            error_analysis = analyze_error(error, code)
            error_context = get_error_context(error, code)
            print(f"Execution error: {error}")
            print(f"Traceback: {traceback.format_exc()}")
    
    # Create and start the thread
    code_thread = threading.Thread(target=run_code)
    code_thread.start()
    
    # Wait for the thread to complete or timeout
    code_thread.join(timeout)
    
    if code_thread.is_alive():
        # If thread is still running after timeout, return timeout error
        return None, "Code execution timed out (limit: 5 seconds)", None, None
    
    return result, error, error_analysis, error_context

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    if not request.is_json:
        return jsonify({
            'error': 'Request must be JSON'
        }), 400

    data = request.get_json()
    
    if 'code' not in data:
        return jsonify({
            'error': 'No code provided'
        }), 400
        
    code = data['code']
    print(f"Received code: {code}")  # Debug log
    
    result, error, error_analysis, error_context = execute_with_timeout(code)
    
    if result:
        print(f"Execution output: {result}")  # Debug log
    
    response = {
        'output': result,
        'error': error,
        'error_analysis': error_analysis,
        'error_context': error_context
    }
    
    print(f"Sending response: {response}")  # Debug log
    return jsonify(response)

if __name__ == '__main__':
    print("Starting Flask server on port 8080...")
    app.run(debug=True, port=8080, host='0.0.0.0')