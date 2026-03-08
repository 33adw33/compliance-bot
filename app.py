import streamlit as st
import openai

st.set_page_config(page_title="Chief Compliance Officer Bot", page_icon="🛡️")
st.title("🛡️ The Compliance Council")

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

query = st.text_area("What's the nightmare now?", 
                     placeholder="e.g., A provider is ghosting our document request...")

if st.button("Consult the Council"):
    if not query:
        st.warning("I can't help you if you don't tell me the problem. We're living in a society!")
    else:
        with st.status("Council is deliberating...", expanded=True) as status:
            try:
                # Agent 1: The Researcher (Using a very stable Claude 3 Haiku ID)
                st.write("Checking the OIG playbook...")
                res_1 = client.chat.completions.create(
                    model="anthropic/claude-3-haiku", 
                    messages=[{"role": "user", "content": f"Quickly identify the top 3 compliance risks here: {query}"}]
                )
                
                # Agent 2: The CCO (Using the most standard Gemini ID)
                st.write("Getting the CCO's take...")
                final_prompt = f"""
                You are a neurotic, skeptical Chief Compliance Officer like Larry David. 
                Review these risks: {res_1.choices[0].message.content}
                Give Andrew a quick, witty, but legally sound verdict. Mention 'it's a society!'
                """
                
                final_res = client.chat.completions.create(
                    model="google/gemini-pro-1.5", 
                    messages=[{"role": "user", "content": final_prompt}]
                )

                status.update(label="Verdict reached!", state="complete", expanded=False)

                st.write("### 👓 The CCO's Verdict:")
                st.markdown(final_res.choices[0].message.content)
            except Exception as e:
                st.error(f"The Council is on a coffee break. (Error: {e})")
