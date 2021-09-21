import datetime
import requests
import time
import re
# INITIAL DATA SCRAPE FROM REDDIT'S ".json" SITE
def request_scrape(URL, WEB = None):
    if WEB == None:
        #FIRST PAGE JUST LOAD THE DATA
        FIRST_DATA = requests.get(URL, headers = {'user-agent': 'Mozilla/5.0'})
        
        return FIRST_DATA
    else:
        #CONTROL NAVIGATION THEREAFTER
        NEXT_SITE = URL +'?&after='+ WEB.json()['data']['after']
        NEXT_DATA = requests.get(NEXT_SITE, headers = {'user-agent': 'Mozilla/5.0'})
        
        return NEXT_DATA


    
# FIND THE TOTAL LENGTH OF THE SUBREDDIT'S '.json' SITE, THESE ARE USUALLY A MAXIMUM OF 39-40 PAGES
# 'PAGE_COUNT' IS AN ARBITRATY NUMBER, THE POINT HERE IS TO FIND PRINT THE MAX PAGE COUNT TO SCREEN
# CREATES A DICTIONARY WITH THE APPROPRIATE NUMBER OF COMMENT PAGES FOR EACH INDIVIDUAL SUBREDDIT
def find_subreddit_json_page_count(SITE_LIST, PAGE_COUNT = 999):
    # DICTIONARY WHERE EACH INDIVIDUAL SUBREDDIT'S MAX PAGE IS RECORDED
    SUBREDDIT_SCRAPE_DICT = {}
    for SITE in SITE_LIST:
        # DECLARATIONS
        COUNTER = 0
        URL_LIST = []
        URL = 'https://www.reddit.com/r/{}/new/.json'.format(SITE)
        # PROGRESS UPDATE, PRINTED TO SCREEN
        print('Getting page count from \'https://www.reddit.com/r/{}/new/.json\''.format(SITE))
        # SCRAPE FIRST PAGE, JUST PASS THE 'URL' TO MY FUNCTION
        RAW_DATA = request_scrape(URL)
        try:
            # SCRAPE POST URLS FROM MAIN PAGE
            while COUNTER <= PAGE_COUNT:
                print('/r/{} pages: {}                                                          '.format(SITE,\
                     COUNTER), end = '\r')
                if COUNTER < 1:
                    # SPECIFY THE BRANCH OF THE .json TREE FOR THE DATA I NEED
                    SUBREDDITS_POST_DATA = RAW_DATA.json()['data']['children']
                    # GET URL FOR POST
                    [URL_LIST.append('https://www.reddit.com{}'.format(SUBREDDITS_POST_DATA[JSON]['data']['permalink']))\
                     for JSON in range(len(SUBREDDITS_POST_DATA)) if '/r/{}/comments/'.format(SITE) in str(\
                     SUBREDDITS_POST_DATA[JSON]['data']['permalink'].lower())]
                else:
                    # SCRAPE PAGES THEREAFTER, PASS THE 'URL', AND THE PREVIOUS '.json' PAGE TO GET NAVIGATION LINK
                    RAW_DATA = request_scrape(URL, RAW_DATA)
                    # SPECIFY THE BRANCH OF THE .json TREE FOR THE DATA I NEED
                    SUBREDDITS_POST_DATA = RAW_DATA.json()['data']['children']
                    # GET URL FOR POST
                    [URL_LIST.append('https://www.reddit.com{}'.format(SUBREDDITS_POST_DATA[JSON]['data']['permalink']))\
                     for JSON in range(len(SUBREDDITS_POST_DATA)) if '/r/{}/comments/'.format(SITE) in str(\
                     SUBREDDITS_POST_DATA[JSON]['data']['permalink'].lower())]
                    # DISPLAY THE "MAX" RANGE OF PAGES FOR THAT PARTICULAR SUBREDDIT, MOST ABOVE 30
                COUNTER += 1
        except:
            print('Logging...                                                                ', end = '\r')
            time.sleep(1)
            # LOGS THE NAME OF THE SUBREDDIT AND HOW MANY PAGES OF COMMENTS BEFORE FAILURE
            # NOTICE 'COUNTER - 1' TO KEEP THE PAGE TOTAL WITHIN BOUNDS
            SUBREDDIT_SCRAPE_DICT[SITE] = COUNTER - 1
    
    return SUBREDDIT_SCRAPE_DICT



# USES THE CREATED DICTIONARY TO SCRAPE REDDIT POSTS FOR THEIR COMMENTS
def find_subreddit_comments(SESSION_PATH, TXT_PATH, SCRAPE_DICT, DATE):
    # USE PRE-DEFINED SUBREDDIT NAMES AND PAGES OF DIFFERENT POSTS
    for SITE, PAGE_COUNT in SCRAPE_DICT.items():
        # DECLARATIONS
        COUNTER = 0
        URL_LIST = []
        COMMENT_SCRAPE_DICT = {}
        URL = 'https://www.reddit.com/r/{}/new/.json'.format(SITE)
        try:
            # SCRAPE POST URLS FROM MAIN PAGE
            while COUNTER <= PAGE_COUNT:
                # PROGRESS UPDATE, PRINTED TO SCREEN
                print('Scraping /r/{} [Completed: {:02.0f}%]                                    '.format(SITE, round(\
                     (COUNTER / PAGE_COUNT) * 100, 2)), end = '\r')
                if COUNTER < 1:
                    # SCRAPE FIRST PAGE, JUST PASS THE 'URL' TO MY 'request_scrape' FUNCTION
                    RAW_DATA = request_scrape(URL)
                    # SPECIFY THE BRANCH OF THE .json TREE FOR THE DATA I NEED
                    SUBREDDITS_POST_DATA = RAW_DATA.json()['data']['children']
                    # GET URL FOR POST
                    [URL_LIST.append('https://www.reddit.com{}'.format(SUBREDDITS_POST_DATA[JSON]['data']['permalink'].lower()))\
                     for JSON in range(len(SUBREDDITS_POST_DATA)) if '/r/{}/comments/'.format(SITE) in str(\
                     SUBREDDITS_POST_DATA[JSON]['data']['permalink'].lower())]
                else:
                    # SCRAPE PAGES THEREAFTER, PASS THE 'URL', AND THE PREVIOUS '.json' PAGE TO GET NAVIGATION LINK
                    RAW_DATA = request_scrape(URL, RAW_DATA)
                    # SPECIFY THE BRANCH OF THE .json TREE FOR THE DATA I NEED
                    SUBREDDITS_POST_DATA = RAW_DATA.json()['data']['children']
                    # GET URL FOR POST
                    [URL_LIST.append('https://www.reddit.com{}'.format(SUBREDDITS_POST_DATA[JSON]['data']['permalink'].lower()))\
                     for JSON in range(len(SUBREDDITS_POST_DATA)) if '/r/{}/comments/'.format(SITE) in str(\
                     SUBREDDITS_POST_DATA[JSON]['data']['permalink'].lower())]
                COUNTER += 1
            # SCRAPE POSTS FOR TEXT
            for URL_LINK in range(len(URL_LIST)):
                print('Logging text [Completed: {:02.0f}%]                                    '.format(round(\
                     (URL_LINK / len(URL_LIST)) * 100, 2)), end = '\r')
                # GET THE CONTENTS OF EACH URL
                COMMENT_DATA = requests.get('{}.json'.format(URL_LIST[URL_LINK]), headers = {'user-agent': 'Mozilla/5.0'})
                # USE RegEx (re) TO SCRAPE .json WEBSITE CONTENTS FOR THE COMMENTS
                # SAVE THE POST URL TO A DICTCIONARY KEY, THE COMMENTS TO THE VALUE
                COMMENT_SCRAPE_DICT[URL_LIST[URL_LINK]] = '{} {}'.format('||'.join([TEXT.replace('\\n', ' ').replace('\t', ' ')\
                                                        .replace('\r', ' ').replace('\"','').replace('\'','').strip() for TEXT in\
                                                        re.findall('(?<=selftext[\'\"]: )[\'\"].*?[\'\"](?=, [\'\"]user_reports)',\
                                                        str(COMMENT_DATA.json()))]),'||'.join([TEXT.replace('\\n', ' ')\
                                                        .replace('\t', ' ').replace('\r', ' ').replace('\"','').replace('\'','')\
                                                        .strip() for TEXT in re.findall('(?<=body[\'\"]: )[\'\"].*?[\'\"](?=, [\'\"]edited)',\
                                                        str(COMMENT_DATA.json()))]))
            print('                                                                             ')
            # SAVE THE 'COMMENT_URL' AND 'COMMENTS' OF THAT DICTIONARY TO A TEXT FILE LOCALLY TO PROCESS LATER
            # MAKING THE SUBREDDIT NAME '.lower()' TO KEEP LISTS AND EXCEL NAMING EASIER LATER
            with open('{}{}_{}.txt'.format(TXT_PATH, SITE.lower(), DATE), 'a', encoding='utf-8') as WRITE_FILE:
                [print('{}|||{}'.format(COMMENT_URL, COMMENTS), file = WRITE_FILE) for COMMENT_URL, COMMENTS in COMMENT_SCRAPE_DICT.items()]
        except:
            # THIS IS SO THE ENTIRE PROCESS IS NOT DE-RAILED WHEN LEFT RUNNING
            with open('{}ERROR_LOG.txt'.format(SESSION_PATH), 'a', encoding = 'utf-8') as ERROR_LOG:
                print('{} - Error on {} at page #{} pulling text from website.'.format(datetime.datetime.now(), SITE,\
                      COUNTER), file = ERROR_LOG)