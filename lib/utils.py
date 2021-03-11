from TikTokApi import TikTokApi
import pandas as pd

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