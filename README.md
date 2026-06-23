# My First Generative AI Chatbot 🤖

### 🚀 Live Demo (No installation required!)
You don't need to install anything to try this out. Just click the link below to open the Glassmorphism UI right in your browser!

👉 **[Try the Live Demo Here](https://raw.githack.com/bajpaiaviral828-cmyk/generative-ai-chatbot/main/demo.html?v=2)**

This is my very first project learning how to build AI applications! I built a command-line chatbot that connects to the Google Gemini API. 

The coolest part is that it actually **remembers** what you say.

## Why I Built This
When I started learning about LLMs, I thought they just magically remembered you. I quickly realized API calls are stateless! The biggest challenge was figuring out how to build a Python array that stores the previous conversation and feeds it back into the prompt every time.

## What I Learned
- **API Integration:** How to get an API key and send requests to Google Gemini.
- **Sliding Window Memory:** If you send too much history to the API, it crashes because of the token limit. I wrote a "sliding window" logic that drops the oldest messages so the prompt doesn't get too long.
- **Saving Data:** I figured out how to use the Python `json` library to save the chat history to `chats.json`. That way, if I close the terminal, my chat is still there when I restart.
- **Rate Limits:** I learned the hard way that Google blocks you if you send messages too fast. I found a library called `tenacity` on StackOverflow that automatically waits and retries if the API crashes.

## How to run it

1. Make sure you have python installed.
2. Install the libraries: `pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and put your Gemini API key in there.
4. Run `python main.py`

## TODOs for the future
- [ ] Add a Web UI instead of just a terminal.
- [ ] Count the actual tokens instead of just deleting messages based on an arbitrary limit.
- [ ] Build a "personality switcher" so the bot can act like different characters.
