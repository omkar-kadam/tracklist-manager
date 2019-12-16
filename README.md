# TracklistManager (WIP) v1.3
1. Extract Tracklist from 1001 Tracklist
- Scrape the tracklist and genrate a list of Songs.

2. Search for those Tracks on YouTube
- Search via Youtube provided API
- Search via Scraping Youtube. [This is the current implementation]

3. Create a Playlist with those Tracks
- Creates a Playlist on Youtube with the Tracklist's Name

4. Download Those Tracks ( Automate ) (WIP)

# Main Components
1. YTPlaylistGenerator.py
2. TracklistGenerator.py
3. YouTubeSearchEngine.py
4. client_secret.json - This can be obtained by registering your application on https://console.developers.google.com

NOTE : client_secret is provided in case of any application failures. 

# Limitations
A LIMIT of 10,000 API cost is applied to a registered user.
Consumption Stats are documented here : https://docs.google.com/spreadsheets/d/1TbroI1frU2IXwGCeVYYCW1At0RwgSlY-QUP9mow-IAA/edit?usp=sharing

# Improvements can be done
1. Making use of DataFrames (JSON) : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html
2. Optimization by enforcing recursion
3. Use of List Comprehension

