from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Define the Incident model
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.Text)

# Create the database tables
with app.app_context():
    db.create_all()

# Define routes
@app.route("/")
def index():
    incidents = Incident.query.all()
    return render_template("index.html", incidents=incidents)

@app.route("/report_incident", methods=["POST"])
def report_incident():
    # Get data from the form
    incident_type = request.form.get("incident_type")
    severity = request.form.get("severity")
    comments = request.form.get("comments")
    
    # Create a new incident
    new_incident = Incident(incident_type=incident_type, severity=severity, comments=comments)
    
    # Add the incident to the database
    db.session.add(new_incident)
    db.session.commit()
    
    # Emit a message to all clients for real-time updates
    socketio.emit("new_incident", {"incident": {"id": new_incident.id, "type": new_incident.incident_type, "severity": new_incident.severity, "comments": new_incident.comments}})
    
    return redirect(url_for("index"))

@app.route("/view_incidents")
def view_incidents():
    incidents = Incident.query.all()
    return render_template("view_incidents.html", incidents=incidents)

# SocketIO event handler for connecting clients
@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == "__main__":
    # Use socketio.run() instead of app.run()
    socketio.run(app, debug=True)
