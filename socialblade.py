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

def get_youtube_info(channel_name):
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
        contexts = {}
        for span in spans:
            if span.get("id") in spans_wanted_id:
                contexts[span.get('id')] = span.contents[0]
        print (contexts)
        return contexts
    except Exception as e:
        print(e)
        print('Couldn\'t update the channel information of {}. Please check your connection.'.format(channel_name))
        return "failed"


def get_twitter_info(username):
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), desired_capabilities=caps,  chrome_options=chrome_options)  
        url = 'https://socialblade.com/twitter/user/' + str(username)
        driver.get(url)
        html = driver.page_source
        driver.close()
        soup = BeautifulSoup(html,'html.parser')
        #print(soup)
        #print('lala\n\n\n',soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span'))
        try:
            contexts = {
                'Followers': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[2].contents[0],
                'Following': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[4].contents[0],
                'Likes': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[6].contents[0],
                'Tweets': soup.find_all('div',{'id':'YouTubeUserTopInfoBlock'})[0].find_all('span')[8].contents[0],
            }
            print(contexts)
            return contexts
        except Exception as e:
            print('Error: {}\nCouldn\'t update the twitter information of {}'.format(e,username))
            return 'failed'

