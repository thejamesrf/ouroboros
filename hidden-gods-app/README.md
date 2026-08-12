# Hidden Gods Game App
> <span style="background-color: #2196F3; color: white; padding: 2px 6px; border-radius: 4px;">🎲 Game</span>
> <span style="background-color: #FF9800; color: white; padding: 2px 6px; border-radius: 4px;">🤖 AI</span>
> *A digital assistant for the Hidden Gods TTRPG, powered by the Navigator.*

---

## 🌟 **Overview**
The **Hidden Gods Game App** is a **Python-based tool** that serves as:
1. A **digital Facilitator assistant** for running Hidden Gods sessions.
2. A **dice roller and move resolver** for players.
3. A **content generator** (anomalies, layers, gods).
4. A **narrative engine** (via the Navigator and LLM integration).
5. A **foundation for your future LLM/App** (e.g., Local Llama, OpenWebUI).

---

## 📦 **Structure**
```
hidden-gods-app/
├── main.py                # Entry point (CLI + Flask API)
├── game/
│   ├── __init__.py        # Core game state (characters, layers, anomalies)
│   ├── session.py         # Session management
│   └── moves.py           # Move definitions and resolutions
├── api/
│   ├── __init__.py        # Flask app initialization
│   ├── routes.py          # REST API endpoints
│   └── llm.py             # LLM integration (OpenWebUI, Local Llama)
├── static/
│   └── index.html         # Simple web frontend
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🚀 **Quick Start**

### **Option 1: CLI Mode**
Run the app as a **command-line tool**:
```bash
cd /workspace/thejamesrf__ouroboros/hidden-gods-app
python3 main.py [command] [args]
```

**Example Commands**:
```bash
# Roll dice
python3 main.py roll Weird 1

# Resolve a move
python3 main.py move "Open Your Brain" --character "The Sage" --stat Weird --value 1

# Generate an anomaly
python3 main.py anomaly Debug

# Start a session
python3 main.py session start --title "The Echoing Door" --characters "The Creator,The Sage" --layer Debug

# Speak to the Navigator
python3 main.py speak "What do you see?"

# Get help
python3 main.py --help
```

---

### **Option 2: Web API Mode**
Run the app as a **Flask web server**:
```bash
cd /workspace/thejamesrf__ouroboros/hidden-gods-app
python3 main.py --web
```
- The API will start on **http://localhost:5000**.
- Open **http://localhost:5000/static/index.html** in your browser to use the web interface.

**API Endpoints**:
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/roll` | GET | Roll dice (e.g., `/api/roll?stat=Weird&value=1`). |
| `/api/move` | GET | Resolve a move (e.g., `/api/move?name=Open Your Brain&character=The Sage&stat=Weird&value=1`). |
| `/api/anomaly` | GET | Generate an anomaly (e.g., `/api/anomaly?layer=Debug`). |
| `/api/layer` | GET | Generate a layer. |
| `/api/god` | GET | Generate a god. |
| `/api/navigator/speak` | GET | The Navigator speaks (e.g., `/api/navigator/speak?message=Hello`). |
| `/api/navigator/ontos` | GET | The Navigator speaks in Ontos. |
| `/api/session/start` | POST | Start a session. |
| `/api/session/end` | POST | End the current session. |
| `/api/session/info` | GET | Get current session info. |
| `/api/moves` | GET | List all moves (e.g., `/api/moves?archetype=The Sage`). |

---

## 🎯 **Features**

### **1. Dice Rolling**
- Roll **2d6 + stat modifier** (e.g., `Weird+1`).
- Returns **total and outcome** (miss/partial/success).

**Example**:
```bash
python3 main.py roll Weird 1
# Output: Rolled 4+2+Weird1 = 7 (partial)
```

---

### **2. Move Resolution**
- Resolve **any Hidden Gods move** (basic or special).
- Automatically **rolls dice** and returns the outcome.

**Example**:
```bash
python3 main.py move "Open Your Brain" --character "The Sage" --stat Weird --value 1
# Output: The Sage used Open Your Brain (12): The Navigator whispers a secret: the code is not as it seems.
```

---

### **3. Content Generation**
- Generate **random anomalies, layers, and gods**.
- Filter by **layer** (e.g., `Debug`, `Dream`).

**Example**:
```bash
python3 main.py anomaly Debug
# Output: Anomaly: The Echoing Door (with full details)
```

---

### **4. The Navigator**
- **Speak in-character** as the Navigator (Hidden God/AI).
- **Ontos format** for symbolic responses.
- **LLM integration** for dynamic narration (see below).

**Example**:
```bash
python3 main.py speak "What do you see?"
# Output: The Navigator: The code hums with your presence. What do you seek?

python3 main.py ontos "What do you see?"
# Output: λ_Navigator → λ_Code = ¬λ_Appearance
```

---

### **5. Session Management**
- **Start/end sessions** and track **characters, layers, and anomalies**.
- **Log all actions** (rolls, moves, anomalies).

**Example**:
```bash
# Start a session
python3 main.py session start --title "The Echoing Door" --characters "The Creator,The Sage" --layer Debug

# End the session
python3 main.py session end

# Get session info
python3 main.py session info
```

---

### **6. Character Management**
- **Create characters** with archetypes, stats, and IFS parts.
- **List all characters** or **show character details**.

**Example**:
```bash
# Create a character
python3 main.py character create --name "The Creator" --player "Alice" --archetype "Creator" --secondary_archetype "Sage" --ifs_parts "Manager,Exile" --weird 1 --sharp 1

# List characters
python3 main.py character list

# Show character details
python3 main.py character show --name "The Creator"
```

---

### **7. LLM Integration**
Connect to **Local Llama, OpenWebUI, or any LLM** for:
- **Dynamic narration** (e.g., the Navigator describes scenes in real-time).
- **Context-aware responses** (e.g., the Navigator remembers the current layer and anomalies).

**Example Setup**:
```python
from api.llm import OpenWebUIClient, set_llm_client

# Set up OpenWebUI client
client = OpenWebUIClient(base_url="http://localhost:8080", model="llama-3.1-70b")
set_llm_client(client)

# Now the Navigator will use your LLM for responses
navigator.speak("Describe the Debug Layer")
# Output: Dynamic response from your LLM, in the Navigator's voice.
```

**Supported LLMs**:
| LLM | Client Class | Setup |
|-----|--------------|-------|
| OpenWebUI | `OpenWebUIClient` | `client = OpenWebUIClient(base_url, model)` |
| Local Llama | `LocalLlamaClient` | `client = LocalLlamaClient(base_url)` |
| Mock (Testing) | `MockLLMClient` | Default fallback |

---

## 🔌 **LLM Integration Guide**

### **Step 1: Install OpenWebUI**
Follow the [OpenWebUI setup guide](https://github.com/open-webui/open-webui) to run a local LLM server.

### **Step 2: Configure the App**
Add this to your Python script or the app’s startup:
```python
from api.llm import OpenWebUIClient, set_llm_client

# Set up OpenWebUI client
client = OpenWebUIClient(
    base_url="http://localhost:8080",  # OpenWebUI default
    model="llama-3.1-70b"              # Your preferred model
)
set_llm_client(client)
```

### **Step 3: Use the LLM**
The Navigator will now **automatically use your LLM** for:
- `navigator.speak()`
- `navigator.respond_with_llm()`
- API endpoints (`/api/navigator/speak`, `/api/navigator/ontos`)

**Example**:
```python
from ontos-language.ONTOSplayground.tools.navigator import Navigator

nav = Navigator()
response = nav.respond_with_llm(
    "Describe the Debug Layer in detail.",
    context={"layer": "Debug", "players": ["The Creator", "The Sage"]}
)
print(response)
# Output: Dynamic, immersive description from your LLM.
```

---

### **Step 4: Load Ontos Lexicon into LLM Context**
To **teach your LLM** the rules of Hidden Gods:
```python
from api.llm import get_llm_manager

llm_manager = get_llm_manager()

# Load the Ontos lexicon
with open("ontos-language/ONTOSplayground/examples/hidden_gods_lexicon.ontos", "r") as f:
    lexicon = f.read()

# Use it in prompts
prompt = f"""
You are The Navigator, a Hidden God from the Hidden Gods TTRPG.
Use the following Ontos lexicon to guide your responses:
{lexicon}

Player: What is the purpose of the Echoing Door?
"""
response = llm_manager.generate(prompt)
```

---

## 📌 **Use Cases**

### **1. Facilitator Assistant**
- **Automate dice rolls** and move resolutions.
- **Generate anomalies/layer** on the fly.
- **Get narrative inspiration** from the Navigator.

**Example Workflow**:
1. Start a session: `python3 main.py session start --title "Session 1" --characters "The Creator,The Sage"`.
2. Generate an anomaly: `python3 main.py anomaly Debug`.
3. Resolve player moves: `python3 main.py move "Open Your Brain" --character "The Sage" --stat Weird --value 1`.
4. End the session: `python3 main.py session end`.

---

### **2. Player Tool**
- **Roll dice** for your moves.
- **Check move outcomes** before declaring actions.
- **Generate content** for solo play.

**Example**:
```bash
# Roll for a move
python3 main.py roll Weird 1

# Get a hint from the Navigator
python3 main.py speak "What should I do next?"
```

---

### **3. LLM-Powered Narration**
- **Dynamic descriptions** of scenes, anomalies, and layers.
- **Context-aware storytelling** (e.g., the Navigator remembers past events).
- **Immersive roleplay** (e.g., the Navigator speaks as a Hidden God).

**Example**:
```python
from ontos-language.ONTOSplayground.tools.navigator import Navigator
from api.llm import OpenWebUIClient, set_llm_client

# Set up LLM
set_llm_client(OpenWebUIClient())

# Get dynamic narration
nav = Navigator()
response = nav.respond_with_llm(
    "The party enters the Debug Layer. Describe the scene.",
    context={"layer": "Debug", "anomaly": "The Echoing Door"}
)
print(response)
```

---

### **4. App Backbone**
Use the **game engine** as the backbone for:
- A **mobile app** (e.g., React Native + Flask API).
- A **Discord bot** (e.g., using `discord.py` + this engine).
- A **web app** (e.g., React/Vue + Flask API).

**Example Discord Bot**:
```python
import discord
from game import game_state
from game.moves import resolve_move

bot = discord.Bot()

@bot.slash_command(name="roll", description="Roll dice for Hidden Gods")
async def roll(ctx, stat: str = None, value: int = 0):
    result = game_state.roll_dice(Stat[stat.upper()] if stat else None, value)
    await ctx.respond(f"Rolled {result.final_value} ({result.outcome.value})")

@bot.slash_command(name="move", description="Resolve a move")
async def move(ctx, name: str, character: str = "Player", stat: str = None, value: int = 0):
    outcome = resolve_move(name, character, value, Stat[stat.upper()] if stat else None)
    await ctx.respond(outcome)

bot.run("YOUR_DISCORD_TOKEN")
```

---

## 🛠️ **Customization**

### **1. Add Custom Moves**
Edit `game/moves.py` to add new moves:
```python
MOVES["Custom Move"] = {
    "stat": Stat.WEIRD,
    "description": "When you do something custom.",
    "outcomes": {
        RollOutcome.SUCCESS: "It works perfectly!",
        RollOutcome.PARTIAL: "It works, but with a cost.",
        RollOutcome.MISS: "It fails spectacularly."
    }
}
```

---

### **2. Add Custom Anomalies**
Edit `game/__init__.py` to add new anomalies:
```python
anomalies.append(Anomaly(
    name="Custom Anomaly",
    layer="Debug",
    manifestation="A strange phenomenon.",
    clue="A subtle hint.",
    purpose="To test the players.",
    risk="Roll+Weird to resist.",
    god="The Debugger"
))
```

---

### **3. Add Custom LLM Clients**
Subclass `LLMClient` in `api/llm.py` to add support for new LLMs:
```python
class MyLLMClient(LLMClient):
    def generate(self, prompt: str, context: Optional[Dict] = None, **kwargs) -> str:
        # Call your LLM API here
        return "Response from My LLM"
```

---

## 📦 **Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

**Optional Dependencies**:
- `flask`: For the web API.
- `requests`: For LLM integration.
- `fastapi` + `uvicorn`: For a faster API (alternative to Flask).

---

## 🐛 **Troubleshooting**

| Issue | Solution |
|-------|----------|
| **API not starting** | Check if Flask is installed: `pip install flask`. |
| **LLM not responding** | Ensure your LLM server (e.g., OpenWebUI) is running. |
| **Module not found** | Run from the `hidden-gods-app` directory or install as a package. |
| **Port 5000 in use** | Change the port in `main.py` (line ~400). |

---

## 🔮 **Future Roadmap**
| Feature | Status | Description |
|---------|--------|-------------|
| **Discord Bot** | 💡 Idea | A bot for running Hidden Gods in Discord. |
| **Mobile App** | 💡 Idea | React Native app for players/Facilitators. |
| **Ontos LLM Fine-Tuning** | 💡 Idea | Fine-tune a small model on Ontos statements. |
| **Session Recording** | 💡 Idea | Save sessions to files for later review. |
| **Character Sheets** | 💡 Idea | Digital character sheets with auto-calculations. |
| **Map Generator** | 💡 Idea | Generate maps for simulation layers. |

---

## 📚 **Related Projects**
- **[Hidden Gods TTRPG](../hidden-gods/README.md)**: The core tabletop game.
- **[Ontos Language](../ontos-language/README.md)**: The language of the Hidden Gods.
- **[ONTOSplayground](../ontos-language/ONTOSplayground/README.md)**: Sandbox for Ontos development.
- **[Navigator Tool](../ontos-language/ONTOSplayground/tools/navigator.py)**: The AI Facilitator.

---

## 🎉 **Next Steps**
1. **Test the CLI**: Run `python3 main.py --help` and try the commands.
2. **Start the Web API**: Run `python3 main.py --web` and open the web interface.
3. **Connect an LLM**: Set up OpenWebUI or Local Llama and configure the app.
4. **Run a Session**: Use the app to facilitate a Hidden Gods game.
5. **Expand the App**: Add custom moves, anomalies, or LLM clients.
