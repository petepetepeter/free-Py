import time
from UTILITY import *
from LIST_MAKER import *
from TEXT_SEARCH import *
from SCRAPE import *
from TEXT_FILTER import *
from BAR_GRAPH import *
from TEXT_LOG import *
# WIKIPEDIA TOP100 ENGLISH LANGUAGE COMMON WORDS
COMMON_WORDS_DICT = {'1': 'the', '2': 'be', '3': 'to', '4': 'of', '5': 'and', '6': 'a', '7': 'in', '8': 'that', '9': 'have',
                    '10': 'i', '11': 'it', '12': 'for', '13': 'not', '14': 'on', '15': 'with', '16': 'he', '17': 'as',
                    '18': 'you', '19': 'do', '20': 'at', '21': 'this', '22': 'but', '23': 'his', '24': 'by', '25': 'from',
                    '26': 'they', '27': 'we', '28': 'say', '29': 'her', '30': 'she', '31': 'or', '32': 'an', '33': 'will',
                    '34': 'my', '35': 'one', '36': 'all', '37': 'would', '38': 'there', '39': 'their', '40': 'what',
                    '41': 'so', '42': 'up', '43': 'out', '44': 'if', '45': 'about', '46': 'who', '47': 'get', '48': 'which',
                    '49': 'go', '50': 'me', '51': 'when', '52': 'make', '53': 'can', '54': 'like', '55': 'time', '56': 'no',
                    '57': 'just', '58': 'him', '59': 'know', '60': 'take', '61': 'people', '62': 'into', '63': 'year', 
                    '64': 'your', '65': 'good', '66': 'some', '67': 'could', '68': 'them', '69': 'see', '70': 'other', 
                    '71': 'than', '72': 'then', '73': 'now', '74': 'look', '75': 'only', '76': 'come', '77': 'its', 
                    '78': 'over', '79': 'think', '80': 'also', '81': 'back', '82': 'after', '83': 'use', '84': 'two', 
                    '85': 'how', '86': 'our', '87': 'work', '88': 'first', '89': 'well', '90': 'way', '91': 'even', 
                    '92': 'new', '93': 'want', '94': 'because', '95': 'any', '96': 'these', '97': 'give', '98': 'day',
                    '99': 'most','100': 'us'}
def main():
#     loading_timer(7)
#     loading_message()
    CONTINUE = 'False Flag'
    print('Please rip this script apart and do what you would like to the code.')
    time.sleep(3)
    while not CONTINUE.lower() in ['e', 'exi', 'exit']:
        print('Attention user, this \'main()\' function will ask if you would like to restart from this position before exiting\n\
entirely. There are a few loops throughout which allow for navigation without stopping the entire program.\n')
        
        CONTINUE, SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, LOAD_DATE = directory_setup()

        if CONTINUE == 'New':
            while not CONTINUE.lower() in ['q', 'quit']:
                # SET UP SCRAPE
                SUBREDDIT_SCRAPE_LIST, CONTINUE = subreddit_scrape_list_maker()
                if CONTINUE.lower() in ['q', 'quit']:
                    break
                SUBREDDIT_SCRAPE_DICT = find_subreddit_json_page_count(SUBREDDIT_SCRAPE_LIST)
                find_subreddit_comments(SESSION_PATH, TXT_PATH, SUBREDDIT_SCRAPE_DICT, LOAD_DATE)
                comments_wordcrunch(SESSION_PATH, TXT_PATH, END_PATH, XLSX_PATH, SUBREDDIT_SCRAPE_DICT, COMMON_WORDS_DICT, LOAD_DATE)
                print('Scrape completed.')
                loading_timer(3)
                print('Updating Wordcrunch \'.txt\' files for viewing.')
                record_xlsx_totals_to_txt_function(SESSION_PATH, XLSX_PATH)                
                time.sleep(1)
                print('For loading, please choose either:\n\t\'Single\' - you can search Wordcrunch text dumps with \'RegEX\',\
 and you can load single \'matplotlib.pyplot\' bargraphs.\n\t\'Comparison\' - you can compare two data sets using \'matplotlib.pyplot\'')
                time.sleep(2)
                LOAD_CHOICE = 'False Flag'
                while not LOAD_CHOICE.lower() in ['q', 'quit']:
                    LOAD_CHOICE = input('Please enter either \'Single\' or \'Comparison\'.\n[Single/Comparison/Quit]\n')
                    if LOAD_CHOICE.lower() in ['s', 'single']:
                        SUBREDDIT_LOAD_LIST, CONTINUE = subreddit_load_list_maker(SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, LOAD_DATE)
                        if CONTINUE.lower() in ['t', 'text']:
                            for SUBREDDIT_NAME in SUBREDDIT_LOAD_LIST:
                                USER_OUTPUT = wordcrunch_search(SESSION_PATH, END_PATH, SUBREDDIT_NAME)
                                if USER_OUTPUT.lower() in ['q', 'quit']:
                                    LOAD_CHOICE = 'Quit'
                                    break
                        elif CONTINUE.lower() in ['g', 'graph']:
                            for SUBREDDIT_NAME in SUBREDDIT_LOAD_LIST:
                                top_100_bargraph(XLSX_PATH, END_PATH, SUBREDDIT_NAME, COMMON_WORDS_DICT)
                                USER_OUTPUT = input('Press [Enter] to load the next graph, or enter \'Quit\' to quit.\n[Enter/Quit]\n')
                                if USER_OUTPUT.lower() in ['q', 'quit']:
                                    LOAD_CHOICE = 'Quit'
                                    break
                    elif LOAD_CHOICE.lower() in ['c', 'comp', 'comparison']:
                        SUBREDDIT_COMPARISON_LIST, USER_OUTPUT = subreddit_comparison_bargraph_file_selector(SESSION_PATH)
                        if USER_OUTPUT.lower() in ['q', 'quit']:
                            LOAD_CHOICE = 'Quit'
                            pass
                        comparison_bargraph(XLSX_PATH, END_PATH, SUBREDDIT_COMPARISON_LIST, COMMON_WORDS_DICT)
                    elif LOAD_CHOICE.lower() in ['q', 'quit']:
                        LOAD_CHOICE = 'Quit'
                        pass
                    else:
                        print('Please enter either \'Single\' or \'Comparison\'.')
                        loading_timer(3)
                    LOAD_CHOICE = 'Quit'

                CONTINUE = input('Restarting \'New\' Wordcrunch scrape loop.\nEnter:\n\t\'Quit\' to exit loop\n\t\'Load\' -\
 to load data\n[Quit/Load]')

        elif CONTINUE == 'Load':
            while not CONTINUE.lower() in ['q', 'quit']:
                # HERE CHOOCE COMPARISON BAR GRAPH OR SINGLE TEXT/TOP100 VIEW
                print('For loading, please choose either:\n\t\'Single\' - you can search Wordcrunch text dumps with \'RegEX\',\
 and you can load single \'matplotlib.pyplot\' bargraphs.\n\t\'Comparison\' - you can compare two data sets using \'matplotlib.pyplot\'')
                time.sleep(2)
                LOAD_CHOICE = 'False Flag'
                while not LOAD_CHOICE.lower() in ['q', 'quit']:
                    LOAD_CHOICE = input('Please enter either \'Single\' or \'Comparison\'.\n[Single/Comparison/Quit]\n')
                    if LOAD_CHOICE.lower() in ['s', 'single']:
                        SUBREDDIT_LOAD_LIST, CONTINUE = subreddit_load_list_maker(SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, LOAD_DATE)
                        if CONTINUE.lower() in ['t', 'text']:
                            for SUBREDDIT_NAME in SUBREDDIT_LOAD_LIST:
                                USER_OUTPUT = wordcrunch_search(SESSION_PATH, END_PATH, SUBREDDIT_NAME)
                                if USER_OUTPUT.lower() in ['q', 'quit']:
                                    LOAD_CHOICE = 'Quit'
                                    break
                        elif CONTINUE.lower() in ['g', 'graph']:
                            for SUBREDDIT_NAME in SUBREDDIT_LOAD_LIST:
                                top_100_bargraph(XLSX_PATH, END_PATH, SUBREDDIT_NAME, COMMON_WORDS_DICT)
                                USER_OUTPUT = input('Press [Enter] to load the next graph, or enter \'Quit\' to quit.\n[Enter/Quit]\n')
                                if USER_OUTPUT.lower() in ['q', 'quit']:
                                    LOAD_CHOICE = 'Quit'
                                    break
                    elif LOAD_CHOICE.lower() in ['c', 'comp', 'comparison']:
                        SUBREDDIT_LOAD_LIST, USER_OUTPUT = subreddit_comparison_bargraph_file_selector(SESSION_PATH)
                        if USER_OUTPUT.lower() in ['q', 'quit']:
                            LOAD_CHOICE = 'Quit'
                            pass
                        comparison_bargraph(XLSX_PATH, END_PATH, SUBREDDIT_LOAD_LIST, COMMON_WORDS_DICT)
                    elif LOAD_CHOICE.lower() in ['q', 'quit']:
                        LOAD_CHOICE = 'Quit'
                        pass
                    else:
                        print('Please enter either \'Single\' or \'Comparison\'.')
                        loading_timer(3)
                    LOAD_CHOICE = 'Quit'
                CONTINUE = input('Restarting Wordcrunch \'Load\' data loop.\nEnter:\n\t\'Quit\' to exit loop\n\t\'New\' -\
 to start a new session\n[Quit]\n')
        elif CONTINUE.lower() in ['q', 'quit']:
            EXIT_CHOICE = False
            while EXIT_CHOICE == False:
                EXIT_CHOICE = input('You are about to leave subReddit Wordcrunch.\nPlease choose:\n\t\'Exit\' - to exit the\
program entirely\n\t\'Restart\' - to load the main menu\n[Exit/Restart]:\n')
                if EXIT_CHOICE.lower() in ['e', 'exi', 'exit']:
                    CONTINUE = 'Exit'
                    print('Updating Wordcrunch \'.txt\' files for viewing.')
                    updtate_xlsx_totals_to_txt_function(SESSION_PATH, XLSX_PATH)
                    EXIT_CHOICE = True
                elif EXIT_CHOICE.lower() in ['r', 'res', 'redo', 'restart']:
                    CONTINUE = 'Restart'
                    EXIT_CHOICE = True
                else:
                    print('Please enter either \'Exit\' or \'Restart\'')
                    loading_timer(3)
        if CONTINUE.lower() in ['q', 'quit']:
            CONTINUE = 'Exit'
if __name__ == '__main__':
    main()