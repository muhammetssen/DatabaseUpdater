def get_youtube_info(channel_name):
    import os  
    from selenium import webdriver  
    from selenium.webdriver.common.keys import Keys  
    from selenium.webdriver.chrome.options import Options  
    from bs4 import BeautifulSoup
    chrome_options = Options()  
    #chrome_options.add_argument("--headless")  
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"  
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), desired_capabilities=caps,  chrome_options=chrome_options)  
    url = "https://socialblade.com/youtube/user/"+ str(channel_name)
    print('Getting html')
    driver.get(url)
    html = driver.page_source
    driver.close()

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
            #contexts.append(span.contents[0])
            contexts[span.get('id')] = span.contents[0]
    print (contexts)
    return contexts

