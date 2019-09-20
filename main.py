import pandas
inf_sheet = pandas.read_excel('excel.xlsx',sheet_name='Influencers')
media_sheet = pandas.read_excel('excel.xlsx',sheet_name='Media Contacts')

if inf_sheet.columns[0] != 'Influencer Name':
    inf_sheet = pandas.read_excel('excel.xlsx',sheet_name='Influencers',skiprows=[0])

if media_sheet.columns[0] != 'Contact Name':
    media_sheet = pandas.read_excel('excel.xlsx',sheet_name='Media Contacts',skiprows=[0])
    


def save():
    header = ['General', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
       'Unnamed: 5', 'Unnamed: 6', 'TangiPlay', 'Unnamed: 8', 'Youtube',
       'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Instagram', 'Unnamed: 14',
       'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18',
       'Unnamed: 19', 'Twitter', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23',
       'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26', 'Facebook', 'Unnamed: 28']
    '''media_sheet.loc[-1] = pandas.read_excel('excel.xlsx',sheet_name='Media Contacts').columns
    media_sheet.index +=1
    media_sheet.sort_index()'''

    '''inf_sheet.loc[-1] = pandas.read_excel('excel.xlsx',sheet_name='Influencers').columns
    inf_sheet.index +=1
    inf_sheet.sort_index()
    '''
    writer = pandas.ExcelWriter('output.xlsx', engine='xlsxwriter')
    media_sheet.to_excel(writer,sheet_name='Media Contact')
    inf_sheet.to_excel(writer,sheet_name='Influencers')
    writer.save()
    return True


names = inf_sheet['Influencer Name']
columns =list( inf_sheet.columns)

def overwrite(sheet,dictionary,name):
    for column in columns:
        sheet.loc[sheet['Influencer Name']==dictionary['Influencer Name'],column] = [dictionary[column]]


for person in names: # Main Loop
    person_information = {}
    for column in columns:
        value = inf_sheet.loc[inf_sheet[str('Influencer Name')] == str(person)][str(column)].values[0]
        #print(pandas.isna(value))
        #if not pandas.isna(value):
        person_information[str(column)] = value
        #else:
         #   person_information[str(column)]='n/a'
    #inf_sheet.loc[inf_sheet['Influencer Name']] == str(person)


    youtube_id = person_information['Youtube Link']
    if not pandas.isna(youtube_id):
        try:
            from socialblade import get_youtube_info
            channel_name = youtube_id.split('/')[4]
            print('Youtube Channel Name: {}'.format(channel_name))
            data = get_youtube_info(channel_name)
            if data != 'failed':
                person_information['Uploads'] = data['youtube-stats-header-uploads']
                person_information['Subscribers'] = data['youtube-stats-header-subs']
                person_information['Video Views'] = data['youtube-stats-header-views']
        except Exception as e:
            print('Error: {}'.format(e))
    
    twitter_link = person_information['Twitter Link']
    if not pandas.isna(twitter_link):
        try:    
            #print('twitter_link : {}'.format(twitter_link))
            words = str(twitter_link).split('/') 
            if 'twitter.com' in words:
                ind = words.index('twitter.com')
            if 'www.twitter.com' in words:
                ind = words.index('www.twitter.com')
            username = words[ind+1]
            print('Twitter Username: {}'.format(username))
            from socialblade import get_twitter_info
            data = get_twitter_info(username)
            if data != 'failed':
                index = columns.index('Twitter Link')
                person_information[columns[index+1]] = data['Followers']
                person_information[columns[index+2]] = data['Following']
                person_information[columns[index+3]]= data['Likes']
                person_information[columns[index+4]]= data['Tweets']
        except Exception as e:
            print('Error: {}'.format(e))            

    instagram_link = person_information['Instagram Link']
    if not pandas.isna(instagram_link):
        try:
            words = str(instagram_link).split('/')
            if 'instagram.com' in words:
                ind = words.index('instagram.com')
            if 'www.instagram.com' in words:
                ind = words.index('www.instagram.com')
            username = words[ind+1]
            print('Instagram Username: {}'.format(username))
            from socialblade import get_instagram_info
            data = get_instagram_info(username)
            if data != 'failed':
                person_information['Media Uploads'] = data['Media Uploads']
                person_information['Followers'] = data['Followers']
                person_information['Following'] = data['Following']
        except Exception as e:
            print('Error: {}'.format(e))
    
    #print(person_information)
    
    overwrite(inf_sheet,person_information,str(person))

save()