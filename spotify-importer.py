import spotipy
from spotipy.oauth2 import SpotifyOAuth
import math
class App:

    def __init__(self):
        self.clientId = ""
        self.clientSecret = ""
        print("Version 1.0 - Spotify Importer | Paul Brennan")
        self.fetchDetails()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.clientId,
                                               client_secret=self.clientSecret,
                                               redirect_uri="https://google.com",
                                               scope="user-library-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"))
        self.readPlaylist()
        self.createPlaylistAndMerge()

    def fetchDetails(self):
        while True:
            try:
                self.playlistName = input("Please enter the name of the new playlist: ")
                self.playlistToCopyId = input("Please enter the playlist id, format: spotify:user:spotifycharts:playlist:37i9dQZEVXbJiZcmkrIHGU : ")
                return
            except Exception as e:
                print("Please ensure you are entering valid information!")

    def readPlaylist(self):
        try:
            while True:
                self.trackIds = []
                results = self.sp.playlist_tracks(self.playlistToCopyId)
                tracks = results['items']
                while results['next']:
                    results = self.sp.next(results)
                    tracks.extend(results['items'])

                for track in tracks:
                    self.trackIds.append(track['track']['uri'])
                return 

        except Exception as e:
            print("Please enter a valid playlist id, the format is:spotify:user:spotifycharts:playlist:37i9dQZEVXbJiZcmkrIHGU : ")

    def createPlaylistAndMerge(self):
        try:
            userId = self.sp.me()['id']
            playlist = self.sp.user_playlist_create(userId, self.playlistName, public=False, description="")
            playlistId = playlist['id']
            totalTracks = len(self.trackIds)
            counter = math.ceil(totalTracks / 100)

            for i in range(counter):

                lowerRange = i*100
                upperRange = (i+1)*100

                if upperRange > totalTracks:
                    upperRange = totalTracks

                self.sp.playlist_add_items(playlistId, self.trackIds[lowerRange:upperRange])
            print("Success! Imported " + str(totalTracks) + " into your spotify account.")
        except Exception as e:
            print("Sorry! Failed to communicate with spotify api, try again in a few minutes and then contact paul.")

def main():
    App()

if __name__=='__main__':
    main()

