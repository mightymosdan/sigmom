import pandas as pd

def parseExcelFile(filepath: str) -> dict:
    """

    Args:
        filepath:   str containing the path to the file being read

    Returns:

    """
    # Read in complete excel file
    xls = pd.ExcelFile(filepath)

    # Read in each individual sheet. Sheet nums are 0-indexed
    marela = pd.read_excel(xls, 1)
    marelaPANAS = pd.read_excel(xls, 2)
    daniel = pd.read_excel(xls, 3)
    danielPANAS = pd.read_excel(xls, 4)
    rainer = pd.read_excel(xls, 5)
    rainerPANAS = pd.read_excel(xls, 6)
    melissa = pd.read_excel(xls, 7)
    melissaPANAS = pd.read_excel(xls, 8)

    sheets = {}

    sheets["marela"] = marela
    sheets["marelaPANAS"] = marelaPANAS
    sheets["daniel"] = daniel
    sheets["danielPANAS"] = danielPANAS
    sheets["rainer"] = rainer
    sheets["rainerPANAS"] = rainerPANAS
    sheets["melissa"] = melissa
    sheets["melissaPANAS"] = melissaPANAS

    return sheets

if __name__ == '__main__':
    sheets = parseExcelFile("data.xlsx")
    print(sheets)