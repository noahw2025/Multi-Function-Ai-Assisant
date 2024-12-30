# Multi-Function AI Pipeline
This project is a multi use case pipeline allowing me to explore the field as a whole and multiple different tools and ways of interacting with different environements

**Tools & Libraries**
- **Python 3.8+** for core development
- **OpenAI GPT-4** for conversational AI and code generation
- **Spotipy** (Spotify API) for music-related features
- **Hugging Face** (Stable Diffusion) for image generation
- **Requests & BeautifulSoup** for web scraping
- **Google Custom Search API** for internet queries

**Techniques & Skills**
- **Intent Recognition** (detecting special markers like `#createspotifyplaylist`)
- **Code Extraction & Execution** from GPT-4 responses
- **File & Process Management** (saving files, opening in IDE, running code)
- **API OAuth2 Authentication** (Spotify OAuth flow)
- **Environment Variable Management** (`.env` + secure key handling)
- **Web Scraping & Summarization** (fetch pages, parse content, summarize with GPT-4)
- **CLI Interaction** (event-driven user input loop)
- **Modular Design & Documentation** (clear README, separate utility modules)

A multi-functional Python AI pipeline integrating:
- **OpenAI GPT-4** for conversational AI and code generation
- **Hugging Face** models for image generation
- **Spotify** for playlist creation and user data retrieval
- **Google Custom Search** + **web scraping** for data gathering and summarization

> **Note:** This project is designed as a *showcase* of multiple AI/ML integrations. You can use it as a personal AI assistant, a code generator, a music playlist curator, or a web data gathering and summarization tool, other functions such as website generators, ai content writers, using bert to parse dat from audio or text

## Project Overview

This pipeline acts as a **unified AI assistant** capable of:
1. Generating or refining code with GPT-4 and automatically extracting that code to run or save locally.  
2. Searching the web, scraping content, then summarizing it with GPT-4.  
3. Interacting with the Spotify API to create playlists and retrieve user listening data.  
4. Generating images on the fly with Hugging Face’s Stable Diffusion model.  

It’s a powerful demonstration of integrating multiple APIs in one cohesive application.

---

## Features

- **AI Chat with Intent Recognition**  
  - Provide instructions or ask questions; the assistant recognizes special “intents” (e.g., to run code, create images, create a Spotify playlist) and executes them automatically.
- **Easy Code Extraction**  
  - GPT-4 code responses are automatically extracted (wrapped in `### ... ###`) and can be saved, opened in PyCharm, or run in the terminal.
- **Spotify Playlist Creation**  
  - Use a reference track to create a brand-new Spotify playlist, plus retrieve top artists/tracks.
- **Image Generation**  
  - Generate images directly from text prompts using the Hugging Face Stable Diffusion XL model.
- **Google Search + Web Scraping**  
  - Perform Google searches for any query, scrape top results, and summarize findings with GPT-4.
- **Fully Customizable**  
  - Swap in your own keys, modify scopes or GPT settings to tailor functionality to your needs.

---

## Architecture

Below is a high-level overview of how the system is orchestrated, including how it **loops back into normal GPT-4 conversation** if no special intent is detected:
         ┌─────────────┐
         │   User CLI  │
         └─────────────┘
               │
               ▼
     ┌────────────────────┐
     │  GPT-4 Interaction │
     └────────────────────┘
               │
               ▼
   ┌─────────────────────────┐
   │Intent Recognition Logic │
   └─────────────────────────┘
         ├─────────────┬───────────────┬──────────────┬────────────────┐
         │             │               │              │                │
   ┌──────┴───────┐    ▼               ▼              ▼                ▼
   │ No recognized │ Spotify API   Hugging Face   Google Search   Web Scraper
   │    intent?    │   (spotipy)    (Diffusion)      (API)       (BeautifulSoup)
   └──────┬───────┘                                                  
          │
   (YES)   │ (NO recognized intent)
          │
          ▼
    ┌───────────────────────────────┐
    │ Continue normal GPT-4 dialog │
    │ (loop back to conversation)  │
    └───────────────────────────────┘
                ▲
                │
                └───────────────────────────────────────────────────────┐
                                                                        │
                                                                        └── back to GPT-4 Interaction


