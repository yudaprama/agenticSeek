# AgenticSeek: Private, Local Manus Alternative.

<p align="center">
<img align="center" src="./media/agentic_seek_logo.png" width="300" height="300" alt="Agentic Seek Logo">
<p>



*A **100% local alternative to Manus AI**, this voice-enabled AI assistant autonomously browses the web, writes code, and plans tasks while keeping all data on your device. Tailored for local reasoning models, it runs entirely on your hardware, ensuring complete privacy and zero cloud dependency.*

[![Visit AgenticSeek](https://img.shields.io/static/v1?label=Website&message=AgenticSeek&color=blue&style=flat-square)](https://fosowl.github.io/agenticSeek.html) ![License](https://img.shields.io/badge/license-GPL--3.0-green) [![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289DA?logo=discord&logoColor=white)](https://discord.gg/8hGDaME3TC) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/fosowl.svg?style=social&label=Update%20%40Fosowl)](https://x.com/Martin993886460) [![GitHub stars](https://img.shields.io/github/stars/Fosowl/agenticSeek?style=social)](https://github.com/Fosowl/agenticSeek/stargazers)

### Why AgenticSeek ?

* 🔒 Fully Local & Private - Everything runs on your machine — no cloud, no data sharing. Your files, conversations, and searches stay private.

* 🌐 Smart Web Browsing - AgenticSeek can browse the internet by itself — search, read, extract info, fill web form — all hands-free.

* 💻 Autonomous Coding Assistant - Need code? It can write, debug, and run programs in Python, C, Go, Java, and more — all without supervision.

* 🧠 Smart Agent Selection - You ask, it figures out the best agent for the job automatically. Like having a team of experts ready to help.

* 📋 Plans & Executes Complex Tasks - From trip planning to complex projects — it can split big tasks into steps and get things done using multiple AI agents.



### **Demo**

> *Can you search for the agenticSeek project, learn what skills are required, then open the CV_candidates.zip and then tell me which match best the project*

https://github.com/user-attachments/assets/b8ca60e9-7b3b-4533-840e-08f9ac426316

Disclaimer: This demo, including all the files that appear (e.g: CV_candidates.zip), are entirely fictional. We are not a corporation, we seek open-source contributors not candidates.

> 🛠⚠️️ **Active Work in Progress**

> 🙏 This project started as a side-project and has zero roadmap and zero funding. It's grown way beyond what I expected by ending in GitHub Trending. Contributions, feedback, and patience are deeply appreciated.

## Prerequisites

Make sure you have chrome driver, docker and python3.10 installed.

For issues related to chrome driver, see the **Chromedriver** section.

### 1. **Clone the repository and setup**

```sh
git clone https://github.com/Fosowl/agenticSeek.git
cd agenticSeek
mv .env.example .env
```

### 2. Change the .env file content

```sh
SEARXNG_BASE_URL="http://127.0.0.1:8080"
REDIS_BASE_URL="redis://redis:6379/0"
WORK_DIR="/Users/mlg/Documents/workspace_for_ai"
OLLAMA_PORT="11434"
LM_STUDIO_PORT="1234"
CUSTOM_ADDITIONAL_LLM_PORT="11435"
OPENAI_API_KEY='optional'
DEEPSEEK_API_KEY='optional'
OPENROUTER_API_KEY='optional'
TOGETHER_API_KEY='optional'
GOOGLE_API_KEY='optional'
ANTHROPIC_API_KEY='optional'
```

**API Key are totally optional for user who choose to run LLM locally. Which is the primary purpose of this project. Leave empty if you have sufficient hardware**

The following environment variables configure your application's connections and API keys.  

Update the `.env` file with your own values as needed:

- **SEARXNG_BASE_URL**: Leave unchanged 
- **REDIS_BASE_URL**: Leave unchanged 
- **WORK_DIR**: Path to your working directory on your local machine. AgenticSeek will be able to read and interact with these files.
- **OLLAMA_PORT**: Port number for the Ollama service.
- **LM_STUDIO_PORT**: Port number for the LM Studio service.
- **CUSTOM_ADDITIONAL_LLM_PORT**: Port for any additional custom LLM service.

All API key environment variables below are **optional**. You only need to provide them if you plan to use external APIs instead of running LLMs locally.

### 3. **Start Docker**

Make sure Docker is installed and running on your system. You can start Docker using the following commands:

- **On Linux/macOS:**  
    Open a terminal and run:
    ```sh
    sudo systemctl start docker
    ```
    Or launch Docker Desktop from your applications menu if installed.

- **On Windows:**  
    Start Docker Desktop from the Start menu.

You can verify Docker is running by executing:
```sh
docker info
```
If you see information about your Docker installation, it is running correctly.

---

## Setup for running LLM locally on your machine

**Hardware Requirements:**

To run LLMs locally, you'll need sufficient hardware. At a minimum, a GPU capable of running Qwen/Deepseek 14B is required. See the FAQ for detailed model/performance recommendations.

**Setup Ollama**

Start Ollama:

```sh
ollama serve
```

The system will automatically select the best available model. We recommend reasoning models such as *Qwen* or *Deepseek*.

See the **FAQ** at the end of the README for required hardware.

```sh
[MAIN]
agent_name = Jarvis # name of your AI
server_address = 127.0.0.1:11434 # Ollama server address
recover_last_session = True # whenever to recover the previous session
save_session = True # whenever to remember the current session
jarvis_personality = False # Whenever to use a more "Jarvis" like personality (experimental)
languages = en # The list of languages
[BROWSER]
headless_browser = True # leave unchanged unless using CLI on host.
stealth_mode = True # Use undetected selenium to reduce browser detection
```

**Warning**:

- The `config.ini` file format does not support comments.
Do not copy and paste the example configuration directly, as comments will cause errors.  Instead, manually modify the `config.ini` file with your desired settings, excluding any comments.

Next step: [Start services and run AgenticSeek](#Start-services-and-Run)

*See the **Known issues** section if you are having issues*

*See the **Config** section for detailed config file explanation.*

---

## Start services and Run

Start required services. This will start all services from the docker-compose.yml, including:
    - searxng
    - redis (required by searxng)
    - frontend
    - backend (if using `full`)

```sh
./start_services.sh full # MacOS
start ./start_services.cmd full # Window
```

**Warning:** This step will download and load all Docker images, which may take up to 30 minutes. After starting the services, please wait until the backend service is fully running (you should see backend: <info> in the log) before sending any messages. The backend services may take longer to start than others.

Go to `http://localhost:3000/` and you should see the web interface.

**Optional:** Run with the CLI interface:

To run with CLI interface you would have to install package on host:

```sh
./install.sh
./install.bat # windows
```

Start services:

```sh
./start_services.sh # MacOS
start ./start_services.cmd # Window
```

Then run : `python3 cli.py`

---

## Usage

Make sure the services are up and running with `./start_services.sh full` and go to `localhost:3000` for web interface.



To exit, simply say/type `goodbye`.

Here are some example usage:

> *Make a snake game in python!*

> *Search the web for top cafes in Rennes, France, and save a list of three with their addresses in rennes_cafes.txt.*

> *Write a Go program to calculate the factorial of a number, save it as factorial.go in your workspace*

> *Search my summer_pictures folder for all JPG files, rename them with today’s date, and save a list of renamed files in photos_list.txt*

> *Search online for popular sci-fi movies from 2024 and pick three to watch tonight. Save the list in movie_night.txt.*

> *Search the web for the latest AI news articles from 2025, select three, and write a Python script to scrape their titles and summaries. Save the script as news_scraper.py and the summaries in ai_news.txt in /home/projects*

> *Friday, search the web for a free stock price API, register with supersuper7434567@gmail.com then write a Python script to fetch using the API daily prices for Tesla, and save the results in stock_prices.csv*

*Note that form filling capabilities are still experimental and might fail.*



After you type your query, AgenticSeek will allocate the best agent for the task.

Because this is an early prototype, the agent routing system might not always allocate the right agent based on your query.

Therefore, you should be very explicit in what you want and how the AI might proceed for example if you want it to conduct a web search, do not say:

`Do you know some good countries for solo-travel?`

Instead, ask:

`Do a web search and find out which are the best country for solo-travel`

---





## Config

Example config:
```
[MAIN]
agent_name = Jarvis
server_address = 127.0.0.1:11434
recover_last_session = False
save_session = False
jarvis_personality = False
languages = en
[BROWSER]
headless_browser = False
stealth_mode = False
```

**Explanation**:

- agent_name -> Name of the agent, e.g., Jarvis.

- server_address -> Ollama server address, e.g., 127.0.0.1:11434.

- recover_last_session -> Restarts from last session (True) or not (False).

- save_session -> Saves session data (True) or not (False).

- jarvis_personality -> Uses a JARVIS-like personality (True) or not (False). This simply change the prompt file.

- languages -> The list of supported language, needed for the llm router to work properly.

- headless_browser -> Runs browser without a visible window (True) or not (False).

- stealth_mode -> Make bot detector time harder. Only downside is you have to manually install the anticaptcha extension.

- languages -> List of supported languages. Required for agent routing system. The longer the languages list the more model will be downloaded.

## Provider

AgenticSeek uses Ollama as the LLM provider. The system automatically selects the best available model from your Ollama installation.

# Known issues

## Chromedriver Issues

**Known error #1:** *chromedriver mismatch*

`Exception: Failed to initialize browser: Message: session not created: This version of ChromeDriver only supports Chrome version 113
Current browser version is 134.0.6998.89 with binary path`

This happen if there is a mismatch between your browser and chromedriver version.

You need to navigate to download the latest version:

https://developer.chrome.com/docs/chromedriver/downloads

If you're using Chrome version 115 or newer go to:

https://googlechromelabs.github.io/chrome-for-testing/

And download the chromedriver version matching your OS.

![alt text](./media/chromedriver_readme.png)

If this section is incomplete please raise an issue.

##  connection adapters Issues

```
Exception: Provider lm-studio failed: HTTP request failed: No connection adapters were found for '127.0.0.1:11434/v1/chat/completions'
```

Make sure you have `http://` in front of the provider IP address :

`provider_server_address = http://127.0.0.1:11434`

## SearxNG base URL must be provided

```
raise ValueError("SearxNG base URL must be provided either as an argument or via the SEARXNG_BASE_URL environment variable.")
ValueError: SearxNG base URL must be provided either as an argument or via the SEARXNG_BASE_URL environment variable.
```

Maybe you didn't move `.env.example` as `.env` ? You can also export SEARXNG_BASE_URL:

`export  SEARXNG_BASE_URL="http://127.0.0.1:8080"`

## FAQ

**Q: What hardware do I need?**  

| Model Size  | GPU  | Comment                                               |
|-----------|--------|-----------------------------------------------------------|
| 7B        | 8GB Vram | ⚠️ Not recommended. Performance is poor, frequent hallucinations, and planner agents will likely fail. |
| 14B        | 12 GB VRAM (e.g. RTX 3060) | ✅ Usable for simple tasks. May struggle with web browsing and planning tasks. |
| 32B        | 24+ GB VRAM (e.g. RTX 4090) | 🚀 Success with most tasks, might still struggle with task planning |
| 70B+        | 48+ GB Vram (eg. mac studio) | 💪 Excellent. Recommended for advanced use cases. |

**Q: Why Deepseek R1 over other models?**  

Deepseek R1 excels at reasoning and tool use for its size. We think it’s a solid fit for our needs other models work fine, but Deepseek is our primary pick.

**Q: I get an error running `cli.py`. What do I do?**  

Ensure local is running (`ollama serve`), your `config.ini` matches your provider, and dependencies are installed. If none work feel free to raise an issue.

**Q: Can it really run 100% locally?**

Yes, with Ollama all LLM models run locally on your machine.

**Q: Why should I use AgenticSeek when I have Manus?**

This started as Side-Project we did out of interest about AI agents. What’s special about it is that we want to use local model and avoid APIs.
We draw inspiration from Jarvis and Friday (Iron man movies) to make it "cool" but for functionality we take more inspiration from Manus, because that's what people want in the first place: a local manus alternative.
Unlike Manus, AgenticSeek prioritizes independence from external systems, giving you more control, privacy and avoid api cost.

## Contribute

We’re looking for developers to improve AgenticSeek! Check out open issues or discussion.

[Contribution guide](./docs/CONTRIBUTING.md)

[![Star History Chart](https://api.star-history.com/svg?repos=Fosowl/agenticSeek&type=Date)](https://www.star-history.com/#Fosowl/agenticSeek&Date)

## Maintainers:

 > [Fosowl](https://github.com/Fosowl) | Paris Time 

 > [antoineVIVIES](https://github.com/antoineVIVIES) | Taipei Time 

 > [steveh8758](https://github.com/steveh8758) | Taipei Time 

## Special Thanks:

 > [tcsenpai](https://github.com/tcsenpai) and [plitc](https://github.com/plitc) For helping with backend dockerization

