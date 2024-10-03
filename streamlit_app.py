import streamlit as st
import subprocess
from streamlit_ace import st_ace

st.set_page_config(page_title='Rust in Streamlit', page_icon='🦀', layout='wide')

def run_rust_code(code):
    with open('code.rs', 'w') as file:
        file.write(code)
    
    process1 = subprocess.Popen(['rustc', 'code.rs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process1.wait()
    
    process2 = subprocess.Popen(['./code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = process2.communicate()
    return result2[0]

def generate_output():
    with col[1]:
        st.subheader('Code Content')
        st.code(st.session_state.editor_code, line_numbers=True)
    
        st.subheader('Code Output')
        output = run_rust_code(st.session_state.editor_code)
        st.code(output, line_numbers=True)

if 'rust_code' not in st.session_state:
    st.session_state.rust_code = ''

if 'editor_code' not in st.session_state:
    st.session_state.editor_code = ''


st.title('🦀 Rust in Streamlit')


col = st.columns(2)

with col[0]:
    st.subheader('Code Input')
    code_selection = st.selectbox('Select an example', ('Hello world!', 'Variable binding'))
    code_dict = {
        "Hello world!": "hello.rs",
        "Variable binding": "variable.rs",
    }

    st.caption(f'Contents of {code_dict[code_selection]}:')
    placeholder = st.empty()
    
    if code_dict[code_selection] == 'hello.rs':
        st.markdown("""The typical rite of passage for learning any new language
            is to write out *Hello world* in that language. So here we go!
        """)
        st.markdown("""**Overview**
        
- First, we'll create a file called *hello.rs*. The underlying code is displayed in the following code editor box. You'll see that we're using `println!()` to print the *Hello world!* text and this is defined inside the `main()` function.
- Secondly, we'll compile the file by running `rustc hello.rs`
- Thirdly, we'll run the compiled file using `./hello`
        """)

        with open(f'content/{code_dict[code_selection]}') as rust_file:
            st.session_state.rust_code = rust_file.read()

    if code_dict[code_selection] == 'variable.rs':
        st.markdown("""Values can be assigned or bound to variables by using the `let` binding.
        """)

        with open(f'content/{code_dict[code_selection]}') as rust_file:
            st.session_state.rust_code = rust_file.read()
    
    with placeholder:
        st.session_state.editor_code = st_ace(st.session_state.rust_code, language='rust', min_lines=8)

    st.button('Run Code', on_click=generate_output)
    
#with col[1]:
    #if st.button('Run Code'):
        #st.subheader('Code Content')
        #st.code(st.session_state.editor_code, line_numbers=True)

        #st.subheader('Code Output')
        #output = run_rust_code(st.session_state.editor_code)
        #st.code(output, line_numbers=True)
