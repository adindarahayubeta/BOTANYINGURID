import random

def generate_hashtags(topic):
    return f"#{topic.replace(' ', '')} #Trending"

def generate_tweet(topic, niche, link):
    templates = {
        "tech": [
            f"{topic} is making waves in tech today!",
            f"Everyone's talking about {topic} 👀💻",
        ],
        "crypto": [
            f"🚀 {topic} is mooning hard today! Crypto fam, stay tuned!",
            f"{topic} is making headlines in the crypto space!",
        ],
        "sports": [
            f"🔥 Big day for sports: {topic} is trending!",
            f"{topic} just shocked the world of sports 😱",
        ],
        "entertainment": [
            f"{topic} is everywhere on social media today 🎬✨",
            f"Can't believe what's happening with {topic}! 🍿",
        ],
    }
    message = random.choice(templates.get(niche, [f"Hot topic: {topic}"]))
    hashtags = generate_hashtags(topic)
    return f"{message}\n\n{hashtags}\n{link}"
