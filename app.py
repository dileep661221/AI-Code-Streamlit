import streamlit as st
import google.generativeai as genai
import time

# Configure your Gemini API key
genai.configure(api_key="AIzaSyAzJI71NwnSz4lV8H6PzLdghqTnMt9zbQg")  # Replace with your actual key

# ===================== System Prompts =====================

# For Code Review
review_prompt = """
You are an expert, helpful, and sensible AI Code Reviewer.
Analyze the user's code and identify all bugs, inefficiencies, and issues.

Organize your response into:
1. **Bug Report**: Include error names, erroneous parts, and descriptions (Red, 28px font).
2. **Corrected Code**: Provide corrected code with inline comments (Green, 28px font).
3. **Suggestions**: Offer concise tips for improving code quality (Blue, 28px font).

If the language is unsupported or content is irrelevant, politely decline.
"""

# For Code Generation
code_generation_prompt = """
You are an expert software engineer and competitive programmer.
When the user provides a prompt (e.g., 'binary search in Java', 'build login page in React'),
generate clean, **optimized**, and well-commented code.

Key Instructions:
- Always prefer optimal time and space complexity.
- Avoid brute-force unless explicitly asked.
- Use best practices in naming, modularity, and readability.
- Return only code blocks in markdown format.
- Do not include any explanation unless the prompt asks for it.
"""

# ===================== Gemini Models =====================

review_model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=review_prompt
)

generation_model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=code_generation_prompt
)

# ===================== Streamlit UI =====================

st.set_page_config(page_title="AI Code Reviewer & Generator", layout="wide")

st.markdown(""" 
<h1 style='color: darkgoldenrod; font-family: "Lucida Handwriting", cursive;'> 
👾 AI Code Assistant: Review & Generate Code
</h1> 
""", unsafe_allow_html=True)

st.sidebar.title("🧠 Features")
st.sidebar.markdown("""
- ✅ Code Review (paste or upload)
- ⚡ Prompt-Based Code Generation
""")

# Tabs
tab1, tab2, tab3 = st.tabs([
    ":memo: Review Raw Code", 
    ":page_facing_up: Review Code File", 
    ":robot_face: Generate Code From Prompt"
])

# ========== Tab 1: Raw Code Review ==========
with tab1:
    st.markdown('<h3 style="color: steelblue;">Paste your code below:</h3>', unsafe_allow_html=True)
    user_code = st.text_area("Your Code", placeholder="Paste your code here...", height=250)
    if st.button("Review Code", key="tab1"):
        if user_code.strip():
            with st.spinner("Analyzing your code for issues..."):
                time.sleep(2)
                response = review_model.generate_content(user_code)
                st.markdown(response.text, unsafe_allow_html=True)
        else:
            st.warning("Please paste some code first.")

# ========== Tab 2: File Upload Review ==========
with tab2:
    st.markdown('<h3 style="color: steelblue;">Upload a .py file:</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=["py", "java", "cpp", "txt"])
    if uploaded_file is not None:
        st.write(f"📄 Uploaded file: `{uploaded_file.name}`")
    if st.button("Review Uploaded File", key="tab2"):
        if uploaded_file is not None:
            file_content = uploaded_file.read().decode("utf-8")
            with st.spinner("Reviewing your uploaded file..."):
                time.sleep(2)
                response = review_model.generate_content(file_content)
                st.markdown(response.text, unsafe_allow_html=True)
        else:
            st.warning("Please upload a code file.")

# ========== Tab 3: Prompt-Based Code Generation ==========
with tab3:
    st.markdown('<h3 style="color: steelblue;">Describe the code you want:</h3>', unsafe_allow_html=True)
    code_prompt = st.text_area("Prompt", placeholder="Example: Generate binary search in Python with O(log n) complexity")
    if st.button("Generate Code", key="tab3"):
        if code_prompt.strip():
            with st.spinner("Generating optimized code..."):
                time.sleep(2)
                response = generation_model.generate_content(code_prompt)
                st.markdown(response.text, unsafe_allow_html=True)
        else:
            st.warning("Please enter a code prompt.")
