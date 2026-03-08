import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="Legal & COMPLAINCE COPILOT", layout="centered")

# 2. Advanced NYT App UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Lora:ital,wght@0,400;0,700;1,400&family=Libre+Franklin:wght@300;700&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Lora', serif !important;
        background-color: #ffffff;
        color: #121212;
    }

    /* Masthead - NYT App Style */
    .masthead-container {
        text-align: center;
        border-bottom: 2px solid #121212;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    .masthead-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 42px !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    .masthead-subline {
        font-family: 'Libre Franklin', sans-serif;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 700;
        border-bottom: 1px solid #e2e2e2;
        padding-bottom: 8px;
        margin-bottom: 30px;
        text-align: center;
        letter-spacing: 1px;
    }

    /* Section Labeling */
    .section-label {
        font-family: 'Libre Franklin', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 12px;
        color: #121212;
        border-top: 1px solid #121212;
        padding-top: 5px;
        margin-top: 40px;
        margin-bottom: 10px;
    }

    /* Article Styling */
    .article-headline {
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 15px;
    }
    
    .stTextArea textarea {
        border-radius: 0px;
        border: 1px solid #cccccc;
        font-family: 'Lora', serif !important;
        background-color: #fafafa;
    }

    /* The "Publish" Button */
    .stButton > button {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Libre Franklin', sans-serif;
        text-transform: uppercase;
        font-size: 13px;
        font-weight: 700;
        border-radius: 0px;
        width: 100%;
        border: none;
        padding: 12px;
        margin-top: 10px;
    }
    
    .stButton > button:hover {
        background-color: #333333;
        color: #ffffff;
    }

    /* Sidebar and Footer */
    [data-testid="stSidebar"] {
        background-color: #f7f7f7;
        border-right: 1px solid #e2e2e2;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding
st.markdown('<div class="masthead-container"><div class="masthead-title">My Legal and COMPLAINCE COPILOT</div></div>', unsafe_allow_html=True)
st.markdown('<div class="masthead-subline">Sunday, March 8, 2026 &nbsp; | &nbsp; Official Investigative Record</div>', unsafe_allow_html=True)

# 4. Input Module
st.markdown('<div class="section-label">Case Briefing</div>', unsafe_allow_html=True)
query = st.text_area("", placeholder="Enter the regulatory matter or legal facts for analysis...", height=150, label_visibility="collapsed")

# 5. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

if st.button("Generate Official Analysis"):
    if not query:
        st.warning("Please provide case details.")
    else:
        with st.status("Reviewing Law and Precedent...", expanded=True):
            try:
                prompt = f"Analyze this issue: {query}. Provide a plain-English summary, a formal memorandum (Abstract, Issues, Facts, Rationale with hover links, and Verdict), and a multi-personality Council deliberation. End with a 0 or 1 grade. No emojis."
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are a professional auditor and legal analyst. Use formal language. No emojis."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                output = res.choices[0].message.content
                
                # Render as the "Lead Article"
                st.markdown('<div class="section-label">Findings & Deliberations</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="article-headline">The Copilot Report: {query[:50]}...</div>', unsafe_allow_html=True)
                st.markdown(output)

                # PDF Generation
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=10)
                pdf.multi_cell(0, 10, txt=f"LEGAL AND COMPLAINCE COPILOT: OFFICIAL RECORD\n\n{output.encode('ascii', 'ignore').decode('ascii')}")
                pdf_output = bytes(pdf.output())
                st.download_button(label="Download Full Brief (PDF)", data=pdf_output, file_name="Copilot_Analysis.pdf")

            except Exception as e:
                st.error(f"System Error: {e}")
