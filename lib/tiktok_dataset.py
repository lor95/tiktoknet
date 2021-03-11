from TikTokApi import TikTokApi # api wrapper import https://github.com/davidteather/TikTok-Api
import pandas as pd
import json

def buildDatasetByHashtag(api, hashtag, _count=10000):
    rows = []
    tiktoks = api.byHashtag(hashtag, count=_count, custom_verifyFp="")
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
    print(pd.json_normalize(rows))
    pd.json_normalize(rows).to_csv("dataset/dataset_"+hashtag+".csv", sep=';', index=False)

def pubAuthList(api, dataset): # returns dataset of users with public liked tiktok's list
    df = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";")
    counter = 1
    size = df.shape[0]
    df1 = pd.DataFrame({'author_id': [], 'author_secUid': [], 'author_nickname': []}, dtype="string")
    for index, row in df.iterrows():
        print("Progress: "+str(counter)+"/"+str(size))
        counter += 1
        if len(api.userLiked(row['author_id'],row['author_secUid'],count=1)) > 0:
            tempDict = {'author_id': row['author_id'], 'author_secUid': row['author_secUid'], 'author_nickname': row['author_nickname']}
            df1 = df1.append(tempDict, ignore_index=True)
    df1.to_csv("dataset/authors/pubLiked_"+dataset+".csv", sep=";", index=False)
