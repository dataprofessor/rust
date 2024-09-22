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

# Use st.empty to create a placeholder for the code editor
code_editor_placeholder = st.empty()

# Create a placeholder for the output
output_placeholder = st.empty()

# Function to update code and run
def update_and_run(code):
    st.session_state.rust_code = code
    result = compile_and_run_rust(code)
    output_placeholder.write(result)

# Initialize session state for Rust code if it doesn't exist
if 'rust_code' not in st.session_state:
    st.session_state.rust_code = initial_rust_code

# Display code editor
response_dict = code_editor_placeholder.code_editor(
    st.session_state.rust_code,
    lang="rust",
    buttons=btn_settings,
    key="rust_code_editor"
)

# Check if the code has been updated
if response_dict['text'] != st.session_state.rust_code:
    update_and_run(response_dict['text'])

# Display the current code
st.code(st.session_state.rust_code)
