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
                "content": "Given multiple articles, generate a short YouTube description that covers all of the articles while mixing in popular keywords without the hashtag. The structure should be a strong intro (2-3 sentences), a detailed outline (150 words), and then the links to the articles. Included 5 main keywords at the bottom (each should have a # before the keyword). DO NOT EXCEED 4,000 CHARACTERS. JUST RESPOND WITH THE DESCRIPTION NO QUOTES: "
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
    try:
        articles_json = json.dumps(articles)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Given multiple articles, generate tags for a YouTube video based on the articles. Use the 'MVC Formula' for the video tags. The first tag should be the main keyword, then some variations, and finally 1-2 tags that describe the video's overall category. EACH TAG SHOULD BE ONE STRING AND PUT INTO AN ARRAY. DO NOT EXCEED 500 CHARACTERS. YOUR RESPONSE MUST ONLY BE THE ARRAY: "
                },
                {
                    "role": "user",
                    "content": articles_json
                }
            ],
            model="llama3-8b-8192",
        )
        return response.choices[0].message.content
    except:
        return []

def generate_title_tiktok(articles):
    articles_json = json.dumps(articles)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a TikTok creator who is making a video about the news. You have a just one article that you want to cover in the video. Your job is to generate a title for the video that will grab people's attention. The title should be short and catchy, and should contain 4 hashtags. You should choose the hashtags based off of relevancy and popularity. DO NOT EXCEED 100 CHARACTERS AND DO NOT INCLUDE QUOTES. JUST RESPOND WITH THE TITLE: "
            },
            {
                "role": "user",
                "content": articles_json
            }
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

def generate_title_youtube(articles):
    articles_json = json.dumps(articles)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a YouTuber who is making a video about the news. You have multiple articles that you want to cover in the video. Your job is to generate a title for the video that will grab people's attention. If there are multiple articles, choose one to make the title about. The title should be short and catchy. DO NOT EXCEED 100 CHARACTERS AND DO NOT INCLUDE QOUTES. JUST RESPOND WITH THE TITLE: "
            },
            {
                "role": "user",
                "content": articles_json
            }
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content
