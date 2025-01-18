from flask import Flask, render_template, request, redirect, url_for, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Flask app
app = Flask(__name__)

# Spotify API credentials
CLIENT_ID = "f7f2841e0c26492681499a53b4eca29f"
CLIENT_SECRET = "8e1a973438214682939b175bb9f1ed1d"
REDIRECT_URI = "http://localhost:80/callback"
SCOPE = "user-modify-playback-state user-read-playback-state"

# Spotipy client
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Home route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET"])
def add_song():
    # Get the song name from the query parameters
    song_name = request.args.get("song_name")
    if not song_name:
        return jsonify({"error": "No song name provided."}), 400

    try:
        # Search and add the song to the Spotify queue
        search_results = sp.search(q=song_name, type="track", limit=1)
        if search_results["tracks"]["items"]:
            track_uri = search_results["tracks"]["items"][0]["uri"]
            print(search_results["tracks"]["items"][0])
            sp.add_to_queue(track_uri)
            name = search_results["tracks"]["items"][0]["name"]
            return jsonify({"message": f"'{name}' has been added to the queue."}), 200
        else:
            return jsonify({"error": "No matching track found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve the queue table for iframe
@app.route("/queue_table")
def queue_table():
    queue_data = sp.queue()
    print(queue_data)
    queue = []
    if "queue" in queue_data and queue_data["queue"]:
        for track in queue_data["queue"]:
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            queue.append({"track": track_name, "artist": artist_name})
    current = None
    if queue_data["currently_playing"]:
        current = {"track":queue_data["currently_playing"]["name"], "artist":queue_data["currently_playing"]["artists"][0]["name"]}
    return render_template("queue_table.html", queue=queue, length=len(queue), now_playing=current)

# Run the Flask app
if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0", debug=True)
