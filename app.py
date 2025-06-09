import streamlit as st
import requests
import json
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PrivChat – PII Detection",
    page_icon="🔒",
    layout="wide"
)

st.markdown("""
<style>
    /* Global styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        background: #121212;
        color: #E0E0E0;
        font-family: "SF Pro Text", "Segoe UI", sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Window frame */
    .window {
        display: flex;
        flex-direction: column;
        width: 100%;
        background: rgba(18, 18, 18, 0.96);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
        margin: 20px auto;
    }
    
    /* Title bar */
    .titlebar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 50px;
        background: rgba(30, 30, 30, 0.8);
        backdrop-filter: blur(10px);
        padding: 0 20px;
        border-bottom: 1px solid #242424;
    }
    
    .title {
        font-family: "SF Mono", monospace;
        font-size: 18px;
        font-weight: 600;
        color: #00FF66;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
    }
    
    /* Main content layout */
    .content {
        display: flex;
        padding: 20px;
        gap: 20px;
    }
    
    /* Chat window */
    .chat-window {
        background: rgba(240, 240, 240, 0.05);
        border: 1px solid #242424;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* Entity highlighting */
    .entity-highlight {
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        margin: 0 2px;
    }
    
    .PERSON { 
        background: rgba(255, 165, 0, 0.3);
        color: #FFA500;
        border: 1px solid rgba(255, 165, 0, 0.5);
    }
    
    .GPE { 
        background: rgba(0, 191, 255, 0.3);
        color: #00BFFF;
        border: 1px solid rgba(0, 191, 255, 0.5);
    }
    
    .ORG { 
        background: rgba(255, 105, 180, 0.3);
        color: #FF69B4;
        border: 1px solid rgba(255, 105, 180, 0.5);
    }
    
    .DATE { 
        background: rgba(147, 112, 219, 0.3);
        color: #9370DB;
        border: 1px solid rgba(147, 112, 219, 0.5);
    }
    
    .MONEY { 
        background: rgba(50, 205, 50, 0.3);
        color: #32CD32;
        border: 1px solid rgba(50, 205, 50, 0.5);
    }
    
    /* Entity details panel */
    .entity-details {
        background: rgba(240, 240, 240, 0.02);
        border: 1px solid #242424;
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
    }
    
    .entity-item {
        background: rgba(240, 240, 240, 0.05);
        border: 1px solid #242424;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Input area */
    .stTextArea > div > div > textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        background-color: #4CAF50 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titlebar"><div class="title">PrivChat – PII Detection</div></div>', unsafe_allow_html=True)

st.markdown('<div class="content">', unsafe_allow_html=True)

user_input = st.text_area("Enter your text:", height=150)

if st.button("Analyze", type="primary"):
    if user_input:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/process",
                    json={"text": user_input}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown('<div class="chat-window">', unsafe_allow_html=True)
                    st.markdown("### Original Text with Detected Entities")
                    
                    highlighted_text = user_input
                    for entity in result["entities"]:
                        highlighted_text = highlighted_text.replace(
                            entity["text"],
                            f'<span class="entity-highlight {entity["label"]}">{entity["text"]}</span>'
                        )
                    st.markdown(highlighted_text, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="entity-details">', unsafe_allow_html=True)
                    st.markdown("### Detected Entities")
                    
                    for entity in result["entities"]:
                        st.markdown(f"""
                        <div class="entity-item">
                            <div>
                                <strong>{entity['label']}</strong>
                                <div>{entity['text']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("### Analysis")
                    st.markdown(f"""
                    <div class="entity-details">
                        {result["llm_response"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Error processing the request.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter some text first.")

st.markdown('</div>', unsafe_allow_html=True) 