import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="The Supreme Compliance Council", page_icon="⚖️", layout="wide")
st.title("⚖️ The Supreme Compliance Council")
st.markdown("---")

# 2. Sidebar Quick-Links
st.sidebar.header("🔗 Regulatory Reference Library")
st.sidebar.markdown("""
* [NYCRR Title 10 (NYSDOH)](https://govt.westlaw.com/nycrr/index?contextData=(sc.Default)&rs=confluence.1.0)
* [CMS State Operations Manual](https://www.cms.gov/medicare/provider-enrollment-and-certification/guidanceforlawsandregulations/nursing-homes)
* [Anti-Kickback Statute (42 U.S.C.)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
* [HIPAA Privacy Rule (45 CFR 164)](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html)
* [GDPR / Data Privacy](https://gdpr-info.eu/)
""")

# 3. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# 4. Input
query = st.text_area("State your case for the Council's review:", 
                     placeholder="e.g., A nurse shared a patient's photo on a private group chat. Define the HIPAA violation, analyze the risk, and provide a resolution.")

if st.button("Convene the Council"):
    if not query:
        st.warning("The Council requires a prompt. It’s a society!")
    else:
        with st.status("The Council is conducting a deep-dive audit...", expanded=True) as status:
            try:
                # THE "DEEP DIVE" PROMPT
                prompt = f"""
                Analyze this issue: {query}
                
                CRITICAL INSTRUCTION: 
                START IMMEDIATELY with a direct, professional introductory sentence describing the domain and issue.
                
                STRUCTURE:
                1. FORMAL REGULATORY FINDINGS: 
                   Write a comprehensive, multi-part analysis for Andrew Weingarten, MHA:
                   - DEFINITION: Define the relevant laws, F-Tags, or statutes involved.
                   - ANALYSIS: Explain how the situation violates or aligns with these laws.
                   - RESOLUTION: Provide a formal recommendation or corrective action plan.
                   ATTACH A HOVER-PREVIEW CITATION [[n]](URL "PREVIEW TEXT") TO EVERY REGULATORY CLAIM.

                2. THE COUNCIL DELIBERATION (THE CHAOS):
                   (Kingsfield, LD, Uncle Phil, Saul, RBG, Obama, etc.)

                3. FINAL VERDICT & GRADE:
                   Professor Kingsfield delivers the final 'Zero or One' grade.

                4. FOOTNOTES & CITATION KEY:
                   Detailed list of all regulations mentioned with live links.
                """
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are a senior compliance auditor. You provide thorough, multi-layered analyses that include definitions, situational applications, and resolutions. You start every response immediately with 'This is an analysis of...' and never use conversational filler."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                verdict = res.choices[0].message.content
                status.update(label="Audit Complete!", state="complete", expanded=False)
                
                st.write("### 📜 The Official Council Verdict:")
                st.markdown(verdict)

                # --- PDF GENERATION ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                def clean_text(text): return text.encode('ascii', 'ignore').decode('ascii')
                p_verdict = clean_text(verdict)
                pdf.multi_cell(0, 10, txt=f"OFFICIAL AUDIT REPORT\nSUBMITTED BY: Andrew Weingarten, MHA\n\n{p_verdict}")
                
                pdf_output = bytes(pdf.output())
                st.download_button(label="📥 Download Audit Report (PDF)", data=pdf_output, file_name="audit_verdict.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"The Council is in a heated sidebar. Error: {e}")
