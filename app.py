import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Shreeyans Arora NER SpaCy Assignment",
    page_icon="🤖",
    layout="wide"
)

st.title("Shreeyans Arora NER SpaCy Assignment")

st.markdown("""
<style>
    .main {
        padding: 2rem;
        background-color: #000000;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #4CAF50 !important;
        border-radius: 8px !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #4CAF50 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 0 1px #4CAF50 !important;
    }
    .entity-box {
        border: 2px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        background-color: #1a1a1a;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2);
    }
    .entity-label {
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 8px;
    }
    .PERSON { background-color: #FFB6C1; color: #000000; }
    .NORP { background-color: #98FB98; color: #000000; }
    .FAC { background-color: #87CEEB; color: #000000; }
    .ORG { background-color: #DDA0DD; color: #000000; }
    .GPE { background-color: #F0E68C; color: #000000; }
    .LOC { background-color: #E6E6FA; color: #000000; }
    .PRODUCT { background-color: #FFA07A; color: #000000; }
    .EVENT { background-color: #B0E0E6; color: #000000; }
    .WORK_OF_ART { background-color: #FFD700; color: #000000; }
    .LAW { background-color: #90EE90; color: #000000; }
    .LANGUAGE { background-color: #FFC0CB; color: #000000; }
    .DATE { background-color: #ADD8E6; color: #000000; }
    .TIME { background-color: #D8BFD8; color: #000000; }
    .PERCENT { background-color: #F5DEB3; color: #000000; }
    .MONEY { background-color: #98FB98; color: #000000; }
    .QUANTITY { background-color: #E0FFFF; color: #000000; }
    .ORDINAL { background-color: #FFE4B5; color: #000000; }
    .CARDINAL { background-color: #DCDCDC; color: #000000; }
    
    .highlight {
        padding: 2px 4px;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .response-box {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 2px solid #4CAF50;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2);
        color: #ffffff;
    }
    
    .legend {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 1rem 0;
        padding: 1rem;
        background-color: #1a1a1a;
        border-radius: 8px;
        border: 2px solid #4CAF50;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2);
    }

    /* Style for Streamlit elements */
    .stButton > button {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #4CAF50;
    }
    
    .stButton > button:hover {
        background-color: #4CAF50;
        color: #ffffff;
    }

    /* Style for headers */
    h1, h2, h3 {
        color: #ffffff;
    }

    /* Style for info and warning messages */
    .stAlert {
        background-color: #1a1a1a;
        border: 2px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

user_input = st.text_area("Enter your prompt:", height=150)

if st.button("Send", type="primary"):
    if user_input:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/process",
                    json={"text": user_input}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.subheader("📊 Detected Named Entities")
                    if result["entities"]:
                        st.markdown("### Entity Type Legend")
                        st.markdown('<div class="legend">', unsafe_allow_html=True)
                        for entity in result["entities"]:
                            st.markdown(
                                f'<span class="entity-label {entity["label"]}">{entity["label"]}</span>',
                                unsafe_allow_html=True
                            )
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        for entity in result["entities"]:
                            st.markdown(f"""
                            <div class="entity-box">
                                <span class="entity-label {entity['label']}">{entity['label']}</span>
                                <strong>{entity['text']}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No named entities detected.")
                    
                    st.subheader("🤖 LLM Response")
                    st.markdown(f"""
                    <div class="response-box">
                        {result["llm_response"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("📝 Original Text with Highlighted Entities")
                    highlighted_text = user_input
                    for entity in result["entities"]:
                        highlighted_text = highlighted_text.replace(
                            entity["text"],
                            f'<span class="highlight entity-label {entity["label"]}">{entity["text"]}</span>'
                        )
                    st.markdown(highlighted_text, unsafe_allow_html=True)
                else:
                    st.error("Error processing the request.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter some text first.") 