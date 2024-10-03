import streamlit as st
import subprocess
import json
from code_editor import code_editor

st.set_page_config(page_title='Rust in Streamlit', page_icon='🦀', layout='wide')

def run_rust_code(code):
    with open('code.rs', 'w') as file:
        file.write(code)
    
    process1 = subprocess.Popen(['rustc', 'code.rs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process1.wait()  # Wait for compilation to finish
    
    process2 = subprocess.Popen(['./code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result2 = process2.communicate()
    return result2[0]

#def code_changed():
    #if 'current_code' in st.session_state and st.session_state.current_code != st.session_state.previous_code:
        #st.session_state.rust_output = run_rust_code(st.session_state.current_code)
        #st.session_state.previous_code = st.session_state.current_code


st.title('🦀 Rust in Streamlit')


col = st.columns(2)

with col[0]:
    st.subheader('Code Input')
    code_selection = st.selectbox('Select an example', ('Hello world!', 'Variable binding'))
    code_dict = {
        "Hello world!": "hello.rs",
        "Variable binding": "variable.rs",
    }

    if code_dict[code_selection] == 'hello.rs':
        st.markdown("""The typical rite of passage for learning any new language
            is to write out *Hello world* in that language. So here we go!
        """)
        st.markdown("""**Overview**
        
- First, we'll create a file called *hello.rs*. The underlying code is displayed in the following code editor box. You'll see that we're using `println!()` to print the *Hello world!* text and this is defined inside the `main()` function.
- Secondly, we'll compile the file by running `rustc hello.rs`
- Thirdly, we'll run the compiled file using `./hello`
        """)

    if code_dict[code_selection] == 'variable.rs':
        st.markdown("""Values can be assigned or bound to variables by using the `let` binding.
        """)
    
    with open('content/btn_settings.json', 'r') as btn_file:
        btn_settings = json.load(btn_file)
    
    #with open('content/hello.rs') as rust_file:
    with open(f'content/{code_dict[code_selection]}') as rust_file:
        rust_code = rust_file.read()
        
    #if 'previous_code' not in st.session_state:
        #st.session_state.previous_code = rust_code
    
    
    response_dict = code_editor(rust_code, lang='rust', height=12, buttons=btn_settings, key='code_editor')
    #st.session_state.current_code = response_dict['text']

    #code_changed()

    #if st.session_state.current_code != '':
        #st.warning('Click on the **update** button in the code editor box above.', icon='⚠️')
        
#with col[1]:
    #if st.session_state.current_code != '':
        #st.subheader('Code Content')
        #st.code(rust_code, line_numbers=True)
        
        #st.subheader('Code Output')
        #if 'rust_output' in st.session_state:
            #st.code(st.session_state.rust_output)
    #else:
        #st.warning('Click on the **update** button in the code editor box shown on the left to run the code.', icon='⚠️')


rust_code
#st.session_state.current_code
#st.session_state.previous_code

st.code(rust_code, line_numbers=True)
output = run_rust_code(rust_code)
st.code(output, line_numbers=True)
