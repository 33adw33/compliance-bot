import streamlit as st
import openai
from fpdf import FPDF
from datetime import date

# 1. Page Config & The Final Extermination Attempt
st.set_page_config(page_title="Legal & Compliance Copilot", layout="centered")

# This is the most aggressive CSS possible to target every known Streamlit watermark
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden !important;}
            header {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            .stDeployButton {display:none !important;}
            #stDecoration {display:none !important;}
            [data-testid="stStatusWidget"] {display:none !important;}
            
            /* Target the specific "Made with Streamlit" floating badge */
            .viewerBadge_container__1QSob {display:none !important;}
            .viewerBadge_link__1S137 {display:none !important;}
            div[class^="viewerBadge"] {display:none !important;}
            
            /* Remove the padding that the header usually takes up */
            .block-container {padding-top: 1rem !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Editorial UI Styling (NYT App Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Lora:ital,wght@0,400;0,700;1,400&family=Libre+Franklin:wght@300;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Lora', serif !important;
        background-color: #ffffff;
        color: #121212;
    }

    .masthead-container {
        text-align: center;
        border-bottom: 2px solid #121212;
        padding-bottom: 5px;
        margin-top: 5px;
    }
    .masthead-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 40px !important;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    .masthead-subline {
        font-family: 'Libre Franklin', sans-serif;
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 700;
        border-bottom: 1px solid #e2e2e2;
        padding-bottom: 8px;
        margin-bottom: 30px;
        text-align: center;
        letter-spacing: 1px;
    }

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

    .article-headline {
        font-family: 'Playfair Display', serif;
        font-size: 34px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 15px;
    }
    
    .stTextArea textarea {
        border-radius: 0px;
        border: 1px solid #cccccc;
        font-family: 'Lora', serif !important;
    }

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
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding
today = date.today().strftime("%A, %B %d, %Y")
st.markdown(f'<div class="masthead-container"><div class="masthead-title">My Legal and Compliance Copilot</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="masthead-subline">{today}</div>', unsafe_allow_html=True)

# 4. Input
query = st.text_area("", placeholder="Enter details for regulatory analysis...", height=200, label_visibility="collapsed")

# 5. Tool Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

if st.button("Generate Official Analysis"):
    if not query:
        st.warning("Submission is empty.")
    else:
        with st.status("Performing Audit...", expanded=True):
            try:
                prompt = f"Analyze this issue: {query}. Structure: Abstract, Formal Memorandum (Abstract, Issues, Facts, Rationale with hover links, Verdict), Council Deliberation, Grade, Citations."
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are a professional legal auditor. No emojis."},
                        {"role": "user", "content": prompt}
                    ]
                )
                output = res.choices[0].message.content
                st.markdown('<div class="section-label">Findings & Deliberations</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="article-headline">The Copilot Report: {query[:50]}...</div>', unsafe_allow_html=True)
                st.markdown(output)
                
                # PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=10)
                pdf.multi_cell(0, 10, txt=f"LEGAL AND COMPLIANCE COPILOT REPORT\n\n{output.encode('ascii', 'ignore').decode('ascii')}")
                pdf_output = bytes(pdf.output())
                st.download_button(label="Download Full Brief (PDF)", data=pdf_output, file_name="Copilot_Analysis.pdf")
            except Exception as e:
                st.error(f"Analysis Error: {e}")
