import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="The Times: Legal Affairs", layout="centered")

# 2. Advanced NYT Digital CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Lora:ital,wght@0,400;0,700;1,400&family=Libre+Franklin:wght@300;700&display=swap');

    /* Global Body Styling */
    html, body, [class*="css"] {
        font-family: 'Lora', serif !important;
        background-color: #ffffff;
        color: #121212;
    }

    /* The Masthead */
    .masthead {
        text-align: center;
        border-bottom: 2px solid #121212;
        padding-bottom: 5px;
        margin-bottom: 2px;
    }
    .masthead h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 65px !important;
        font-weight: 700;
        margin-bottom: 0px;
        letter-spacing: -2px;
    }
    .date-line {
        font-family: 'Libre Franklin', sans-serif;
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 700;
        border-bottom: 1px solid #e2e2e2;
        padding-bottom: 10px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* Section Headers */
    .section-header {
        font-family: 'Libre Franklin', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 1px;
        border-top: 1px solid #121212;
        padding-top: 5px;
        margin-top: 30px;
    }

    /* Article Body */
    .article-title {
        font-family: 'Playfair Display', serif;
        font-size: 32px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 15px;
    }
    
    .stTextArea textarea {
        border-radius: 0px;
        border: 1px solid #e2e2e2;
        font-family: 'Lora', serif !important;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #121212;
        color: white;
        font-family: 'Libre Franklin', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        border-radius: 0px;
        width: 100%;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #333333;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. NYT Digital Masthead
st.markdown('<div class="masthead"><h1>The New York Times</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="date-line">Sunday, March 8, 2026 &nbsp; | &nbsp; Legal & Compliance Edition</div>', unsafe_allow_html=True)

# 4. Input Area (The "Lead Story" Submission)
st.markdown('<div class="section-header">Case Submission</div>', unsafe_allow_html=True)
query = st.text_area("", placeholder="Enter the details of the regulatory matter here...", height=150)

# 5. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

if st.button("Publish Analysis"):
    if not query:
        st.warning("A case submission is required to publish.")
    else:
        with st.status("Gathering Testimony...", expanded=True):
            try:
                prompt = f"""
                Analyze this issue: {query}
                STRUCTURE:
                1. STRAIGHT-TALK SUMMARY: 3-4 sentence plain English lead.
                2. FORMAL MEMORANDUM: Subject, To (Andrew Weingarten, MHA), Abstract, Issue Presented, Legal Rationale (with hover links), and Verdict.
                3. THE COUNCIL DELIBERATION: The multi-personality breakdown (No Emojis).
                4. FINAL GRADE: Kingsfield 0 or 1.
                5. CITATION KEY.
                """
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are an elite legal analyst for a major newspaper. Use formal, crisp language. No emojis."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                output = res.choices[0].message.content
                
                # Split output into sections for NYT styling
                st.markdown('<div class="section-header">Analysis</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="article-title">The Compliance Brief: {query[:50]}...</div>', unsafe_allow_html=True)
                st.markdown(output)

                # --- PDF GENERATION ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=10)
                pdf.multi_cell(0, 10, txt=f"OFFICIAL RECORD: {query[:30]}\n\n{output.encode('ascii', 'ignore').decode('ascii')}")
                pdf_output = bytes(pdf.output())
                st.download_button(label="Download Full Article (PDF)", data=pdf_output, file_name="NYT_Legal_Brief.pdf")

            except Exception as e:
                st.error(f"The printing press stalled: {e}")
