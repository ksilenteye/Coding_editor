import streamlit as st
import sys
from io import StringIO
import contextlib
import traceback
import autopep8

st.set_page_config(page_title="Python Code Editor", layout="wide")

try:
    from streamlit_ace import st_ace
    HAS_ACE = True
except ImportError:
    HAS_ACE = False

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
            # Create a safe environment for code execution
            safe_globals = create_safe_globals()
            exec(code, safe_globals, {})
        return output.getvalue(), None
    except Exception as e:
        error = f"{type(e).__name__}: {str(e)}"
        return None, error

def main():
    st.title("🐍 Python Code Editor")
    
    # Initialize session state for code if it doesn't exist
    if 'code' not in st.session_state:
        st.session_state.code = 'print("Hello, World!")'
    
    # Sidebar with examples
    with st.sidebar:
        st.header("Example Scripts")
        if st.button("Hello World"):
            st.session_state.code = 'print("Hello, World!")'
        if st.button("Fibonacci"):
            st.session_state.code = '''def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)'''
        if st.button("Sorting"):
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
    
    # Main area with code editor and output
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Code Editor")
        if HAS_ACE:
            code = st_ace(
                value=st.session_state.code,
                language='python',
                theme='monokai',
                height=400,
                key="ace_editor"
            )
        else:
            code = st.text_area("", st.session_state.code, height=400, key="code_editor")
        st.session_state.code = code
        
        if st.button("▶️ Run Code"):
            output, error = execute_code(code)
            
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("Code executed successfully!")
                st.code(output, language="text")
    
    with col2:
        st.subheader("Help")
        st.markdown("""
        ### Instructions
        1. Write or paste your Python code in the editor
        2. Click "Run Code" to execute
        3. See output below the editor
        
        ### Features
        - Safe execution environment
        - Example scripts in sidebar
        - Real-time output
        
        ### Tips
        - Use print() to see output
        - Check example scripts for inspiration
        - Clear formatting is maintained
        """)

if __name__ == "__main__":
    main() 