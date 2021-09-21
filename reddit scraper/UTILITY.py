import time
import datetime
import os

# LOADING LINE ANIMATION
def loading_timer(TIME_LIMIT):
    TIMER_COUNTER = 0
    while TIMER_COUNTER < TIME_LIMIT:
        print('Loading{}'.format('.' * TIMER_COUNTER), end = '\r')
        time.sleep(1)
        TIMER_COUNTER += 1



# ANIMATION FOR ANYONE FROM CLASS
def loading_message():
    time.sleep(2)
    print('HELLO CIT 144!', end = '\r')
    time.sleep(4)
    print('                                                                                               ', end = '\r')
    print('Please try and break this program by finding bugs.', end = '\r')
    time.sleep(5)
    print('                                                                                               ', end = '\r')
    STUPID_LOOP = 0
    while STUPID_LOOP <= 4:
        print('I don\'t know what I am doing, so there must be something wrong{}'.format('.' * STUPID_LOOP), end = '\r')
        time.sleep(1)
        STUPID_LOOP += 1
    print('I don\'t know what I am doing, so there must be something wrong.... somewharee', end = '\r')
    time.sleep(3)
    print('                                                                                               ', end = '\r')



def absolute_path_assignment(ROOT_PATH, DATE):
    DIRECTORY_EXISTS = False
    ERROR = False
    if not ROOT_PATH.endswith('\\'):
        ROOT_PATH = '{}\\'.format(ROOT_PATH)
    # MAKE A SESSION FOLDER DIRECTORY TO SAVE SUB-DIRECTORIES IN
    SESSION_PATH = '{}{}_Wordcrunch_Data\\'.format(ROOT_PATH, DATE)    
    # MAKE A DOWNLOAD PATH TO SAVE THE SCRAPED '.txt' FILES
    TXT_PATH = '{}Raw_txt_Folder\\'.format(SESSION_PATH)
    # MAKE A DOWNLOAD PATH TO SAVE THE NEWLY FORMED '.xlsx' FILES
    XLSX_PATH = '{}xlsx_Folder\\'.format(SESSION_PATH)
    # MAKE A DOWNLOAD PATH TO SAVE THE ANALYSIS DUMP '.txt' FILES
    END_PATH = '{}Wordcrunch_Totals\\'.format(SESSION_PATH)
    # 'TRY' AND 'EXCEPT' FOR CORRECT DIRECTORY SYNTAX
    if not os.path.isdir(ROOT_PATH):
        try:
            os.mkdir(ROOT_PATH)
            print(ROOT_PATH)
        except Exception as e:
            ERROR = True
            print(e.args)
    else:
        DIRECTORY_EXISTS = True
        print('\n{} already exists.'.format(ROOT_PATH))
    if not os.path.isdir(SESSION_PATH):
        try:
            os.mkdir(SESSION_PATH)
            print(SESSION_PATH)
        except Exception as e:
            ERROR = True
            print(e.args)
    else:
        DIRECTORY_EXISTS = True
        print('\n{} already exists.'.format(SESSION_PATH))
    if not os.path.isdir(TXT_PATH):
        try:
            os.mkdir(TXT_PATH)
            print(TXT_PATH)
        except Exception as e:
            ERROR = True
            print(e.args)
    else:
        DIRECTORY_EXISTS = True
        print('\n{} already exists.'.format(TXT_PATH))
    if not os.path.isdir(XLSX_PATH):
        try:
            os.mkdir(XLSX_PATH)
            print(XLSX_PATH)
        except Exception as e:
            ERROR = True
            print(e.args)
    else:
        DIRECTORY_EXISTS = True
        print('\n{} already exists.'.format(XLSX_PATH))
    if not os.path.isdir(END_PATH):
        try:
            os.mkdir(END_PATH)
            print(END_PATH)
        except Exception as e:
            ERROR = True
            print(e.args)
    else:
        DIRECTORY_EXISTS = True
        print('\n{} already exists.'.format(END_PATH))

    return SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, ERROR, DIRECTORY_EXISTS



def absolute_path_check():
    QUIT_FLAG = False
    loading_timer(4)
    print('Your current working directory is \'{}\''.format(os.getcwd()))
    time.sleep(2)
    loading_timer(3)
    print('Please enter the name of a subdirectory folder to create here, or the absolute path of a new directory folder.\
\nOr type \'Quit\' to quit this session.')
    time.sleep(3)
    ROOT_PATH = input('EXAMPLE: \'C:\\Users\\Smith\\Documents\\NEW_DIRECTORY_FOLDER\\\'\n[Absolute Path/Quit]\n\n')
    if ROOT_PATH.lower() in ['q', 'quit']:
        QUIT_FLAG = True
        time.sleep(2)
        
        return ROOT_PATH, QUIT_FLAG
    elif os.path.isabs(ROOT_PATH):
        time.sleep(2)
        
        return ROOT_PATH, QUIT_FLAG
    else:
        ROOT_PATH = '{}\\{}'.format(os.getcwd(), ROOT_PATH)
        time.sleep(2)            
        
        return ROOT_PATH, QUIT_FLAG



def load_path_assignment(LOAD_PATH):
    ERROR = False
    SESSION_PATH_EXISTS = False
    TXT_PATH_EXISTS = False
    XLSX_PATH_EXISTS = False
    END_PATH_EXISTS = False
    SESSION_PATH = LOAD_PATH
    if not LOAD_PATH.endswith('\\'):
        LOAD_PATH = '{}\\'.format(LOAD_PATH)
    SESSION_PATH = LOAD_PATH
    # MAKE A DOWNLOAD PATH TO SAVE THE SCRAPED '.txt' FILES
    TXT_PATH = '{}Raw_txt_Folder\\'.format(SESSION_PATH)
    # MAKE A DOWNLOAD PATH TO SAVE THE NEWLY FORMED '.xlsx' FILES
    XLSX_PATH = '{}xlsx_Folder\\'.format(SESSION_PATH)
    # MAKE A DOWNLOAD PATH TO SAVE THE ANALYSIS DUMP '.txt' FILES
    END_PATH = '{}Wordcrunch_Totals\\'.format(SESSION_PATH)
    LOAD_DATE = SESSION_PATH.split('_Wordcrunch')[0][-8:]
    # 'TRY' AND 'EXCEPT' FOR CORRECT DIRECTORY SYNTAX
    if not os.path.isdir(SESSION_PATH):
        ERROR = True
        print('\nError: \'{}\' does not exist, please check syntax.'.format(SESSION_PATH))
    else:
        SESSION_PATH_EXISTS = True
        print('\n{} already exists.'.format(SESSION_PATH))
    if not os.path.isdir(TXT_PATH):
        ERROR = True
        print('\nError: \'{}\' does not exist, please check syntax.'.format(TXT_PATH))
    else:
        TXT_PATH_EXISTS = True
        print('\n{} already exists.'.format(TXT_PATH))
    if not os.path.isdir(XLSX_PATH):
        ERROR = True
        print('\nError: \'{}\' does not exist, please check syntax.'.format(XLSX_PATH))
    else:
        XLSX_PATH_EXISTS = True
        print('\n{} already exists.'.format(XLSX_PATH))
    if not os.path.isdir(END_PATH):
        ERROR = True
        print('\nError: \'{}\' does not exist, please check syntax.'.format(END_PATH))
    else:
        END_PATH_EXISTS = True
        print('\n{} already exists.'.format(END_PATH))
    
    return SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, LOAD_DATE, ERROR, SESSION_PATH_EXISTS, TXT_PATH_EXISTS, XLSX_PATH_EXISTS, END_PATH_EXISTS



# BEGIN BY DESIGNATING WHERE TO SAVE THE 'Wordcrunch' SCRAPE DATA
def directory_setup():
    # DATE OF SCRAPE FOR '.txt' FILE NAMING
    # PRINTS IN 'mm_dd_yy' FORMAT
    DATE = datetime.datetime.now()
    DATE = DATE.strftime('%x').replace('/', '_')
    print('Thank you for using subReddit Wordcrunch!')
    time.sleep(2)
    FIRST_LAYER_FLAG = True
    while FIRST_LAYER_FLAG == True:
        loading_timer(4)
        print('Please choose one of the following:                   \n\n\t\'Scrape\' - if you would like to start a new\
 Wordcrunch session\n\t\'Load\' - if you would like to load older Wordcrunch data\n\t\'Quit\' - if you would like to quit\
 this session')
        START_DECISION = input('[Scrape/Load/Quit]:\n\n')
        if START_DECISION.lower() in ['s', 'n', 'scrape', 'start', 'new']:
            NEW_LOOP_FLAG = True
            while NEW_LOOP_FLAG == True:
                # ABSOLUTE PATH CHECK
                ROOT_PATH, QUIT_FLAG = absolute_path_check()
                if QUIT_FLAG == True:
                    time.sleep(2)
                    FIRST_LAYER_FLAG = False
                    NEW_LOOP_FLAG = False
                    USER_CHOICE = 'Quit'
                    
                    return USER_CHOICE, None, None, None, None, None
                else:
                    # ABSOLUTE PATH ASSIGNMENT
                    SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, ERROR, DIRECTORY_EXISTS = absolute_path_assignment(ROOT_PATH, DATE)
                    if DIRECTORY_EXISTS == False and ERROR == False:
                        # FUNCTION EXIT
                        print('\nSuccess!')
                        time.sleep(1)
                        loading_timer(3)
                        FIRST_LAYER_FLAG = False
                        NEW_LOOP_FLAG = False
                        USER_CHOICE = 'New'
                        
                        return USER_CHOICE, SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, DATE
                    if DIRECTORY_EXISTS == True:
                        print('\nPlease choose another directory.\nThere is a chance of overwriting data if using a\
 previously created directory.')
                        time.sleep(2)
                        loading_timer(3)
                    if ERROR == True:
                        print('Something went wrong during the creation of the directories.\nPlease check syntax, and try\
 again.')
                        time.sleep(2)
                        loading_timer(3)
        elif START_DECISION.lower() in ['l', 'o', 'old', 'load', 'older']:
            LOAD_LOOP_FLAG = True
            while LOAD_LOOP_FLAG == True:
                loading_timer(3)
                print('This Wordcrunch program must have the existing directory with these exact subdirectories to correctly\
 load its data:\n\n\t\t\'MM_DD_YY_Wordcrunch_Data\' - the main directory. Where:\n\t\t\t\'MM\' - is the month in which the\
 previous scrape took place\n\t\t\t\'DD\' - is the day in which the previous scrape took place\n\t\t\t\'YY\' - is the year in\
 which the previous scrape took place\n\n\t\t\'Raw_txt_Folder\' - subdirectory where the raw text scrape data is saved\n\t\t\
\'xlsx_Folder\' - subdirectory where the Excel spreadsheet from each processed subReddit is saved\n\t\t\'Wordcrunch_Totals\'\
 - subdirectory where the total processed text is saved\n')
                time.sleep(3)
                loading_timer(7)
                print('Please determine the absolute path to the main directory from which you would like to load Wordcrunch\
 the data.\nOr type\'Quit\' to quit.')
                LOAD_PATH = input('EXAMPLE: \'C:\\Users\\SMITH\\Documents\\{}_Wordcrunch_Data\'\n[Absolute Path/Quit]\n\n'\
                                  .format(DATE))
                if LOAD_PATH.lower() in ['q', 'quit']:
                    loading_timer(4)
                    FIRST_LAYER_FLAG = False
                    LOAD_LOOP_FLAG = False
                    USER_CHOICE = 'Quit'
                    
                    return USER_CHOICE, None, None, None, None, None
                else:
                    # ABSOLUTE PATH CHECK AND ASSIGNMENT
                    SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, LOAD_DATE, ERROR, SESSION_PATH_EXISTS, TXT_PATH_EXISTS, XLSX_PATH_EXISTS,\
                    END_PATH_EXISTS = load_path_assignment(LOAD_PATH)
                    if ERROR:
                        # FUNCTION RESTART
                        pass
                    if SESSION_PATH_EXISTS and TXT_PATH_EXISTS and XLSX_PATH_EXISTS and END_PATH_EXISTS:
                        # FUNCTION EXIT
                        print('\nSuccess!')
                        time.sleep(1)
                        loading_timer(3)
                        FIRST_LAYER_FLAG = False
                        LOAD_LOOP_FLAG = False
                        USER_CHOICE = 'Load'
                        
                        return USER_CHOICE, SESSION_PATH, TXT_PATH, XLSX_PATH, END_PATH, LOAD_DATE
        elif START_DECISION.lower() in ['q', 'quit']:
            # FUNCTION EXIT
            time.sleep(1)
            USER_CHOICE = 'Quit'
            FIRST_LAYER_FLAG = False
            
            return USER_CHOICE, None, None, None, None, None
        else:
            # FUNCTION RESTART
            print('Please check for correct syntax and spelling.')
            time.sleep(2)
            loading_timer(4)