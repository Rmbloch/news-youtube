# Automated News Youtube Channel
> A fully automated youtube channel that focuses on daily global news. This program uses GNews API to grab articles, Groq API to generate commentary/summaries, google speech API for text to speech and speech to text, python libraries such as movie.py for creating the videos, youtube data v3 API to upload video. That is a very simple overview on how the code works. If you are interested in following the code... almost all of the code is run through script.py. None of this code is not to be reused, but can be used as inspiration. 

# Technologies Used
- Python
- GNews API
- Groq AI API (specifically using the AI model **llama3-8b-8192**)
- Google Speech API
- Google storage
- Many libraries
- YouTube Data v3 API
- Docker

# How I run this program
> Since this code is not designed to be reused by anyone else, I will not cover how to change it to run on your computer. I use docker to organize all the dependencies and packages in one place and to ensure nothing is installed on my computer. This program is run everyday on a Raspberry Pi using a cron task (which simply calls `docker compose up` once a day).

