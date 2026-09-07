import os
import random
from groq import Groq
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# ১. টপিক নির্বাচন (অ্যান্ড্রয়েড ও বাটন মোবাইল)
topics = [
    "অ্যান্ড্রয়েড ফোন স্লো হয়ে গেলে ফাস্ট করার উপায়",
    "বাটন মোবাইলে সিম নেটওয়ার্ক না পাওয়া সমস্যার সমাধান",
    "অ্যান্ড্রয়েড ফোনের ব্যাটারি ড্রেন দ্রুত হওয়ার কারণ ও সমাধান",
    "বাটন মোবাইলে হেডফোন মোড অন হয়ে থাকলে কীভাবে অফ করবেন",
    "অ্যান্ড্রয়েড ফোনে অ্যাপ ইনস্টল না হওয়া (App Not Installed) সমস্যার সমাধান",
    "বাটন মোবাইলের কিপ্যাড বা বোতাম কাজ না করলে কী করবেন",
    "অ্যান্ড্রয়েড ফোনের স্টোরেজ ফুল সমস্যার সহজ সমাধান",
    "বাটন মোবাইলে কল ইনকামিং ব্লক হয়ে গেলে ছাড়ানোর উপায়",
    "অ্যান্ড্রয়েড ফোন অতিরিক্ত গরম হওয়া কমানোর টিপস",
    "বাটন মোবাইলের ডিসপ্লে সাদা হয়ে গেলে করণীয়"
]

selected_topic = random.choice(topics)

# ২. Groq AI দিয়ে কন্টেন্ট জেনারেট করা
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

prompt = f"""
তুমি একজন মোবাইল টেক বিশেষজ্ঞ। 'Mobile User' ব্লগের জন্য নিচে দেওয়া বিষয়ের ওপর একটি বিস্তারিত এবং আকর্ষণীয় ব্লগ পোস্ট বাংলা ভাষায় লেখো:

বিষয়: {selected_topic}

পোস্টের ফরম্যাট:
- একটি আকর্ষণীয় শিরোনাম (Title)
- ভূমিকা
- মূল সমস্যাগুলো
- ধাপ অনুসারে ৩-৫টি সহজ সমাধান (HTML Formatting যেমন <h3>, <p>, <ul>, <li> ব্যবহার করবে)
- উপসংহার

প্রথম লাইনে শুধুমাত্র Title টি দেবে (যেমন: Title: আপনার শিরোনাম)। এরপর থেকে মূল কন্টেন্ট শুরু করবে।
"""

response = groq_client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.3-70b-versatile",
)

full_content = response.choices[0].message.content

# Title এবং Body আলাদা করা
lines = full_content.split("\n")
title = lines[0].replace("Title:", "").strip()
body = "\n".join(lines[1:]).strip()

# ৩. Blogger API দিয়ে পোস্ট তৈরি করা
BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")
CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")

creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

blogger = build('blogger', 'v3', credentials=creds)

post_body = {
    'kind': 'blogger#post',
    'title': title,
    'content': body,
    'labels': ['Android Solution', 'Button Phone', 'Mobile Tips']
}

posts = blogger.posts()
result = posts.insert(blogId=BLOG_ID, body=post_body).execute()

print(f"Post Published Successfully! URL: {result.get('url')}")
