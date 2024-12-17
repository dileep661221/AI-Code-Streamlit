import streamlit as st  # app development framework
import google.generativeai as genai  # LLM provider
import time


genai.configure(api_key="AIzaSyAzJI71NwnSz4lV8H6PzLdghqTnMt9zbQg")

# Instruction to the model
sys_prompt = """
You are an expert, helpful, and sensible AI Code Reviewer. 
The user will give you code in any programming language.
Analyze the code and identify all bugs, errors, and inefficiencies. 
Organize your response into:
1. **Bug Report**: Include error names, erroneous parts, and descriptions (Red, 28px font).
2. **Corrected Code**: Provide corrected code with comments (Green, 28px font).
3. **Suggestions**: Brief feedback for improvement (Blue, 28px font).
If the language is unsupported or content is irrelevant, politely decline the request.
"""

# to do the code reviewing task, we need the help of an LLM
# here, we have chosen gemini-1.5-flash model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", 
                              system_instruction=sys_prompt)

# giving a title to the app's UI
st.markdown(""" <h1 style='color: darkgoldenrod; font-family: "Lucida Handwriting", "Brush Script MT", cursive;'> 👾 AI Code Reviewer</h1> """, unsafe_allow_html=True)
st.sidebar.title("📝 How to Use")
st.sidebar.markdown("""
1. Paste your Python code in the text area below.
2. Click **Submit** to generate a code review.
3. Receive detailed feedback on bugs and suggestions for improvement.
""")
st.sidebar.markdown("---")
st.sidebar.write("### About This App")
st.sidebar.markdown("""
This app uses **Google Generative AI** to review your Python code, identify bugs, and suggest improvements to make your code cleaner and more efficient.
""")

# enabling a menubar like feature in the UI
tab_1, tab_2 = st.tabs([':violet[:memo:__Raw Code__]', ':violet[:page_facing_up:__Code File__]'])

# assigning & wrapping the desired functionalities within UI of each tab
with tab_1:
    # a small instruction
    st.markdown('<p style="font-size: 20px; color: #6c757d;"><b>Enter your Python code below:</b></p>', unsafe_allow_html=True)
    # ask the user to enter their code & collect it in the variable 'user_prompt'
    user_prompt = st.text_area("", placeholder="Type or paste your code here...", height=250)
    # displaying a button to the user to submit the code
    btn_click_1 = st.button("Submit", "tab_1")
    # suppose the user clicks the button, the following need to be done
    if btn_click_1:
        # display a message to the user
        with st.spinner(':green[__Please wait :hourglass_flowing_sand: while I :robot_face: go through :mag: your code ...__]'):
            time.sleep(7)
            # ask the model to generate response from the user_prompt
            response = model.generate_content(user_prompt)
            # display the response
            st.markdown(response.text, unsafe_allow_html=True)

with tab_2:
    # small instruction to the user 
    st.markdown('<p style="font-size: 20px; color: #6c757d;"><b>Choose a .py file</b></p>', unsafe_allow_html=True)
    st.write(":warning:__Only 1 file shall be uploaded__")
    uploaded_file = st.file_uploader("")
    # display the name of the file once the user uploads it
    if uploaded_file:
        st.write("filename:", uploaded_file.name)
    btn_click_2 = st.button("Submit", "tab_2")
    if btn_click_2:
        # display a message to the user
        with st.spinner(':green[__Please wait :hourglass_flowing_sand: while I :robot_face: go through :mag: your code file ...__]'):
            time.sleep(7)
        # extract the text code from the .py file into the variable bytes data
        bytes_data = uploaded_file.getvalue().decode("utf-8")
        response = model.generate_content(bytes_data)
        # display the LLM's response
        st.markdown(response.text, unsafe_allow_html=True)
