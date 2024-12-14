import gspread
import config

from datetime import datetime
from tinydb import TinyDB, Query

# Connect to google sheet and/or tab
def sheet_connect(sheet, tab = ''):
    sheet_connect = gspread.service_account(filename=f"{config.base_path}/credentials.json")
    sheet = sheet_connect.open_by_key(config.sheets[sheet])

    if tab == '':
        return sheet
    else:
        sheet_tab = sheet.worksheet(tab)
        # Return the sheet tab
        return sheet_tab

def score_update(division = ''):
    if division == '':
        return False

    # balance_log = general.sheet_connect('putting_league', config.sheet_tabs['putting_league'])
    sheet = sheet_connect('putting_league', config.sheet_tabs['current_week'])

    score_db = TinyDB(f"{config.db_path}/{division}_scores.json")
    score_db.truncate()
    
    cells = config.division_cells[f"{division}"]
    print(cells)
    scores_from_sheet = sheet.batch_get([cells])
    scores_from_sheet = scores_from_sheet[0]
    print(scores_from_sheet)
    details = {}

    for items in scores_from_sheet:
        # print(items)
        try:
            position = items[0]
        except IndexError:
            position = ''
        
        try:
            name = items[1]
        except IndexError:
            name = ''

        try:
            score = items[2]
        except IndexError:
            score = ''
        
        try:
            details[items[0]] = {
                'position':position,
                'name':name,
                'score':score,
            }
        except IndexError:
            error = ''

        try:
            score_db.insert(details)
            print('Successful db write')
            
        except ValueError as e:
            print(f"[DB Error] pro_scores.insert(): {e}")
        
        
    score_db.close()
    
    return True


for div in config.divisions:
    print(score_update(div))