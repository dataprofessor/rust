import streamlit as st
import subprocess

st.title('🦀 Rust in Streamlit')

process1 = subprocess.Popen(["rustc", "test.rs", "|", "./hello"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result1 = process1.communicate()
st.write(result1)
