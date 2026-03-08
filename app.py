import streamlit as st
import openai
from fpdf import FPDF
from datetime import date

# 1. Page Config
st.set_page_config(page_title="Legal & Compliance Copilot", layout="centered")

# 2. NYT Digital App UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Lora:ital,wght@0,400;0,700;1,400&family=Libre+Franklin:wght@300;700&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Lora', serif !important;
        background-color: #ffffff;
        color: #121212;
    }

    /* Masthead - Editorial Style */
    .masthead-container {
        text-align: center;
        border-bottom: 2px solid #121212;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    .masthead-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 38px !important;
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

    /* Article Headline Styling */
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

    /* Professional Action Button */
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
    
    .stButton > button:hover {
        background-color: #333333;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding & Date Line
today = date.today().strftime("%A, %B %d, %Y").upper()
st.markdown(f'<div class="masthead-container"><div class="masthead-title">My Legal and Compliance Copilot</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="masthead-subline">{today} &nbsp; | &nbsp; OFFICIAL INVESTIGATIVE RECORD</div>', unsafe_allow_html=True)

# 4. Submission Module
st.markdown('<div class="section-label">Case Briefing</div>', unsafe_allow_html=True)
query = st.text_area("", placeholder="Enter regulatory matter or legal facts for analysis...", height=150, label_visibility="collapsed")

# 5. Tool Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

if st.button("Generate Official Analysis"):
    if not query:
        st.warning("Please provide case details.")
    else:
        with st.status("Analyzing Precedent...", expanded=True):
            try:
                # Optimized Hybrid Prompt
                prompt = f"""
                Analyze this issue: {query}
                
                STRUCTURE:
                1. ABSTRACT: 3-4 sentence plain English summary.
                2. FORMAL MEMORANDUM:
                   - Subject
                   - To: Andrew Weingarten, MHA
                   - Issue Presented
                   - Summary of Facts
                   - Legal Rationale (Use hover links [[n]](URL "Preview Text"))
                   - The Verdict
                3. THE COUNCIL DELIBERATION (Kingsfield, Larry David, Saul Goodman, etc. No emojis.)
                4. FINAL GRADE: 0 or 1.
                5. CITATION KEY.
                """
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are a professional legal auditor. Start every response with 'This is an analysis of...'. No emojis."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                output = res.choices[0].message.content
                
                # Render Article Output
                st.markdown('<div class="section-label">Findings & Deliberations</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="article-headline">The Copilot Report: {query[:50]}...</div>', unsafe_allow_html=True)
                st.markdown(output)

                # PDF Export Logic
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=10)
                pdf.multi_cell(0, 10, txt=f"LEGAL AND COMPLIANCE COPILOT: OFFICIAL RECORD\n\n{output.encode('ascii', 'ignore').decode('ascii')}")
                pdf_output = bytes(pdf.output())
                st.download_button(label="Download Full Brief (PDF)", data=pdf_output, file_name="Copilot_Analysis.pdf")

            except Exception as e:
                st.error(f"Analysis Error: {e}")
