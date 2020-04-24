import requests
import time
from tqdm import tqdm_notebook as tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



def getUsingRequests(url, fileName):

    chunk_size = 256 # chunk_size divides the response data into given number of bytes
    r = requests.get(url,stream = True)

    with open(fileName, 'wb') as f:

        try:
            print("Track :", fileName)
            print('File Size :' + str(int(r.headers['Content-Length'])/1048576) + 'MB')

            for chunk in tqdm(r.iter_content(chunk_size = chunk_size)): # iter_content iterates over data in given chunks size to avoid clogging up the memory space of the system
                f.write(chunk)

            print("Track Downloaded :", fileName)
            time.sleep(5)

        except Exception as e:
            print(e)
            
            
def getURL(fileName):

    # Selenium Code to Initiate the traversal of webpage
    options = Options()
    options.add_argument('--headless')  # To Start Chrome without opening
    driver = webdriver.Chrome(options=options)

    driver.get('https://myfreemp3c.com/')
    in_div = driver.find_element_by_id('query')
    in_div.send_keys(fileName,Keys.ENTER)  # Here it returns the result to driver, you need to process on driver

    result = driver.find_element_by_id('result')  # Here find the traversed page element with it's id and store the result

    time.sleep(1)  # To Load the DOM in memory
    inner_html = driver.execute_script("return arguments[0].innerHTML;", result)
    # print(inner_html)
    
    soup = BeautifulSoup(inner_html,'html5lib')
    lst_div = soup.find('div', {'class':'list-group'})
    lst_a = soup.findAll('a', {'rel':'nofollow'})
    
    set_url = ''
    refs = []

    for each in lst_a:
        refs.append(str(each['href']))  # Getting all links in a List

    for each in refs:
        if fileName in each:
            href = each.split()

            for dw_url in href:
                if "https://d." in dw_url:
                    set_url = dw_url
                    break

            if set_url:
                break

    if not set_url and refs:
        rel_url = refs[0].split('/')
        rel_url[2] = rel_url[2].replace('d','s')
        rel_url.insert(3,'stream')
        rel_url = "/".join(rel_url)

        return rel_url

    if not '/stream/' in set_url and set_url:
        set_url = set_url.split('/')
        set_url[2] = set_url[2].replace('d','s')
        set_url.insert(3,'stream')
        set_url = "/".join(set_url)
        return set_url

    return set_url


def getmp3(playlist):

    keys = playlist.keys()

    for key in keys:
        fileName = playlist[key]

        try:
            url = getURL(fileName)
            if url:
                getUsingRequests(url, fileName+'.mp3')
            else:
                print("Error Parsing URL")

        except Exception as e:
            print(e)

    return

