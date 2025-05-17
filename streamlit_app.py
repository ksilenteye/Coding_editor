import streamlit as st
from streamlit_ace import st_ace
import io
import contextlib

st.set_page_config(layout="wide")
st.title("🐍 Python Code Editor")

# Example Scripts
example_scripts = {
    "Level01: Hello World": 'print("Hello, World!")',
    "Level02: Fibonacci": '''
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)
''',
    "Level03: Sorting": '''
def sort_example():
    arr = [5, 2, 9, 1]
    arr.sort()
    print("Sorted:", arr)

sort_example()
''',
    "Level04: Bubble Sort": '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
print("Original array:", numbers)
print("Sorted array:", bubble_sort(numbers.copy()))
'''
}

# State init
if "selected_script" not in st.session_state:
    st.session_state.selected_script = list(example_scripts.values())[0]
if "editor_code" not in st.session_state:
    st.session_state.editor_code = st.session_state.selected_script

# Layout
editor_col, help_col = st.columns([3, 1])

with editor_col:
    st.markdown("### 🖊️ Code Editor")
    st.session_state.editor_code = st_ace(
        value=st.session_state.editor_code,
        language="python",
        theme="monokai",
        key="editor"
    )

    run = st.button("▶️ Run Code")
    output = ""

    if run:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                exec(st.session_state.editor_code, {})
            except Exception as e:
                print(f"Error: {e}")
            output = buf.getvalue()

    if run:
        st.success("Code executed successfully!")
        st.code(output or "No output", language="text")

    # ↓ Below the output: Example scripts as horizontal list
    st.markdown("### 📜 Example Scripts")
    cols = st.columns(len(example_scripts))
    for i, (name, script) in enumerate(example_scripts.items()):
        if cols[i].button(name):
            st.session_state.selected_script = script
            st.session_state.editor_code = script
            st.rerun()

    # ↓ Below horizontal buttons: show currently selected code
    st.markdown("### 🔍 Selected Example Script")
    st.code(st.session_state.selected_script, language="python")

with help_col:
    st.markdown("### Help")
    st.markdown("""
    - Write code above ☝️
    - Click **Run Code** ▶️ to execute
    - Choose scripts below to auto-load them
    - Use `print()` to show output
    """)
