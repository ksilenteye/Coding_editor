import streamlit as st
import sys
from io import StringIO
import contextlib
import traceback

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

def analyze_code(code):
    """Analyze and explain the given Python code."""
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
    
    # Initialize session state for code if it doesn't exist
    if 'code' not in st.session_state:
        st.session_state.code = 'print("Hello, World!")'
    
    # Sidebar with examples
    with st.sidebar:
        st.header("Example Scripts")
        if st.button("Level01: Hello World"):
            st.session_state.code = 'print("Hello, World!")'
        if st.button("Level02: Fibonacci"):
            st.session_state.code = '''def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)'''
        if st.button("Level03: Sorting"):
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

        if st.button("Level04: Bubble Sort"):
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

        if st.button("Level05: Prime no"):
            st.session_state.code = ''''def is_prime(n):
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

        if st.button("Level06: Tower of Hanoi"):
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

        if st.button("Level07: Object-Oriented"):
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

        if st.button("Level08: Binary Search Tree"):
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
    
    # Main area with code editor and output
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Code Editor")
        code = st.text_area("", st.session_state.code, height=400, key="code_editor")
                # Use ACE editor if available, otherwise use standard text area
        if HAS_ACE:
            code = st_ace(
                value=st.session_state.code,
                language='python',
                theme='monokai',
                height=400,
                key="ace_editor"
            )
        else:
            code = st.text_area(
                "Python Code",
                value=st.session_state.code,
                height=400,
                key="code_editor"
            )
        st.session_state.code = code
        
        # Create a row of buttons using columns
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