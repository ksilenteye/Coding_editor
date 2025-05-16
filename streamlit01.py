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
    except Exception:
        error = traceback.format_exc()
        return None, error

def main():
    st.title("🐍 Python Code Editor")

    # Sidebar with leveled examples
    st.sidebar.header("📚 Example Scripts by Level")
    
    # Level 1: Basics
    st.sidebar.subheader("Level 1: Basics")
    if st.sidebar.button("Hello World"):
        st.session_state.code = '''# Simple print statement
print("Hello, World!")'''

    if st.sidebar.button("Basic Math"):
        st.session_state.code = '''# Basic arithmetic operations
a = 10
b = 5
print(f"Addition: {a + b}")
print(f"Subtraction: {a - b}")
print(f"Multiplication: {a * b}")
print(f"Division: {a / b}")'''

    # Level 2: Variables and Types
    st.sidebar.subheader("Level 2: Variables & Types")
    if st.sidebar.button("Data Types"):
        st.session_state.code = '''# Working with different data types
name = "Alice"
age = 25
height = 1.75
is_student = True

print(f"Name: {name} ({type(name)})")
print(f"Age: {age} ({type(age)})")
print(f"Height: {height} ({type(height)})")
print(f"Is Student: {is_student} ({type(is_student)})")'''

    # Level 3: Control Flow
    st.sidebar.subheader("Level 3: Control Flow")
    if st.sidebar.button("If-Else"):
        st.session_state.code = '''# Grade calculator
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Score: {score}")
print(f"Grade: {grade}")'''

    # Level 4: Loops
    st.sidebar.subheader("Level 4: Loops")
    if st.sidebar.button("For Loop"):
        st.session_state.code = '''# Print multiplication table
number = 5
print(f"Multiplication table for {number}:")

for i in range(1, 11):
    result = number * i
    print(f"{number} x {i} = {result}")'''

    # Level 5: Functions
    st.sidebar.subheader("Level 5: Functions")
    if st.sidebar.button("Fibonacci"):
        st.session_state.code = '''def fibonacci(n):
    """Generate Fibonacci sequence up to n terms"""
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

print("First 10 Fibonacci numbers:")
fibonacci(10)'''

    # Level 6: Lists and Sorting
    st.sidebar.subheader("Level 6: Lists & Sorting")
    if st.sidebar.button("Bubble Sort"):
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

    # Level 7: Prime Numbers
    st.sidebar.subheader("Level 7: Number Theory")
    if st.sidebar.button("Prime Numbers"):
        st.session_state.code = '''def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_primes(start, end):
    """Find all prime numbers in a range"""
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

# Find primes between 1 and 100
primes = find_primes(1, 100)
print(f"Prime numbers between 1 and 100:")
print(primes)
print(f"Total count: {len(primes)}")'''

    # Level 8: Recursion
    st.sidebar.subheader("Level 8: Recursion")
    if st.sidebar.button("Tower of Hanoi"):
        st.session_state.code = '''def tower_of_hanoi(n, source, auxiliary, target):
    """Solve Tower of Hanoi puzzle"""
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    
    tower_of_hanoi(n-1, source, target, auxiliary)
    print(f"Move disk {n} from {source} to {target}")
    tower_of_hanoi(n-1, auxiliary, source, target)

# Solve for 3 disks
print("Tower of Hanoi solution for 3 disks:")
tower_of_hanoi(3, 'A', 'B', 'C')'''

    # Level 9: OOP
    st.sidebar.subheader("Level 9: Object-Oriented")
    if st.sidebar.button("Bank Account"):
        st.session_state.code = '''class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return f"Deposited ${amount}. New balance: ${self.balance}"
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Insufficient funds!"

# Create and use a bank account
account = BankAccount("Alice", 1000)
print(account.deposit(500))
print(account.withdraw(200))
print(account.withdraw(2000))'''

    # Level 10: Advanced
    st.sidebar.subheader("Level 10: Advanced")
    if st.sidebar.button("Binary Search Tree"):
        st.session_state.code = '''class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

# Create and test BST
bst = BinarySearchTree()
numbers = [50, 30, 70, 20, 40, 60, 80]

print("Inserting numbers:", numbers)
for num in numbers:
    bst.insert(num)

print("Inorder traversal of BST:", bst.inorder_traversal())'''

    # Initialize session state
    if 'code' not in st.session_state:
        st.session_state.code = 'print("Hello, World!")'

    # Layout columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Code Editor")
        
        # Use ACE editor if available, otherwise use standard text area
        if HAS_ACE:
            code = st_ace(
                value=st.session_state.code,
                language='python',
                theme='monokai',
                key="ace_editor",
                height=400,
                enable_snippets=True,
                show_gutter=True,
                wrap=True,
                auto_update=True,
                font_size=14,
                show_print_margin=True,
                annotations=None,
                markers=None,
                keybinding='vscode',
                min_lines=20,
                max_lines=None,
                placeholder='Write your Python code here...',
                focus=False,
                cursor_style="smooth",
                tab_size=4,
                show_invisibles=False,
                key_bindings={"find": "Ctrl-F", "replace": "Ctrl-H"},
            )
        else:
            code = st.text_area(
                "Python Code",
                value=st.session_state.code,
                height=400,
                key="code_editor"
            )
        
        st.session_state.code = code

        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if st.button("▶️ Run Code"):
                output, error = execute_code(code)
                if error:
                    st.exception(error)
                else:
                    st.success("Code executed successfully!")
                    st.code(output, language="text")

        with button_col2:
            if st.button("🧽 Beautify Code"):
                st.session_state.code = autopep8.fix_code(code)

    with col2:
        st.subheader("Help")
        st.markdown("""
        ### Instructions
        1. Choose an example by difficulty level
        2. Modify the code as needed
        3. Run or beautify your code

        ### Features
        - Code editor with syntax highlighting
        - Code autocompletion
        - Code beautification
        - Progressive learning examples
        
        ### Keyboard Shortcuts
        - **Tab**: Indent
        - **Shift+Tab**: Unindent
        """ + ("""
        - **Ctrl+Space**: Show completions
        - **Ctrl+F**: Find
        - **Ctrl+H**: Replace
        """ if HAS_ACE else ""))

if __name__ == "__main__":
    main() 