import streamlit as st
import subprocess
from code_editor import code_editor

st.title('🦀 Rust in Streamlit')

#rust_code = """fn main() {
#    println!("Hello World! Rust works!");
#}
#"""

with open('hello.rs') as rust_file:
    rust_code = rust_file.read()

btn_settings_editor_btns = [{
    "name": "copy",
    "feather": "Copy",
    "hasText": True,
    "alwaysOn": True,
    "commands": ["copyAll"],
    "style": {"top": "0rem", "right": "0.4rem"}
  },{
    "name": "update",
    "feather": "RefreshCw",
    "primary": True,
    "hasText": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "style": {"bottom": "0rem", "right": "0.4rem"}
  }]

response_dict = code_editor(rust_code, lang="rust", buttons=btn_settings_editor_btns)
response_dict

process1 = subprocess.Popen(["rustc", "hello.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
process2 = subprocess.Popen(["./hello"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result2 = process2.communicate()
st.write(result2[0])
