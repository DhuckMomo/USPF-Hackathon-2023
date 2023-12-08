from flask import Flask, render_template, request

app = Flask(__name__)

# Fake data for prediction
risk_factors = {
    "Location": {
        "High-risk": 0.5,
        "Moderate-risk": 0.3,
        "Low-risk": 0.1
    },
    "Building Type": {
        "Unreinforced masonry": 0.7,
        "Concrete": 0.4,
        "Steel": 0.2
    },
    "Building Age": {
        "Pre-1970": 0.6,
        "1970-2000": 0.4,
        "Post-2000": 0.2
    },
    "Preparedness Level": {
        "No prior training or emergency kit": 0.8,
        "Basic training and kit": 0.5,
        "Advanced training and comprehensive kit": 0.2
    }
}

@app.route("/", methods=["GET", "POST"])
def predict_risk():
    if request.method == "POST":
        location = request.form.get("location")
        building_type = request.form.get("building_type")
        building_age = request.form.get("building_age")
        preparedness_level = request.form.get("preparedness_level")

        risk_score = 0
        for factor, value in risk_factors.items():
            risk_score += value[request.form.get(factor.lower())]

        # Convert score to percentage
        risk_percentage = round(risk_score * 100, 2)
        return render_template("index.html", risk_percentage=risk_percentage)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
