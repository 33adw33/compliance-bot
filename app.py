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
* [OIG Safe Harbor Regulations](https://oig.hhs.gov/compliance/safe-harbor-regulations/)
* [Anti-Kickback Statute (42 U.S.C.)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
* [Stark Law (42 U.S.C.)](https://www.law.cornell.edu/uscode/text/42/1395nn)
""")

# 3. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# 4. Input
query = st.text_area("State your case for the Council's review:", 
                     placeholder="e.g., Facility staffing is 1:15 despite a 1:8 requirement...")

if st.button("Convene the Council"):
    if not query:
        st.warning("The Council requires a prompt. It’s a society!")
    else:
        with st.status("The Council is auditing the records...", expanded=True) as status:
            try:
                # HYPERLINKED CITATION PROMPT
                prompt = f"""
                Analyze this healthcare compliance issue: {query}
                
                CRITICAL INSTRUCTION: You MUST include superscript markers that are LIVE HYPERLINKS in Section 1. 
                Example: 'This violates 10 NYCRR [[1]](https://govt.westlaw.com/nycrr/)...'

                STRUCTURE YOUR RESPONSE:

                1. FORMAL REGULATORY FINDINGS: 
                   Write a dense, professional paragraph for Andrew Weingarten, MHA. 
                   YOU MUST ATTACH A HYPERLINKED MARKER [[1]](URL), [[2]](URL), etc., TO EVERY LEGAL CLAIM.

                2. THE COUNCIL DELIBERATION (THE CHAOS):
                   (Kingsfield, LD, Uncle Phil, Saul, RBG, Obama, etc.)

                3. FINAL VERDICT & GRADE:
                   Professor Kingsfield delivers the final 'Zero or One' grade.

                4. FOOTNOTES & CITATION KEY:
                   Provide a numbered list matching the markers. 
                   List the EXACT regulation name and the full URL again for reference.
                """
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are a legal auditor. You ALWAYS embed live markdown hyperlinks into your citation numbers [1](url) so they are clickable."},
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
