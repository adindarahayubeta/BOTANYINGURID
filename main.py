import tweepy
import requests
import random
import os
from config import *
from tweet_templates import generate_tweet
from image_urls import IMAGE_URLS
from io import BytesIO

USED_LOG = "used_images.txt"

def get_trending_topics():
    # Karena akses API trending terbatas, pakai daftar topik manual
    return ["Bitcoin", "AI", "Tesla", "NBA", "Netflix"]

def pick_topic_by_niche(trends):
    for niche, keywords in NICHES.items():
        for keyword in keywords:
            for trend in trends:
                if keyword.lower() in trend.lower():
                    return trend, niche
    # fallback kalau tidak cocok
    return random.choice(trends), "general"

def pick_random_image_url():
    if os.path.exists(USED_LOG):
        with open(USED_LOG, "r") as f:
            used = f.read().splitlines()
    else:
        used = []

    unused = list(set(IMAGE_URLS) - set(used))

    if not unused:
        print("Semua gambar URL sudah dipakai. Reset log untuk mulai ulang.")
        return None

    chosen = random.choice(unused)

    with open(USED_LOG, "a") as f:
        f.write(chosen + "\n")

    return chosen

def tweet_with_image_url(text, image_url):
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Download gambar dari URL ke memori
    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    media = api.media_upload(filename='temp.jpg', file=image_data)

    api.update_status(status=text, media_ids=[media.media_id])
    print("Tweet berhasil dikirim:", text)

if __name__ == "__main__":
    trends = get_trending_topics()
    topic, niche = pick_topic_by_niche(trends)
    link = LINK_TEMPLATE.format(topic.replace(" ", "-"))
    tweet_text = generate_tweet(topic, niche, link)
    image_url = pick_random_image_url()

    if image_url:
        tweet_with_image_url(tweet_text, image_url)
    else:
        print("Tidak ada gambar URL yang tersedia.")

if __name__ == "__main__":
    try:
        trends = get_trending_topics()
        topic, niche = pick_topic_by_niche(trends)
        link = LINK_TEMPLATE.format(topic.replace(" ", "-"))
        tweet_text = generate_tweet(topic, niche, link)
        image_url = pick_random_image_url()

        if image_url:
            tweet_with_image_url(tweet_text, image_url)
        else:
            print("Tidak ada gambar URL yang tersedia.")
    except Exception as e:
        print("Error saat menjalankan bot:", e)
        import traceback
        traceback.print_exc()
        exit(1)

