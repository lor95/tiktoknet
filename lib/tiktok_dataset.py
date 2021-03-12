from TikTokApi import TikTokApi
import pandas as pd
import lib.utils as utils
import os
import uuid

def checkConnections(api, dataset): #dataset is the hashtag
    df = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";")
    df['likedBy_id'] = ""
    df['likedBy_secUid'] = ""
    df['likedBy_nickname'] = ""
    df['idcopy'] = ""
    #print(df)
    if os.path.exists("./dataset/authors/pubLiked_"+dataset+".csv"):
        df1 = pd.read_csv("./dataset/authors/pubLiked_"+dataset+".csv", sep = ";")
    else:
        df1 = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";") # default
    for index, row in df1.iterrows():
        tiktoks = api.userLiked(row['author_id'],row['author_secUid'],count=10000)
        if(len(tiktoks) > 0):
            df2 = utils.datasetHelper(tiktoks)
            print(df2)
            for index, row in df2.iterrows():
                if row["desc"].lower().find(dataset.lower()) != -1: # check if row contains tiktoks
                    df = df.append(row, ignore_index=True)
                if row['id'] in list(df["id"]):
                    if not df.loc[df['id'] == row["id"], 'likedBy_id']: # if cell is empty
                        df.loc[df['id'] == row["id"], 'likedBy_id'] = row["author_id"]
                        df.loc[df['id'] == row["id"], 'likedBy_secUid'] = row["author_secUid"]
                        df.loc[df['id'] == row["id"], 'likedBy_nickname'] = row["author_nickname"]
                    else:
                        df_temp = df.loc[df['id'] == row["id"]]
                        df_temp['idcopy'] = df_temp['id']
                        df_temp['id'] = df_temp['id'] + "_" + str(uuid.uuid4().hex)
                        df_temp["likedBy_id"] = row["author_id"]
                        df_temp["likedBy_secUid"] = row["author_secUid"]
                        df_temp["likedBy_nickname"] = row["author_nickname"]
                        df = df.append([df_temp], ignore_index=True)
    df.drop_duplicates(inplace=True)
    df.to_csv("dataset/dataset_"+dataset+"_connections.csv", sep=';', index=False)
    #return True

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
        print("Parsing: "+str(counter)+"/"+str(size))
        counter += 1
        if len(api.userLiked(row['author_id'],row['author_secUid'],count=1)) > 0:
            tempDict = {'author_id': row['author_id'], 'author_secUid': row['author_secUid'], 'author_nickname': row['author_nickname']}
            df1 = df1.append(tempDict, ignore_index=True)
        #if df1.shape[0] == 4:
            #break           
    df1.drop_duplicates(inplace=True)
    df1.to_csv("dataset/authors/pubLiked_"+dataset+".csv", sep=";", index=False)
