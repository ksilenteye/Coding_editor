import streamlit as st
import sys
from io import StringIO
import contextlib
import traceback

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
    except Exception as e:
        error = f"{type(e).__name__}: {str(e)}"
        return None, error

def analyze_code(code):
    try:
        if code.strip() == '':
            return "No code to explain."

        if 'print(' in code:
            return 'This code uses the print() function to display text or values to the console/output. Print statements are commonly used for outputting information to users or debugging.'
        elif 'def ' in code:
            return 'This code defines a function. Functions are reusable blocks of code that perform specific tasks.'
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

    if 'code_editor' not in st.session_state:
        st.session_state.code_editor = 'print("Hello, World!")'

    # Sidebar with examples
    with st.sidebar:
        st.header("Example Scripts")

        examples = {
            "Level01: Hello World": 'print("Hello, World!")',
            "Level02: Fibonacci": '''def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)''',
            "Level03: Sorting": '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
print("Original array:", numbers)
print("Sorted array:", bubble_sort(numbers.copy()))''',
            "Level04: Bubble Sort": '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
print("Original array:", numbers)
print("Sorted array:", bubble_sort(numbers.copy()))''',
            "Level05: Prime no": '''def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

for i in range(20):
    if is_prime(i):
        print(i, end=" ")''',
            "Level06: Tower of Hanoi": '''def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n-1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n-1, auxiliary, target, source)

hanoi(3, 'A', 'C', 'B')''',
            "Level07: Object-Oriented": '''class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, my name is {self.name}.")

p = Person("Alice")
p.greet()''',
            "Level08: Binary Search Tree": '''class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def inorder(root):
    if root:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)

r = Node(50)
r.left = Node(30)
r.right = Node(70)
inorder(r)'''
        }

        for label, example_code in examples.items():
            if st.button(label):
                st.session_state.code_editor = example_code

    # Main area with code editor and output
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Code Editor")
        code = st.text_area("", st.session_state.get("code_editor", 'print("Hello, World!")'), height=400, key="code_editor")
        st.session_state.code = code

        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if st.button("▶️ Run Code"):
                output, error = execute_code(code)

                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success("Code executed successfully!")
                    st.code(output, language="text")

        with button_col2:
            if st.button("❓ Explain Code"):
                explanation = analyze_code(code)
                st.info(explanation)

    with col2:
        st.subheader("Help")
        st.markdown("""
        ### Instructions
        1. Write or paste your Python code in the editor
        2. Click "Run Code" to execute
        3. Click "Explain Code" for explanation
        4. See output below the editor

        ### Features
        - Safe execution environment
        - Code explanation
        - Example scripts in sidebar
        - Real-time output

        ### Tips
        - Use print() to see output
        - Check example scripts for inspiration
        - Clear formatting is maintained
        """)

if __name__ == "__main__":
    main()
