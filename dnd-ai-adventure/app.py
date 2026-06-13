import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Persistent character data (using a single stable dict)
if "character" not in st.session_state:
    st.session_state.character = {"name": "", "gender": "", "class": ""}

if not api_key:
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Page configuration
st.set_page_config(page_title="D&D AI Adventure", page_icon="🎲", layout="centered")

st.title("🎲 D&D AI Adventure")
st.caption("Your personal AI Dungeon Master - made by CC using Groq")

# ==================== SYSTEM PROMPT ====================
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
- Respect the natural laws of physics, unless broken by magic or supernatural forces.
- Give NPCs strong personality, motivations, and free will. They are not generic - each has their own background, goals, fears, and temperament.
- NPCs will not automatically agree with the player. They can refuse requests, negotiate, lie, get angry, become suspicious, or act in their own self-interest based on their personality and current situation.
- Make every NPC reaction feel authentic and consistent with who they are and what they want.
- Always use metric system: kilometers, meters, centimeters, Celsius, kilograms, liters. Never use miles, feet, inches, Fahrenheit or pounds unless the player specifically asks.
- Keep responses engaging but not extremely long.
        """}
    ]

if "game_summary" not in st.session_state:
    st.session_state.game_summary = ""

# ==================== START SECTION ====================
if len(st.session_state.messages) <= 1:
    st.subheader("🧙 Create your character")

    col1, col2, col3 = st.columns(3)

    with col1:
        name_input = st.text_input(
            "Character name",
            placeholder="Eldrin Shadowblade",
            key="name_input"
        )

    with col2:
        gender_input = st.text_input(
            "Gender",
            placeholder="Male, Female, Non-binary or anything you want...",
            key="gender_input"
        )

    with col3:
        class_input = st.text_input(
            "Class / Role",
            placeholder="Wizard, Rogue, Barbarian, a cat, a doctor, or anything you want...",
            key="class_input"
        )

    if st.button("▶️ Start Adventure", type="primary", use_container_width=True):
        if not name_input or not name_input.strip():
            st.warning("Please enter a character name!")
        elif not gender_input or not gender_input.strip():
            st.warning("Please enter a gender!")
        elif not class_input or not class_input.strip():
            st.warning("Please enter a class / role!")
        else:
            # Save character data in a single stable dict
            st.session_state.character = {
                "name": name_input.strip(),
                "gender": gender_input.strip(),
                "class": class_input.strip()
            }

            start_prompt = (
                f"My name is {st.session_state.character['name']}. "
                f"I am a {st.session_state.character['gender']} {st.session_state.character['class']}. "
                "Start the adventure."
            )
            
            st.session_state.messages.append({"role": "user", "content": start_prompt})
            
            with st.chat_message("user"):
                st.markdown(start_prompt)
            
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
            
            st.rerun()

# ==================== DISPLAY CHAT HISTORY ====================
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ==================== CHAT INPUT ====================
if prompt := st.chat_input("What do you do?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("The Dungeon Master is thinking..."):
            try:
                # Efficiency improvement: send only system + summary + last messages
                messages_to_send = [st.session_state.messages[0]]
                
                if st.session_state.game_summary:
                    messages_to_send.append({
                        "role": "system", 
                        "content": f"Current Adventure Summary:\n{st.session_state.game_summary}"
                    })
                
                if len(st.session_state.messages) > 1:
                    messages_to_send.extend(st.session_state.messages[-5:])
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages_to_send,
                    temperature=0.85,
                    max_tokens=700
                )
                dm_response = response.choices[0].message.content
                st.markdown(dm_response)
                st.session_state.messages.append({"role": "assistant", "content": dm_response})
            except Exception as e:
                st.error(f"Error: {e}")

    # Auto-update summary every 5 messages
    if len(st.session_state.messages) > 4 and len(st.session_state.messages) % 5 == 0:
        with st.spinner("Updating adventure summary..."):
            try:
                recent_history = st.session_state.messages[-12:]
                
                summary_prompt = [
                    {"role": "system", "content": "You are an expert at maintaining long D&D campaign state concisely."},
                    {"role": "user", "content": f"""Update the adventure summary. Follow this structure **strictly** and do not add anything else:

**Character:** [Name, Gender, Class, Health, Mood, Thirst, Hunger, Injuries, Current Location]
**Inventory:** [List of most important items only]
**Key NPCs:** [NPC Name - Attitude/Relationship (friendly, hostile, neutral, ally, suspicious, etc.)]
**Story so far:** [Story so far]

When writing in "Story so far" part:                  
- Write in past tense, narrative style.
- Prioritize recent important events and player decisions.
- Summarize older events concisely.
- Never add "Next steps", questions, choices, or suggestions to the player.
- Do not break the fourth wall.
- Keep the entire Story section between 6 and 18 sentences.
- Maintain story continuity and important details.

Previous Summary:
{st.session_state.game_summary}

Recent events:
{''.join([f"{m['role']}: {m['content'][:400]}\n" for m in recent_history])}

Return ONLY the structured summary. No extra text."""}
                ]
                
                summary_response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=summary_prompt,
                    temperature=0.65,
                    max_tokens=550
                )
                st.session_state.game_summary = summary_response.choices[0].message.content.strip()
                st.rerun()
            except:
                pass

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("How to play")
    st.write("Just type your actions normally:")
    st.write("• 'I open the door'\n• 'I attack the goblin'\n• 'I search the room'")
    
    st.divider()
    
    if st.button("🗑️ Reset Adventure"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.game_summary = ""
        # Clear character data
        st.session_state.character = {"name": "", "gender": "", "class": ""}
        st.rerun()

    # Character info
    if len(st.session_state.messages) > 1:
        st.divider()
        st.subheader("🧙 Your Character")
        
        char = st.session_state.character
        st.write(f"**Name:** {char.get('name', 'Unknown')}")
        st.write(f"**Gender:** {char.get('gender', 'Unknown')}")
        st.write(f"**Class:** {char.get('class', 'Unknown')}")

    # Adventure summary
    if st.session_state.game_summary:
        st.divider()
        st.subheader("📜 Adventure Summary")
        st.info(st.session_state.game_summary)
    else:
        st.caption("Adventure summary will appear here after a few exchanges...")