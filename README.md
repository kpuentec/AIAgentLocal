# AIAgentLocal

**AI Agent Local** is a local-first AI agent leveraging the qwen3:8b model from Ollama for powerful conversational workflows. Designed with privacy and security in mind, it integrates email and calendar management with AI tools while running entirely on your machine. Support for additional AI models is coming soon as well as additional tools.

---

## Features

- Conversational AI powered by Ollama’s qwen3:8b model
- Fetch and summarize unread emails (currently supports Google Gmail only)
- Add events to Google Calendar
- Secure local environment variable management with .env files
- Extensible architecture built on LangChain and LangGraph
- Tkinter desktop app with scrollable chat window and input box
  
(More features and model integrations coming soon!)
---

## Setup

### Prerequisites

- Gmail account with App Passwords enabled (required for IMAP access)
- Google Cloud project with Calendar API enabled
- [Python 3](https://www.python.org/) (required)
- Git

---

### Install & Run


    # Clone the repo
    git clone https://github.com/kpuentec/MidnightMP3.git
    cd MidnightMP3

    # Install dependencies
    pip install requirements.txt

    # Config and Run the app(see below)
    python ai_app.py

---
### Configuration

1. Create a .env file in your project folder with the following variables:
   
IMAP_HOST=imap.gmail.com
IMAP_USER=your-email@gmail.com
IMAP_PASSWORD=your-app-password
IMAP_FOLDER=Inbox
IMAP_PORT=993

*You must generate an App Password in your Google account security settings for IMAP_PASSWORD if you have 2FA enabled.*
2.  For Google Calendar integration, download your credentials.json from the Google Cloud Console and place it in the same folder as your scripts.
 
---
### File Structure

utils/

  ├── email_tools.py          # Email fetch & summarize tools

  ├── calendar_tools.py       # Google Calendar event creation

├── main.py                 # Core orchestration & AI agent logic and graph

├── ai_app.py               # Tkinter desktop chat app

├── .env                    # Environment variables (KEEP THIS SAFE, THIS IS YOUR PERSONAL DATA)

├── credentials.json        # Google Calendar OAuth credentials (KEEP THIS SAFE, THIS IS YOUR PERSONAL DATA)

├── requirements.txt        # Dependencies

├── .gitignore     

├── LICENSE

└── README.md

---
### Purpose

AI AGENTLOCAL empowers users with a secure, local AI agent capable of managing emails and calendars through natural language. By running models like qwen3:8b locally and restricting cloud data exposure, it ensures privacy while enabling powerful automation workflows. The included Tkinter app provides a simple but effective desktop interface to interact with the agent live.
Future AI agent could potentially:

*  Email support beyond Gmail

*  Natural language email replies and smart scheduling 

*  Enhanced UI and voice control

*  Play music downloaded on your device

*  Scan and detect network threats on your local environment

*  Adapt UI dynamically using generative design

---
### Security

* Uses .env files to keep secrets local and out of version control

* Stores OAuth tokens securely with automatic refreshing

* Direct connections to Gmail and Google Calendar APIs minimize external data exposure

* Fully runs on your local machine to protect sensitive information


---
### Credits

Tools Used:

* Ollama qwen3
* LangChain
* Google API Python Client
* imap-tools
* dotnev
* Python Tkinter

---
### License

This project is licensed under the MIT License — see LICENSE for details. (2025)
