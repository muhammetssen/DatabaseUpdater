count = 1
import pandas
from socialblade import get_instagram_info,get_twitter_info,get_youtube_info
from time import time
import sys

is_youtube = True if "youtube" in sys.argv else False
is_twitter = True if "twitter" in sys.argv else False
is_instagram = True if "instagram" in sys.argv else False


start = time()
inf_sheet = pandas.read_excel('excel.xlsx',sheet_name='Influencers')

media_sheet = pandas.read_excel('excel.xlsx',sheet_name='Media Contact')

if inf_sheet.columns[2] != 'Influencer Name / Brand Name':
    inf_sheet = pandas.read_excel('excel.xlsx',sheet_name='Influencers',skiprows=[0])

if media_sheet.columns[2] != 'Contact Name':
    media_sheet = pandas.read_excel('excel.xlsx',sheet_name='Media Contact',skiprows=[0])
    


def save():
    header = ['General', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
       'Unnamed: 5', 'Unnamed: 6', 'TangiPlay', 'Unnamed: 8', 'Youtube',
       'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Instagram', 'Unnamed: 14',
       'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18',
       'Unnamed: 19', 'Twitter', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23',
       'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26', 'Facebook', 'Unnamed: 28']
    '''media_sheet.loc[-1] = pandas.read_excel('excel.xlsx',sheet_name='Media Contact').columns
    media_sheet.index +=1
    media_sheet.sort_index()'''

    '''inf_sheet.loc[-1] = pandas.read_excel('excel.xlsx',sheet_name='Influencers').columns
    inf_sheet.index +=1
    inf_sheet.sort_index()
    '''
    inf_sheet.style.set_properties(**{"color":"#ff0000"})
    writer = pandas.ExcelWriter('output.xlsx', engine='openpyxl')
    #inf_sheet.style.apply("background-color :yellow")  #DataFrame object
    media_sheet.to_excel(writer,sheet_name='Media Contact')
    inf_sheet.to_excel(writer,sheet_name='Influencers',index=False)
#    inf_sheet.style.set_properties(color="yellow",align="right")
 #   inf_sheet.style.apply()
#    worksheet.conditional_format('E2:E4',{'type':'3_color_scale'})
    writer.close()
    writer.save()
    return True


names = inf_sheet['Influencer Name / Brand Name']
columns =list( inf_sheet.columns)

def overwrite(sheet,dictionary,name):
    for column in columns:
        sheet.loc[sheet['Influencer Name / Brand Name']==dictionary['Influencer Name / Brand Name'],column] = [dictionary[column]]

import threading
def update_person(person):
    person_information = {}
    for column in columns:
        value = inf_sheet.loc[inf_sheet[str('Influencer Name / Brand Name')] == str(person)][str(column)].values[0]
        #print(pandas.isna(value))
        #if not pandas.isna(value):
        person_information[str(column)] = value
        #else:
         #   person_information[str(column)]='n/a'
    #inf_sheet.loc[inf_sheet['Influencer Name / Brand Name']] == str(person)

    usernames = {}
    results = {}
    
    youtube_id = person_information['Youtube Link']
    if not pandas.isna(youtube_id) and is_youtube:
        try:
            channel_name = youtube_id.split('/')[4]
            usernames['youtube'] = channel_name
            #results['youtube']=  get_youtube_info(channel_name)
        except:
            print('Invalid Youtube URL! Please check the Youtube URL of {}'.format(person))

    twitter_link = person_information['Twitter Link'] 
    if not pandas.isna(twitter_link) and is_twitter:
        try:
            words = str(twitter_link).split('/') 
            if 'twitter.com' in words:
                ind = words.index('twitter.com')
            if 'www.twitter.com' in words:
                ind = words.index('www.twitter.com')
            username = words[ind+1]
            usernames['twitter'] = username
            #results['twitter'] = get_twitter_info(username)
        except:
            print('Invalid Twitter Username! Please check the Twitter Username of {}'.format(person))
    
    instagram_link = person_information['Instagram Link']
    if not pandas.isna(instagram_link) and is_instagram:
        try:
            words = str(instagram_link).split('/')
            if 'instagram.com' in words:
                ind = words.index('instagram.com')
            if 'www.instagram.com' in words:
                ind = words.index('www.instagram.com')
            username = words[ind+1]
            usernames['instagram'] = username
            #results['instagram'] = get_instagram_info(username)
        except:
            print('Invalid Instagram Username! Please check the Instagram Username of {}'.format(person))
        
    
    threads = {}
    functions = {
        'instagram':get_instagram_info,
        'twitter':get_twitter_info,
        'youtube':get_youtube_info
    }
    for platform in usernames.keys():
        threads[platform] = threading.Thread(target=functions[platform],args=(usernames[platform],results,))
    for thread in threads.keys():
        threads[thread].start()
    for thread in threads.keys():
        threads[thread].join()
    #print(usernames)
    for platform in usernames.keys():

        if platform == 'youtube' :
            try:
                data = results[platform]
                #print('Youtube Channel Name: {}'.format(usernames['youtube']))
                #if data != 'failed':
                person_information['Uploads'] = data['youtube-stats-header-uploads']
                person_information['Subscribers'] = data['youtube-stats-header-subs']
                person_information['Video Views'] = data['youtube-stats-header-views']
            except Exception as e:
                print('Error: {}'.format(e))
        elif platform == 'twitter' :
            
            try:    
                data = results[platform]
                #print('twitter_link : {}'.format(twitter_link))
                #print('Twitter Username: {}'.format(usernames[platform]))
                #if data != 'failed':
                for key in data.keys():
                    person_information[key] = data[key]
            except Exception as e:
                print('Error: {}'.format(e))            
        elif platform =='instagram' :
            try:
                data = results[platform]
                #print('Instagram Username: {}'.format(usernames[platform]))
                #if data != 'failed':
                person_information['Media Uploads'] = data['Media Uploads']
                person_information['Followers'] = data['Followers']
                person_information['Following'] = data['Following']
            except Exception as e:
                print('Error: {}'.format(e))

        

    overwrite(inf_sheet,person_information,str(person))




person_list_lists = []
from multiprocessing import Process
for x in range(len(names)//count+1):
    for name in names[x*count:x*count+count]:
        person_list_lists.append(name)
        #temp.append(name)

for person_list in person_list_lists:
    print(person_list_lists.index(person_list),'/',len(person_list_lists),'\t',person_list)
    update_person(person_list)
    save()
    
print(time()-start)
print('count=',count)

#2 188
#4 178