from UTILITY import loading_timer
import os
import re
import time

# FUNCTION THAT SCRAPES A SUBREDDIT'S SYNOPSIS FOR A RegEX SEARCH WITH AN OPTION TO LOG THE RESULTS
def wordcrunch_search(SESSION_PATH, END_PATH, SUBREDDIT):
    # OPEN THE 'WordCrunch' SYNOPSIS
    with open('{}{}_WordCrunch.txt'.format(END_PATH, SUBREDDIT.lower()), 'r', encoding = 'utf-8') as CRUNCH:
        LINES = CRUNCH.read()
    # SEPARATE SPECIFIC LINES
    URL = re.findall('(?<=\\n)URL: .*?\\n(?=Post)',LINES)
    POST_COUNT = re.findall('(?<=\\n)Post Count: .*?\\n(?=Common)',LINES)
    COMMON_WORD_COUNT = re.findall('(?<=\\n)Common Word Count: .*?\\n(?=Forum)',LINES)
    FORUM = re.findall('(?<=\\n)Forum: .*?](?=\\n)',LINES)
    try:
        os.mkdir('{}{}_RegEX/'.format(SESSION_PATH, SUBREDDIT.lower()))
        SAVE_PATH = '{}{}_RegEX/'.format(SESSION_PATH, SUBREDDIT.lower())
    except:
        SAVE_PATH = '{}{}_RegEX/'.format(SESSION_PATH, SUBREDDIT.lower())
    LOGGING_FLAG = False
    time.sleep(3)
    print('Please input how you would like to search the subReddit Wordcrunch file. Type:\n\t\'RNG\' - to search individual\
 posts by a \'(MIN, MAX)\' range of commom words\n\t\'STR\' - to search individual posts by a RegEX formatted \'re.search\'\
 string\n\t\'NXT\' - to move to the next Wordcrunch file in your list (if available)')
    while LOGGING_FLAG == False:
        time.sleep(3)
        USER_INPUT = input('What would you like to do?\n[RNG/STR/NXT/Quit]\n')
        if USER_INPUT.lower() in ['r', 'rng', 'range']:
            loading_timer(3)
            print('Please make sure that \'MIN\' < \'MAX\'.')
            loading_timer(3)
            RANGE_FLAG = True
            while RANGE_FLAG == True:
                try:
                    MIN = int(input('MIN =           '))
                    MAX = int(input('MAX =           '))
                except Exception as e:
                    print(e.args)
                if MIN < MAX:
                    RANGE_FLAG = False
                else:
                    print('Please make sure that ingeter \'MIN\' is LESS than integer \'MAX\'.')
                    loading_timer(2)
            print('Results:')
            SEARCH_RESULTS = [print('{}{}{}{}\n'.format(URL[INDEX_NUM], POST_COUNT[INDEX_NUM], COMMON_WORD_COUNT[INDEX_NUM],\
             FORUM[INDEX_NUM])) for INDEX_NUM in range(len(URL)) if MIN <= int(COMMON_WORD_COUNT[INDEX_NUM].split()[3]) <= MAX]
            time.sleep(2)
            LOGGING = input('Would you like to export these results to\n\'{}Common_Word_Count_{}-{}.txt\'\n[Yes/No]\n'\
                            .format(SAVE_PATH, MIN, MAX))
            if LOGGING.lower() in ['y', 'ye', 'yes', 'yep', 'yea']:
                with open('{}Common_Word_Count_{}-{}.txt'.format(SAVE_PATH, MIN, MAX), 'w', encoding = 'utf-8')as REGEX:
                    print(SEARCH_RESULTS, file = REGEX)
                print('Completed')
                loading_timer(2)
            else:
                pass
        elif USER_INPUT.lower() in ['s', 'str', 'string']:
            loading_timer(3)
            print('Please make sure that \'SEARCH_STRING\' if formatted for \'re.search()\'.')
            loading_timer(3)
            STRING_FLAG = True
            while STRING_FLAG == True:
                try:
                    SEARCH_STRING = input('SEARCH_STRING =')
                    print('Results:')
                    SEARCH_RESULTS = [print('{}{}{}{}\n'.format(URL[INDEX_NUM], POST_COUNT[INDEX_NUM], COMMON_WORD_COUNT[INDEX_NUM],\
                     FORUM[INDEX_NUM])) for INDEX_NUM in range(len(URL)) if re.search(SEARCH_STRING,FORUM[INDEX_NUM])]
                    STRING_FLAG = False
                except Exception as e:
                    print(e.args)
            time.sleep(2)
            LOGGING = input('Would you like to export these results to\n\'{}{}.txt\'?\n[Yes/No]\n'.format(\
                            SAVE_PATH, ''.join([LETTER for LETTER in SEARCH_STRING if LETTER.isalnum()])))
            if LOGGING.lower() in ['y', 'ye', 'yes', 'yep', 'yea']:
                with open('{}{}.txt'.format(SAVE_PATH, ''.join([LETTER for LETTER in SEARCH_STRING if LETTER.isalnum()])), 'w',\
                          encoding = 'utf-8') as REGEX:[print('{}{}{}{}\n'.format(URL[INDEX_NUM], POST_COUNT[INDEX_NUM],\
                          COMMON_WORD_COUNT[INDEX_NUM], FORUM[INDEX_NUM]), file = REGEX) for INDEX_NUM in range(len(URL))\
                          if re.search(SEARCH_STRING, FORUM[INDEX_NUM])]
                print('Completed')
                loading_timer(2)
            else:
                pass
        elif USER_INPUT.lower() in ['q', 'n', 'nxt', 'next', 'quit']:
            if USER_INPUT.lower() in ['q', 'quit']:
                USER_INPUT = 'Quit'
                LOGGING_FLAG = True
            elif USER_INPUT.lower() in ['n', 'nxt', 'next']:
                USER_INPUT = 'Next'
                LOGGING_FLAG = True
        else:
            print('Please enter either \'RNG\', \'STR\', or \'NXT\'.')
            loading_timer(2)
    
    return USER_INPUT