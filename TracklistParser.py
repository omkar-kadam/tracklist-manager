import requests
from bs4 import BeautifulSoup


def get1001Tracklist(URL):
    r = requests.get(URL, headers={'User-agent': 'surfacer 1.3'})
    content = r.content
    page = BeautifulSoup(content, 'html5lib')
    # Extract Data
    schema = page.find('div', attrs={'class': 'mainContentDiv', 'id': 'mainContentDiv'})
    getTracklistMeta = schema.find('div', attrs={'itemtype': 'http://schema.org/MusicPlaylist'})

    # Get Tracklistmeta . FOR SCIENCE purpose
    tracklistMeta = {"Name": getTracklistMeta.find('meta', attrs={'itemprop': 'name'}).get('content'),
                     "Genre": getTracklistMeta.find('meta', attrs={'itemprop': 'genre'}).get('content'),
                     "Artist": getTracklistMeta.find('meta', attrs={'itemprop': 'author'}).get('content')}
    # Get Tracks Data
    table = schema.find('table', attrs={'class': 'default full tl hover'})
    tracksMeta = table.findAll('meta')
    tracks = []
    for each in range(len(tracksMeta)):    
        if tracksMeta[each].get('itemprop') == 'name':
           tracks.append(tracksMeta[each].get('content'))
    tracklist = {}
    name = getTracklistMeta.find('meta', attrs={'itemprop': 'name'}).get('content')
    tracklist[name] = tracks
    return name, tracklist


def getMixesDBTracklist(URL):
    r = requests.get(URL, headers={'User-agent': 'surfacer 1.3'})
    content = r.content
    page = BeautifulSoup(content, 'html5lib')
    if 'Tracklist' == (page.find('h2',{'id': 'Tracklist'}).span).text:
        tracklistName = (page.find('title').text).split(" | ")[0]

        mainDiv = page.find('div', {'id': 'mw-content-text'})
        try:
            lstLi = mainDiv.ol.findAll('li')
        except AttributeError:
            mainDiv = mainDiv.find('div', {'class': 'list'})
            lstLi = mainDiv.findAll('div', {'class': 'list-track'})

        tracks = []
        actualData = []
        for each in lstLi:
            actualData.append(each.text)
        for each in actualData:
            while '[' in each:
                if '[' in each:
                    ss = each.index('[')
                if ']' in each:
                    se = each.index(']')
                each = each[0:ss:] + each[se+1::]
            each = each.replace("'", ' ')
            each = each.replace("?", ' ')
            each = each.strip()
            tracks.append(each)
        # Cleaning Tracks
        while '' in tracks:
            tracks.remove('')
        print("\nTracks To Add : "+str(len(tracks)))
        for each in tracks:
            print(each)
        return tracklistName, tracks
    else:
        print("Invalid URL")
        return 0, 0


def tracklistCleaner(tracklistname, tracklist):  # Removing ID Tracks from 1001 Tracklist
    cleanedTracks = []
    for each in tracklist[tracklistname]:
        if '- ID' in each:
            print("Removing ID Track : ", each)
        else:
            cleanedTracks.append(each)
    cleanedTracks = list(set(cleanedTracks))  # Setting Unique Tracks
    print("\nTracks To Add : "+str(len(cleanedTracks)))  # Printing Tracks to Add
    for each in cleanedTracks:
        print(each)
    return tracklistname, cleanedTracks


def generateTracklist():
    TURL = input("Enter 1001Tracklist or MixesDB URL : ")  # Main input point
    if 'https://www.1001tracklists.com/tracklist/' in TURL: 
        print("\nFetching Tracklist.....")
        tracklistName, tracklist = get1001Tracklist(TURL)
        print("\nCleaning Tracklist.....")
        cleanedName, cleanedTracks = tracklistCleaner(tracklistName, tracklist)
        if cleanedName and cleanedTracks:
            return cleanedName, cleanedTracks
        else:
            print("Failed to Generate Tracklist.\nTry Another Tracklist")
            return generateTracklist()
    elif 'https://www.mixesdb.com/w/' in TURL:  # Addition for MixesDB website
        print("\nFetching Tracklist.....")
        tracklistName, tracklist = getMixesDBTracklist(TURL)
        if tracklistName and tracklist:
            return tracklistName, tracklist
        else:
            print("Failed to Generate Tracklist.\nTry Another Tracklist")
            return generateTracklist()
    else:
        print("Not A Valid Tracklist.\nTry Again")
        return generateTracklist()

# Tname, Tlist = generateTracklist() # Temp code for running in same class
# print(Tname,Tlist)
