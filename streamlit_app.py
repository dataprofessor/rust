import streamlit as st
import subprocess
import json
from code_editor import code_editor

def compile_and_run_rust(code):
    with open('code.rs', "w") as file:
        file.write(code)
    
    process1 = subprocess.Popen(["rustc", "code.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout1, stderr1 = process1.communicate()
    
    if process1.returncode != 0:
        st.error(f"Compilation Error:\n{stderr1}")
        return
    
    process2 = subprocess.Popen(["./code"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout2, stderr2 = process2.communicate()
    
    if stderr2:
        st.error(f"Runtime Error:\n{stderr2}")
    else:
        st.success("Execution Result:")
        st.code(stdout2)

def on_code_change():
    if st.session_state.code_editor:  # Check if code_editor is not empty
        st.session_state.rust_code = st.session_state.code_editor['text']
        compile_and_run_rust(st.session_state.rust_code)

st.title('🦀 Rust in Streamlit')

if 'rust_code' not in st.session_state:
    with open('hello.rs') as rust_file:
        st.session_state.rust_code = rust_file.read()

with open('btn_settings.json', 'r') as btn_file:
    btn_settings = json.load(btn_file)

response_dict = code_editor(st.session_state.rust_code, lang="rust", buttons=btn_settings, key="code_editor", on_change=on_code_change)

st.subheader("Rust Code:")
st.code(st.session_state.rust_code, language="rust")

if response_dict and st.session_state.rust_code != response_dict['text']:
    on_code_change()
