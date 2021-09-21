import re
import pandas
from matplotlib.pyplot import *
from TEXT_LOG import *

def grouping_chi_squared(SESSION_PATH, XLSX_PATH, SUBREDDIT, GROUPING = 15):
    # DECLARATIONS
    INDIVIDUAL_SUBREDDIT_TOTAL_WORD_COUNT_DICT = {}
    DATAFRAME1 = pandas.read_excel('{}{}.xlsx'.format(XLSX_PATH, SUBREDDIT))
    # LOAD SUBREDDIT TOTAL WORD COUNT NUMBERS FROM '.txt' FILE
    with open('{}subReddit_Word_Count_Total.txt'.format(SESSION_PATH), 'r', encoding = 'utf-8') as WORD_COUNT_FILE:
        RAW_TEXT_DUMP = WORD_COUNT_FILE.read()
    RAW_TEXT_LIST = RAW_TEXT_DUMP.replace('\'', '').replace('{', '').replace('}', '').split(',')
    # POPULATE DICTIONARY
    for ELEMENT in RAW_TEXT_LIST:
        INDIVIDUAL_SUBREDDIT_TOTAL_WORD_COUNT_DICT[ELEMENT.split(':')[0].strip()] = int(ELEMENT.split(':')[1].strip())
    # LOAD SUBREDDIT INDIVIDUAL WORD COUNT TOTALS DICTIONARY FROM '.txt' FILES
    ALL_DATA_RAW_INDIVIDUAL_WORD_COUNT = individual_word_count_txt_file_to_dictionary(SESSION_PATH)
    # COMBINE ALL INDIVIDUAL SUBREDDITS TO A GRAND TOTAL FOR EACH INDIVIDUAL WORD
    ALL_DATA_CLEANED_INDIVIDUAL_WORD_COUNT = all_data_individual_word_count_totals_compiler(ALL_DATA_RAW_INDIVIDUAL_WORD_COUNT)
    # MAKE DATAFRAME FROM DICTIONARY
    WORD_DATAFRAME = pandas.DataFrame.from_dict(ALL_DATA_CLEANED_INDIVIDUAL_WORD_COUNT, orient = 'index', columns = ['All Data'])
    WORD_DATAFRAME = WORD_DATAFRAME.rename_axis('Word')
    # MAKE A MERGED DATAFRAME FROM THE 'SUBREDDIT' DATAFRAME AND THE COLLECTION OF DATA
    MERGED = pandas.merge(DATAFRAME1, WORD_DATAFRAME, how = 'inner', on = ['Word'])
    WORD_VISIBLE = MERGED
    MERGED = MERGED[[DATAFRAME1.columns[1], 'All Data']]
    START = 0
    END = 0
    FIND = 0
    FAIL = 0
    FAILED_LIST = []
    # THIS GOES THROUGH 'MERGED' DATAFRAME IN GROUPINGS OF SIZE 'GROUPING' TO FIND THE CHI SQUARE NUMBER
    for NUM_COUNT in range(len(MERGED[::GROUPING])):
        # MOVING 'START' AND 'END' BY AMOUNT 'GROUPING'
        END += GROUPING
        if len(MERGED.iloc[START:END]) > 10:
            chi2, p, dof, expected = chi2_contingency(MERGED.iloc[START:END].T)
            if p < 0.05:
                # IF CHI SQUARED SHOWS A RELATIONSHIP
                FIND += 1
            else:
                # IF CHI SQUARED FAILS TO SHOW A RELATIONSHIP
                RESULT = zip(WORD_VISIBLE['Word'][START:END].values, [[NUMBER[0], NUMBER[1]] for NUMBER in MERGED.iloc[START:END]\
                                                                      [[MERGED.columns[0], MERGED.columns[1]]].values])
                FAILED_LIST.append([WORD for WORD in RESULT])
                FAIL += 1
        # MOVING 'START' AND 'END' BY AMOUNT 'GROUPING'
        START += GROUPING
    if FAIL > 0:
        WORDS = []
        [WORDS.append(WORD) for LIST in FAILED_LIST for WORD in LIST]
        # EXPORT THE SUBREDDIT'S FAILED LIST TO '.txt'
        with open('{}CHI_SQUARED_FAILED.txt'.format(SESSION_PATH), 'a', encoding = 'utf-8') as FILE:
            print('subReddit: {}\nIndividual Words: {}\nTotal Word Count: {}\nGroup Size: {}\nRelationships: {}\nFailures: {}\
\nWords: {}\n'.format(DATAFRAME1.columns[1], len(MERGED), sum(MERGED[MERGED.columns[0]]), GROUPING, FIND, FAIL, WORDS), file = FILE)



def chi_zip(TEMP_LIST_LIST):
    # THIS REFORMATS STRING TO INTEGERS FOR THE 'WORD' SECTION OF THE DICITONARY
    TEMP_WORD_LIST = []
    TEMP_NUMBERS_LIST = []
    WORDS_LIST = []
    LIST = TEMP_LIST_LIST[1 : -1]
    [TEMP_WORD_LIST.append(WORD) for WORD in re.findall('(?<=\(\').*?(?=\')', LIST)]
    [TEMP_NUMBERS_LIST.append(NUMBER_LIST) for NUMBER_LIST in re.findall('(?<=\[).*?(?=\])', LIST)]
    for NUMBER in range(len(TEMP_NUMBERS_LIST)):
        TEMP_NUMBERS_LIST[NUMBER] = TEMP_NUMBERS_LIST[NUMBER].replace(',', '').split()
        TEMP_NUMBERS_LIST[NUMBER] = [int(TEMP_NUMBERS_LIST[NUMBER][0]), int(TEMP_NUMBERS_LIST[NUMBER][1])]
    WORDS_LIST = zip(TEMP_WORD_LIST, TEMP_NUMBERS_LIST)
    
    # THIS APPLIES THE LIST OF TUPLES TO THE FUNCTION CALL
    return [TUPLE for TUPLE in WORDS_LIST]



def chi_txt_reader(SESSION_PATH):
    # DECLARATIONS
    with open('{}CHI_SQUARED_FAILED.txt'.format(SESSION_PATH), 'r', encoding = 'utf-8') as FILE:
        CHI_TXT = FILE.read()
    FAILURE_DICTIONARY = {}
    SUBREDDIT_NAME_LIST = []
    INDIVIDUAL_WORD_LIST = []
    TOTAL_WORD_LIST = []
    GROUP_SIZE_LIST = []
    RELATIONSHIPS_LIST = []
    FAILURES_LIST = []
    TEMP_LIST_LIST = []
    # USING REGULAR EXPRESSIONS TO FILTER THE '.txt' FILE INTO INDIVIDUAL LISTS
    [SUBREDDIT_NAME_LIST.append(NAME) for NAME in re.findall('(?<=subReddit: ).*?(?=\\n)', CHI_TXT)]
    [INDIVIDUAL_WORD_LIST.append(COUNT) for COUNT in re.findall('(?<=Individual Words: ).*?(?=\\n)', CHI_TXT)]
    [TOTAL_WORD_LIST.append(COUNT) for COUNT in re.findall('(?<=Total Word Count: ).*?(?=\\n)', CHI_TXT)]
    [GROUP_SIZE_LIST.append(GROUPING_SIZE) for GROUPING_SIZE in re.findall('(?<=Group Size: ).*?(?=\\n)', CHI_TXT)]
    [RELATIONSHIPS_LIST.append(COUNT) for COUNT in re.findall('(?<=Relationships: ).*?(?=\\n)', CHI_TXT)]
    [FAILURES_LIST.append(COUNT) for COUNT in re.findall('(?<=Failures: ).*?(?=\\n)', CHI_TXT)]
    [TEMP_LIST_LIST.append(TEMP_LIST) for TEMP_LIST in re.findall('(?<=Words: )\[.*?\](?=\\n)', CHI_TXT)]
    # LISTS TO DICITONARY
    for ELEMENT in range(len(SUBREDDIT_NAME_LIST)):
        FAILURE_DICTIONARY[SUBREDDIT_NAME_LIST[ELEMENT]] = {'Individual Words' : INDIVIDUAL_WORD_LIST[ELEMENT],
                                                        'Total Word Count' : TOTAL_WORD_LIST[ELEMENT],
                                                        'Group Size' : GROUP_SIZE_LIST[ELEMENT],
                                                        'Relationships' : RELATIONSHIPS_LIST[ELEMENT],
                                                        'Failures' : FAILURES_LIST[ELEMENT],
                                                        'Words' : chi_zip(TEMP_LIST_LIST[ELEMENT])}
    
    return FAILURE_DICTIONARY



def chi_bargraph(SUBREDDIT, DICTIONARY, SESSION_PATH):
    # DECLARATIONS
    INDIVIDUAL_WORDS = DICTIONARY['Individual Words']
    TOTAL_WORD_COUNT = DICTIONARY['Total Word Count']
    WORDS_LIST = []
    [WORDS_LIST.append(WORD[0]) for WORD in DICTIONARY['Words']]
    OBSERVED_NUM_LIST = []
    [OBSERVED_NUM_LIST.append(OBSERVED[1][0]) for OBSERVED in DICTIONARY['Words']]
    TOTAL_NUM_LIST = []
    [TOTAL_NUM_LIST.append(TOTAL[1][1]) for TOTAL in DICTIONARY['Words']]
    PD_DICT = {}
    PD_DICT['Word'] = WORDS_LIST
    PD_DICT['Observed'] = OBSERVED_NUM_LIST
    PD_DICT['Total'] = TOTAL_NUM_LIST
    # MAKE PANDAS DATAFRAME FROM DICTIONARY
    DF = pandas.DataFrame.from_dict(PD_DICT)
    DF = DF.rename_axis(SUBREDDIT)
    # DECLARE THE INFORMATIVE TEXT STATEMENT FOR THE BARGRAPH
    BOX_TEXT = 'Based on the frequency of their usage,\n there were {} words from a total of {}\n individual words used in \
\'/r/{}\' which failed\n to show a significant relationship (p > 0.05)\n to how frequently they appeared in the total\n data\
 sample taken on 10/31/20.'.format(len(DF), INDIVIDUAL_WORDS, SUBREDDIT)
    # IF SUBREDDIT'S BARGRAPH CAN DISPLAY THE WORDS LISTED ON THE Y-AXIS
    if len(DF) < 100:
        WORD_INDEX_NUMBERS = []
        [WORD_INDEX_NUMBERS.append(NUMBER) for NUMBER in DF[DF.columns[0]].index]
        FIGURE1, FIGURE1_AXIS = matplotlib.pyplot.subplots(1, 1, constrained_layout = False, figsize = (20, 20))
        GRID_SPEC = FIGURE1.add_gridspec(2, 2, wspace = 0, hspace = 0)
        TEXT = FIGURE1.add_subplot(GRID_SPEC[0,1])
        TEXT.text(ha = 'right', x = .99, y = .65, s = BOX_TEXT, bbox = dict(boxstyle = 'round', facecolor = 'gray',\
                  alpha = 0.5), fontsize = 15)
        TEXT.set_axis_off()
        DF.plot(kind = 'barh', ax = FIGURE1_AXIS, legend = True).set_yticklabels(['{}'.format(DF.Word[NUMBER]) for\
                NUMBER in WORD_INDEX_NUMBERS], fontsize = 16)
        FIGURE1_AXIS.legend(['/r/{}'.format(SUBREDDIT), 'All Data'], prop = {'size' : 18})
        FIGURE1_AXIS.set_title('Word Frequency From /r/{}'.format(SUBREDDIT), fontsize = 20)
        FIGURE1_AXIS.set_ylabel('')
        matplotlib.pyplot.show()
    # IF THE BARGRAPH RETURNS TOO MANY 'FAILED' WORDS TO LABEL THE Y-AXIS
    else:
        WORD_INDEX_NUMBERS = []
        [WORD_INDEX_NUMBERS.append(NUMBER) for NUMBER in DF[DF.columns[0]].index]
        FIGURE1, FIGURE1_AXIS = matplotlib.pyplot.subplots(1, 1, constrained_layout = False, figsize = (20, 20))
        GRID_SPEC = FIGURE1.add_gridspec(2, 2, wspace = 0, hspace = 0)
        TEXT = FIGURE1.add_subplot(GRID_SPEC[0,1])
        TEXT.text(ha = 'right', x = .99, y = .6, s = '{}\n\n*Note: Too many words to label Y-axis.'.format(BOX_TEXT),\
                  bbox = dict(boxstyle = 'round', facecolor = 'gray', alpha = 0.5), fontsize = 15)
        TEXT.set_axis_off()
        DF.plot(kind = 'barh', ax = FIGURE1_AXIS, legend = True).set_yticklabels(['{}'.format(DF.Observed[NUMBER]) for\
                NUMBER in WORD_INDEX_NUMBERS],fontsize = 13)
        FIGURE1_AXIS.set_yticks([])
        FIGURE1_AXIS.legend(['/r/{}'.format(SUBREDDIT), 'All Data'], prop = {'size' : 18})
        FIGURE1_AXIS.set_title('Word Frequency From /r/{}'.format(SUBREDDIT), fontsize = 20)
        FIGURE1_AXIS.set_ylabel('')
        matplotlib.pyplot.show()

    matplotlib.pyplot.close('all')