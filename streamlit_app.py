import streamlit as st
import subprocess
import json
from code_editor import code_editor

def update_and_run_code():
    # Write the updated code to file
    with open('code.rs', "w") as file:
        file.write(st.session_state.rust_code)
    
    # Compile and run the Rust code
    process1 = subprocess.Popen(["rustc", "code.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process1.wait()  # Wait for compilation to finish
    
    if process1.returncode == 0:  # Check if compilation was successful
        process2 = subprocess.Popen(["./code"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result2 = process2.communicate()
        st.session_state.output = result2[0]
    else:
        st.session_state.output = "Compilation error: " + process1.communicate()[1]

st.title('🦀 Rust in Streamlit')

# Initialize session state
if 'rust_code' not in st.session_state:
    with open('hello.rs') as rust_file:
        st.session_state.rust_code = rust_file.read()

if 'output' not in st.session_state:
    st.session_state.output = ""

# Load button settings
with open('btn_settings.json', 'r') as btn_file:
    btn_settings = json.load(btn_file)

# Use the code editor
response_dict = code_editor(st.session_state.rust_code, lang="rust", buttons=btn_settings)

# Update session state when code changes
if response_dict['text'] != st.session_state.rust_code:
    st.session_state.rust_code = response_dict['text']
    st.rerun()  # Rerun the script to update the UI

# Display the current code
st.code(st.session_state.rust_code)

# Button to update and run the code
if st.button('Update and Run Code'):
    update_and_run_code()

# Display the output
st.write(st.session_state.output)
