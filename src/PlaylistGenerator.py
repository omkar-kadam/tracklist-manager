import google_auth_httplib2
import html
import time
from utils.fetchmp3 import getmp3
from utils import tracklist_parser
from utils import youtube_search_engine
from utils.spotify_integration import SpotifyConnector
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build


globalTracklistName = 0
client_secret_file = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']  # Auth Scopes for Youtube


def OAuthVerification():

    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    token = flow.run_console()
    youtube = build('youtube', 'v3', credentials=token)

    return youtube  # Returning Youtube Object


# Insert Playlist
def insertPlaylist(youtube, tracklistname):

    inserted_playlist_item = youtube.playlists().insert(part="snippet,status", body={
              "snippet": {
                "title": tracklistname,
                "description": tracklistname
              },
              "status": {
                "privacyStatus": "public"
              }
            })

    details = inserted_playlist_item.execute()
    # print(details['id'])
    playlist_id = details['id']

    return playlist_id


# Search for a Video element
def searchUsingAPI(youtube, trackTitle):

        searchResult = youtube.search().list(part='snippet', q=trackTitle, type='video', maxResults=20).execute()
        videoTitles = {}

        for snippet in searchResult['items']:
            videoId = snippet['id']['videoId']
            vidTitle = snippet['snippet']['title']
            videoTitles[videoId] = html.unescape(vidTitle)

        print(videoTitles)
                
        # -----------Video Compare Logic----------------
        keys = videoTitles.keys()
        matchResults = {}

        for key in keys:
            print(videoTitles[key])
            if str(videoTitles[key]).lower() == html.unescape(trackTitle).lower():
                matchResults[key] = 1
            else:
                matchResults[key] = 0

        print(matchResults)
         
        # -----------------Actual Video Id-----------------
        relativeVideoIds = []  # Which varies based on video title
        actualVideoIds = []  # List of videos which are exact match with the title
        matchResultsKeys = matchResults.keys()

        for eachKey in matchResultsKeys:
            if int(matchResults[eachKey]) == 1:
                actualVideoIds.append(eachKey)
            else:
                relativeVideoIds.append(eachKey)

        print("Relative Videos", relativeVideoIds)
        print("Actual Videos", actualVideoIds)
        
        # -----------------Adding Videos to Playlist------------
        if actualVideoIds:
            actualVideoId = actualVideoIds[0]
            print("Getting Actual Video", actualVideoId)
            return actualVideoId
        elif relativeVideoIds:
            actualVideoId = relativeVideoIds[0]
            print("Getting Relative Video", actualVideoId)
            return actualVideoId
        else:
            return "Video Not Found"


def insertTracks(youtube, playlistId, cleanedTracks):  # youtube object is required only for Searching via API

    print("Creating your Youtube Playlist. It may take a while....")
    playListData = {}

    for trackTitle in cleanedTracks:
        time.sleep(3) # To avoid hitting limits

        """
        Search using---------------------- Youtube API
        actualVideoId = searchUsingAPI(youtube,trackTitle)
        """
        
        # Search Using---------------------- Youtube Crawler
        actualVideoId = youtube_search_engine.searchUsingScraper(trackTitle)

        if actualVideoId == "Video Not Found":
            print(actualVideoId)
        elif actualVideoId == "Failed To Generate URL":
            print(actualVideoId)
        else:
            print("Inserting : ", trackTitle)
            playListData[actualVideoId] = trackTitle
            insertPlaylistItem(playlistId, actualVideoId)

    return playListData


def insertPlaylistItem(playlistId, actualVideoId):

    youtube.playlistItems().insert(part='snippet', body={
      "snippet": {
        "playlistId": playlistId,
        "resourceId": {
          "kind": "youtube#video",
          "videoId": actualVideoId
        }
      }
    }).execute()



if __name__ == '__main__':
    
    flg = True
    
    while flg:

        tracklistCleanedName, cleanedTracks = tracklist_parser.generateTracklist()

        print()
        service = int(input('Please select Service to save Tracks: 1.Youtube 2.Spotify ? [1 or 2]: '))

        if service == 1:
            youtube = OAuthVerification()
            playlistId = insertPlaylist(youtube, tracklistCleanedName)
            playListData = insertTracks(youtube, playlistId, cleanedTracks)

            prompt = str(input("Do You Want to Download the Tracks Locally ? [Yes/No]: ")).lower()

            if prompt == 'yes' or prompt == 'y' and playListData:
                getmp3(playListData)
                print("Tracks Downloaded")
            elif not playListData:
                print("PlayList is empty")
            else:
                print("Tracks Successfully Added on Youtube")

        elif service == 2:
            if SpotifyConnector(tracklistCleanedName, cleanedTracks):  # Returns a Boolean
                print("Successfully created a Spotify Playlist")
            else:
                print("An Error Occurred while creating a Spotify Playlist")

        print()
        end_choice = input('Do you want to add tracks again !? [Yes/No]')

        if end_choice.lower() == 'yes':
            flg = True
        else:
            flg = False
