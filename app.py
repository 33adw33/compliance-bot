import streamlit as st
import openai

# 1. Page Config (No more "Legal SuperBot"!)
st.set_page_config(page_title="Chief Compliance Officer Bot", page_icon="🛡️")
st.title("🛡️ The Compliance Council")
st.markdown("---")

# 2. Connect to the "Vault" (Streamlit Secrets)
# This replaces the sidebar credential boxes!
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# 3. The Larry David Input Section
query = st.text_area("What regulatory nightmare are we dealing with now?", 
                     placeholder="e.g., A doctor wants us to pay for his 'educational' trip to Vegas...")

if st.button("Consult the Council"):
    if not query:
        st.warning("I can't help you if you don't tell me the problem. We're living in a society!")
    else:
        with st.spinner("The Council is arguing... please wait."):
            try:
                # THE REASONER (DeepSeek R1 via OpenRouter)
                res_1 = client.chat.completions.create(
                    model="deepseek/deepseek-r1",
                    messages=[{"role": "user", "content": f"Analyze this healthcare compliance issue: {query}"}]
                )
                
                # THE CHAIRPERSON (Gemini 1.5 Pro via OpenRouter)
                final_prompt = f"""
                You are a neurotic, highly experienced Chief Compliance Officer like Larry David. 
                Review this analysis from your associate: {res_1.choices[0].message.content}
                
                Summarize the final verdict for Andrew. Be skeptical, be thorough, 
                and remind him that we live in a society with rules!
                """
                
                final_res = client.chat.completions.create(
                    model="google/gemini-pro-1.5",
                    messages=[{"role": "user", "content": final_prompt}]
                )

                st.write("### 👓 The CCO's Verdict:")
                st.markdown(final_res.choices[0].message.content)
                
                with st.expander("See Raw Regulatory Analysis"):
                    st.write(res_1.choices[0].message.content)
            except Exception as e:
                st.error(f"The Council is on a coffee break. (Error: {e})")
                st.info("Check your OpenRouter credits or Secret keys!")
