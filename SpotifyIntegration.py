import requests
from urllib.parse import quote
import re
import time
import webbrowser
import json


class Auth(object):
    creds = ''
    token = ''

    def __init__(self):  # Constructor to initialize the
        self.creds = {
            'client_id': '26c805b413e140b7ad89fee98c1e5964',
            'response_type': 'token',
            'redirect_uri': 'https://www.google.com/',
            'scope': 'playlist-read-private playlist-modify-private playlist-modify-public',
            'show_dialog': 'True'
        }

    def GetToken(self):  # First method to call from outside Class
        auth_url = 'https://accounts.spotify.com/authorize'
        uri = 'redirect_uri=' + quote(self.creds['redirect_uri'], safe='')
        scope = 'scope=' + quote(self.creds['scope'], safe='')
        url = auth_url + '?' + 'client_id=' + self.creds['client_id'] + '&' + 'response_type=' + self.creds[
            'response_type'] + '&' + uri + '&' + scope

        print("You will be redirected to Google page. Please enter the Access Token below.")
        time.sleep(2)
        print()
        webbrowser.open(url)

        token = input('Enter the Access Token : ')
        if 'access_denied' in token:
            print('Failed to Grant Access')
            return False
        self.token = token
        return token


class Setup(object):
    userid = ''
    token = ''
    tracklist = ''
    tracks = []
    playlistid = ''

    def __init__(self, access_token, TracklistName, Tracks):
        self.token = access_token
        self.tracklist = TracklistName
        self.tracks = Tracks

    def info(self):
        url = 'https://api.spotify.com/v1/me'
        response = requests.get(url, headers={'Authorization': 'Bearer ' + self.token})
        if checkresponse(response):
            print()
            print()
            print('Extracting User Info...')
            print()
            time.sleep(2)
            user_details = response.json()
            self.userid = user_details['id']
        else:
            return False
        return self.checkUserPlaylists()

    def insertTracks(self):
        # Creating a playlist
        print('Creating Playlist...')
        playlisturl = 'https://api.spotify.com/v1/users/' + self.userid + '/playlists'
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        data = {
            'name': self.tracklist,
            'public': False
        }

        response = requests.post(playlisturl, headers=headers, data=json.dumps(data))
        if checkresponse(response):
            print('Playlist Successfully Created !')
            print()
            print()
            print('Inserting Tracks')
            print('.')
            print('.')
            time.sleep(2)
            playlist_json = response.json()
            self.playlistid = playlist_json['id']

            # Searching for Tracks
            final_playlist = {}
            for track in self.tracks:
                trackmap = self.searchTracks(track)  # Main Method
                if trackmap:
                    final_playlist[trackmap[0]] = trackmap[1]

            uris = []  # Final list for Tracks to insert
            for key in final_playlist.keys():  # Forming URI's to append in payload
                uris.append('spotify:track:' + key)
            if uris:
                uri = quote(','.join(uris), safe='')
                playlist_url = 'https://api.spotify.com/v1/playlists/' + self.playlistid + '/tracks?'
                query = playlist_url + 'uris=' + uri

                response = requests.post(query, headers={'Authorization': 'Bearer ' + self.token})
                if checkresponse(response):
                    print('Playlist Successfully Updated')
                    return True
                else:
                    print("Failed to Update Playlist")
            else:
                print("No Tracks Found !")
                return False
        else:
            return False

    def searchTracks(self, name):
        # ascii_name = quote(name, safe='')  # ASCII Convert the values
        name = name.split(' - ')
        track_name = name[1]
        track_ascii = quote(name[1], safe='')
        # artist_name = name[0] For later search refining process
        # BASE URL
        url = 'https://api.spotify.com/v1/search?'
        q = 'q' + '=' + track_ascii + '&' + 'type=track'
        time.sleep(1)
        response_body = requests.get(url + q, headers={'Authorization': 'Bearer ' + self.token})
        if checkresponse(response_body):
            raw_json = response_body.json()
            tracks_json = raw_json['tracks']
            id_mapping = []
            for item in tracks_json['items']:
                if (re.sub(r'\W', '', track_name)).lower() == (re.sub(r'\W', '', item['name'])).lower():
                    print('Track Found !', item['name'])
                    id_mapping.append(item['id'])
                    id_mapping.append(item['name'])
                    break
            return id_mapping

    def checkUserPlaylists(self):
        url = 'https://api.spotify.com/v1/users/' + self.userid + '/playlists'
        response = requests.get(url, headers={'Authorization': 'Bearer ' + self.token})
        if checkresponse(response):
            raw_data = response.json()
            userslist = []
            items = raw_data['items']
            for item in items:
                userslist.append(item['name'])

            if self.tracklist in userslist:
                print('Tracklist Already Found -> ', self.tracklist)
                print('Exiting... ', self.tracklist)
                time.sleep(2)
                return False
            else:
                return self.insertTracks()
        else:
            return self.insertTracks()


def checkresponse(response):
    if response.status_code == 200 or response.status_code == 201:
        return True
    else:
        print('Exception Occurred --> ', str(response.status_code), response.reason)
        return False


def SpotifyConnector(tracklistname, tracks):
    auth = Auth()
    access_token = auth.GetToken()

    if access_token:
        user = Setup(access_token, tracklistname, tracks)
        if user.info():
            print('Transaction Complete ! :)')
            return True
        print('Transaction Failed ! :(')
        return False
    return False

#  tracks = ['Daft Punk - Crescendolls',"Eric Prydz - Slammin' (Axwell Remix)"]
#  SpotifyConnector('009 Tracks',tracks)
