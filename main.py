from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "your-secret-key-change-this-in-production"

# Simple in-memory storage for demo purposes
# In production, you'd use a proper database
data_file = "data.json"


def load_data():
    """Load data from JSON file"""
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return {"posts": [], "contacts": []}


def save_data(data):
    """Save data to JSON file"""
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def index():
    """Home page with recent posts"""
    data = load_data()
    recent_posts = data["posts"][-3:]  # Show last 3 posts
    return render_template("index.html", posts=recent_posts)


@app.route("/about")
def about():
    """About page"""
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page with form"""
    if request.method == "POST":
        data = load_data()
        contact_entry = {
            "id": len(data["contacts"]) + 1,
            "name": request.form["name"],
            "email": request.form["email"],
            "message": request.form["message"],
            "timestamp": datetime.now().isoformat(),
        }
        data["contacts"].append(contact_entry)
        save_data(data)
        flash("Thank you for your message! We'll get back to you soon.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/blog")
def blog():
    """Blog page showing all posts"""
    data = load_data()
    return render_template("blog.html", posts=data["posts"])


@app.route("/blog/new", methods=["GET", "POST"])
def new_post():
    """Create new blog post"""
    if request.method == "POST":
        data = load_data()
        post = {
            "id": len(data["posts"]) + 1,
            "title": request.form["title"],
            "content": request.form["content"],
            "author": request.form["author"],
            "timestamp": datetime.now().isoformat(),
        }
        data["posts"].append(post)
        save_data(data)
        flash("Post created successfully!", "success")
        return redirect(url_for("blog"))
    return render_template("new_post.html")


@app.route("/blog/<int:post_id>")
def view_post(post_id):
    """View individual blog post"""
    data = load_data()
    post = next((p for p in data["posts"] if p["id"] == post_id), None)
    if not post:
        flash("Post not found!", "danger")
        return redirect(url_for("blog"))
    return render_template("post.html", post=post)


@app.route("/api/posts")
def api_posts():
    """API endpoint for posts"""
    data = load_data()
    return jsonify(data["posts"])


@app.route("/api/contacts")
def api_contacts():
    """API endpoint for contacts"""
    data = load_data()
    return jsonify(data["contacts"])


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template("500.html"), 500


if __name__ == "__main__":
    # Initialize with sample data if data file doesn't exist
    if not os.path.exists(data_file):
        sample_data = {
            "posts": [
                {
                    "id": 1,
                    "title": "Welcome to Our Blog",
                    "content": "This is our first blog post. Welcome to our website!",
                    "author": "Admin",
                    "timestamp": datetime.now().isoformat(),
                }
            ],
            "contacts": [],
        }
        save_data(sample_data)

    app.run(debug=True)
