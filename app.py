import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="SuperBot: Paxton x Gemini", page_icon="⚖️")
st.title("⚖️ Legal SuperBot")
st.caption("Powered by Paxton AI (Retrieval) and Gemini (Reasoning)")

with st.sidebar:
    st.header("Credentials")
    gemini_api_key = st.text_input("Enter Gemini API Key", type="password")
    paxton_api_key = st.text_input("Enter Paxton API Key", type="password", help="Leave blank for Mock Paxton")

if "messages" not in st.session_state:
    st.session_state.messages =[]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a complex legal question..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not gemini_api_key:
        st.error("Please enter your Gemini API Key in the sidebar to continue.")
        st.stop()

    with st.status("Querying Paxton AI database...") as status:
        if paxton_api_key:
            pass 
        else:
            time.sleep(1.5) 
            paxton_raw_data = f"""[SIMULATED PAXTON RETRIEVAL]
            Search Query: '{prompt}'
            Results: Under standard US commercial code, liability requires proof of negligence. 
            Precedent: 'Smith v. Global Corp (2019)' established that entities are not liable for unforeseeable events.
            """
        status.update(label="Paxton retrieved dense legal data!", state="complete")

    with st.status("Flushing through Gemini...") as status:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        flush_prompt = f"""
        You are a brilliant Senior Partner at a top law firm. A client asked: "{prompt}"
        Our AI paralegal retrieved these facts: {paxton_raw_data}
        Synthesize this raw data into a clear email to the client. Rely ONLY on the Paxton data provided.
        """
        
        response = model.generate_content(flush_prompt)
        status.update(label="Gemini synthesized the response!", state="complete")

    with st.chat_message("assistant"):
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})

