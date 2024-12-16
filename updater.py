import gspread
import config
import json

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

    sheet = sheet_connect('putting_league', config.sheet_tabs['current_week'])
    
    cells = config.division_cells[f"{division}"]
    
    scores_from_sheet = sheet.batch_get([cells])
    scores_from_sheet = scores_from_sheet[0]
    
    scores_db = {}
    scores_html = ''

    for items in scores_from_sheet:
        print(items)
        try:
            scores_html += f"<tr><td scope='row'>{items[0]}</td><th class='name'>{items[1]}</th><td class='score'>{items[2]}</td></tr>"
        except IndexError:
            scores_html = ''

    scores_db = {
        'scores_html': scores_html,
    }

    log_json = json.dumps(scores_db)

    log_file = open(f"{config.db_path}/{division}_scores.json", "w")
    log_file.write(f"{log_json}\n")
    log_file.close()
    
    return True

for div in config.divisions:
    print(score_update(div))