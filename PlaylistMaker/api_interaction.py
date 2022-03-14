import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import json
import random
from typing import List


class API_Interaction:
    def __init__(self, number: int= 10) -> None:
        self.number = number 
        
        scopes = [
            "playlist-modify-public", 
            "user-library-read", 
            "playlist-read-private",
            "playlist-modify-private"
        ]

        with open("secrets.json", "r") as file:
            file = json.load(file) 
            client_id = file["client_id"]
            client_secret = file["client_secret"]
            self.playlist_id = file["playlist_id"]
        
        self.SPOTIFY = spotipy.Spotify(
            auth_manager= SpotifyOAuth(
                client_id= client_id,
                client_secret= client_secret,
                redirect_uri= "http://example.com/callback/",
                scope= " ".join(scopes)
            )
        )
        

    def read_user_playlist(self) -> List[str]:
        playlists = self.SPOTIFY.current_user_playlists(limit= self.number)
        playlist_ids = []

        if not playlists:
            raise RuntimeError("could not find users playlists")

        for playlist in playlists["items"]:
            id_ = playlist["id"]
            if id_ == self.playlist_id:
                continue

            playlist_ids.append(id_)
        
        return playlist_ids


    def read_playlist_content(self, id_: str) -> List[str]:
        song_ids = []

        result = self.SPOTIFY.playlist(id_)
        if not result:
            raise RuntimeError(f"could not find the playlist at id: {id_}")

        for song in result["tracks"]["items"]:
            song_id = song["track"]["id"]
            song_ids.append(song_id)

        return song_ids


    def choose_songs(self) -> List[str]:
        songs_to_add = []
        playlists = self.read_user_playlist()
        extra_songs = self.number % len(playlists)                  # number of songs that exceed playlist count

        if extra_songs > 0:
            num = (self.number - extra_songs) // len(playlists)     # songs per playlist to be added
        else:
            num = 1     # default song per playlist ratio
        
        for id_ in playlists:
            song_ids = self.read_playlist_content(id_)
            songs_to_add.extend(random.sample(song_ids, num))
        
        if extra_songs > 0:
            extras = random.sample(playlists, extra_songs)
            for id_ in extras:
                song_ids = self.read_playlist_content(id_)
                songs_to_add.extend(random.sample(song_ids, 1))
        
        return songs_to_add
    

    def empty_playlist(self) -> None:
        songs = self.read_playlist_content(self.playlist_id)
        self.SPOTIFY.playlist_remove_all_occurrences_of_items(self.playlist_id, songs)


    def add_songs_to_playlist(self) -> None:
        songs = self.choose_songs()
        self.empty_playlist()
        self.SPOTIFY.playlist_add_items(self.playlist_id, songs)  
