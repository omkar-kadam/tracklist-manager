import requests
import html
from bs4 import BeautifulSoup
from urllib.parse import quote



def searchUsingScraper(trackName):

    trackName = quote(trackName)

    if trackName:
        url = 'https://www.youtube.com/results?search_query='
        generatedURL = url+trackName
        response = requests.get(generatedURL, headers={'user-agent': 'Surfacer 1.3'})
        content = response.content
    else:
        print("URL not Generated")

        return "Failed To Generate URL"

    page = BeautifulSoup(content, 'html5lib')
    atags = page.findAll('a', attrs={'aria-hidden': ''})
    
    # Getting All Video Names and Urls
    videoLibrary = []
    cleanId = ''

    for each in range(len(atags)):
        if atags[each].get('href') != '' and atags[each].has_attr('aria-describedby') and '&list=' not in atags[each].get('href'):
            filteredTags = {} 
            if '=' in atags[each].get('href'):  # Filtering out channels from the search
                filteredTags['Name'] = atags[each].get('title')
                cleanId = atags[each].get('href')
                cleanId = cleanId.split("=")
                filteredTags['VideoUrl'] = cleanId[1]
                videoLibrary.append(filteredTags)
                
    # Checking each video name with the original string
    actualMatch = [] 
    relativeMatch = []

    for each in videoLibrary:
        if html.unescape(each['Name'].lower()) == trackName.lower():
            actualMatch.append(each['VideoUrl'])
        else:
            relativeMatch.append(each['VideoUrl'])

    if actualMatch:
        return actualMatch[0]  # return videoId from Here
    elif relativeMatch:
        return relativeMatch[0]  # return videoId from Here
    else:
        return "Video Not Found"


# ur = searchUsingScraper('Alaia & Gallo ft. Dames Brown - Trippin (P.o.L. Mix)')
# print(ur)
