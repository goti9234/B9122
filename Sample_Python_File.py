from bs4 import BeautifulSoup
import urllib.request

#Initializing
url = "http://www8.gsb.columbia.edu/" # initial URL
maxNumUrl = 50 # maximum number of URLs to visit
keywords = ['finance', 'engineering', 'business', 'research']

#Step 1 - Creating Lists and Dictionaries
urls = {}
seen = {}
opened = []

#Step 2 - Adding values to the dictionary urls
urls[url] = 1

#Step 3-Creating the while loop and executing subcommands
while len(urls) > 0 and len(opened) < maxNumUrl:
    #Step 3a - Getting the URL with the largest score
    max_score_url = max(urls, key = urls.get)
    #Step 3a - Assigning it to curr_url and deleting it from urls
    curr_url = max_score_url
    del urls[max_score_url]
    #Step 3b - Adding curr_url to opened if it can be opened
    try:
        webpage = urllib.request.urlopen(curr_url)
        opened.append(curr_url)
        soup = BeautifulSoup(webpage, features = 'lxml')
        htmltext = soup.get_text().lower()
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~|+='''
        score = 0
        #Step 3d - Counting the number of keywords
        for punc in htmltext: 
            if punc in punctuations: 
                htmltext = htmltext.replace(punc, ' ') 
        htmltext = htmltext.split()
        for keyword in keywords:
            count = htmltext.count(keyword)
            score = score + count
        #Step 3e - Adding the URL and it's score to seen
        seen[curr_url] = score
        #Step 3f - Checking if score > 0, finding href tags and appending baby links to URLs
        if score > 0:
            for link in soup.find_all('a'):
                baby_link = str(link.get('href'))
                if baby_link in seen.keys():
                    continue
                else:
                    urls[baby_link] = score
    except:
        continue

#Step 4 - Printing Number of URLs seen and URLs opened
print('Number of URLs seen = ' + str(len(seen)))
print('Number of URLs opened = ' + str(len(opened)))

#Step 5 - Printing the top 25 URLs seen
seen_top_25 = dict(sorted(seen.items(), key = lambda x: x[1], reverse = True)[:25])
for key in seen_top_25:
    print (key)