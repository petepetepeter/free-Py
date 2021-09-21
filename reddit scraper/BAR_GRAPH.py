import re
import pandas
import matplotlib.pyplot


# CALCULATING THE LETTER FREQUENCIES
# RETURNS A DICTIONARY TO USE IN BAR GRAPH
def subreddit_lettercrunch(END_PATH, SUBREDDIT):
    LETTER_DICT = {}
    TOTALS = []
    with open('{}{}_WordCrunch.txt'.format(END_PATH, SUBREDDIT.lower()), 'r', encoding = 'utf-8') as LETTER_CRUNCH:
        LINES = LETTER_CRUNCH.read()
    # USE RegEX TO SEPARATE SPECIFIC LINES
    LETTER_LIST = re.findall('([A-Z]: \d*?)\n', LINES)
    # MAKE FIRST ENTRY IN 'LETTER_DICT'
    LETTER_DICT['Total'] = 0
    # POPULATE 'LETTER_DICT'
    for LINE in LETTER_LIST:
        LETTER_DICT[LINE.split(':')[0].strip()] = LINE.split(':')[1].strip()
    # CALCULATE TOTAL LETTER COUNT FROM SCRAPE
    for LETTER, LETTER_COUNT in LETTER_DICT.items():
        TOTALS.append(int(LETTER_COUNT))
    TOTAL_LETTER_COUNT = sum(TOTALS)
    # EDIT FIRST ENTRY IN 'LETTER_DICT'
    LETTER_DICT['Total'] = TOTAL_LETTER_COUNT
    # APPEND CALCULATED PERCENTAGE
    for LETTER, LETTER_COUNT in LETTER_DICT.items():
        if LETTER != 'Total':
            LETTER_DICT[LETTER] = '{}:{} %'.format(LETTER_COUNT, round((int(LETTER_COUNT) / int(LETTER_DICT['Total'])) * 100, 2))
    
    return LETTER_DICT



# SORTING ALGORITH TO ORGANIZE DATAFRAME AND COMMON WORD INTERSECTION
# RETURNS LIST TO POPULATE BAR GRAPH
def letter_rank_sort(DICT):
    # DECLARATION
    LETTER_TEMP = []
    # TRANSFER DICTIONARY TO LIST
    for LETTER, LETTER_COUNT in DICT.items():
        if LETTER != 'Total':
            LETTER_TEMP.append(f"{LETTER}:{LETTER_COUNT.split(':')[0].strip()}:{LETTER_COUNT.split(':')[1].strip()}")
    for ELEMENT in range(0, len(LETTER_TEMP)):
        TEMP = LETTER_TEMP[ELEMENT]
        TEMP2 = ELEMENT - 1
        # SORT BASED ON TOTAL LETTERS COUNTED
        while (TEMP2 >= 0) and (int(LETTER_TEMP[TEMP2].split(':')[1].strip()) < int(TEMP.split(':')[1].strip())):
            LETTER_TEMP[TEMP2 + 1] = LETTER_TEMP[TEMP2]
            TEMP2 = TEMP2 - 1
        LETTER_TEMP[TEMP2 + 1] = TEMP

    return LETTER_TEMP



# ORGANIZES DATAFRAME AND 'COMMON' WORDS INTERSECTION IN ASCENDING ORDER
def word_rank_sort(LIST):
    for ELEMENT in range(0, len(LIST)):
        TEMP = LIST[ELEMENT]
        TEMP2 = ELEMENT - 1
        # SORT BASED ON RANK FROM WIKIPEDIA LIST
        while (TEMP2 >= 0) and (int(LIST[TEMP2][1:4].replace('-', ' ').strip()) > int(TEMP[1:4].replace('-', ' ').strip())):
            LIST[TEMP2 + 1] = LIST[TEMP2]
            TEMP2 = TEMP2 - 1
        LIST[TEMP2 + 1] = TEMP


# ORGANIZES 'COMMON' WORDS AND MERGED DATAFRAME COMPARISON IN DESCENDING ORDER
def comparison_word_rank_sort(LIST):
    for ELEMENT in range(0, len(LIST)):
        TEMP = LIST[ELEMENT]
        TEMP2 = ELEMENT - 1
        # SORT BASED ON RANK FROM WIKIPEDIA LIST
        while (TEMP2 >= 0) and (int(LIST[TEMP2].replace('-', '').replace('|', ' ').replace('(', '').replace(')', '').replace(\
                                'x', '').split()[1].strip()) < int(TEMP.replace('-', '').replace('|', ' ').replace('(', '')\
                                .replace(')', '').replace('x', '').split()[1].strip())):
            LIST[TEMP2 + 1] = LIST[TEMP2]
            TEMP2 = TEMP2 - 1
        LIST[TEMP2 + 1] = TEMP



# FUNCTION TO FIND THE RATIO COMPARISON BETWEEN THE DATAFRAME AND THE LIST OF COMMON ENGLISH WORDS FROM WIKIPEDIA
def top100_comparison(DATAFRAME, END_RANGE, COMMON_WORDS):
    # DECLARATIONS
    TEMP_NUMBER_COLLECTION = []
    # COLLECTION OF THE 'END_RANGE' NUMBER OF HIGHEST WORD COUNT FROM 'DATAFRAME'
    DATAFRAME_TOP100 = set(DATAFRAME[:END_RANGE].Word.values)
    # INTERSECTION OF TOP100 COMMON WORDS AND 'END_RANGE' NUMBER OF WORDS FROM 'DATAFRAME'
    DATAFRAME_COMMON_WORD_INTERSECTION = DATAFRAME_TOP100.intersection(set(COMMON_WORDS.values()))
    # UNION OF TOP100 COMMON WORDS AND 'END_RANGE' NUMBER OF WORDS FROM 'DATAFRAME'
    DATAFRAME_COMMON_WORD_UNION = DATAFRAME_TOP100.union(set(COMMON_WORDS.values()))
    # CALCULATING RANK SIMILARITY RATIO BETWEEN TOP100 COMMON WORDS LIST AND 'END_RANGE' NUMBER OF WORDS FROM 'DATAFRAME'
    for NUMBER in range(len(COMMON_WORDS)):
        if COMMON_WORDS[str(NUMBER + 1)] in DATAFRAME[:END_RANGE].Word.values:
            if NUMBER==DATAFRAME[DATAFRAME['Word']==COMMON_WORDS[str(NUMBER + 1 )]].index[0]:
                # EXACT RANKING MATCH
                TEMP_NUMBER_COLLECTION.append(100)
            else:
                # DIFFERENT RANKING, BUT ON LIST
                TEMP_NUMBER_COLLECTION.append(100 - len(range(min(NUMBER, DATAFRAME[DATAFRAME['Word'] == COMMON_WORDS[\
                                              str(NUMBER + 1 )]].index[0]), max(NUMBER, DATAFRAME[DATAFRAME['Word'] ==\
                                              COMMON_WORDS[str(NUMBER + 1)]].index[0]))))
        else:
            # WORD NOT IN 'DATAFRAME'
            TEMP_NUMBER_COLLECTION.append(0)
    # CALCULATIONS
    RANK_RATIO = sum(TEMP_NUMBER_COLLECTION) / 100
    JACCARD_INDEX = round(len(DATAFRAME_COMMON_WORD_INTERSECTION) / len(DATAFRAME_COMMON_WORD_UNION) * 100, 2)
    # CONVERT A SET TO A LIST
    DATAFRAME_COMMON_WORD_INTERSECTION = list(DATAFRAME_COMMON_WORD_INTERSECTION)
    
    return RANK_RATIO, JACCARD_INDEX, DATAFRAME_COMMON_WORD_INTERSECTION



# FUNCTION TO DELETE PLOT TICK MARKS
def remove_ticks(AXES):
    AXES.set_xticks([])
    AXES.set_yticks([])



# CREATE A BAR GRAPH OF THE 'TOP_NUM' OF COUNT OF WORDS USED IN THAT SUBREDDIT
def top_100_bargraph(XLSX_PATH, END_PATH, SUBREDDIT, COMMON_WORDS, END_RANGE = 100):
    # DECLARATIONS
    WORD_INDEX_NUMBERS = []
    YLABEL_TICK_RANGE = []
    # LOAD 'SUBREDDIT' DATAFRAME
    DATA_SET = pandas.read_excel('{}{}.xlsx'.format(XLSX_PATH, SUBREDDIT.lower()))
    # GET LETTER FREQUENCY STATISTICS FOR 'SUBREDDIT' WITH 'subreddit_lettercrunch'
    LETTER_FREQENCY_DICT = subreddit_lettercrunch(END_PATH, SUBREDDIT.lower())
    # CREATE A SORTED LIST OF LETTER FREQUENCY WITH 'letter_rank_sort'
    LETTER_LIST_RANKED = letter_rank_sort(LETTER_FREQENCY_DICT)
    # USE 'top100_comparison' FUNCTION TO RETURN WORD RANK RATIO, JACCARD SIMILARITY INDEX, 'DATA_SET' AND 'COMMON_WORDS' INTERSECTION
    RANK_RATIO, JACCARD_INDEX, COMMON_WORD_INTERSECTION = top100_comparison(DATA_SET, END_RANGE, COMMON_WORDS)
    # X-AXIS LABELS OF 'DataFrame.nlargest()' COUNTS
    [WORD_INDEX_NUMBERS.append(NUMBER) for NUMBER in DATA_SET.nlargest(END_RANGE, DATA_SET.columns[1]).index] 
    # BUILDING THE INTERSECTION LIST TO DISPLAY ON THE SECOND PLOT
    for COMMON_WORD in range(len(COMMON_WORD_INTERSECTION)):
        if COMMON_WORD_INTERSECTION[COMMON_WORD] in COMMON_WORDS.values():
            COMMON_WORD_INTERSECTION[COMMON_WORD] = '#{} - {} - (x{})'.format([RANK for RANK, WORD in COMMON_WORDS.items()\
                                                  if WORD == COMMON_WORD_INTERSECTION[COMMON_WORD]][0],\
                                                  COMMON_WORD_INTERSECTION[COMMON_WORD], DATA_SET.loc[DATA_SET['Word'] ==\
                                                  COMMON_WORD_INTERSECTION[COMMON_WORD], DATA_SET.columns[1]].values[0])
    # ORGANIZE 'COMMON_WORD_INTERSECTION' BASED ON THE WIKIPEDIA RANKINGS THROUGH A SIMPLE BUBBLE SORT
    word_rank_sort(COMMON_WORD_INTERSECTION)
    # RANGE FOR MAX TOTALS OF 'DataFrame.nlargest()' ITEMS FOR Y-AXIS
    [YLABEL_TICK_RANGE.append(NUMBER) for LIST in DATA_SET.nlargest(END_RANGE, DATA_SET.columns[1]).values for NUMBER in LIST[1:]]
    # BASE LEVEL PLOT FIGURE
    FIGURE1, FIGURE1_AXIS = matplotlib.pyplot.subplots(1, 1, constrained_layout = False, figsize = (30, 30))
    # DIVIDE THE BASE LEVEL PLOT FIGURE INTO A GRID
    GRID_SPEC = FIGURE1.add_gridspec(5, 3, wspace = 0, hspace = 0)
    # MAIN PLOT TITLE
    FIGURE1_AXIS.set_title('/r/{} Wordcrunch Statistics'.format(DATA_SET.columns[1]), fontsize = 35, pad = 10)
    # SPECIFY THE PLOT FROM PANDAS DATAFRAME 'DATA_SET'
    DATA_SET.nlargest(END_RANGE, DATA_SET.columns[1]).plot(kind = 'barh' ,fontsize = 30, ax = FIGURE1_AXIS, width = .5,\
                      grid = False, legend = False).set_yticklabels(DATA_SET.Word[[NUMBER for NUMBER in WORD_INDEX_NUMBERS]],\
                      fontsize = 22)
    # DECLARE SECOND PLOT CANVAS WITHIN THE FIRST BASE FIGURE
    FIGURE2 = FIGURE1.add_subplot(GRID_SPEC[0:4,2:])
    FIGURE2.set_axis_off()
    # A INDEX 'COUNTER' TO PLACE APPROPRIATE DATA AS LABEL ON EACH INDEPENDENT BAR
    WORD_INDEX_COUNTER = 0
    for RECTANGLE_PLOT in FIGURE1_AXIS.patches:
        # 'matplotlib.annotate()' FOR PLACING TEXT ON EACH BAR RECTANGLE
        FIGURE1_AXIS.annotate(DATA_SET[DATA_SET.columns[1]][WORD_INDEX_COUNTER], (RECTANGLE_PLOT.get_bbox().x1 + (RECTANGLE_PLOT\
                             .get_bbox().x1 * .02), RECTANGLE_PLOT.get_bbox().y1 - (RECTANGLE_PLOT.get_bbox().y1 -\
                             RECTANGLE_PLOT.get_bbox().y0)), rotation = 0, fontsize = 20)
        WORD_INDEX_COUNTER += 1
    # MAKING 4 SEPARATE TEXT LISTS MAPPED INTO 'FIGURE2'
    # 1ST
    FIGURE2.text(va = 'top', x = 1.01, y = 1.015, s = '\nCommon Words Found In \'{}\':\n      Wikipedia Rank --  Word  --\
SubReddit Count \n{}'.format(DATA_SET.columns[1], '\n'.join(COMMON_WORD_INTERSECTION[:25])), fontsize = 25)
    # 2ND
    FIGURE2.text(va = 'top', x = 1.01, y = .4192, s = '{}'.format('\n'.join(COMMON_WORD_INTERSECTION[25:50])), fontsize = 25)
    # 3RD
    FIGURE2.text(va = 'top', x = 1.55, y = .951, s = '{}'.format('\n'.join(COMMON_WORD_INTERSECTION[50:75])), fontsize = 25)
    # 4TH
    FIGURE2.text(va = 'top', x = 1.55, y = .4192, s = '{}'.format('\n'.join(COMMON_WORD_INTERSECTION[75:100])), fontsize = 25)
    # EXTRA STATISTICS RETURNED FROM 'top100()'
    FIGURE2.text(ha = 'right', x = .99, y = -.35, s = 'Jaccard Similarity: {}%\nWikipedia Rank Similarity: {}%'.format(\
                JACCARD_INDEX, RANK_RATIO), fontsize = 24)
    FIGURE3 = FIGURE1.add_subplot(GRID_SPEC[0:2,2:])
    FIGURE3_AXES = [[LETTER.split(':')[0], int(LETTER.split(':')[1])] for LETTER in LETTER_LIST_RANKED]
    pandas.DataFrame(FIGURE3_AXES, columns = ['Letter', 'Letter Count']).plot(kind = 'bar', legend = False, ax = FIGURE3,\
                                                                x = 'Letter', y = 'Letter Count', rot = 0, fontsize = 27)
    FIGURE3.set_xlabel('Letter Frequency', fontsize = 30)
    FIGURE1_AXIS.legend(fontsize = 30, loc = 'upper left', bbox_to_anchor = (-.015, -.029))
    # PLOTTING
    matplotlib.pyplot.show()

def comparison_bargraph(XLSX_PATH, END_PATH, SUBREDDIT_LIST, COMMON_WORDS, END_RANGE = 100):
    # DECLARATIONS
    WORD_INDEX_NUMBERS = []
    YLABEL_TICK_RANGE = []
    # LOAD FIRST AND SECOND 'SUBREDDIT' DATAFRAMES FOR COMPARISON GRAPH
    DATA_SET1 = pandas.read_excel('{}{}.xlsx'.format(XLSX_PATH, SUBREDDIT_LIST[0].lower()))
    DATA_SET2 = pandas.read_excel('{}{}.xlsx'.format(XLSX_PATH, SUBREDDIT_LIST[1].lower()))
    # MAKE 'FIRST' THE LARGER DATAFRAME, OTHERWISE DO NOTHING
    if len(DATA_SET1) < len(DATA_SET2):
        TRANSFER_DATAFRAME = DATA_SET1
        TRANSFER_NAME = SUBREDDIT_LIST[0].lower()
        DATA_SET1 = DATA_SET2
        SUBREDDIT_LIST[0] = SUBREDDIT_LIST[1].lower()
        DATA_SET2 = TRANSFER_DATAFRAME
        SUBREDDIT_LIST[1] = TRANSFER_NAME
    else:
        pass
    # GET FIRST AND SECOND LETTER FREQUENCY STATISTICS DICT WITH 'subreddit_lettercrunch'
    LETTER_FREQENCY_DICT1 = subreddit_lettercrunch(END_PATH, SUBREDDIT_LIST[0].lower())
    LETTER_FREQENCY_DICT2 = subreddit_lettercrunch(END_PATH, SUBREDDIT_LIST[1].lower())
    # CREATE A SORTED LIST OF LETTER FREQUENCY WITH 'letter_rank_sort'
    LETTER_LIST_RANKED1 = letter_rank_sort(LETTER_FREQENCY_DICT1)
    LETTER_LIST_RANKED2 = letter_rank_sort(LETTER_FREQENCY_DICT2)
    
    MERGE_DATAFRAME = pandas.merge(DATA_SET1[:END_RANGE], DATA_SET2[:END_RANGE], how = 'inner', on = ['Word'])
    
    # USE 'top100_comparison' FUNCTION TO RETURN WORD RANK RATIO, JACCARD SIMILARITY INDEX, 'DATA_SET' AND 'COMMON_WORDS' INTERSECTION
    RANK_RATIO, JACCARD_INDEX, COMMON_WORD_INTERSECTION = top100_comparison(MERGE_DATAFRAME, END_RANGE, COMMON_WORDS)
    # X-AXIS LABELS OF 'DataFrame.nlargest()' COUNT FROM 'MERGE_DATAFRAME.columns[1]'
    [WORD_INDEX_NUMBERS.append(NUMBER) for NUMBER in MERGE_DATAFRAME.nlargest(END_RANGE, MERGE_DATAFRAME.columns[1]).index] 
    # COMPARED TO WIKIPEDIA'S 'TOP100'
    for COMMON_WORD in range(len(COMMON_WORD_INTERSECTION)):
        if COMMON_WORD_INTERSECTION[COMMON_WORD] in COMMON_WORDS.values():
            COMMON_WORD_INTERSECTION[COMMON_WORD] = '{}  -  (x{})  |  (x{})'.format(COMMON_WORD_INTERSECTION[COMMON_WORD],\
                                                  MERGE_DATAFRAME.loc[MERGE_DATAFRAME['Word'] == COMMON_WORD_INTERSECTION[COMMON_WORD],\
                                                  MERGE_DATAFRAME.columns[1]].values[0], MERGE_DATAFRAME.loc[MERGE_DATAFRAME['Word'] ==\
                                                  COMMON_WORD_INTERSECTION[COMMON_WORD], MERGE_DATAFRAME.columns[2]].values[0])
    # ORGANIZE 'COMMON_WORD_INTERSECTION' BASED ON THE RANKINGS OF DATA_SET1
    comparison_word_rank_sort(COMMON_WORD_INTERSECTION)
    # RANGE FOR MAX TOTALS OF 'DataFrame.nlargest()' ITEMS FOR Y-AXIS
    [YLABEL_TICK_RANGE.append(NUMBER) for LIST in MERGE_DATAFRAME.nlargest(END_RANGE, MERGE_DATAFRAME.columns[1]).values for NUMBER in LIST[1:]]
    # BASE LEVEL PLOT FIGURE
    FIGURE1, FIGURE1_AXIS = matplotlib.pyplot.subplots(1, 1, constrained_layout = False, figsize = (30, 30))
    # DIVIDE THE BASE LEVEL PLOT FIGURE INTO A GRID
    GRID_SPEC = FIGURE1.add_gridspec(5, 3, wspace = 0, hspace = 0.11)
    # MAIN PLOT TITLE
    FIGURE1_AXIS.set_title('/r/{} vs /r/{} Wordcrunch'.format(DATA_SET1.columns[1], DATA_SET2.columns[1]), fontsize = 35,\
                           pad = 10)
    MERGE_DATAFRAME.plot(kind = 'barh' ,fontsize = 30, ax = FIGURE1_AXIS, width = .5, grid = False, legend = True)\
             .set_yticklabels(MERGE_DATAFRAME.Word[[NUMBER for NUMBER in WORD_INDEX_NUMBERS]], fontsize = 24)
    # DECLARE SECOND PLOT CANVAS WITHIN THE FIRST BASE FIGURE
    FIGURE2 = FIGURE1.add_subplot(GRID_SPEC[0:4,2:])
    FIGURE2.set_axis_off()
    # MAKING 4 SEPARATE TEXT LISTS MAPPED INTO 'FIGURE2'
    # 1ST
    FIGURE2.text(va = 'top', x = 1.01, y = 1.015, s = '\n            Wikipedia\'s Top100 \'Common\' Words:\n      \'Word\'   |\
    Set #1 Count   |   Set #2 Count   \n       /r/{} vs /r/{}\n\n{}'.format(SUBREDDIT_LIST[0].lower(), \
    SUBREDDIT_LIST[1].lower(), '\n'.join(COMMON_WORD_INTERSECTION[:25])),fontsize = 25)
    # 2ND
    FIGURE2.text(va = 'top', x = 1.01, y = .3517, s = '{}'.format('\n'.join(COMMON_WORD_INTERSECTION[25:50])), fontsize = 25)
    # 3RD
    FIGURE2.text(va = 'top', x = 1.65, y = .907, s = '{}'.format('\n'.join(COMMON_WORD_INTERSECTION[50:75])), fontsize = 25)
    # 4TH
    FIGURE2.text(va = 'top', x = 1.65, y = .3517, s = '{}'.format('\n'.join(COMMON_WORD_INTERSECTION[75:100])), fontsize = 25)
    # EXTRA STATISTICS RETURNED FROM 'top100()'
    FIGURE2.text(ha = 'right', x = .99, y = -.35, s = 'Jaccard Similarity: {}%\nWikipedia Rank Similarity: {}%'.format(\
                JACCARD_INDEX, RANK_RATIO), fontsize = 24)
    FIGURE3 = FIGURE1.add_subplot(GRID_SPEC[0:2,2:])
    FIGURE3_AXES = [[LETTER.split(':')[0], int(LETTER.split(':')[1])] for LETTER in LETTER_LIST_RANKED1]
    FIGURE3.set_ylabel('/r/{}'.format(SUBREDDIT_LIST[0]), fontsize = 28)
    FIGURE4 = FIGURE1.add_subplot(GRID_SPEC[2:4,2:])
    FIGURE4_AXES = [[LETTER.split(':')[0], int(LETTER.split(':')[1])] for LETTER in LETTER_LIST_RANKED2]
    FIGURE4.set_ylabel('/r/{}'.format(SUBREDDIT_LIST[1]), fontsize = 28)
    pandas.DataFrame(FIGURE3_AXES, columns = ['Letter', 'Letter Count']).plot(kind = 'bar', legend = False, ax = FIGURE3,\
                                                                x = 'Letter', y = 'Letter Count', rot = 0, fontsize = 27)
    pandas.DataFrame(FIGURE4_AXES, columns = ['Letter', 'Letter Count']).plot(kind = 'bar', legend = False, ax = FIGURE4,\
                                                                x = 'Letter', y = 'Letter Count', rot = 0, fontsize = 27)
    FIGURE4.set_xlabel('Letter Frequency', fontsize = 30)
    FIGURE1_AXIS.legend(fontsize = 30, loc = 'upper left', bbox_to_anchor = (-.015, -.029))
    # PLOTTING
    matplotlib.pyplot.show()