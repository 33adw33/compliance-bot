import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="The Supreme Compliance Council", page_icon="⚖️", layout="wide")
st.title("⚖️ The Supreme Compliance Council")

# 2. Sidebar Quick-Links (The Hyperlinks)
st.sidebar.header("🔗 Regulatory Reference Library")
st.sidebar.markdown("""
* [NYCRR Title 10 (NYSDOH)](https://www.health.ny.gov/regulations/nycrr/title_10/)
* [CMS State Operations Manual (Appendix PP)](https://www.cms.gov/medicare/provider-enrollment-and-certification/guidanceforlawsandregulations/nursing-homes)
* [OIG Safe Harbor Regulations (42 CFR 1001.952)](https://oig.hhs.gov/compliance/safe-harbor-regulations/)
* [Anti-Kickback Statute (42 U.S.C. § 1320a-7b)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
* [Stark Law (42 U.S.C. § 1395nn)](https://www.law.cornell.edu/uscode/text/42/1395nn)
""")

# 3. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# 4. Input
query = st.text_area("State your case for the Council's review:", 
                     placeholder="e.g., A provider is offering a 'volume-based discount' on lab services...")

if st.button("Convene the Council"):
    if not query:
        st.warning("The Council requires a prompt. It’s a society!")
    else:
        with st.status("The Council is auditing the records...", expanded=True) as status:
            try:
                # PROMPT WITH HYPERLINK INSTRUCTION
                prompt = f"""
                Analyze this healthcare compliance issue: {query}
                
                STRUCTURE:
                1. FORMAL REGULATORY FINDINGS: 
                   Write a professional paragraph addressed to Andrew Weingarten, MHA.
                
                2. CITATIONS & HYPERLINKS:
                   Provide a list of relevant citations. 
                   Where possible, format them as markdown links using these base URLs:
                   - NYCRR Title 10: https://govt.westlaw.com/nycrr/
                   - CMS F-Tags: https://www.cms.gov/files/document/appendix-pp-guidance-surveyor-long-term-care-facilities.pdf
                   - Federal Statutes: https://www.law.cornell.edu/uscode/text/42/
                
                3. THE COUNCIL DELIBERATION (THE CHAOS):
                   (Kingsfield, LD, Uncle Phil, Saul, RBG, Obama, etc.)

                4. FINAL VERDICT & GRADE.
                """
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[{"role": "user", "content": prompt}]
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
