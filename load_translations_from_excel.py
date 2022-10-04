import openpyxl

def load_translations_from_excel(excel_path):
    print("Load previous  from excel " + excel_path)
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    # Create a dictionary of translations, the key is the path
    # The value is a tuple that contains the english and the translation
    translations=dict()

    # Build the dictionary
    for row in list(ws.rows)[1:]:
        [ path, english, translation ] = [ cell.value for cell in row ]
        translations[path] = (english, translation)

    return translations