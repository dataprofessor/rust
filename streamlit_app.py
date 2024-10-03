import streamlit as st
import subprocess
import json
import os
import re
from code_editor import code_editor

def wrap_in_main(code):
    # Check if there's already a main function
    if re.search(r'fn\s+main\s*\(', code):
        return code
    else:
        # Wrap the code in a main function
        return f"""
fn main() {{
    {code}
}}
"""

def run_rust_code(code):
    # Wrap the code in a main function if it's not already there
    wrapped_code = wrap_in_main(code)
    
    with open('code.rs', "w") as file:
        file.write(wrapped_code)
    
    # Compile the Rust code
    compile_process = subprocess.Popen(["rustc", "code.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    compile_stdout, compile_stderr = compile_process.communicate()
    
    if compile_process.returncode != 0:
        return f"Compilation Error:\n{compile_stderr}"
    
    # Determine the correct binary name
    binary_name = "code.exe" if os.name == 'nt' else "./code"
    
    # Check if the binary exists
    if not os.path.exists(binary_name):
        return f"Error: Compiled binary not found. Expected at: {binary_name}"
    
    # Run the compiled binary
    run_process = subprocess.Popen([binary_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    run_stdout, run_stderr = run_process.communicate()
    
    if run_process.returncode != 0:
        return f"Runtime Error:\n{run_stderr}"
    
    return run_stdout

def code_changed():
    if 'current_code' in st.session_state and st.session_state.current_code != st.session_state.previous_code:
        st.session_state.rust_output = run_rust_code(st.session_state.current_code)
        st.session_state.previous_code = st.session_state.current_code

st.title('🦀 Rust in Streamlit')

# Initialize with a simple "Hello, World!" program if no file exists
initial_code = """
println!("Hello, World!");
"""

try:
    with open('hello.rs') as rust_file:
        initial_code = rust_file.read()
except FileNotFoundError:
    st.warning("hello.rs file not found. Starting with a basic 'Hello, World!' program.")

try:
    with open('btn_settings.json', 'r') as btn_file:
        btn_settings = json.load(btn_file)
except FileNotFoundError:
    st.warning("btn_settings.json file not found. Using default settings.")
    btn_settings = {}  # Use empty dict as default

if 'previous_code' not in st.session_state:
    st.session_state.previous_code = initial_code

response_dict = code_editor(initial_code, lang="rust", buttons=btn_settings, key="code_editor")

st.session_state.current_code = response_dict['text']
code_changed()

st.subheader("Rust Code:")
st.code(st.session_state.current_code, language="rust")

st.subheader("Output:")
if 'rust_output' in st.session_state:
    st.text(st.session_state.rust_output)
