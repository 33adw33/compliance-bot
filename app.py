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
                     placeholder="e.g., A vendor offered me courtside Knicks tickets...")

if st.button("Convene the Council"):
    if not query:
        st.warning("The Council requires a prompt. We're living in a society!")
    else:
        with st.status("The Council is deliberating (and arguing)...", expanded=True) as status:
            try:
                st.write("🎙️ Summoning the legal legends...")
                
                # The "Super-Prompt" with Uncle Phil added
                prompt = f"""
                You are the Supreme Compliance Council. Analyze this issue: {query}
                
                Synthesize a single, unified response using these specific voices:
                - Larry David & Jerry Seinfeld: The neurotic, 'it's a society' skepticism.
                - Uncle Phil (Judge Banks): The booming authority, moral integrity, and 'not in my house' discipline.
                - RBG & Obama: The intellectual, measured, constitutional precision.
                - Saul Goodman & Jackie Chiles: The fast-talking, 'outrageous' loophole hunting.
                - Vinny Gambino: The street-smart, 'magic grits' common sense.
                - Mickey Haller & Michael Clayton: The gritty, 'fixer' realism.
                - John Milton & Kevin Lomax: The dark, devil's advocate intensity.
                - Rudy Baylor & Frank Galvin: The underdog's passion for justice.
                - Dr. Gonzo: The drug-addled, legal-adjacent insanity.

                VERDICT REQUIREMENTS:
                1. Professional enough for a Healthcare Master of Administration (MHA).
                2. Witty, sharp, and distinctively character-driven.
                3. Conclude with a clear 'Legal/Compliance Risk Level'.
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
                class PDF(FPDF):
                    def header(self):
                        self.set_font('Arial', 'B', 15)
                        self.cell(0, 10, 'The Supreme Compliance Council Report', 0, 1, 'C')
                        self.ln(5)

                pdf = PDF()
                pdf.add_page()
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 10, txt=f"ISSUE SUBMITTED:\n{query}\n\nVERDICT:\n{verdict}".encode('latin-1', 'ignore').decode('latin-1'))
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button(label="📥 Download Council Verdict (PDF)", data=pdf_bytes, file_name="compliance_verdict.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"The Council is in a heated sidebar. Error: {e}")
