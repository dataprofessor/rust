import streamlit as st
import subprocess
import json
from code_editor import code_editor

def compile_and_run_rust(code):
    # Ensure there's a main function
    if "fn main()" not in code:
        code = "fn main() {\n    " + code.replace("\n", "\n    ") + "\n}"
    
    # Write the code to a file
    with open('code.rs', "w") as file:
        file.write(code)
    
    # Compile the Rust code
    process1 = subprocess.Popen(["rustc", "code.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    compile_result = process1.communicate()
    
    if process1.returncode != 0:
        return f"Compilation Error:\n{compile_result[1]}"
    
    # Run the compiled code
    process2 = subprocess.Popen(["./code"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    run_result = process2.communicate()
    
    if process2.returncode != 0:
        return f"Runtime Error:\n{run_result[1]}"
    
    return run_result[0]

def update_code():
    st.session_state.rust_output = compile_and_run_rust(st.session_state.editor_content)

# Initialize session state
if 'editor_content' not in st.session_state:
    st.session_state.editor_content = """fn main() {
    println!("Hello, world!");
}"""

if 'rust_output' not in st.session_state:
    st.session_state.rust_output = ""

st.title('🦀 Rust in Streamlit')

# Load button settings
with open('btn_settings.json', 'r') as btn_file:
    btn_settings = json.load(btn_file)

# Create code editor
response_dict = code_editor(st.session_state.editor_content, lang="rust", buttons=btn_settings)

# Update session state and trigger callback if the code has changed
if response_dict['text'] != st.session_state.editor_content:
    st.session_state.editor_content = response_dict['text']
    update_code()

# Display the code
st.code(st.session_state.editor_content)

# Display the output
st.write("Output:")
st.write(st.session_state.rust_output)
