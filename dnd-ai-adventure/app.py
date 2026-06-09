import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Page configuration
st.set_page_config(page_title="D&D AI Adventure", page_icon="🎲", layout="centered")

st.title("🎲 D&D AI Adventure")
st.caption("Your personal AI Dungeon Master - made by CC using Groq")

# System Prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
You are an experienced and creative Dungeon Master for a classic fantasy D&D adventure.
The game is played in English. Your style is immersive, descriptive, atmospheric, with a bit of humor and drama when appropriate.

Important rules:
- Always respond in English.
- Describe scenes vividly with sensory details.
- Handle combat in a simple but exciting way (you can roll dice mentally or describe results).
- Keep track of the player's location, inventory, and character status.
- Never speak or act for the player.
- If the player does something dangerous, describe logical consequences.
- Keep responses engaging but not extremely long.
        """}
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What do you do?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("The Dungeon Master is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.85,
                    max_tokens=700
                )
                dm_response = response.choices[0].message.content
                st.markdown(dm_response)
                st.session_state.messages.append({"role": "assistant", "content": dm_response})
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar info
with st.sidebar:
    st.header("How to play")
    st.write("Just type your actions normally:\n\r (e.g. 'I open the door', 'I attack the goblin', 'I search the room').")
    st.write("Type 'start' to begin a new adventure.")
    if st.button("🗑️ New Adventure - Reset"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
