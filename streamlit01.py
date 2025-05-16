import streamlit as st
import sys
from io import StringIO
import contextlib
import traceback
import autopep8
from streamlit_ace import st_ace

st.set_page_config(page_title="Python Code Editor", layout="wide")

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
            'chr': chr,
            'ord': ord,
        }
    }
    return safe_globals

def execute_code(code):
    output = StringIO()
    error = None
    
    try:
        with contextlib.redirect_stdout(output):
            safe_globals = create_safe_globals()
            exec(code, safe_globals, {})
        return output.getvalue(), None
    except Exception:
        error = traceback.format_exc()
        return None, error

def analyze_code(code):
    try:
        if code.strip() == '':
            return "No code to explain."
        
        if 'print(' in code:
            return 'This code uses the print() function to display text or values.'
        elif 'def ' in code:
            return 'This code defines a function. Functions are reusable blocks of code.'
        elif 'for ' in code:
            return 'This code contains a loop that repeats a set of instructions.'
        elif 'if ' in code:
            return 'This code makes decisions using conditional statements.'
        elif 'while ' in code:
            return 'This code uses a while loop to repeat actions while a condition is true.'
        elif any(op in code for op in ['+', '-', '*', '/', '%']):
            return 'This code performs mathematical operations.'
        elif '=' in code:
            return 'This code assigns values to variables.'
        else:
            return 'This code performs basic operations.'
    except Exception as e:
        return f"Error analyzing code: {str(e)}"

def main():
    st.title("🐍 Python Code Editor")

    # Sidebar - Beginner Mode & Examples
    beginner_mode = st.sidebar.checkbox("👶 Beginner Mode", value=True)

    st.sidebar.header("Example Scripts")
    if st.sidebar.button("Hello World"):
        st.session_state.code = 'print("Hello, World!")'
    if st.sidebar.button("Fibonacci"):
        st.session_state.code = '''def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)'''
    if st.sidebar.button("Sorting"):
        st.session_state.code = '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
print("Original array:", numbers)
print("Sorted array:", bubble_sort(numbers.copy()))'''

    # Initialize session state
    if 'code' not in st.session_state:
        st.session_state.code = 'print("Hello, World!")'

    # Layout columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Code Editor")
        code = st_ace(value=st.session_state.code, language='python', theme='monokai', key="ace_editor", height=400)
        st.session_state.code = code

        button_col1, button_col2, button_col3 = st.columns(3)

        with button_col1:
            if st.button("▶️ Run Code"):
                output, error = execute_code(code)
                if error:
                    st.exception(error)
                else:
                    st.success("Code executed successfully!")
                    st.code(output, language="text")

        with button_col2:
            if st.button("❓ Explain Code"):
                explanation = analyze_code(code)
                st.info(explanation)

                if beginner_mode:
                    if 'for ' in code:
                        st.warning("🧠 Hint: 'for' loops are great for repeating steps over items like lists.")
                    elif 'def ' in code:
                        st.warning("🧠 Hint: Functions help organize code into reusable blocks.")

        with button_col3:
            if st.button("🧽 Beautify Code"):
                st.session_state.code = autopep8.fix_code(code)

    with col2:
        st.subheader("Help")
        st.markdown("""
        ### Instructions
        1. Write or paste your Python code
        2. Run, explain, or beautify it
        3. Use beginner mode for hints

        ### Features
        - Syntax highlighting editor
        - Code execution and explanation
        - Code beautification
        - Beginner-friendly guidance
        - Example snippets
        """)

if __name__ == "__main__":
    main() 