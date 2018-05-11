from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# all the urls of thread pages in FChat
wwws = []
first = "http://www.ferrarichat.com/forum/ferraris/"
wwws.append(first)
for i in range(2, 21):
    www = "http://www.ferrarichat.com/forum/ferraris/index"+str(i)+".html"
    wwws.append(www)


def url_extract(www):
    """
    Extract thread URLs from main forum URLs
    :param www: main site link
    :return: all urls from classifieds forum
    """
    # import page and scrape for links
    page = requests.get(www)
    soup = BeautifulSoup(page.content, "lxml")
    # print(soup.prettify())
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    # subset of links with thread links
    links = [x for x in links if x]  # removing empty elements
    sub = "http://www.ferrarichat.com/forum/ferraris/5"
    links = [s for s in links if sub in s]  # finding only the links for thread posts

    # find list of unique post ids
    ids = []
    for i in range(0, len(links)):
        a = links[i]
        a = a[42:48]
        ids.append(a)
    ids = list(set(ids))

    # match with original list to keep a set of unique urls
    urls = []
    for i in range(0, len(ids)):
        a = [s for s in links if ids[i] in s]
        a = a[0]
        urls.append(a)

    return urls

df = []
for i in range(0, 19):  # 20 total pages in classified section
    www = wwws[i]
    x = url_extract(www)
    df.append(x)

df = [item for sublist in df for item in sublist]  # flattening all lists within the list
df = [s for s in df if 'wanted' or 'wtb' not in s]  # removing wanted ads
df = [s for s in df if 'wtb' not in s]  # removing wtb ads


def first_extract(df):
    """
    Extract the first post from each thread URL
    :param df: list of URLs
    :return: list of first posts for each df
    """
    firsts = []
    for k in range(0, len(df)):
        www1 = df[k]
        page = requests.get(www1)
        soup = BeautifulSoup(page.content, 'lxml')
        posts = soup.find_all(id=re.compile('post_message_'))  # extract just the posts from thread
        posts = str(posts)  # convert to strings
        posts = posts.split('</div>')  # splits posts
        posts = posts[0]  # picks only first post
        posts = posts.replace('<br/>', '')
        firsts.append(posts)
    return firsts
firsts = first_extract(df)

data = pd.DataFrame({'Url': df, 'First Post': firsts}, columns=['Url', 'First Post'])
###########################################################################################
# Combining url and first post, then extracting data from it




