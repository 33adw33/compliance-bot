import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="The Supreme Compliance Council", page_icon="⚖️", layout="wide")
st.title("⚖️ The Supreme Compliance Council")
st.markdown("---")

# 2. Sidebar Quick-Links (The Hyperlinks)
st.sidebar.header("🔗 Regulatory Reference Library")
st.sidebar.markdown("""
* [NYCRR Title 10 (NYSDOH)](https://govt.westlaw.com/nycrr/index?contextData=(sc.Default)&rs=confluence.1.0)
* [CMS State Operations Manual](https://www.cms.gov/medicare/provider-enrollment-and-certification/guidanceforlawsandregulations/nursing-homes)
* [OIG Safe Harbor Regulations](https://oig.hhs.gov/compliance/safe-harbor-regulations/)
* [Anti-Kickback Statute (42 U.S.C.)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
* [Stark Law (42 U.S.C.)](https://www.law.cornell.edu/uscode/text/42/1395nn)
""")

# 3. Connection to OpenRouter
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
                # THE FINAL SCHOLARLY AUDITOR PROMPT
                prompt = f"""
                Analyze this healthcare compliance issue: {query}
                
                STRUCTURE YOUR RESPONSE EXACTLY AS FOLLOWS:

                1. FORMAL REGULATORY FINDINGS (EXECUTIVE SUMMARY): 
                   Write a dense, professional paragraph addressed to Andrew Weingarten, MHA. 
                   Include superscript footnote markers like this [1], [2] at the end of key legal or regulatory statements.

                2. THE COUNCIL DELIBERATION (THE CHAOS):
                   Provide a witty, multi-personality breakdown (Kingsfield, Larry David, Uncle Phil, Saul Goodman, RBG, Obama, etc.).

                3. FINAL VERDICT & GRADE:
                   Professor Kingsfield delivers the final 'Zero or One' grade and Risk Level.

                4. FOOTNOTES & CITATION KEY (NO GUESSING):
                   Provide a numbered list matching the markers [1], [2] above.
                   For each number, state EXACTLY what it means, the specific statute or regulation title (e.g., 10 NYCRR § 415.13), 
                   and provide a clickable hyperlink to the source so Andrew can verify the law.
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
                
                def clean_text(text):
                    # Strip emojis and non-Latin1 chars that crash PDF generators
                    return text.encode('ascii', 'ignore').decode('ascii')
                
                p_query = clean_text(query)
                p_verdict = clean_text(verdict)
                
                pdf.multi_cell(0, 10, txt=f"OFFICIAL AUDIT REPORT\nSUBMITTED BY: Andrew Weingarten, MHA\n\nISSUE:\n{p_query}\n\n{p_verdict}")
                
                pdf_output = bytes(pdf.output())
                
                st.download_button(
                    label="📥 Download Audit Report (PDF)", 
                    data=pdf_output, 
                    file_name="audit_verdict
