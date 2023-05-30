import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

time_travel = input("What year do you want to travel to? Type the date in this format: YYYY-MM-DD ")
URL = f"https://www.billboard.com/charts/hot-100/{time_travel}"

CLIENT_ID = "your spotify client id"
CLIENT_SECRET = "your spotify client secret"

response = requests.get(URL)
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")

song_titles_data = soup.select("li ul li h3")
song_titles = [song.getText().strip() for song in song_titles_data]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://localhost:8080/",
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True
                                               ))

user_id = sp.current_user()["id"]

song_uris = []
year = time_travel.split("-")[0]

for song in song_titles:

    result = sp.search(q=f"track:{song} year:{year}", type="track")
    pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(song_uris)

playlist = sp.user_playlist_create(user=user_id,name=f"100 Billboard Tracks of {year}", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

