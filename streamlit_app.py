import streamlit as st
import subprocess
import json
from code_editor import code_editor

def run_rust_code(code):
    with open('code.rs', "w") as file:
        file.write(code)
    
    process1 = subprocess.Popen(["rustc", "code.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process1.wait()  # Wait for compilation to finish
    
    process2 = subprocess.Popen(["./code"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = process2.communicate()
    return result2[0]

def code_changed():
    if 'current_code' in st.session_state and st.session_state.current_code != st.session_state.previous_code:
        st.session_state.rust_output = run_rust_code(st.session_state.current_code)
        st.session_state.previous_code = st.session_state.current_code

st.title('🦀 Rust in Streamlit')

with open('hello.rs') as rust_file:
    rust_code = rust_file.read()

with open('btn_settings.json', 'r') as btn_file:
    btn_settings = json.load(btn_file)

if 'previous_code' not in st.session_state:
    st.session_state.previous_code = rust_code

response_dict = code_editor(rust_code, lang="rust", buttons=btn_settings, key="code_editor")

st.session_state.current_code = response_dict['text']
code_changed()

st.code(st.session_state.current_code)

if 'rust_output' in st.session_state:
    st.write(st.session_state.rust_output)
