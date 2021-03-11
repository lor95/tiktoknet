from TikTokApi import TikTokApi
import pandas as pd
import lib.utils as utils
import json

def buildDatasetByHashtag(api, hashtag, url_orig, _count=10000):
    tiktoks = api.byHashtag(hashtag, count=_count, custom_verifyFp="")
    df = utils.datasetHelper(tiktoks)
    _id = ""
    if url_orig:
        tiktok = api.getTikTokByUrl(url_orig)
        _id = tiktok["itemInfo"]["itemStruct"]["id"]
        if _id not in list(df["id"]):
            tiktokL = [tiktok["itemInfo"]["itemStruct"]]
            df = df.append(utils.datasetHelper(tiktokL), ignore_index = True)
    df['originalVideo'] = 0
    df.loc[df['id'] == _id, 'originalVideo'] = 1 # search for the original video and flag it
    df.to_csv("dataset/dataset_"+hashtag+".csv", sep=';', index=False)

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
