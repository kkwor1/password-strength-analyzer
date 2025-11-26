from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)


# ----------------------------
# Character Sets
# ----------------------------
LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"


# ----------------------------
# Helper Functions
# ----------------------------

def detect_charset(password):
    """Return the total size of character sets used by the password."""
    k = 0
    used = {
        "lower": False,
        "upper": False,
        "digit": False,
        "symbol": False
    }

    for ch in password:
        if ch in LOWER:
            used["lower"] = True
        elif ch in UPPER:
            used["upper"] = True
        elif ch in DIGITS:
            used["digit"] = True
        else:
            used["symbol"] = True

    if used["lower"]:
        k += len(LOWER)
    if used["upper"]:
        k += len(UPPER)
    if used["digit"]:
        k += len(DIGITS)
    if used["symbol"]:
        k += len(SYMBOLS)

    return k


def classify_strength(entropy):
    """Classify password strength by entropy."""
    if entropy < 28:
        return "Weak", "Add more characters or include symbols."
    elif entropy < 36:
        return "Moderate", "Consider increasing password length."
    elif entropy < 60:
        return "Strong", "Good password — adding more characters improves security."
    else:
        return "Very Strong", "Great password! Very high resistance to brute-force attacks."


def seconds_to_human(t):
    """Convert seconds to human readable format."""
    if t < 60:
        return f"{t:.2f} sec"
    mins = t / 60
    if mins < 60:
        return f"{mins:.2f} min"
    hrs = mins / 60
    if hrs < 24:
        return f"{hrs:.2f} hours"
    days = hrs / 24
    if days < 365:
        return f"{days:.2f} days"
    years = days / 365
    return f"{years:.2f} years"


# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "No password provided"}), 400

    n = len(password)
    k = detect_charset(password)

    # Avoid math errors
    if n == 0 or k == 0:
        return jsonify({
            "length": n,
            "charset": k,
            "combinations": 0,
            "entropy": 0,
            "time_1e9": "—",
            "strength": "Weak",
            "feedback": "Password is empty."
        })

    # Total combinations: k^n
    combinations = k ** n

    # Entropy: log2(k^n) = n * log2(k)
    entropy = n * math.log2(k)

    # Estimated brute force time at 1 billion guesses/sec
    guesses_per_sec = 1_000_000_000
    time_seconds = combinations / guesses_per_sec
    time_human = seconds_to_human(time_seconds)

    strength, feedback = classify_strength(entropy)

    return jsonify({
        "length": n,
        "charset": k,
        "combinations": f"{combinations:.3e}",
        "entropy": entropy,
        "time_1e9": time_human,
        "strength": strength,
        "feedback": feedback
    })


# ----------------------------
# Run App
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
