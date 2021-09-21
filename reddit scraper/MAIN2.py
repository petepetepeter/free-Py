import os
import re
import time
import pandas
from scipy.stats import *
from matplotlib.pyplot import *
from TEXT_LOG import *
from CHI_SQUARED import *

# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH

SESSION_PATH = r'C:\Users\Pete\Documents\CLASSES\CIT 144 PYTHON 1\Wordcrunch\11_08_20_Wordcrunch_Data\\'
TXT_PATH = '{}Raw_txt_Folder\\'.format(SESSION_PATH)
XLSX_PATH = '{}xlsx_Folder\\'.format(SESSION_PATH)
END_PATH = '{}Wordcrunch_Totals\\'.format(SESSION_PATH)

# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH
# SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH SET YOUR DOWNLOAD/LOAD PATH

def loading_timer(TIME_LIMIT):
    TIMER_COUNTER = 0
    while TIMER_COUNTER < TIME_LIMIT:
        print('Loading{}'.format('.' * TIMER_COUNTER), end = '\r')
        time.sleep(1)
        TIMER_COUNTER += 1



def main():
    MAIN_FLAG = False
    while MAIN_FLAG == False:
        CHI_DICTIONARY = chi_txt_reader(SESSION_PATH)
        print('The following is a list of subReddits scraped on 10/31/20.', end = '\r')
        time.sleep(5)
        print('                                                             ', end = '\r')
        [print('|{:^25}|'.format(SUBREDDIT)) for SUBREDDIT in list(CHI_DICTIONARY.keys())]
        loading_timer(5)
        print('                              ', end = '\r')
        USER_INPUT = 'False Flag'
        while not USER_INPUT.lower() in ['q', 'quit']:
            USER_INPUT = input('Please, either select a \'subReddit\' from the list, type \'Print\' to see the list again,\
 or enter \'Quit\' to quit.\n[subReddit/Print/Quit]\n')
            if USER_INPUT.lower() in ['q', 'quit']:
                MAIN_FLAG = True
                print('Goodbye')
            elif USER_INPUT.lower() in ['p', 'print']:
                [print('|{:^25}|'.format(SUBREDDIT)) for SUBREDDIT in list(CHI_DICTIONARY.keys())]
                pass
            elif USER_INPUT.lower() in list(CHI_DICTIONARY.keys()):
                chi_bargraph(USER_INPUT.lower(), CHI_DICTIONARY[USER_INPUT.lower()], SESSION_PATH)
            else:
                print('Please either enter a valid \'subReddit\' or \'Quit\'.')
                loading_timer(4)


if __name__ == '__main__':
    main()