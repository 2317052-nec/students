from flask import Flask, request, redirect, url_for, render_template, session

app = Flask(__name__)
app.secret_key = 'secret123'

# In-memory database
forum = {
    "AI": [{"title": "Is AI Dangerous?", "replies": ["Yes", "Depends on usage."]}],
    "Web Dev": []
}

ADMIN_PASSWORD = "admin123"

@app.route('/')
def home():
    return render_template('index.html', forum=forum, page="home", admin=session.get("admin", False))

@app.route('/add_topic', methods=['POST'])
def add_topic():
    topic = request.form['topic']
    if topic and topic not in forum:
        forum[topic] = []
    return redirect(url_for('home'))

@app.route('/delete_topic/<topic>')
def delete_topic(topic):
    if session.get("admin"):
        forum.pop(topic, None)
    return redirect(url_for('home'))

@app.route('/topic/<topic>')
def view_topic(topic):
    return render_template('index.html', forum=forum, page="topic", topic=topic,
                           threads=forum.get(topic, []), admin=session.get("admin", False))

@app.route('/topic/<topic>/add_thread', methods=['POST'])
def add_thread(topic):
    title = request.form['title']
    if title:
        forum[topic].append({"title": title, "replies": []})
    return redirect(url_for('view_topic', topic=topic))

@app.route('/topic/<topic>/delete_thread/<int:tid>')
def delete_thread(topic, tid):
    if session.get("admin"):
        del forum[topic][tid]
    return redirect(url_for('view_topic', topic=topic))

@app.route('/topic/<topic>/<int:tid>')
def view_thread(topic, tid):
    thread = forum[topic][tid]
    return render_template('index.html', forum=forum, page="thread", topic=topic,
                           thread_id=tid, thread=thread, admin=session.get("admin", False))

@app.route('/topic/<topic>/<int:tid>/reply', methods=['POST'])
def add_reply(topic, tid):
    reply = request.form['reply']
    if reply:
        forum[topic][tid]["replies"].append(reply)
    return redirect(url_for('view_thread', topic=topic, tid=tid))

@app.route('/topic/<topic>/<int:tid>/delete_reply/<int:rid>')
def delete_reply(topic, tid, rid):
    if session.get("admin"):
        del forum[topic][tid]["replies"][rid]
    return redirect(url_for('view_thread', topic=topic, tid=tid))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('home'))
        return "Wrong password"
    return render_template('index.html', page="admin", forum=forum, admin=False)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)