from TikTokApi import TikTokApi
import pandas as pd
import lib.utils as utils
import os
import uuid

def ETL(dataset):
    df = pd.read_csv("./dataset/dataset_"+dataset+"_connections.csv", sep=";")
    df = df[['id', 'createTime','video_id','video_duration','author_id','author_uniqueId',
    'author_nickname','author_verified','author_secUid','music_id','music_title',
    'music_authorName','stats_shareCount','stats_commentCount','stats_playCount',
    'duetInfo_duetFromId','authorStats_followingCount','authorStats_followerCount',
    'authorStats_heartCount','authorStats_videoCount','duetEnabled','originalVideo',
    'likedBy_id','likedBy_secUid','likedBy_nickname','idcopy']] # extract columns
    df['originalVideo'] = df['originalVideo'].fillna(0)
    try:
        df['createTime'] = pd.to_datetime(df['createTime']*1000, unit='ms') # convert to datetime
    except:
        print("createTime column already converted")
    df.to_csv("dataset/dataset_"+dataset+"_connections.csv", sep=';', index=False) #save filtered dataset

def checkConnections(api, dataset): #dataset is the hashtag
    df = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";")
    df['likedBy_id'] = "NaN"
    df['likedBy_secUid'] = "NaN"
    df['likedBy_nickname'] = "NaN"
    df['idcopy'] = "NaN"
    #print(df)
    if os.path.exists("./dataset/authors/pubLiked_"+dataset+".csv"):
        df1 = pd.read_csv("./dataset/authors/pubLiked_"+dataset+".csv", sep = ";")
    else:
        df1 = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";") # default
    for index, row in df1.iterrows(): # users with open liked list
        tiktoks = api.userLiked(row['author_id'],row['author_secUid'],count=10000)
        if(len(tiktoks) > 0):
            df2 = utils.datasetHelper(tiktoks)
            #df2.to_csv("./dataset/test_"+str(uuid.uuid4().hex)+".csv",sep=";",index=False)
            for index, row1 in df2.iterrows(): # liked tiktoks
                if (row1["desc"].lower().find(dataset.lower()) != -1) and (row1["id"] not in list(df["id"])): 
                    df = df.append(row1, ignore_index=True)
                if row1["id"] in list(df["id"]):
                    if pd.isnull(df.loc[df['id'] == row1["id"], 'likedBy_id'].iloc[:].values): # if cell is empty
                        df.loc[df['id'] == row1["id"], 'likedBy_id'] = row["author_id"]
                        df.loc[df['id'] == row1["id"], 'likedBy_secUid'] = row["author_secUid"]
                        df.loc[df['id'] == row1["id"], 'likedBy_nickname'] = row["author_nickname"]
                    else:
                        df_temp = df.loc[df['id'] == row1["id"]] # TESTARE (CASO IN CUI UN VIDEO è PIACIUTO A PIù DI UN UTENTE)
                        df_temp['idcopy'] = df_temp['id']
                        df_temp['id'] = df_temp['id'] + "_" + str(uuid.uuid4().hex)
                        df_temp["likedBy_id"] = row["author_id"]
                        df_temp["likedBy_secUid"] = row["author_secUid"]
                        df_temp["likedBy_nickname"] = row["author_nickname"]
                        df = df.append([df_temp], ignore_index=True)
    #df.drop_duplicates(keep='first',inplace=True)
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
        #if df1.shape[0] == 15: # subset of users
            #break           
    df1.drop_duplicates(keep='first',inplace=True)
    df1.to_csv("dataset/authors/pubLiked_"+dataset+".csv", sep=";", index=False)