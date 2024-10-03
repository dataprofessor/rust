import streamlit as st
import subprocess
import json
import os
from code_editor import code_editor

def run_rust_code(code):
    with open('code.rs', "w") as file:
        file.write(code)
    
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

with open('content/hello.rs') as rust_file:
    rust_code = rust_file.read()

with open('content/btn_settings.json', 'r') as btn_file:
    btn_settings = json.load(btn_file)

if 'previous_code' not in st.session_state:
    st.session_state.previous_code = rust_code

response_dict = code_editor(rust_code, lang="rust", buttons=btn_settings, key="code_editor")

st.session_state.current_code = response_dict['text']
code_changed()

st.code(st.session_state.current_code)

if 'rust_output' in st.session_state:
    st.write(st.session_state.rust_output)
