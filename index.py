import execjs
import spotipy
import time

from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth

# Load the JavaScript file
with open('script.js', 'r') as file:
    js_code = file.read()

# Create a runtime context with the loaded JavaScript code
context = execjs.compile(js_code)

# Execute JavaScript code
context.call("main")

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'ajofwiajfdovjoiajfknbvoajfiojaWDFP'
TOKEN_INFO = 'token_info'

# Set your Spotify API credentials
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
#REDIRECT_URI = 'https://open.spotify.com'
#USERNAME = 'Blahhh'

@app.route('/')
def login():
  auth_url = create_spotify_oauth().get_authorize_url()
  return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
  session.clear()
  code = request.args.get('code')
  token_info = create_spotify_oauth().get_access_token(code)
  session[TOKEN_INFO] = token_info
  return redirect(url_for('friendsPlaylist', external = True))

@app.route('/friendsPlaylist')
def friendsPlaylist():
  try:
    token_info = get_token()
  except:
    print("User not logged in")
    return redirect('/')
  
  sp = spotipy.Spotify(auth=token_info['access_token'])
  # Read song URIs from a text file
  with open('uris.txt', 'r') as file:
      song_uris = [line.strip() for line in file]


  current_user_id = sp.me()['id']
  # Create a new private playlist
  playlist = sp.user_playlist_create(user= current_user_id, name='Blitz', public=False)

  # Add songs to the playlist
  sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
  return("SUCCESS!!!")
  
def get_token():
  token_info = session.get(TOKEN_INFO, None)
  if not token_info:
    redirect(url_for('login', external = False))
    
  now = int(time.time())
    
  is_expired = token_info['expires_at'] - now < 60
  if(is_expired):
    spotify_oauth = create_spotify_oauth()
    token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
  return token_info

def create_spotify_oauth():
  return SpotifyOAuth(
    client_id= CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    redirect_uri=url_for('redirect_page', _external = True), 
    scope= 'user-library-read playlist-modify-public playlist-modify-private'
    )

app.run(debug=True)

