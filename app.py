import streamlit as st
import openai

# 1. Page Config
st.set_page_config(page_title="Chief Compliance Officer Bot", page_icon="🛡️")
st.title("🛡️ The Compliance Council")
st.subheader("March 2026 Edition: DeepSeek + Claude + Gemini")

# 2. Connection
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

query = st.text_area("What's the nightmare now?", 
                     placeholder="e.g., Is it a kickback if I buy the surveyor a latte?")

if st.button("Consult the Council"):
    if not query:
        st.warning("I can't help you if you don't tell me the problem. We're living in a society!")
    else:
        with st.status("Council is deliberating...", expanded=True) as status:
            try:
                # Agent 1: The Heavy Researcher (DeepSeek V3)
                st.write("🔍 DeepSeek V3 is cross-referencing OIG bulletins...")
                res_1 = client.chat.completions.create(
                    model="deepseek/deepseek-v3", 
                    messages=[{"role": "user", "content": f"Analyze this healthcare compliance issue for Stark/Anti-Kickback risks: {query}"}]
                )
                
                # Agent 2: The Ethical Guard (Claude 4.6 Sonnet)
                st.write("⚖️ Claude 4.6 is checking HIPAA and ethical guardrails...")
                res_2 = client.chat.completions.create(
                    model="anthropic/claude-4.6-sonnet", 
                    messages=[{"role": "user", "content": f"What are the privacy and ethical implications here? {query}"}]
                )

                # Agent 3: The CCO (Gemini 3.1 Flash - Larry David Mode)
                st.write("👓 Formatting the Larry David verdict...")
                final_prompt = f"""
                You are a neurotic, skeptical Chief Compliance Officer (think Larry David). 
                Review these two expert opinions:
                Analysis A: {res_1.choices[0].message.content}
                Analysis B: {res_2.choices[0].message.content}
                
                Give Andrew a final verdict. Be witty, observant, and remind him that 
                'it's a society' and we have to follow the rules. Keep it concise.
                """
                
                final_res = client.chat.completions.create(
                    model="google/gemini-3.1-flash", 
                    messages=[{"role": "user", "content": final_prompt}]
                )

                status.update(label="Verdict reached!", state="complete", expanded=False)

                st.write("---")
                st.write("### 👓 The CCO's Final Verdict:")
                st.markdown(final_res.choices[0].message.content)
                
                with st.expander("See Raw Council Deliberations"):
                    st.write("**DeepSeek (Regulatory):**", res_1.choices[0].message.content)
                    st.write("**Claude (Ethics/Privacy):**", res_2.choices[0].message.content)

            except Exception as e:
                st.error(f"The Council is on a coffee break. (Error: {e})")
                st.info("Check your OpenRouter credits—DeepSeek V3 is cheap, but not free!")
