import json

import openpyxl


# Load the XLSX file
def convertJson(excel_file):

    wb = openpyxl.load_workbook(excel_file)

    # Select the first sheet
    sheet = wb.active

    # Get the data from the sheet as a list of dictionaries
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[6]== None:
            continue
        
        cclist = row[10].split(',')
        if "" in cclist:
            cclist.remove("")

        data.append({'fname': row[0], 'lname': row[1], 'address': row[2], 'city': row[3],'state': row[4],'zip': row[5],'email': row[6],'note': row[7],'product': row[8],'amount': row[9], 'cc': cclist})

    # Convert the data to a JSON string
    # json_data = json.dumps(data)

    # Print the JSON string
    # print(data)
    return data
