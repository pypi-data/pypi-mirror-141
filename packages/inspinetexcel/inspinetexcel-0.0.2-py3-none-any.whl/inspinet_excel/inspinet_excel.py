import itertools

def get_column_numbers(ws, header_row, col_dict, ResetCounters):
    '''This function check if all columns exist in provided worksheet, and will return their column number
        
        INPUT:
        ws - worksheet to check
        header_row - row number with header
        col_dict - dictionaly of columns name and their column number in worksheet
        ResetCounters - True or False, where True counters will be reset to zero
        
        OUTPUT is an array:
        True or False --- where True = all column headers found, and False where problem
        col_dict --- updated dict
        err_msg --- comment what was wrong
    '''

    if ws == None:
        return False
    
    if col_dict == None:
        return False
    
    if header_row == None:
        return False
    
    if not type(col_dict) == dict:
        return False

    if not type(ResetCounters) == bool:
        return False
    
    if not type(header_row) == int:
        return False
    
    if ResetCounters:
        for column in col_dict:
            col_dict[column] = 0 #reset counters
    
    tmp_header = {}
    err_msg = ''

    for col in range(1,ws.max_column+1):
        tmp_header.update({ col: str(ws.cell(row=header_row, column=col).value) })

    err = False
    try:
        for column in col_dict:
            for col in tmp_header:
                if str(tmp_header[col]) == column:
                    col_dict[column] = col
                    break
            if col_dict[column] == 0:
                err = True
                err_msg = str(err_msg) + "Missing column '" + str(column) + "' in sheet '" + str(ws.title) + "'. "
    except KeyError:
        err = True
        err_msg = "Missing column '" + str(column) + "' in sheet '" + str(ws.title) + "'. "
    if err == True:
        return False, col_dict, err_msg
    else:
        return True, col_dict, err_msg
        



        
        
def read_spreadsheet(ws, header_row):
    spreadsheet = {}
    ws_max_rows = ws.max_row
    ws_max_columns = ws.max_column
    for row in range(header_row,ws_max_rows+1):
        #if row % 10:
        #    screen("temp","loading spreadsheet copy to memory ["+str(round(row/ws_max_rows*100,1))+"%]     ")
        for col in range(1,ws_max_columns+1):
            
            tmp_xy = str(row)+'|'+str(col)
            tmp_value = ws.cell(row=row, column=col).value
            spreadsheet.update({str(tmp_xy):str(tmp_value)})
    #screen("debu","     loaded spreadsheet copy to memory [max rows: "+str(ws_max_rows+1)+", max columns: "+str(ws_max_columns+1)+", total: "+str(len(spreadsheet))+"]                         ")
    return spreadsheet




def dict_xy2(spreadsheet, criterias, columns):
    if len(criterias) > 3:
        return (0, None, "Error: Too many criterias (max 3 allowed)")
    if len(criterias) < 1:
        return (0, None, "Error: No criterias provided (min 1 required)")

    if len(criterias) == 3:
        result = [ [ first_col[:int(first_col.find('|'))], first_col[int(first_col.find('|'))+1:] ] for first_col, second_col in spreadsheet.items() if \
            ( \
                (second_col == str(criterias[0][1]) and first_col.endswith('|'+str(columns[criterias[0][0]]))) or \
                (second_col == str(criterias[1][1]) and first_col.endswith('|'+str(columns[criterias[1][0]]))) or \
                (second_col == str(criterias[2][1]) and first_col.endswith('|'+str(columns[criterias[2][0]])))
            )]
    elif len(criterias) == 2:
            result = [ [ first_col[:int(first_col.find('|'))], first_col[int(first_col.find('|'))+1:] ] for first_col, second_col in spreadsheet.items() if \
            ( \
                (second_col == str(criterias[0][1]) and first_col.endswith('|'+str(columns[criterias[0][0]]))) or \
                (second_col == str(criterias[1][1]) and first_col.endswith('|'+str(columns[criterias[1][0]])))
            )]
    elif len(criterias) == 1:
            result = [ [ first_col[:int(first_col.find('|'))], first_col[int(first_col.find('|'))+1:] ] for first_col, second_col in spreadsheet.items() if \
            ( \
                (second_col == str(criterias[0][1]) and first_col.endswith('|'+str(columns[criterias[0][0]])))
            )]
    else:
        return (0, None, "Error: No criterias provided (min 1 required)")

    tmp_result = sorted(result, key=lambda x: x[0])
    an_iterator = itertools.groupby(tmp_result, lambda x : x[0] )
    result2 = []
    for key, group in an_iterator:
        result2 += [[key, list(group)]]
    tmp_result = None

    result3 = [ [first_col, second_col] for first_col, second_col in result2 if \
        ( \
            (len(second_col) == len(criterias))
        )]
    
    result = None
    result2 = None
    return (len(result3), result3, '')
