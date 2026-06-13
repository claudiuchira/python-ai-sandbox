# 🎲 D&D AI Adventure

A fun, interactive AI-powered Dungeon Master built with Groq and Streamlit.

**🎮 Play Live:** [https://xn9vcdhdqxgzdbfurcnuuq.streamlit.app/](https://xn9vcdhdqxgzdbfurcnuuq.streamlit.app/)

## ✨ Features

- Fully interactive AI Dungeon Master
- Immersive storytelling with Groq (Llama 3.1)
- Real-time chat interface
- Classic fantasy D&D style
- Responsive web app (works on mobile too)

## Recent Improvements (June 14, 2026)

- Fixed token limit errors by implementing concise side-storytelling, enabling truly infinite-length adventures
- Added character creation (Name, Gender, and Class) at the beginning of the story
- Improved mobile experience by replacing the need to type `start` with a Start button
- Moved from a basic prompt-based chat to a more structured and reliable adventure experience
- Improved conversation flow and story consistency
- Better handling of player actions and world state
- More stable and production-ready code


## 🚀 How to Run Locally

1. Clone the repository:
   git clone https://github.com/claudiuchira/python-ai-sandbox.git
   cd python-ai-sandbox/dnd-ai-adventure

Install dependencies:Bashpip install -r requirements.txt
Create a .env file and add your Groq API key:envGROQ_API_KEY=gsk_your_key_here
Run the app:Bashstreamlit run app.py

🎮 How to Play

Type normal actions like:
"I go north"
"I attack the goblin"
"I search the room"
"I open the chest"
"I drink a healing potion"

Type start to begin a new adventure.

🛠️ Technologies Used

Groq (Llama-3.1-8b-instant)
Streamlit - for the web interface
Python

📌 Project Goal
This is a personal learning project to explore:

Working with Groq API
Building interactive AI applications
Prompt engineering for creative AI

👤 Author
Claudiu-Razvan Chira
Technical Team Lead | Python & AI Enthusiast

Made with ❤️ in Timișoara, Romania