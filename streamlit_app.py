import streamlit as st
import subprocess
import json
from code_editor import code_editor

st.title('🦀 Rust in Streamlit')

#rust_code = """fn main() {
#    println!("Hello World! Rust works!");
#}
#"""

with open('hello.rs') as rust_file:
    rust_code = rust_file.read()

with open('btn_settings.json', 'r') as btn_file:
    btn_settings = json.load(btn_file)

st.write(btn_settings)

response_dict = code_editor(rust_code, lang="rust", buttons=btn_settings)
response_dict

process1 = subprocess.Popen(["rustc", "hello.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
process2 = subprocess.Popen(["./hello"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result2 = process2.communicate()
st.write(result2[0])
