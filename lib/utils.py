from TikTokApi import TikTokApi
import pandas as pd

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    #print("\033[A                             \033[A")
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

def datasetHelper(tiktoks):
    rows = []
    for tiktok in tiktoks:
        _row = {}
        for key in tiktok:
            elem = tiktok.get(key)
            if isinstance(elem, dict) or isinstance(elem, list):
                if isinstance(elem, list):
                    elem = elem[0]
                for elem_k in elem:
                    _row[key + "_" + elem_k] = str(elem.get(elem_k)).replace(";", "")
            else:
                _row[key] = str(elem).replace(";", "")
        rows.append(_row)
    return pd.json_normalize(rows)

def checkAvLikedPerc(api, dataset, _iter = 0): # prints tiktok liked list availability
    counter = 0
    ct = 0
    df = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";")
    den = df.shape[0]
    if _iter > 0: # _iter != default
        den = _iter
    for index, row in df.iterrows():
        counter += len(api.userLiked(row['author_id'],row['author_secUid'],count=1))
        ct += 1
        if ct == _iter and den == _iter:
            break # stop loop if target
    print("\n\nAvailability: " + str(round((counter/den)*100, 2)) + "% (" + str(counter) + "/" + str(den) + ")")