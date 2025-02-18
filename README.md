# Queue

this repository hosts the source code of my spotify queue manager application at [music.prigoana.com](https://music.prigoana.com/)

## Roadmap
- Switch to actual WSGI server
- Improve front-end
- add lastfm integration
- add next/previous track and pause/resume
## Deployment
NOTE: This won't work for you if you don't have Spotify Premium.  

Download and extract the repository, open it, and replace the Spotify Client ID and Secret in ``.env`` with your own. You can generate  your own [here] (https://developer.spotify.com/dashboard/).  
  
  install requirements using  
```pip install -r requirements.txt```  
then  
``python app.py``

## Usage
Play a track or playlist on the account associated with your API key, then on the web app and add tracks to queue there.
