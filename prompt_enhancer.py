import streamlit as st
import google.generativeai as genai
from time import sleep
from streamlit.components.v1 import html

def initialize_gemini(api_key):
    """Initialize Gemini API with the provided key"""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def enhance_prompt(model, role, context, task):
    """Enhance the user's prompt using Gemini API"""
    base_prompt = f"""
    As an AI prompt expert, enhance the following prompt components into a comprehensive prompt.
    Add specific format instructions for the response and include requirements for clarifying assumptions.
    
    Original Components:
    Role: {role}
    Context: {context}
    Task: {task}
    
    Create a well-structured prompt that:
    1. Maintains the original intent
    2. Adds specific format requirements for the response
    3. Requires clarification of assumptions before proceeding
    4. Includes any necessary context or background information
    5. Specifies any constraints or limitations
    """
    
    try:
        response = model.generate_content(base_prompt)
        return response.text
    except Exception as e:
        return f"Error generating enhanced prompt: {str(e)}"

def create_copy_button(text):
    """Create an HTML/JavaScript copy button that won't affect the page state"""
    copy_button_html = f"""
        <div style="position: relative; margin-bottom: 15px;">
            <button 
                onclick="copyText()"
                style="
                    background-color: white;
                    border: 1px solid #ccc;
                    padding: 8px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    font-size: 14px;
                "
            >
                <span style="font-size: 16px;">📋</span>
                <span>Copy</span>
            </button>
            <textarea id="textToCopy" style="position: absolute; top: -9999px;">{text}</textarea>
            <script>
                function copyText() {{
                    var copyText = document.getElementById("textToCopy");
                    copyText.select();
                    document.execCommand("copy");
                    var button = event.target;
                    if (button.tagName === 'SPAN') button = button.parentElement;
                    var originalText = button.innerHTML;
                    button.innerHTML = '<span>✓ Copied!</span>';
                    setTimeout(function() {{
                        button.innerHTML = originalText;
                    }}, 2000);
                }}
            </script>
        </div>
    """
    return copy_button_html

def main():
    st.set_page_config(page_title="AI Prompt Enhancer", layout="wide")
    
    # Custom CSS for better UI
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            background-color: #f0f2f6;
        }
        .stTextArea > div > div > textarea {
            background-color: #f0f2f6;
        }
        .output-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #dee2e6;
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title with custom styling
    st.title("🚀 AI Prompt Enhancer")
    st.markdown("---")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter your Gemini API Key", type="password")
        st.markdown("""
        > Note: Your API key is not stored and will be cleared when you refresh the page.
        """)
    
    # Main content area
    if api_key:
        model = initialize_gemini(api_key)
        
        # Input fields with better organization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input Components")
            role = st.text_input("Role", placeholder="e.g., Senior Software Engineer")
            context = st.text_area("Context", placeholder="Describe the situation or background")
            task = st.text_area("Task", placeholder="What needs to be accomplished?")
        
        # Process button
        if st.button("Enhance Prompt", type="primary"):
            with st.spinner("Enhancing your prompt..."):
                # Add slight delay for better UX
                sleep(0.5)
                enhanced_prompt = enhance_prompt(model, role, context, task)
                
                with col2:
                    st.subheader("Enhanced Prompt")
                    
                    # Add copy button using HTML component
                    html(create_copy_button(enhanced_prompt), height=50)
                    
                    # Display the enhanced prompt
                    st.markdown('<div class="output-container">', unsafe_allow_html=True)
                    st.markdown(enhanced_prompt)
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to get started.")
        
        # Example section
        st.markdown("### Example Input")
        st.markdown("""
        **Role:** Technical Project Manager
        
        **Context:** Working with a remote team on a new mobile app
        
        **Task:** Create a project timeline and resource allocation plan
        """)

if __name__ == "__main__":
    main()