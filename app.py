import streamlit as st
import openai

st.set_page_config(page_title="Chief Compliance Officer Bot", page_icon="🛡️")
st.title("🛡️ The Compliance Council")

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

query = st.text_area("What regulatory nightmare are we dealing with now?", 
                     placeholder="e.g., A doctor wants us to pay for his 'educational' trip to Vegas...")

if st.button("Consult the Council"):
    if not query:
        st.warning("I can't help you if you don't tell me the problem. We're living in a society!")
    else:
        with st.spinner("The Council is arguing... please wait."):
            try:
                # Using the most stable model IDs for 2026
                # 1. THE REASONER
                res_1 = client.chat.completions.create(
                    model="deepseek/deepseek-r1", 
                    messages=[{"role": "user", "content": f"Analyze this healthcare compliance issue: {query}"}]
                )
                
                # 2. THE CHAIRPERSON (Using the standard Gemini ID)
                final_prompt = f"""
                You are a neurotic, highly experienced Chief Compliance Officer like Larry David. 
                Review this analysis: {res_1.choices[0].message.content}
                Summarize the final verdict for Andrew. Be skeptical and witty.
                """
                
                final_res = client.chat.completions.create(
                    model="google/gemini-flash-1.5", # More stable endpoint
                    messages=[{"role": "user", "content": final_prompt}]
                )

                st.write("### 👓 The CCO's Verdict:")
                st.markdown(final_res.choices[0].message.content)
            except Exception as e:
                st.error(f"The Council is on a coffee break. (Error: {e})")
