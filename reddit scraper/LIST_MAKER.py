from SCRAPE import request_scrape
from UTILITY import loading_timer
from TEXT_LOG import wordcrunch_word_total_list_sorter
import time
import requests
import os
import re

# LIST OF SUBREDDITS FOR 'NEW' SCRAPE
def subreddit_scrape_list_maker():
    loading_timer(5)
    # DECLARING THE NAMES OF THE LISTS TO PASS THE 'if' STATEMENTS AT THE BEGINNING OF THE 'while' LOOP
    DIRECTORY_TEMP_LIST = ''
    USER_INPUT_TEMP_LIST = ''
    INPUT_FLAG = False
    while INPUT_FLAG == False:
        USER_READY_FLAG = False
        if len(DIRECTORY_TEMP_LIST) > 0:
            if DIRECTORY_TEMP_LIST[0].lower() in ['q', 'quit']:
                CONTINUE = 'Quit'
                
                return DIRECTORY_TEMP_LIST, CONTINUE
            else:
                print('Your subReddit Wordcrunch scrape list:\n')
                [print('| {} |'.format(SUBREDDIT_TITLE), end = '') for SUBREDDIT_TITLE in DIRECTORY_TEMP_LIST]
                print('')
                loading_timer(5)
                while USER_READY_FLAG == False:
                    USER_READY = input('Are you ready to begin scraping?\n[Yes/No]:\n')
                    if USER_READY.lower() in ['y', 'yea', 'yep', 'yes']:
                        # FUNCTION EXIT
                        INPUT_FLAG = True
                        USER_READY_FLAG = True
                        CONTINUE = 'Yes'

                        return DIRECTORY_TEMP_LIST, CONTINUE
                    elif USER_READY.lower() in ['n', 'no', 'nop', 'nope']:
                        DIRECTORY_TEMP_LIST = ''
                        USER_INPUT_TEMP_LIST = ''
                        USER_READY_FLAG = True
                        pass
                    else:
                        print('Please enter either \'Yes\' or \'No\'.')
                        loading_timer(3)
        if len(USER_INPUT_TEMP_LIST) > 0:
            if USER_INPUT_TEMP_LIST[0].lower() in ['q', 'quit']:
                CONTINUE = 'Quit'
                
                return USER_INPUT_TEMP_LIST, CONTINUE
            else:
                print('Your subReddit Wordcrunch scrape list:\n')
                [print('| {} |'.format(SUBREDDIT_TITLE), end = '') for SUBREDDIT_TITLE in USER_INPUT_TEMP_LIST]
                print('')
                loading_timer(5)
                while USER_READY_FLAG == False:
                    USER_READY = input('Are you ready to begin scraping?\n[Yes/No]:\n')
                    if USER_READY.lower() in ['y', 'yea', 'yep', 'yes']:
                        # FUNCTION EXIT
                        INPUT_FLAG = True
                        USER_READY_FLAG = True
                        CONTINUE = 'Yes'

                        return USER_INPUT_TEMP_LIST, CONTINUE
                    elif USER_READY.lower() in ['n', 'no', 'nop', 'nope']:
                        DIRECTORY_TEMP_LIST = ''
                        USER_INPUT_TEMP_LIST = ''
                        USER_READY_FLAG = True
                        pass
                    else:
                        print('Please enter either \'Yes\' or \'No\'.')
                        loading_timer(3)
        LIST_CHOICE = input('Please input if you would like to \'Browse\' a subReddit directory, or \'Enter\' your own\
 list:\n[Browse/Enter/Quit]\n')
        if LIST_CHOICE.lower() in ['b', 'browse']:
            DIRECTORY_INPUT = 'False Flag'
            DIRECTORY_TEMP_LIST = []
            SUBDIRECTORIES_JSON = requests.get(r'https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits.json',\
                                               headers = {'user-agent': 'Mozilla/5.0'})
            LIST_OF_SUBREDDITS = [SUBREDDIT for SUBREDDIT in re.findall('(?<=/r/)\w*', SUBDIRECTORIES_JSON.json()['data']['content_md'])\
                                  if SUBREDDIT != 'ListOfSubreddits']
            loading_timer(6)
            [print('| {} |'.format(SUBREDDIT_TITLE),  end = '') for SUBREDDIT_TITLE in LIST_OF_SUBREDDITS]
            print('')
            time.sleep(2)
            print('WARNING! A scrape of a large raw-text file from a popular subReddit can take multiple hours. Depending on\
 the speed of your computer, it is advised to only scrape one (1) subReddit at a time.\n')
            loading_timer(10)
            print('Please enter the name(s) of each subReddit you would like to Wordcrunch, one at a time.\nBe sure to check\
 for spelling to ensure proper functionality.\nEnter\'Quit\' when finished.')
            while not DIRECTORY_INPUT.lower() in ['q', 'quit']:
                DIRECTORY_INPUT = input('[subReddit Title/Quit]\n')
                try:
                    URL = 'https://www.reddit.com/r/{}/new/.json'.format(DIRECTORY_INPUT.lower())
                    RAW_DATA = request_scrape(URL)
                    RAW_DATA.json()['error']
                    print('ERROR: \'{}\' is incorrect.\nPlease check subReddit listing.'.format(URL))
                except:
                    if DIRECTORY_INPUT.lower() in ['q', 'quit']:
                        DIRECTORY_TEMP_LIST.append(DIRECTORY_INPUT)
                        pass
                    elif not any(DIRECTORY_INPUT.lower() in ELEMENT for ELEMENT in DIRECTORY_TEMP_LIST):
                        DIRECTORY_TEMP_LIST.append(DIRECTORY_INPUT.lower())
                        print('Added: /r/{}'.format(DIRECTORY_INPUT.lower()))
                    else:
                        print('Already added /r/{}'.format(DIRECTORY_INPUT.lower()))
            DIRECTORY_TEMP_LIST = DIRECTORY_TEMP_LIST[:len(DIRECTORY_TEMP_LIST) - 1]
        elif LIST_CHOICE.lower() in ['e', 'enter']:
            USER_INPUT = 'False Flag'
            USER_INPUT_TEMP_LIST = []
            time.sleep(2)
            print('WARNING! A scrape of a large raw-text file from a popular subReddit can take multiple hours. Depending on\
 the speed of your computer, it is advised to only scrape one (1) subReddit at a time.\n')
            loading_timer(10)
            print('Please enter the name(s) of each subReddit you would like to Wordcrunch, one at a time.\nBe sure to check\
 for spelling to ensure proper functionality.\nEnter\'Quit\' when finished.')
            while not USER_INPUT.lower() in ['q', 'quit']:
                USER_INPUT = input('[subReddit Title/Quit]\n')
                try:
                    URL = 'https://www.reddit.com/r/{}/new/.json'.format(USER_INPUT.lower())
                    RAW_DATA = request_scrape(URL)
                    RAW_DATA.json()['error']
                    print('ERROR: \'{}\' is incorrect.\nPlease check subReddit listing.'.format(URL))
                except:
                    if USER_INPUT.lower() in ['q', 'quit']:
                        USER_INPUT_TEMP_LIST.append(USER_INPUT)
                        pass
                    elif not any(USER_INPUT.lower() in ELEMENT for ELEMENT in USER_INPUT_TEMP_LIST):
                        USER_INPUT_TEMP_LIST.append(USER_INPUT.lower())
                        print('Added: /r/{}'.format(USER_INPUT.lower()))
                    else:
                        print('Already added /r/{}'.format(USER_INPUT.lower()))
            USER_INPUT_TEMP_LIST = USER_INPUT_TEMP_LIST[:len(USER_INPUT_TEMP_LIST) - 1]
        elif LIST_CHOICE.lower() in ['q', 'quit']:
            # FUNCTION EXIT
            CONTINUE = 'Quit'
            INPUT_FLAG = True
            
            return None, CONTINUE
        else:
            print('Please enter either \'Browse\' or \'Enter\'.')
            loading_timer(3)




def subreddit_load_list_maker(SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, LOAD_DATE):
    USER_FILE_LIST = ''
    LOAD_FLAG = False
    # READS TEXT FILE TO GET A TEXT DUMP TO BUILD A COMPARISON DICTIONARY
    with open('{}subReddit_Word_Count_Total.txt'.format(SESSION_PATH), 'r', encoding = 'utf-8') as WORD_COUNT_FILE:
        RAW_TEXT_DUMP = WORD_COUNT_FILE.read()
    RAW_TEXT_LIST = RAW_TEXT_DUMP.replace('\'', '').replace('{', '').replace('}', '').split(',')
    # DECLARE AND POPULATE COMPARISON DICTIONARY
    SUBREDDIT_WORD_COUNT_DICT = {}
    for ELEMENT in RAW_TEXT_LIST:
        SUBREDDIT_WORD_COUNT_DICT[ELEMENT.split(':')[0].strip()] = int(ELEMENT.split(':')[1].strip())

    TEMP_LIST = wordcrunch_word_total_list_sorter(SUBREDDIT_WORD_COUNT_DICT)
    # DELETE DICTIONARY IN ORDER TO RE-ORGANIZE FILES IN DESCENDING ORDER
    SUBREDDIT_WORD_COUNT_DICT = {}
    for FILE in TEMP_LIST:
        SUBREDDIT_WORD_COUNT_DICT[FILE.split()[0].strip()] = FILE.split()[1].strip()
    while LOAD_FLAG == False:
        USER_READY_FLAG = False
        if len(USER_FILE_LIST) > 0:
            print('Your selected Wordcrunch load list is:\n')
            [print('| {} |'.format(SUBREDDIT_TITLE), end = '') for SUBREDDIT_TITLE in USER_FILE_LIST]
            print('')
            loading_timer(5)
            while USER_READY_FLAG == False:
                USER_READY = input('Are you ready to load data?\n[Yes/No]:\n')
                if USER_READY.lower() in ['y', 'yea', 'yep', 'yes']:
                    if LOAD_CHOICE.lower() in ['t', 'text']:
                        CONTINUE = 'Text'
                    if LOAD_CHOICE.lower() in ['g', 'graph']:
                        CONTINUE = 'Graph'
                    # FUNCTION EXIT
                    LOAD_FLAG = True
                    USER_READY_FLAG = True

                    return USER_FILE_LIST, CONTINUE
                elif USER_READY.lower() in ['n', 'no', 'nop', 'nope']:
                    USER_FILE_LIST = ''
                    USER_READY_FLAG = True
                    pass
                else:
                    print('Please enter either \'Yes\' or \'No\'.')
                    loading_timer(3)
        LOAD_CHOICE = input('Please input one:\n\t\'Text\' -  If you would like to load a text search function using RegularExpression.\
\n\t\'Graph\' - If you would like to load a visual graph based off of word and letter counts.\n[Text/Graph/Quit]\n')
        if LOAD_CHOICE.lower() in ['t', 'text']:
            USER_INPUT = 'False Flag'
            USER_FILE_LIST = []
            print('The following will be a list of the Wordcrunch files available to view in \'matplotlib\'. The format \
is:\n\t\'subReddit Name\':\'Word Count Total\'')
            loading_timer(6)
            print('Files:           ')
            [print('| {}:{} |'.format(SUBREDDIT_NAME, WORD_COUNT), end = '') for SUBREDDIT_NAME, WORD_COUNT in SUBREDDIT_WORD_COUNT_DICT.items()]
            print('')
            time.sleep(2)
            print('Please enter the name(s) of each file you would like to load one at a time.\nBe sure to check for spelling\
 for proper functionality.\nEnter \'Quit\' when finished')
            while not USER_INPUT.lower() in ['q', 'quit']:
                USER_INPUT = input('[File Name/Quit]\n')
                if not USER_INPUT.lower() in ['q', 'quit']:
                    if USER_INPUT.lower().endswith('.txt'):
                        USER_INPUT = USER_INPUT.split('.txt')[0]
                    if not USER_INPUT.endswith(LOAD_DATE):
                        USER_INPUT = '{}_{}'.format(USER_INPUT, LOAD_DATE)
                    if not os.path.isfile('{}{}.txt'.format(TXT_PATH, USER_INPUT.lower())):
                        print('Please check spelling.')
                        time.sleep(1)
                        pass
                    else:
                        if not any(USER_INPUT.lower() in ELEMENT for ELEMENT in USER_FILE_LIST):
                            USER_FILE_LIST.append(USER_INPUT.lower())
                            print('Added: {}.txt'.format(USER_INPUT.lower()))
                        else:
                            print('Already added {}.txt'.format(USER_INPUT.lower()))
                for FILE in USER_FILE_LIST:
                    FILE = FILE.split('_')[0]
        elif LOAD_CHOICE.lower() in ['g', 'graph']:
            USER_INPUT = 'False Flag'
            USER_FILE_LIST = []
            print('The following will be a list of the Wordcrunch files available to view in \'matplotlib\'. The format \
is:\n\t\'subReddit Name\':\'Word Count Total\'')
            loading_timer(6)
            print('Files:           ')
            [print('| {}:{} |'.format(SUBREDDIT_NAME, WORD_COUNT), end = '') for SUBREDDIT_NAME, WORD_COUNT in SUBREDDIT_WORD_COUNT_DICT.items()]
            print('')
            time.sleep(2)
            print('Please enter the name(s) of each file you would like to load one at a time.\nBe sure to check for spelling\
 for proper functionality.\nEnter \'Quit\' when finished')
            while not USER_INPUT.lower() in ['q', 'quit']:
                USER_INPUT = input('[File Name/Quit]\n')
                if not USER_INPUT.lower() in ['q', 'quit']:
                    if USER_INPUT.lower().endswith('.xlsx'):
                        USER_INPUT = USER_INPUT.split('.xlsx')[0]
                    if not os.path.isfile('{}{}.xlsx'.format(XLSX_PATH, USER_INPUT.lower())):
                        print('Please check spelling.')
                        time.sleep(1)
                        pass
                    else:
                        if not any(USER_INPUT.lower() in ELEMENT for ELEMENT in USER_FILE_LIST):
                            USER_FILE_LIST.append(USER_INPUT.lower())
                            print('Added: {}.xlsx'.format(USER_INPUT.lower()))
                        else:
                            print('Already added {}.xlsx'.format(USER_INPUT.lower()))
        elif LOAD_CHOICE.lower() in ['q', 'quit']:
            # FUNCTION EXIT
            CONTINUE = 'Quit'
            LOAD_FLAG = True
            
            return None, CONTINUE
        else:
            print('Please enter either \'Text\' or \'Graph\'')
            loading_timer(3)



# UTILITY FUNCTION
def subreddit_comparison_bargraph_file_selector(SESSION_PATH):
    loading_timer(3)
    # READS TEXT FILE TO GET A TEXT DUMP TO BUILD A COMPARISON DICTIONARY
    with open('{}subReddit_Word_Count_Total.txt'.format(SESSION_PATH), 'r', encoding = 'utf-8') as WORD_COUNT_FILE:
        RAW_TEXT_DUMP = WORD_COUNT_FILE.read()
    RAW_TEXT_LIST = RAW_TEXT_DUMP.replace('\'', '').replace('{', '').replace('}', '').split(',')
    # DECLARE AND POPULATE COMPARISON DICTIONARY
    XLSX_WORD_COUNT_DICT = {}
    for ELEMENT in RAW_TEXT_LIST:
        XLSX_WORD_COUNT_DICT[ELEMENT.split(':')[0].strip()] = int(ELEMENT.split(':')[1].strip())

    TEMP_LIST = wordcrunch_word_total_list_sorter(XLSX_WORD_COUNT_DICT)
    # DELETE DICTIONARY IN ORDER TO RE-ORGANIZE FILES IN DESCENDING ORDER
    XLSX_WORD_COUNT_DICT = {}
    for FILE in TEMP_LIST:
        XLSX_WORD_COUNT_DICT[FILE.split()[0].strip()] = FILE.split()[1].strip()
    # PRINT LIST OF FILES
    print('The following will be a list of the Wordcrunch files available for comparison. The format is:\n\t\'subReddit Name\'\
:\'Word Count Total\'')
    loading_timer(3)
    print('Files:           ')
    [print('| {}:{} |'.format(SUBREDDIT_NAME, WORD_COUNT), end = '') for SUBREDDIT_NAME, WORD_COUNT in XLSX_WORD_COUNT_DICT.items()]
    print('')
    loading_timer(3)
    print('                  ')
    # PROMPT USER TO CHOOSE
    print('Select two subReddit Wordcrunch files to load for comparison, or type \'Quit\' to quit.\nThe subReddit with the\
 larger total word count will be the basis of comparison.')
    time.sleep(2)
    USER_CHOICE_LIST = []
    while len(USER_CHOICE_LIST) < 2:
        FILE_CORRECT_FLAG = False
        while FILE_CORRECT_FLAG == False:
            USER_FILE_CHOICE = input('Please check for correct spelling of the file name.\n[File Name/Quit]\n')
            if os.path.isfile('{}{}.xlsx'.format(XLSX_PATH, USER_FILE_CHOICE)):
                USER_CHOICE_LIST.append(USER_FILE_CHOICE)
                FILE_CORRECT_FLAG = True
                print('Added: {}.xlsx'.format(USER_FILE_CHOICE))
            elif USER_FILE_CHOICE.lower() in ['q', 'quit']:
                FILE_CORRECT_FLAG = True
                USER_CHOICE_LIST = ['1', '2']
    if USER_FILE_CHOICE.lower() in ['q', 'quit']:
        QUIT_LIST = []
        USER_FILE_CHOICE = 'Quit'

        return QUIT_LIST, USER_FILE_CHOICE

    print('You have chosen:')
    [print('| {}:{} |'.format(SUBREDDIT_NAME, WORD_COUNT), end = '') for SUBREDDIT_NAME, WORD_COUNT in XLSX_WORD_COUNT_DICT.items()\
     if SUBREDDIT_NAME in USER_CHOICE_LIST]
    print('')
    time.sleep(2)

    return USER_CHOICE_LIST, USER_FILE_CHOICE