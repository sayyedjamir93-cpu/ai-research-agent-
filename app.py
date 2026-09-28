import os
from flask import Flask, render_template, request
from graph import graph
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

# Store last 5 searches
history = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        question = request.form["question"]

        state = {
            "question": question,
            "search_results": [],
            "pages": [],
            "summary": "",
            "sources": [],
            "steps": 0
        }

        result = graph.invoke(state)

        history.insert(0, question)
        if len(history) > 5:
            history.pop()

        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

        return render_template(
            "index.html",
            summary=result["summary"],
            sources=result["sources"],
            steps=result["steps"],
            timestamp=timestamp,
            history=history
        )

    return render_template(
        "index.html",
        summary=None,
        sources=[],
        steps=0,
        timestamp=None,
        history=history
    )

if __name__ == "__main__":
    app.run(debug=True)