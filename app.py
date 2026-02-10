from flask import Flask, request, jsonify
import requests
import math
import os

app = Flask(__name__)

OFFICIAL_EMAIL = "your_chitkara_email@chitkara.edu.in"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fibonacci(n):
    a, b = 0, 1
    res = []
    for _ in range(n):
        res.append(a)
        a, b = b, a + b
    return res

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def lcm(numbers):
    l = numbers[0]
    for i in numbers[1:]:
        l = l * i // math.gcd(l, i)
    return l

def hcf(numbers):
    h = numbers[0]
    for i in numbers[1:]:
        h = math.gcd(h, i)
    return h

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        data = request.json

        if "fibonacci" in data:
            result = fibonacci(int(data["fibonacci"]))

        elif "prime" in data:
            result = [x for x in data["prime"] if is_prime(x)]

        elif "lcm" in data:
            result = lcm(data["lcm"])

        elif "hcf" in data:
            result = hcf(data["hcf"])

        elif "AI" in data:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": data['AI']}]}]
            }
            r = requests.post(url, json=payload)
            result = r.json()["candidates"][0]["content"]["parts"][0]["text"]

        else:
            return jsonify({"is_success": False}), 400

        return jsonify({
            "is_success": True,
            "official_email": OFFICIAL_EMAIL,
            "data": result
        })

    except:
        return jsonify({"is_success": False}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    })

if __name__ == "__main__":
    app.run()