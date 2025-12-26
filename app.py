import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API ---
genai.configure(api_key="YOUR_API")
model = genai.GenerativeModel(model_name="gemini-2.0-flash")
chat = model.start_chat(history=[])

# --- Page Settings ---
st.set_page_config(page_title="Career Chatbot", layout="centered")
st.title("🎓 Career Guidance Chatbot")

# --- Form for Career Suggestions ---
with st.form("career_form"):
    name = st.text_input("👤 Your Name")
    skills = st.text_area("🛠️ Your Skills")
    interests = st.text_area("🎯 Your Interests")
    goals = st.text_area("🚀 Your Career Goals")
    submit = st.form_submit_button("Suggest Careers 🔍")

if submit:
    with st.spinner("Thinking..."):
        prompt = f"""
Suggest top 3 career options for the following profile:
- Name: {name}
- Skills: {skills}
- Interests: {interests}
- Career Goals: {goals}

Be friendly and explain each career in 2 lines. Also mention why it's a good fit.
"""
        res = chat.send_message(prompt)
        st.subheader("🤖 Gemini Suggests:")
        st.success(res.text)

# --- Divider for Chat ---
st.markdown("---")
st.markdown("### 💬 Ask Me Anything About Careers")

# --- Initialize Session State for Chat ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_input_placeholder = st.empty()
user_msg = chat_input_placeholder.text_input("Type your question:")

if st.button("Send 💬"):
    if user_msg.strip() != "":
        st.session_state.chat_history.append(("You", user_msg))
        reply = chat.send_message(user_msg)
        st.session_state.chat_history.append(("Gemini", reply.text))
        chat_input_placeholder.empty()  # This clears the input field

# --- Display Chat History ---
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"🧑 **You**: {message}")
    else:
        st.markdown(f"🤖 **Gemini**: {message}")
