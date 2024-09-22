import streamlit as st
import subprocess
import json
from code_editor import code_editor

def compile_and_run_rust(code):
    # Write the code to a file
    with open('code.rs', "w") as file:
        file.write(code)
    
    # Compile the Rust code
    process1 = subprocess.Popen(["rustc", "code.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    compile_result = process1.communicate()
    
    if process1.returncode != 0:
        # If compilation failed, return the error
        return f"Compilation Error:\n{compile_result[1]}"
    
    # Run the compiled code
    process2 = subprocess.Popen(["./code"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    run_result = process2.communicate()
    
    if process2.returncode != 0:
        # If execution failed, return the error
        return f"Execution Error:\n{run_result[1]}"
    
    # Return the output
    return run_result[0]

st.title('🦀 Rust in Streamlit')

# Read initial Rust code
with open('hello.rs') as rust_file:
    initial_rust_code = rust_file.read()

# Read button settings
with open('btn_settings.json', 'r') as btn_file:
    btn_settings = json.load(btn_file)

# Initialize session state for Rust code if it doesn't exist
if 'rust_code' not in st.session_state:
    st.session_state.rust_code = initial_rust_code

# Display code editor
response_dict = code_editor(st.session_state.rust_code, lang="rust", buttons=btn_settings)

# Check if the code has been updated
if response_dict['text'] != st.session_state.rust_code:
    st.session_state.rust_code = response_dict['text']
    st.experimental_rerun()

# Display the current code
st.code(st.session_state.rust_code)

# Compile and run the code
result = compile_and_run_rust(st.session_state.rust_code)
st.write(result)
