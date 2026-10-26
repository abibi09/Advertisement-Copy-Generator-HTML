from flask import Flask, request, jsonify, send_from_directory
import re
import pandas as pd

app = Flask(__name__)

POWER_WORDS = [
    "discover", "exclusive", "limited", "proven", "powerful",
    "transform", "easy", "new", "save", "free", "premium",
    "amazing", "boost", "best", "special", "today"
]

EMOTIONAL_TRIGGERS = {
    "Curiosity": ["discover", "secret", "uncover", "explore"],
    "Urgency": ["today", "limited", "now", "hurry"],
    "Trust": ["reliable", "proven", "trusted", "quality"],
    "Excitement": ["amazing", "exciting", "transform", "powerful"],
    "Value": ["save", "value", "affordable", "free"]
}

PLATFORM_LIMITS = {
    "Instagram": {"headline": 100, "body": 2200},
    "Facebook": {"headline": 40, "body": 500},
    "Google Ads": {"headline": 30, "body": 90},
    "LinkedIn": {"headline": 70, "body": 600},
    "Email Marketing": {"headline": 60, "body": 500},
    "General": {"headline": 100, "body": 500}
}

TONE_OPENINGS = {
    "Creative": [
        "Imagine something extraordinary:",
        "Ready for something new?",
        "Make your next move count:"
    ],
    "Professional": [
        "Discover a practical solution:",
        "Meet a smarter way to work:",
        "Choose a solution designed for you:"
    ],
    "Funny": [
        "Your old routine called—it wants an upgrade!",
        "Why settle for boring?",
        "Good news: your search can take a break!"
    ],
    "Friendly": [
        "We've got something for you:",
        "Let's make life a little easier:",
        "Here's something you'll love:"
    ],
    "Persuasive": [
        "It's time to make a change:",
        "Don't miss this opportunity:",
        "Take the next step today:"
    ],
    "Luxury": [
        "Experience a more refined choice:",
        "Discover a premium experience:",
        "Make room for something exceptional:"
    ]
}

CALLS_TO_ACTION = {
    "Instagram": ["Shop Now", "Explore More", "See What's New"],
    "Facebook": ["Learn More", "Get Started", "Shop Today"],
    "Google Ads": ["Get Started", "Learn More", "Discover More"],
    "LinkedIn": ["Connect With Us", "Learn More", "Get in Touch"],
    "Email Marketing": ["Read More", "Claim Your Offer", "Get Started"],
    "General": ["Learn More", "Get Started", "Discover More"]
}

VALID_GOALS = {"Awareness", "Traffic", "Sales", "Engagement", "Leads"}


def clean_text(value, default=""):
    if not isinstance(value, str):
        return default
    return re.sub(r"\s+", " ", value).strip() or default


def find_keywords(text):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]{2,}\b", text.lower())
    ignored = {
        "the", "and", "for", "with", "this", "that", "from",
        "your", "you", "are", "our", "has", "have", "can",
        "will", "into", "its", "all", "new"
    }
    return list(dict.fromkeys(word for word in words if word not in ignored))[:8]


def find_triggers(text):
    lowered = text.lower()
    return [
        trigger
        for trigger, words in EMOTIONAL_TRIGGERS.items()
        if any(re.search(r"\b" + re.escape(word) + r"\b", lowered) for word in words)
    ]


def estimate_ctr(headline, body, keywords, platform):
    """Heuristic score, not a trained model or real measured CTR."""
    text = f"{headline} {body}".lower()
    score = 40

    if any(word in text for word in POWER_WORDS):
        score += 15
    if any(keyword in text for keyword in keywords):
        score += 15
    if any(word in text for word in ["you", "your", "we", "yourself"]):
        score += 10
    if any(word in text for word in ["today", "now", "limited", "discover"]):
        score += 10

    limits = PLATFORM_LIMITS[platform]
    if len(headline) <= limits["headline"]:
        score += 5
    if len(body) <= limits["body"]:
        score += 5

    return min(score, 100)


def generate_variations(product, description, platform, tone, audience, goal):
    limits = PLATFORM_LIMITS[platform]
    openings = TONE_OPENINGS[tone]
    ctas = CALLS_TO_ACTION[platform]
    keywords = find_keywords(description)

    benefit = description.rstrip(".!? ")
    if len(benefit) > 180:
        benefit = benefit[:177].rsplit(" ", 1)[0] + "..."

    audience_text = audience if audience and audience.lower() != "everyone" else "you"
    goal_lines = {
        "Awareness": [f"Meet a simple way to make {product} part of your day.", f"See why {audience_text} are taking a closer look at {product}.", f"Get to know {product} and what it can offer."],
        "Traffic": [f"Visit our page to learn more about {product}.", f"Explore the details and find the right fit for {audience_text}.", f"Take a closer look at {product} online."],
        "Sales": [f"Ready to try it? Choose {product} today.", f"Make {product} your next smart purchase.", f"Order today and enjoy the benefits for yourself."],
        "Engagement": [f"What matters most to you in {product}? Tell us below.", f"Share this with someone who would love {product}.", f"Join the conversation—what do you think of {product}?"],
        "Leads": [f"Contact us to find out how {product} can help.", f"Request more information and explore your options.", f"Get in touch to learn whether {product} is right for you."]
    }

    variations = []
    headline_templates = [
        f"Discover {product}",
        f"A Better Everyday Choice",
        f"Meet Your New {product}"
    ]

    for index in range(3):
        headline = headline_templates[index][:limits["headline"]]
        body = f"{openings[index]} {product}: {benefit}. {goal_lines.get(goal, goal_lines['Awareness'])[index]}"
        body = re.sub(r"\s+", " ", body).strip()[:limits["body"]]

        variations.append({
            "variant": f"Variation {index + 1}",
            "headline": headline,
            "body": body,
            "cta": ctas[index],
            "platform": platform,
            "headline_characters": len(headline),
            "body_characters": len(body),
            "headline_limit": limits["headline"],
            "body_limit": limits["body"],
            "keywords": keywords,
            "emotional_triggers": find_triggers(f"{headline} {body}"),
            "estimated_ctr_score": estimate_ctr(headline, body, keywords, platform)
        })

    comparison = pd.DataFrame([
        {
            "Variation": item["variant"],
            "Headline Characters": item["headline_characters"],
            "Body Characters": item["body_characters"],
            "Estimated Engagement Score": item["estimated_ctr_score"]
        }
        for item in variations
    ])

    return variations, comparison.to_dict(orient="records")


@app.route("/")
def home():
    # Serve the HTML from Flask so the page can call /generate without CORS issues.
    return send_from_directory(".", "index.html")


@app.route("/health")
def health():
    return jsonify({
        "message": "Advertisement Copy Generator API is running.",
        "status": "success"
    })


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    product = clean_text(data.get("product"), "Your Product")[:100]
    description = clean_text(
        data.get("description"),
        "A useful solution designed to make your everyday life easier"
    )[:1500]
    platform = clean_text(data.get("platform"), "Instagram")
    tone = clean_text(data.get("tone"), "Creative")
    audience = clean_text(data.get("audience"), "everyone")[:150]
    goal = clean_text(data.get("goal"), "Awareness")

    if platform not in PLATFORM_LIMITS:
        return jsonify({"error": "Please select a supported advertising platform."}), 400
    if tone not in TONE_OPENINGS:
        return jsonify({"error": "Please select a supported writing tone."}), 400
    if goal not in VALID_GOALS:
        return jsonify({"error": "Please select a supported advertising goal."}), 400

    variations, comparison = generate_variations(
        product, description, platform, tone, audience, goal
    )

    return jsonify({
        "status": "success",
        "product": product,
        "platform": platform,
        "variations": variations,
        "ab_comparison": comparison,
        "note": (
            "Estimated engagement scores are heuristic estimates, not measured "
            "click-through rates or predictions from a trained model."
        )
    })


if __name__ == "__main__":
    app.run(debug=True)
