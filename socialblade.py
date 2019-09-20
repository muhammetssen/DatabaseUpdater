import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

from bs4 import BeautifulSoup
chrome_options = Options()  
chrome_options.add_argument("--headless")  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal"  


def get_youtube_info(channel_name,dictionary,index='youtube'):
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), desired_capabilities=caps,  chrome_options=chrome_options)  
    url = "https://socialblade.com/youtube/channel/"+ str(channel_name)
    driver.get(url)
    html = driver.page_source
    driver.close()
    try:
        soup = BeautifulSoup(html,"html.parser")
        div_block = soup.find_all("div",{"id":"YouTubeUserTopInfoBlockTop"})
        spans = div_block[0].find_all("span")
        spans_wanted_id = [
            "youtube-stats-header-uploads",
            "youtube-stats-header-subs",
            "youtube-stats-header-views"    ]
        youtube_contexts = {}
        for span in spans:
            if span.get("id") in spans_wanted_id:
                youtube_contexts[span.get('id')] = span.contents[0]
        print (youtube_contexts)
        dictionary[index] = youtube_contexts
        return youtube_contexts
    except Exception as e:
        print(e)
        print('Couldn\'t update the channel information of {}. Please check your connection.'.format(channel_name))
        return "failed"


def get_twitter_info(username,dictionary,index='twitter'):
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), desired_capabilities=caps,  chrome_options=chrome_options)  
    url = 'https://socialblade.com/twitter/user/' + str(username)
    driver.get(url)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html,'html.parser')
    #print(soup)
    #print('lala\n\n\n',soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span'))
    try:
        twitter_contexts = {
            'Followers': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[2].contents[0],
            'Following': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[4].contents[0],
            'Likes': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[6].contents[0],
            'Tweets': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[8].contents[0],
        }
        dictionary[index] = twitter_contexts
        print(twitter_contexts)
        return twitter_contexts
    except Exception as e:
        print('Error: {}\nCouldn\'t update the twitter information of {}'.format(e,username))
        return 'failed'

def get_instagram_info(username,dictionary,index='instagram'):
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), desired_capabilities=caps,  chrome_options=chrome_options)  
    url = 'https://www.instagram.com/' + str(username)
    driver.get(url)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html,'html.parser')
    try:
        lis = soup.find_all('li',{'class':'Y8-fY'})
        instagram_contexts = {
            'Media Uploads' : lis[0].contents[0].contents[0].contents[0],
            'Followers' : lis[1].contents[0].contents[0].contents[0],
            'Following' : lis[2].contents[0].contents[0].contents[0],
        }
        print(instagram_contexts)
        dictionary[index] = instagram_contexts
        return instagram_contexts
    except Exception as e:
        print('Error: {}'.format(e))
        print('Couldn\'t update the instagram information of{}'.format(username))
        return
    ###Get data from twitter instead of socialblade
    ##Average rt and like