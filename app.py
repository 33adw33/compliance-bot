import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="The Supreme Compliance Council", page_icon="⚖️", layout="wide")
st.title("⚖️ The Supreme Compliance Council")
st.markdown("---")

# 2. Sidebar Quick-Links for easy reference
st.sidebar.header("🔗 Regulatory Reference Library")
st.sidebar.markdown("""
* [NYCRR Title 10 (NYSDOH)](https://govt.westlaw.com/nycrr/index?contextData=(sc.Default)&rs=confluence.1.0)
* [CMS State Operations Manual](https://www.cms.gov/medicare/provider-enrollment-and-certification/guidanceforlawsandregulations/nursing-homes)
* [Anti-Kickback Statute (42 U.S.C.)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
* [HIPAA Privacy Rule](https://www.hhs.gov/hipaa/index.html)
""")

# 3. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# 4. Input
query = st.text_area("State your case (Plain English is fine!):", 
                     placeholder="e.g., A provider is charging extra for 'premium water' in the waiting room...")

if st.button("Convene the Council"):
    if not query:
        st.warning("The Council requires a prompt. It’s a society!")
    else:
        with st.status("Drafting the Straight-Talk Memo & Convening the Nuts...", expanded=True) as status:
            try:
                # THE HYBRID PROMPT
                prompt = f"""
                Analyze this issue: {query}
                
                STRUCTURE YOUR RESPONSE EXACTLY LIKE THIS:

                ### 📝 THE STRAIGHT-TALK SUMMARY (The "Fred" Version)
                *Write a 3-4 sentence 'plain English' summary of what is happening here so anyone can understand it instantly.*

                ---

                ### 📜 OFFICIAL EXECUTIVE MEMORANDUM
                **Subject:** Analysis of {query[:40]}...
                **To:** Andrew Weingarten, MHA
                
                **ABSTRACT**
                A formal, professional summary of the regulatory findings.
                
                **ISSUE PRESENTED**
                - Bullet points of the specific legal/compliance questions.
                
                **LEGAL RATIONALE**
                A dense, formal paragraph using professional terminology. 
                YOU MUST ATTACH HOVER-PREVIEW CITATIONS [[n]](URL "PREVIEW TEXT") TO EVERY CLAIM.

                **THE VERDICT**
                Final Judgment and Mandates.

                ---

                ### 🤡 THE COUNCIL DELIBERATION (The Nuts)
                *Provide the witty, multi-personality breakdown:*
                - Professor Kingsfield (The Paper Chase)
                - Larry David & Jerry Seinfeld (Neurotic skepticism)
                - Uncle Phil (Moral authority)
                - Saul Goodman & Jackie Chiles (Loopholes & Outrage)
                - RBG & Obama (Measured precision)
                - Vinny Gambino (Common sense)
                - Dr. Gonzo (Legal-adjacent insanity)

                ---

                ### 🎓 FINAL GRADE
                Professor Kingsfield's 0 or 1 grade.

                ### 📑 FOOTNOTES & CITATION KEY
                Detailed list of all regulations mentioned with live links.
                """
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[
                        {"role": "system", "content": "You are a professional auditor who balances high-level legal precision with plain-English accessibility. You never use conversational filler like 'Okay'."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                verdict = res.choices[0].message.content
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                st.write(verdict)

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
