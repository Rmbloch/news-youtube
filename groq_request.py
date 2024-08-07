import json
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def summarize_article(link):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your job is to generate a description/commentary of current events for a video. Given a link, your response should ONLY BE THE COMMENTARY. Do not include any blank fields: ",
            },
            {
                "role": "user",
                "content": link,
            },
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

def generate_description(articles):
    articles_json = json.dumps(articles)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Given multiple articles, generate a short YouTube description that covers all of the articles while mixing in popular keywords without the hashtag. DO NOT EXCEED 4,000 CHARACTERS. JUST RESPOND WITH THE DESCRIPTION NO QUOTES: "
            },
            {
                "role": "user",
                "content": articles_json
            }
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

def generate_tags(articles):
    articles_json = json.dumps(articles)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Given multiple articles, generate tags for a YouTube video based on the articles. DO NOT EXCEED 500 CHARACTERS. JUST RESPOND WITH THE TAGS IN AN ARRAY: "
            },
            {
                "role": "user",
                "content": articles_json
            }
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content
