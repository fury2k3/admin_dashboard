from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://aziz:Ug5QGHollyLoraMt@cluster0.awwuqab.mongodb.net/event_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.event_db  # Replace with your actual database name
events_collection = db.events  # Replace with your actual collection name

# List to store messages
messages = []

@app.route('/')
def index():
    # Fetch events from the database
    events = list(events_collection.find({}))  # Fetch all events
    total_events = events_collection.count_documents({})
    total_participants = sum(event.get('participants', 0) for event in events)
    total_revenue = sum(event.get('revenue', 0) for event in events)

    # Render the main dashboard template with messages and events
    return render_template('index.html',
                           total_events=total_events,
                           total_participants=total_participants,
                           total_revenue=total_revenue,
                           events=events,
                           current_year=2024,
                           messages=messages)

@app.route('/sendmessage', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    # Append the received message to the messages list
    messages.append(data)  # Storing message in memory
    return jsonify({"status": "success", "data": data})

@app.route('/get_support_messages', methods=['GET'])
def get_support_messages():
    return jsonify(messages)



if __name__ == '__main__':
    app.run(debug=True)
