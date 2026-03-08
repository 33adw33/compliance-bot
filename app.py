import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="The Times | Legal & Compliance", layout="centered")

# 2. Advanced Digital App CSS (NYT Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Lora:ital,wght@0,400;0,700;1,400&family=Libre+Franklin:wght@300;700&display=swap');

    /* Global Foundation */
    html, body, [class*="css"] {
        font-family: 'Lora', serif !important;
        background-color: #ffffff;
        color: #121212;
    }

    /* The App Masthead */
    .masthead-container {
        text-align: center;
        border-bottom: 2px solid #121212;
        padding-bottom: 5px;
        margin-bottom: 2px;
    }
    .masthead-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 52px !important;
        font-weight: 700;
        margin-bottom: 0px;
        letter-spacing: -1.5px;
    }
    .masthead-subline {
        font-family: 'Libre Franklin', sans-serif;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 700;
        border-bottom: 1px solid #e2e2e2;
        padding-bottom: 8px;
        margin-bottom: 25px;
        text-align: center;
        letter-spacing: 0.5px;
    }

    /* Section Labeling (The "App" look) */
    .section-label {
        font-family: 'Libre Franklin', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 13px;
        color: #121212;
        border-top: 1px solid #121212;
        padding-top: 6px;
        margin-top: 35px;
        margin-bottom: 15px;
    }

    /* Article Headlines */
    .article-headline {
        font-family: 'Playfair Display', serif;
        font-size: 34px;
        font-weight: 700;
        line-height: 1.05;
        margin-bottom: 12px;
        color: #121212;
    }
    
    .article-summary {
        font-family: 'Lora', serif;
        font-size: 18px;
        color: #444444;
        line-height: 1.4;
        margin-bottom: 20px;
    }

    /* Card/Module Styling */
    .stTextArea textarea {
        border-radius: 0px;
        border: 1px solid #cccccc;
        font-family: 'Lora', serif !important;
        padding: 15px;
    }

    /* Primary Action Button */
    .stButton > button {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Libre Franklin', sans-serif;
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        border-radius: 0px;
        width: 100%;
        border: 1px solid #121212;
        padding: 10px;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #ffffff;
        color: #121212;
    }

    /* Result Area Bordering */
    .result-block {
        border-left: 1px solid #e2e2e2;
        padding-left: 20px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. The Digital App Masthead
st.markdown('<div class="masthead-container"><div class="masthead-title">The Times</div></div>', unsafe_allow_html=True)
st.markdown('<div class="masthead-subline">Sunday, March 8, 2026 &nbsp; | &nbsp; Legal & Compliance Brief</div>', unsafe_allow_html=True)

# 4. The Lead Input
st.markdown('<div class="section-label">Submission for Analysis</div>', unsafe_allow_html=True)
query = st.text_area("", placeholder="Enter case details for the Council's review...", height=120, label_visibility="collapsed")

# 5. Tool Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

if st.button("Publish Analysis"):
    if not query:
        st.warning("Please enter a case for review.")
    else:
        with st.status("Analyzing Records...", expanded=True):
            try:
                # Prompt setup to match the structured memo style
                prompt = f"Analyze this issue: {query}. Provide a plain-English summary, a formal memorandum (Abstract, Issues, Facts, Rationale with hover links, and Verdict), and a multi-personality Council deliberation. End with a 0 or 1 grade."
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are a professional auditor. Use formal language. No emojis."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                output = res.choices[0].message.content
                
                # Render as a "Story"
                st.markdown('<div class="section-label">The Report</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="article-headline">{query[:55]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-block">{output}</div>', unsafe_allow_html=True)

                # --- PDF GENERATION ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=10)
                pdf.multi_cell(0, 10, txt=f"THE TIMES: OFFICIAL RECORD\n\n{output.encode('ascii', 'ignore').decode('ascii')}")
                pdf_output = bytes(pdf.output())
                st.download_button(label="Download Full Record (PDF)", data=pdf_output, file_name="Times_Audit.pdf")

            except Exception as e:
                st.error(f"Error: {e}")
