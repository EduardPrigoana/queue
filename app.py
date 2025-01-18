from flask import Flask, render_template, request, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Flask app
app = Flask(__name__)

# Spotify API credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://0.0.0.0/callback"
SCOPE = "user-modify-playback-state user-read-playback-state"

# Spotipy client
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=False  # Disable interactive input
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

@app.route("/queue_table")
def queue_table():
    queue_data = sp.queue()
    print(queue_data)
    queue = []
    if "queue" in queue_data and queue_data["queue"]:
        for track in queue_data["queue"]:
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            artist_uri = track["artists"][0]["uri"]  # Get the Spotify URI for the artist
            artist_link = f"https://open.spotify.com/artist/{artist_uri.split(':')[-1]}"  # Construct the Spotify artist link
            track_uri = track["uri"]  # Get the Spotify URI for the track
            track_link = f"https://open.spotify.com/track/{track_uri.split(':')[-1]}"  # Construct the Spotify track link
            queue.append({
                "track": track_name,
                "artist": artist_name,
                "track_link": track_link,
                "artist_link": artist_link
            })
    current = None
    if queue_data["currently_playing"]:
        current_track = queue_data["currently_playing"]
        current = {
            "track": current_track["name"],
            "artist": current_track["artists"][0]["name"],
            "track_link": f"https://open.spotify.com/track/{current_track['uri'].split(':')[-1]}",
            "artist_link": f"https://open.spotify.com/artist/{current_track['artists'][0]['uri'].split(':')[-1]}"
        }
    return render_template("queue_table.html", queue=queue, length=len(queue), now_playing=current)


# Run the Flask app
if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0", debug=True)
