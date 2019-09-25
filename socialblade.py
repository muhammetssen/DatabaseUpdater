import os  
from selenium import webdriver  

from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


chrome_options = Options()  
chrome_options.add_argument("--headless")  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"  

load_time = 20

def get_youtube_info(channel_name,dictionary,index='youtube'):
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), desired_capabilities=caps,  chrome_options=chrome_options)  
    url = "https://socialblade.com/youtube/channel/"+ str(channel_name)
    wait = WebDriverWait(driver,load_time) 
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.ID,'YouTubeUserTopInfoBlockTop')))
    driver.execute_script("window.stop()")
    html = driver.page_source
    driver.quit()
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
    url = 'https://www.twitter.com/' + str(username)
    wait = WebDriverWait(driver,load_time) 
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'ProfileNav')))
    driver.execute_script("window.stop()")        
    html = driver.page_source
    driver.quit()
    try:
        soup = BeautifulSoup(html,'html.parser')
        ul_element = (soup.find_all('ul',{'class':'ProfileNav-list'})[0])
        li_wanted_class = {
           'ProfileNav-item--tweets' : 'Tweets',
            'ProfileNav-item--following':'Following_t',
            'ProfileNav-item--followers':'Followers_t',
            'ProfileNav-item--favorites' :'Likes'
        }
        data = {}
        li_elements = ul_element.find_all('li')[:-3]
        for li_element in li_elements:
            for wanted_class in li_wanted_class:
                if wanted_class in li_element['class']:
                    data[wanted_class] = (li_element.find('span',{'class':'ProfileNav-value'}))['data-count']
        twitter_contexts = {}
        for category in data.keys():
            twitter_contexts[li_wanted_class[category]] = data[category] 
        dictionary[index]= twitter_contexts
        '''
        spans = soup.find_all('span',{'class':'ProfileNav-value'})
        twitter_contexts={}
        cache=[]
        for span in spans[0:4]:
            data = span['data-count']
            if '\n' in data:
                data = str(data).split('\n')[0]
            cache.append(data)
        twitter_contexts['Tweets'] = cache[0]
        twitter_contexts['Following'] = cache[1]
        twitter_contexts['Followers'] = cache[2]
        twitter_contexts['Likes'] = cache[3]
        dictionary[index]= twitter_contexts
        '''
        print(twitter_contexts)
        return twitter_contexts
    except Exception as e:
        print('Error: {}\nCouldn\'t update the twitter information of {}'.format(e,username))
        return 'failed'

    #For Social Blade
    '''url = 'https://socialblade.com/twitter/user/' + str(username)
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
'''
def get_instagram_info(username,dictionary,index='instagram'):
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), desired_capabilities=caps,  chrome_options=chrome_options)  
    url = 'https://www.instagram.com/' + str(username)
    wait = WebDriverWait(driver,load_time) 
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'k9GMp')))
    driver.execute_script("window.stop()")
    html = driver.page_source
    driver.quit()
    try:
        soup = BeautifulSoup(html,'html.parser')
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
        print('Couldn\'t update the instagram information of {}'.format(username))
        return 'failed'
    ##Average rt and like