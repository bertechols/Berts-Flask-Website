from flask import Flask, render_template, request, redirect, flash
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'a_random_secret_key_for_flask_messages'  # Needed for flash messages

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        full_message = f"From: {name} <{email}>\n\n{message}"

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
                server.sendmail(
                    from_addr=os.getenv("EMAIL_USER"),
                    to_addrs="bert.echols@icloud.com",
                    msg=f"Subject: Contact Form Message\n\n{full_message}"
                )
            flash("Email sent successfully!", "success")
        except Exception as e:
            print("Email send failed:", e)
            flash("There was an error sending your message.", "error")

        return redirect("/contact")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)

