import streamlit as st
import sys
from io import StringIO
import contextlib
import traceback
import autopep8

st.set_page_config(page_title="Python Code Editor", layout="wide")

# Try to import streamlit-ace, use fallback if not available
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
            safe_globals = create_safe_globals()
            exec(code, safe_globals, {})
        return output.getvalue(), None
    except Exception as e:
        error = f"{type(e).__name__}: {str(e)}"
        return None, error

def main():
    st.title("🐍 Python Code Editor")

    if 'code' not in st.session_state:
        st.session_state['code'] = 'print("Hello, World!")'

    if 'example_display' not in st.session_state:
        st.session_state['example_display'] = ''

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
            "Level04: Bubble Sort": '''# Bubble Sort Algorithm Example
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Example usage
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
                st.session_state['example_display'] = example_code

    # Main area with code editor and output
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Code Editor")

        if HAS_ACE:
            code_input = st_ace(
                value=st.session_state['code'],
                language='python',
                theme='monokai',
                height=400,
                key="code_editor"
            )
            if code_input is not None:
                st.session_state['code'] = code_input
        else:
            st.session_state['code'] = st.text_area(
                "Python Code",
                value=st.session_state['code'],
                height=400,
                key="code_editor"
            )

        st.markdown("### Selected Example Code")
        st.code(st.session_state['example_display'], language='python')

        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if st.button("▶️ Run Code"):
                output, error = execute_code(st.session_state['code'])

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
        3. Click any Example Script to view it
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
