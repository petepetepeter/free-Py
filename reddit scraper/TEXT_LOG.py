import os
import pandas


# READS '.txt' TOP100 FILE AND RETURNS A SINGLE DICTIONARY WITH EVERY WORDCRUNCH SUBREDDIT SCRAPE
def top100_word_count_txt_file_to_dictionary(SESSION_PATH):
    TOP100_DICT = {}
    TEMP_NAME = []
    TEMP_VALUES = []
    # LOAD 'TOP100_Common_Words.txt' FILE
    with open('{}subReddit_TOP100_Words.txt'.format(SESSION_PATH), 'r', encoding = 'utf-8') as TOP100_WORDS_FILE:
        TEXT_DUMP = TOP100_WORDS_FILE.read()
    TEXT_LIST = TEXT_DUMP
    TEXT_LIST = TEXT_LIST.split(']')
    # SEPARATE THE ENTRIES TO STRINGS OF SUBREDDIT NAME AND TOP100 WORD/COUNT
    for ELEMENT in TEXT_LIST:
        ELEMENT = ELEMENT.replace('{', '').replace('}', '').replace('[', '').replace('\'', '').replace(',', '').replace('\n', '')
        ELEMENT = ELEMENT.split(':', 1)
        if len(ELEMENT) > 1:
            TEMP_NAME.append(ELEMENT[0].strip())
            TEMP_VALUES.append(ELEMENT[1].replace(':', '').split())
    # TURN STRINGS INTO FUNCTIONING DICTIONARIES
    for LIST in range(len(TEMP_VALUES)):
        TEMP_WORD = []
        TEMP_COUNT = []
        counter = 0
        for ELEMENT in TEMP_VALUES[LIST]:
            counter += 1
            if counter % 2 != 0:
                TEMP_WORD.append(ELEMENT)
            if counter % 2 == 0:
                TEMP_COUNT.append(int(ELEMENT))
        TOP100_DICT[TEMP_NAME[LIST]] = [{ELEMENT[0]:ELEMENT[1]}for ELEMENT in zip(TEMP_WORD,TEMP_COUNT)]
    
    return TOP100_DICT



# GETS NUMBERS OFF INDIVIDUAL WORD COUNT '.txt'
def individual_word_count_txt_file_to_dictionary(SESSION_PATH):
    TOTAL_COUNT_DICT = {}
    TEMP_NAME = []
    TEMP_VALUES = []
    # LOAD Individual_Word_Count.txt' FILE
    with open('{}All_Data_Individual_Word_Count.txt'.format(SESSION_PATH), 'r', encoding = 'utf-8') as TOP100_WORDS_FILE:
        TEXT_DUMP = TOP100_WORDS_FILE.read()
    TEXT_LIST = TEXT_DUMP
    TEXT_LIST = TEXT_LIST.split(']')
    # SEPARATE THE ENTRIES TO STRINGS OF SUBREDDIT NAME AND TOP100 WORD/COUNT
    for ELEMENT in TEXT_LIST:
        ELEMENT = ELEMENT.replace('{', '').replace('}', '').replace('[', '').replace('\'', '').replace(',', '').replace('\n', '')
        ELEMENT = ELEMENT.split(':', 1)
        if len(ELEMENT) > 1:
            TEMP_NAME.append(ELEMENT[0].strip())
            TEMP_VALUES.append(ELEMENT[1].replace(':', '').split())
    # TURN STRINGS INTO FUNCTIONING DICTIONARIES
    for LIST in range(len(TEMP_VALUES)):
        TEMP_WORD = []
        TEMP_COUNT = []
        counter = 0
        for ELEMENT in TEMP_VALUES[LIST]:
            counter += 1
            if counter % 2 != 0:
                TEMP_WORD.append(ELEMENT)
            if counter % 2 == 0:
                TEMP_COUNT.append(int(ELEMENT))
        TOTAL_COUNT_DICT[TEMP_NAME[LIST]] = [{ELEMENT[0]:ELEMENT[1]}for ELEMENT in zip(TEMP_WORD,TEMP_COUNT)]
    
    return TOTAL_COUNT_DICT



def all_data_individual_word_count_totals_compiler(SUBREDDIT_RAW_NUMBERS_DICT):
    INDIVIDUAL_WORD_NUMBERS = {}
    for INDEX in range(len(SUBREDDIT_RAW_NUMBERS_DICT.values())):
        for WORD in list(SUBREDDIT_RAW_NUMBERS_DICT.values())[INDEX]:
            TEMP = 0
            try:
                TEMP = list(WORD.values())[0]
                INDIVIDUAL_WORD_NUMBERS[str(list(WORD.keys())[0])] += TEMP
            except:
                INDIVIDUAL_WORD_NUMBERS[str(list(WORD.keys())[0])] = list(WORD.values())[0]
    
    return INDIVIDUAL_WORD_NUMBERS


# TAKES A WORD TOTAL DICTIONARY AND RETURNS THE SORTED LIST IN DESCENDING ORDER
def wordcrunch_word_total_list_sorter(WORD_COUNT_DICT):
    # TEMP LIST TO HELP SORT FILES BY WORD COUNT TOTAL IN DESCENDING ORDER
    TEMP_LIST = []
    [TEMP_LIST.append('{} {}'.format(SUBREDDIT_NAME, WORD_COUNT)) for SUBREDDIT_NAME, WORD_COUNT in WORD_COUNT_DICT.items()]
    for ELEMENT in range(0, len(TEMP_LIST)):
        TEMP = TEMP_LIST[ELEMENT]
        TEMP2 = ELEMENT - 1
        # SORT DESCENDING ORDER BASED ON WORD COUNT TOTAL
        while (TEMP2 >= 0) and (int(TEMP_LIST[TEMP2].split()[1].strip()) < int(TEMP.split()[1].strip())):
            TEMP_LIST[TEMP2 + 1] = TEMP_LIST[TEMP2]
            TEMP2 = TEMP2 - 1
        TEMP_LIST[TEMP2 + 1] = TEMP
    
    return TEMP_LIST



# WILL UPDATE 'Word_Count_Totals.txt' 'TOP100_Common_Words.txt' 'Individual_Word_Count.txt' 
# WITH THE CURRENT FILE LISTING AND TOTAL NUMBERS PULLED FROM THE '.xlsx' FILES
def updtate_xlsx_totals_to_txt_function(SESSION_PATH, XLSX_PATH):
    TOTAL_XLSX_DUMP = [item for item in os.listdir(XLSX_PATH) if item.endswith('xlsx')]
    XLSX_TOTAL_WORD_COUNT_DICT = {}
    XLSX_TOP_100_WORDS_DICT = {}
    XLSX_INDIVIDUAL_WORD_COUNT = {}
    # THE TOTAL AMOUNT OF WORDS FROM A WORDCRUNCH XLSX FILE
    for FILE in TOTAL_XLSX_DUMP:
        DATAFRAME = pandas.read_excel('{}{}'.format(XLSX_PATH, FILE))
        SUM = sum(DATAFRAME[DATAFRAME.columns[1]].values)
        XLSX_TOTAL_WORD_COUNT_DICT[DATAFRAME.columns[1]] = SUM
        XLSX_TOP_100_WORDS_DICT[DATAFRAME.columns[1]] = [{DATAFRAME['Word'][INDEX] : DATAFRAME[DATAFRAME.columns[1]][INDEX]} for INDEX in range(len(DATAFRAME[:100]))]
        XLSX_INDIVIDUAL_WORD_COUNT[DATAFRAME.columns[1]] = [{DATAFRAME['Word'][INDEX] : DATAFRAME[DATAFRAME.columns[1]][INDEX]} for INDEX in range(len(DATAFRAME))]
    # FUNCTION RETURNS A WORD COUNT TOTALS LIST ORGANIZED BY DESCENDING ORDER
    TEMP_LIST = wordcrunch_word_total_list_sorter(XLSX_TOTAL_WORD_COUNT_DICT)

    # DELETE DICTIONARY IN ORDER TO RE-ORGANIZE FILES IN DESCENDING ORDER
    XLSX_TOTAL_WORD_COUNT_DICT = {}
    for FILE in TEMP_LIST:
        XLSX_TOTAL_WORD_COUNT_DICT[FILE.split()[0].strip()] = FILE.split()[1].strip()

    # OVERWRITE THE '.txt' OLD NUMBERS ARE LESS THAN NEW NUMBERS
    # WORD COUNT
    # READS TEXT FILE TO GET A TEXT DUMP TO BUILD A COMPARISON DICTIONARY
    with open('{}subReddit_Word_Count_Total.txt'.format(SESSION_PATH), 'r', encoding = 'utf-8') as WORD_COUNT_FILE:
        RAW_TEXT_DUMP = WORD_COUNT_FILE.read()
    RAW_TEXT_LIST = RAW_TEXT_DUMP.replace('\'', '').replace('{', '').replace('}', '').split(',')
    # DECLARE AND POPULATE COMPARISON DICTIONARY
    COMPARISON_WORD_COUNT_DICT = {}
    for ELEMENT in RAW_TEXT_LIST:
        COMPARISON_WORD_COUNT_DICT[ELEMENT.split(':')[0].strip()] = int(ELEMENT.split(':')[1].strip())
    if len(COMPARISON_WORD_COUNT_DICT) < len(XLSX_TOTAL_WORD_COUNT_DICT):
        # APPEND ENTRIES NOT FOUND ON LIST
        with open('{}subReddit_Word_Count_Total.txt'.format(SESSION_PATH), 'w', encoding = 'utf-8') as WORD_COUNT_FILE:
            print(XLSX_TOTAL_WORD_COUNT_DICT, file = WORD_COUNT_FILE)

    # TOP100 WORDS
    COMPARISON_TOP100_WORD_DICT = top100_word_count_txt_file_to_dictionary(SESSION_PATH)
    if len(COMPARISON_TOP100_WORD_DICT) < len(XLSX_TOP_100_WORDS_DICT):
        with open('{}subReddit_TOP100_Words.txt'.format(SESSION_PATH), 'w', encoding = 'utf-8') as TOP100_WORDS_FILE:
            print(XLSX_TOP_100_WORDS_DICT, file = TOP100_WORDS_FILE)
            
    # INDIVIDUAL WORDS
    COMPARISON_INDIVIDUAL_WORD_COUNT_DICT = individual_word_count_txt_file_to_dictionary(SESSION_PATH)
    if len(COMPARISON_INDIVIDUAL_WORD_COUNT_DICT) < len(XLSX_INDIVIDUAL_WORD_COUNT):
        with open('{}All_Data_Individual_Word_Count.txt'.format(SESSION_PATH), 'w', encoding = 'utf-8') as INDIVIDUAL_WORD_COUNT_FILE:
            print(XLSX_INDIVIDUAL_WORD_COUNT, file = INDIVIDUAL_WORD_COUNT_FILE)



# RECORDS TOTALS TO '.txt' FILE AFTER FIRST SCRAPE USING '.xlsx' FILE(S)
def record_xlsx_totals_to_txt_function(SESSION_PATH, XLSX_PATH):
    TOTAL_XLSX_DUMP = [item for item in os.listdir(XLSX_PATH) if item.endswith('xlsx')]
    XLSX_TOTAL_WORD_COUNT_DICT = {}
    XLSX_TOP_100_WORDS_DICT = {}
    XLSX_INDIVIDUAL_WORD_COUNT = {}
    # THE TOTAL AMOUNT OF WORDS FROM A WORDCRUNCH XLSX FILE
    for FILE in TOTAL_XLSX_DUMP:
        DATAFRAME = pandas.read_excel('{}{}'.format(XLSX_PATH, FILE))
        SUM = sum(DATAFRAME[DATAFRAME.columns[1]].values)
        XLSX_TOTAL_WORD_COUNT_DICT[DATAFRAME.columns[1]] = SUM
        XLSX_TOP_100_WORDS_DICT[DATAFRAME.columns[1]] = [{DATAFRAME['Word'][INDEX] : DATAFRAME[DATAFRAME.columns[1]][INDEX]} for INDEX in range(len(DATAFRAME[:100]))]
        XLSX_INDIVIDUAL_WORD_COUNT[DATAFRAME.columns[1]] = [{DATAFRAME['Word'][INDEX] : DATAFRAME[DATAFRAME.columns[1]][INDEX]} for INDEX in range(len(DATAFRAME))]
    # FUNCTION RETURNS A WORD COUNT TOTALS LIST ORGANIZED BY DESCENDING ORDER
    TEMP_LIST = wordcrunch_word_total_list_sorter(XLSX_TOTAL_WORD_COUNT_DICT)

    # DELETE DICTIONARY IN ORDER TO RE-ORGANIZE FILES IN DESCENDING ORDER
    XLSX_TOTAL_WORD_COUNT_DICT = {}
    for FILE in TEMP_LIST:
        XLSX_TOTAL_WORD_COUNT_DICT[FILE.split()[0].strip()] = FILE.split()[1].strip()
    
    with open('{}subReddit_Word_Count_Total.txt'.format(SESSION_PATH), 'w', encoding = 'utf-8') as WORD_COUNT_FILE:
        print(XLSX_TOTAL_WORD_COUNT_DICT, file = WORD_COUNT_FILE)
    with open('{}subReddit_TOP100_Words.txt'.format(SESSION_PATH), 'w', encoding = 'utf-8') as TOP100_WORDS_FILE:
            print(XLSX_TOP_100_WORDS_DICT, file = TOP100_WORDS_FILE)
    with open('{}All_Data_Individual_Word_Count.txt'.format(SESSION_PATH), 'w', encoding = 'utf-8') as INDIVIDUAL_WORD_COUNT_FILE:
            print(XLSX_INDIVIDUAL_WORD_COUNT, file = INDIVIDUAL_WORD_COUNT_FILE)