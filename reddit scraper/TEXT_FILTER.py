import datetime
import pandas
import time
from spellchecker import SpellChecker

def wordcrunch_text_file_filter(TXT_PATH, SUBREDDIT, DATE):
    # DELCARATIONS
    POST_DICT = {}
    # PROGRESS UPDATE, PRINTED TO SCREEN
    print('Loading...', end = '\r')
    # LOAD THE CORRECT '.txt' NAME AS 'FILE' VARIABLE
    FILE = '{}_{}.txt'.format(SUBREDDIT.lower(), DATE)
    # READ AND SEPARATE ALL COMMENTS IN '.txt' FILE
    # BE SURE TO HAVE ALREADY DESIGNATED THE CORRECT DIRECTORY PATH IN 'TXT_PATH'
    with open('{}{}'.format(TXT_PATH, FILE), 'r', encoding="utf-8") as TEXT_FILE:
        TEXT_LINES = TEXT_FILE.readlines()
    # MAKE A DICTIONARY WITH THE POST'S URL AS THE KEY AND ALL IT'S COMMENTS AS A LIST FOR THE VALUE
    # FIRST FILTER, CHECKING FOR: RANDOM CHARACTERS
    for LINE in TEXT_LINES:
        POST_DICT[LINE.split('|||')[0]] = [' '.join(COMMENT.replace(',', ' ').replace('=', ' ').replace('(', ' ')\
                                           .replace(')', ' ').replace('.', ' ').replace('?', ' ').replace('!', ' ')\
                                           .replace('\\', ' ').replace('/', ' ').replace('\'', '').replace('‘', '')\
                                           .replace('’', '').replace('”', ' ').replace('“', ' ').replace(';', ' ')\
                                           .replace('~', ' ').replace('@', ' ').replace('»', ' ').replace('%', ' ')\
                                           .replace('^', ' ').replace('|', ' ').replace('{', ' ').replace('}', ' ')\
                                           .replace('`', ' ').replace('[', ' ').replace(']', ' ').replace('-', ' ')\
                                           .replace('&', ' ').replace('$', ' ').replace('*', ' ').replace(':', ' ')\
                                           .replace('_', ' ').replace('•', ' ').replace('#', ' ').replace('´', '')\
                                           .replace('+', ' ').lower().strip().split()) for COMMENT in LINE.split('|||')[1]\
                                           .split('||') if len(COMMENT) > 0]
    time.sleep(1)

    return POST_DICT



def wordcrunch_spellcheck_filter(POST_DICT, COMMON_WORDS):
    # DECLARATIONS
    WORD_LIST = []
    COMMON_WORD_COUNT = {}
    TOTAL_COMMENTS_COUNTER = 0
    POST_PROGRESS_COUNTER = 0
    COMMON_WORD_COUNTER = 0
    # TOTAL POST COUNT
    TOTAL_POSTS = len(POST_DICT.keys())
    # SECOND FILTER, CHECKING FOR: MISSSPELLINGS, INTEGERS IN STRINGS
    for POST_URL, COMMENTS_LIST in POST_DICT.items():
        # COUNTER TO MEASURE THE COMMON WORDS IN POST
        COMMON_WORD_COUNTER = 0
        # PRINT THE PERCENTAGE COMPLETED TO SCREEN
        print('\rChecking spelling [Completed: {:02.0f}%]                                    '.format(round(\
             (POST_PROGRESS_COUNTER / TOTAL_POSTS) * 100, 2)), end = '\r')
        # COUNTER TO MEASURE THE PERCENTAGE COMPLETED
        POST_PROGRESS_COUNTER += 1
        for COMMENT in COMMENTS_LIST:
            TOTAL_COMMENTS_COUNTER += 1
            # SpellChecker() RETURNS WHAT IT CONSIDERS A MISSPELLING
            MISSPELLED = SpellChecker().unknown(COMMENT.split())
            for WORD in COMMENT.split():
                # COMPARISON TO 'MISSPELLED'
                if not WORD in MISSPELLED:
                    # CHECK STRING FOR INTEGER
                    if any(LETTER.isdigit() for LETTER in WORD):
                        pass
                    else:
                        # APPEND FILTERED WORD TO 'WORD_LIST'
                        WORD_LIST.append(WORD.strip())
                        # COUNT COMMON WORDS PER POST
                        if WORD in COMMON_WORDS.values():
                            COMMON_WORD_COUNTER += 1
        # RECORDING THE COMMON WORD COUNT BY POST URL
        COMMON_WORD_COUNT[POST_URL] = COMMON_WORD_COUNTER
    # MAKE A LIST WITH THE POSTS SORTED BY THEIR COMMON WORD COUNTS
    COMMON_WORD_USAGE_CONVERSATIONS = sorted(COMMON_WORD_COUNT, key = COMMON_WORD_COUNT.get, reverse = True)
    # PREPARE LIST FOR LOGGING AT THE END
    CONVERSATION_WRAPPER = ['\nURL: {}\nPost Count: {}\nCommon Word Count: {}\nForum: {}'.format(\
                            URL, len(POST_DICT[URL]), COMMON_WORD_COUNT[URL], POST_DICT[URL]) for URL in\
                            COMMON_WORD_USAGE_CONVERSATIONS]
    
    return TOTAL_POSTS, TOTAL_COMMENTS_COUNTER, WORD_LIST, CONVERSATION_WRAPPER



def wordcrunch_counter(WORD_LIST):
    # DECLARATIONS
    WORD_DICT = {}
    A_COUNTER = 0
    B_COUNTER = 0
    C_COUNTER = 0
    D_COUNTER = 0
    E_COUNTER = 0
    F_COUNTER = 0
    G_COUNTER = 0
    H_COUNTER = 0
    I_COUNTER = 0
    J_COUNTER = 0
    K_COUNTER = 0
    L_COUNTER = 0
    M_COUNTER = 0
    N_COUNTER = 0
    O_COUNTER = 0
    P_COUNTER = 0
    Q_COUNTER = 0
    R_COUNTER = 0
    S_COUNTER = 0
    T_COUNTER = 0
    U_COUNTER = 0
    V_COUNTER = 0
    W_COUNTER = 0
    X_COUNTER = 0
    Y_COUNTER = 0
    Z_COUNTER = 0
    UNKNOWN_COUNTER = 0
    WORD_PROGRESS_COUNTER = 0
    LETTER_PROGRESS_COUNTER = 0
    # CREATE A SET OF UNIQUE WORDS
    WORD_SET = set(WORD_LIST)
    # UNIQUE WORD COUNT
    UNIQUE_WORD_COUNT = len(WORD_SET)
    # CREATE DICTIONARY OF WORD / COUNT OF THAT SPECIFIC WORD
    for WORD in WORD_SET:
        # COUNTER TO MEASURE THE PERCENTAGE COMPLETED
        WORD_PROGRESS_COUNTER += 1
        # PRINT THE PERCENTAGE COMPLETED TO SCREEN
        print('Counting words [Completed: {:02.0f}%]                                       '.format(round(\
             (WORD_PROGRESS_COUNTER / len(WORD_SET)) * 100, 2)), end = '\r')
        WORD_DICT[WORD] = WORD_LIST.count(WORD)
    for WORD in WORD_LIST:
        # COUNTER TO MEASURE THE PERCENTAGE COMPLETED
        LETTER_PROGRESS_COUNTER += 1
        # PRINT THE PERCENTAGE COMPLETED TO SCREEN
        print('Counting letters [Completed: {:02.0f}%]                                    '.format(round(\
             (LETTER_PROGRESS_COUNTER / len(WORD_LIST)) * 100, 2)), end = '\r')
        for LETTER in WORD:
            if LETTER == 'a':
                A_COUNTER += 1
            elif LETTER == 'b':
                B_COUNTER += 1
            elif LETTER == 'c':
                C_COUNTER += 1
            elif LETTER == 'd':
                D_COUNTER += 1
            elif LETTER == 'e':
                E_COUNTER += 1
            elif LETTER == 'f':
                F_COUNTER += 1
            elif LETTER == 'g':
                G_COUNTER += 1
            elif LETTER == 'h':
                H_COUNTER += 1
            elif LETTER == 'i':
                I_COUNTER += 1
            elif LETTER == 'j':
                J_COUNTER += 1
            elif LETTER == 'k':
                K_COUNTER += 1
            elif LETTER == 'l':
                L_COUNTER += 1
            elif LETTER == 'm':
                M_COUNTER += 1
            elif LETTER == 'n':
                N_COUNTER += 1
            elif LETTER == 'o':
                O_COUNTER += 1
            elif LETTER == 'p':
                P_COUNTER += 1
            elif LETTER == 'q':
                Q_COUNTER += 1
            elif LETTER == 'r':
                R_COUNTER += 1
            elif LETTER == 's':
                S_COUNTER += 1
            elif LETTER == 't':
                T_COUNTER += 1
            elif LETTER == 'u':
                U_COUNTER += 1
            elif LETTER == 'v':
                V_COUNTER += 1
            elif LETTER == 'w':
                W_COUNTER += 1
            elif LETTER == 'x':
                X_COUNTER += 1
            elif LETTER == 'y':
                Y_COUNTER += 1
            elif LETTER == 'z':
                Z_COUNTER += 1
            else:
                UNKNOWN_COUNTER += 1
    LETTER_COUNT = 'A: {}\nB: {}\nC: {}\nD: {}\nE: {}\nF: {}\nG: {}\nH: {}\nI: {}\nJ: {}\nK: {}\nL: {}\nM: {}\nN: {}\nO: {}\n\
P: {}\nQ: {}\nR: {}\nS: {}\nT: {}\nU: {}\nV: {}\nW: {}\nX: {}\nY: {}\nZ: {}\nUnknown: {}\n'.format(A_COUNTER, B_COUNTER,\
                    C_COUNTER, D_COUNTER, E_COUNTER, F_COUNTER, G_COUNTER, H_COUNTER, I_COUNTER, J_COUNTER, K_COUNTER,\
                    L_COUNTER, M_COUNTER, N_COUNTER, O_COUNTER, P_COUNTER, Q_COUNTER, R_COUNTER, S_COUNTER, T_COUNTER,\
                    U_COUNTER, V_COUNTER, W_COUNTER, X_COUNTER, Y_COUNTER, Z_COUNTER, UNKNOWN_COUNTER)
    
    return UNIQUE_WORD_COUNT, WORD_DICT, LETTER_COUNT



# READ EACH '.txt' FILE SAVED LOCALLY FOR .json SCRAPED TEXT FROM EACH SUBREDDIT
# MAKE A DATAFRAME, THEN SAVE THAT DATAFRAME LOCALLY TO A '.xlsx' FILE
def comments_wordcrunch(SESSION_PATH, TXT_PATH, END_PATH, XLSX_PATH, SCRAPE_DICT, COMMON_WORDS, DATE):
    # ITERATE THROUGH THE DIFFERENT SUBREDDIT '.txt' FILES I HAVE SCRAPED
    for SUBREDDIT, PAGE_COUNT in SCRAPE_DICT.items():
        try:
            START_TIME = time.time()
            print('Processing scrape from: /r/{}'.format(SUBREDDIT.lower()))
            # CALL 'wordcrunch_text_file_filter()' TO SEPARATE POST URLS AND REPLIES
            POST_DICT = wordcrunch_text_file_filter(TXT_PATH, SUBREDDIT, DATE)
            # CALL 'wordcrunch_spellcheck_filter()' TO SPELLCHECK AND FILTER POSTS AND WORDS
            TOTAL_POSTS, TOTAL_COMMENTS_COUNTER, WORD_LIST, CONVERSATION_WRAPPER = wordcrunch_spellcheck_filter(POST_DICT, 
                                                                                                            COMMON_WORDS)
            time.sleep(1)
            # CALL 'wordcrunch_counter()' TO COUNT WORDS // LETTERS
            UNIQUE_WORD_COUNT, WORD_DICT, LETTER_COUNT = wordcrunch_counter(WORD_LIST)
            # PROGRESS UPDATE, PRINTED TO SCREEN
            print('Logging to \'.txt\' file...                     ', end = '\r')
            time.sleep(1)
            TOTAL_TIME = time.time() - START_TIME
            SCRAPE_TIME = str(datetime.timedelta(seconds = int(TOTAL_TIME)))
            # LOG THE SUBREDDIT // TOTAL PAGES // TOTAL POSTS // TOTAL COMMENT COUNT // TOTAL WORD COUNT 
            # // UNIQUE WORD COUNT // TIME SPENT SCRAPING TEXT // LETTER COUNT // POSTS & REPLIES WITHIN THEM
            with open('{}{}_WordCrunch.txt'.format(END_PATH, SUBREDDIT.lower()), 'w', encoding='utf-8') as SCRAPE_LOG:
                print('Reddit: {}\nScrape Time: {}\nPages: {}\nIndividual Posts: {}\nTotal Comments: {}\nTotal Words: {}\
\nUnique Words: {}\nLetter Totals:\n{}\n\n{}'.format(SUBREDDIT.lower(), SCRAPE_TIME, PAGE_COUNT, TOTAL_POSTS, TOTAL_COMMENTS_COUNTER,\
                      len(WORD_LIST), UNIQUE_WORD_COUNT, LETTER_COUNT, '\n'.join(CONVERSATION_WRAPPER)), file = SCRAPE_LOG)
            # PROGRESS UPDATE, PRINTED TO SCREEN
            print('Saving to \'.xlsx\' file...                      ', end = '\r')
            time.sleep(1)
            # CREATE PANDAS DATAFRAME FROM 'WORD_DICT' DICTIONARY
            PANDAS_DATAFRAME = pandas.DataFrame.from_dict(WORD_DICT, orient ='index', columns = [SUBREDDIT.lower()])
            # RENAME INDEX TO 'Word'
            PANDAS_DATAFRAME = PANDAS_DATAFRAME.rename_axis('Word')
            # SORT 'Word' VALUES IN DESCENDING ORDER
            PANDAS_DATAFRAME = PANDAS_DATAFRAME.sort_values(by = SUBREDDIT.lower(), ascending = False)
            # DELETES ANY 'NaN' ROWS IF THEY EXIST
            PANDAS_DATAFRAME = PANDAS_DATAFRAME.drop(PANDAS_DATAFRAME[PANDAS_DATAFRAME.isnull().T.any()].index)
            # EXPOTS THE DATAFRAME TO AN '.xlsx' FILE
            # BE SURE TO HAVE ALREADY DESIGNATED THE CORRECT DIRECTORY PATH IN 'XLSX_PATH'
            PANDAS_DATAFRAME.to_excel('{}{}.xlsx'.format(XLSX_PATH, SUBREDDIT.lower()))
            print('Completed /r/{} Wordcrunch.'.format(SUBREDDIT.lower()))
        except:
            # THIS IS SO THE ENTIRE PROCESS IS NOT DE-RAILED WHEN LEFT RUNNING
            with open('{}ERROR_LOG.txt'.format(SESSION_PATH), 'a', encoding = 'utf-8') as ERROR_LOG:
                print('{} - Error on subReddit "{}" while counting words / letters.'.format(datetime.datetime.now(), SUBREDDIT),\
                      file = ERROR_LOG)