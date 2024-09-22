import streamlit as st
import subprocess
from code_editor import code_editor

st.title('🦀 Rust in Streamlit')

rust_code = """
    fn main() {
    println!("Hello World! Rust works!");
    }
  """

response_dict = code_editor(rust_code, lang="rust")
response_dict

process1 = subprocess.Popen(["rustc", "hello.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
process2 = subprocess.Popen(["./hello"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result2 = process2.communicate()
st.write(result2[0])
