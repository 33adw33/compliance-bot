import streamlit as st
import openai

# 1. Page Config
st.set_page_config(page_title="Chief Compliance Officer Bot", page_icon="🛡️")
st.title("🛡️ The Compliance Council")
st.markdown("---")

# 2. Connection to OpenRouter
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
        with st.status("The Council is arguing in the hallway...", expanded=True) as status:
            context_notes = ""
            
            # Step 1: DeepSeek (The 2026 Stable ID)
            try:
                st.write("🔍 DeepSeek V3.2 is checking the OIG playbook...")
                res_1 = client.chat.completions.create(
                    model="deepseek/deepseek-chat",
                    messages=[{"role": "user", "content": f"Analyze this healthcare compliance issue for Stark/Anti-Kickback: {query}"}]
                )
                context_notes += f"\nRegulatory Notes: {res_1.choices[0].message.content}"
            except Exception:
                st.write("⚠️ DeepSeek is on a break, skipping...")

            # Step 2: Claude (The 2026 Stable ID)
            try:
                st.write("⚖️ Claude 4.6 is checking HIPAA/Ethics...")
                res_2 = client.chat.completions.create(
                    model="anthropic/claude-3.5-sonnet",
                    messages=[{"role": "user", "content": f"What are the ethical and HIPAA risks here? {query}"}]
                )
                context_notes += f"\nEthical Notes: {res_2.choices[0].message.content}"
            except Exception:
                st.write("⚠️ Claude is on a break, skipping...")

            # Step 3: Gemini (The 2026 Stable ID)
            try:
                st.write("👓 Getting the CCO's final verdict...")
                # Using the newest stable Flash ID for 2026
                final_res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001",
                    messages=[{"role": "user", "content": f"You are a neurotic, highly experienced CCO like Larry David. Review this: {context_notes if context_notes else query}. Give Andrew a witty, legally sound verdict. Remind him it's a society!"}]
                )
                status.update(label="Verdict reached!", state="complete", expanded=False)
                st.write("### 👓 The CCO's Final Verdict:")
                st.markdown(final_res.choices[0].message.content)
                
            except Exception as e:
                # THE ULTIMATE FALLBACK (If everything above fails)
                st.write("🚨 Emergency: Calling the Backup CCO...")
                final_res = client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[{"role": "user", "content": f"You are a neurotic CCO like Larry David. Andrew needs help: {query}. Give him a witty verdict and say 'it's a society!'"}]
                )
                status.update(label="Emergency Verdict Reached!", state="complete", expanded=False)
                st.write("### 👓 The CCO's Emergency Verdict:")
                st.markdown(final_res.choices[0].message.content)
