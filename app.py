import streamlit as st
import openai
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="The Supreme Compliance Council", page_icon="⚖️")
st.title("⚖️ The Supreme Compliance Council")
st.markdown("---")

# 2. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# 3. Input
query = st.text_area("State your case for the Council's review:", 
                     placeholder="e.g., A provider is ghosting our document request...")

if st.button("Convene the Council"):
    if not query:
        st.warning("The Council requires a prompt. It’s a society!")
    else:
        with st.status("The Council is arguing in the hallway...", expanded=True) as status:
            try:
                # The "Formal + Chaos" Prompt
                prompt = f"""
                Analyze this issue: {query}
                
                STRUCTURE YOUR RESPONSE EXACTLY AS FOLLOWS:

                1. FORMAL REGULATORY FINDINGS: 
                   Write a single, dense, professional paragraph in the style of Westlaw, Paxton AI, and the ABA. 
                   Use citations where appropriate (e.g., 42 U.S.C. § 1320a-7b). 
                   Address this to Andrew Weingarten, MHA. It must be cold, analytical, and authoritative.

                2. THE COUNCIL DELIBERATION (THE CHAOS):
                   Provide a witty, multi-personality breakdown from these voices:
                   - Professor Kingsfield: (Frame the Socratic challenge)
                   - Larry David & Jerry Seinfeld: (Neurotic skepticism)
                   - Uncle Phil: (Moral authority)
                   - RBG & Obama: (Measured precision)
                   - Saul Goodman & Jackie Chiles: (Loophole hunting)
                   - Vinny Gambino: (Common sense)
                   - Mickey Haller & Michael Clayton: (Fixer realism)
                   - John Milton & Kevin Lomax: (Devil's advocate)
                   - Rudy Baylor & Frank Galvin: (Underdog justice)
                   - Dr. Gonzo: (Legal-adjacent insanity)

                3. FINAL VERDICT & GRADE:
                   Professor Kingsfield returns to deliver the final 'Zero or One' grade 
                   and a clear 'Legal/Compliance Risk Level'.
                """
                
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=[{"role": "user", "content": prompt}]
                )
                
                verdict = res.choices[0].message.content
                status.update(label="Verdict reached!", state="complete", expanded=False)
                
                st.write("### 📜 The Official Council Verdict:")
                st.markdown(verdict)

                # --- PDF GENERATION ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                
                # Cleaning characters for Latin-1 PDF
                clean_verdict = verdict.replace('\u2013', '-').replace('\u2014', '-').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2026', '...')
                clean_query = query.replace('\u2013', '-').replace('\u2014', '-').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2026', '...')
                
                pdf.multi_cell(0, 10, txt=f"ISSUE SUBMITTED:\n{clean_query}\n\nVERDICT:\n{clean_verdict}".encode('latin-1', 'replace').decode('latin-1'))
                
                pdf_output = pdf.output(dest='S')
                
                st.download_button(
                    label="📥 Download Council Verdict (PDF)", 
                    data=pdf_output, 
                    file_name="compliance_verdict.pdf", 
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"The Council is in a heated sidebar. Error: {e}")
