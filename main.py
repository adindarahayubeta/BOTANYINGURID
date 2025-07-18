import tweepy
import requests
import random
import os
from config import *
from tweet_templates import generate_tweet

USED_LOG = "used.txt"

def get_trending_topics():
    url = "https://api.twitter.com/1.1/trends/place.json?id=1"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    trends = [t["name"] for t in response.json()[0]["trends"]]
    return trends

def pick_topic_by_niche(trends):
    for niche, keywords in NICHES.items():
        for keyword in keywords:
            for trend in trends:
                if keyword.lower() in trend.lower():
                    return trend, niche
    return random.choice(trends), "general"

def pick_random_image(path="images"):
    all_images = [f for f in os.listdir(path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    if os.path.exists(USED_LOG):
        with open(USED_LOG, "r") as f:
            used = f.read().splitlines()
    else:
        used = []

    unused_images = list(set(all_images) - set(used))

    if not unused_images:
        print("Semua gambar sudah dipakai. Reset log atau tambah gambar baru.")
        return None

    chosen = random.choice(unused_images)

    with open(USED_LOG, "a") as f:
        f.write(chosen + "\n")

    return os.path.join(path, chosen)

def tweet_with_image(text, image_path):
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    media = api.media_upload(image_path)
    api.update_status(status=text, media_ids=[media.media_id])
    print("Tweet berhasil dikirim:", text)

if __name__ == "__main__":
    trends = get_trending_topics()
    topic, niche = pick_topic_by_niche(trends)
    link = LINK_TEMPLATE.format(topic.replace(" ", "-"))
    tweet_text = generate_tweet(topic, niche, link)
    image_path = pick_random_image("images")

    if image_path:
        tweet_with_image(tweet_text, image_path)
    else:
        print("Tidak ada gambar untuk dipakai.")
