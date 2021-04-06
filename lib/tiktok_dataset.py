from TikTokApi import TikTokApi
from TikTokApi import browser
import pandas as pd
import lib.utils as utils
import os
import uuid
import logging

def ETL(dataset):
    dataset = dataset.split(",")[0]
    df = pd.read_csv("./dataset/dataset_"+dataset+"_connections.csv", sep=";")
    df = df[['id', 'createTime','video_id','video_duration','author_id','author_uniqueId',
    'author_nickname','author_verified','author_secUid','music_id','music_title',
    'music_authorName','stats_diggCount','stats_shareCount','stats_commentCount','stats_playCount',
    'duetInfo_duetFromId','authorStats_diggCount','authorStats_followingCount','authorStats_followerCount',
    'authorStats_heartCount','authorStats_videoCount','duetEnabled','originalVideo',
    'likedBy_id','likedBy_secUid','likedBy_uniqueId','idcopy']] # extract columns
    df['id'] = df['id'].astype("string")
    df['originalVideo'] = df['originalVideo'].fillna(0)
    try:
        df['createTime'] = pd.to_datetime(df['createTime']*1000, unit='ms') # convert to datetime
    except:
        print("createTime column already converted")
    df.loc[df['idcopy'] != '-','id'] = df['idcopy']
    df.drop(['idcopy'], axis=1, inplace=True)
    df.to_csv("dataset/dataset_"+dataset+"_connections_etl.csv", sep=';', index=False) #save filtered dataset

def checkConnections(api, dataset, count=0): #dataset is the hashtag
    list_of_tags = dataset.split(",")
    dataset = list_of_tags[0]
    logger = logging.getLogger()
    pd.options.mode.chained_assignment = None
    print("Generating connection's dataset. This operation may take a while...\n")
    if count == 0:
        df = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";")
        df['id'] = df['id'].astype("string")
        df['likedBy_id'] = "-"
        df['likedBy_secUid'] = "-"
        df['likedBy_uniqueId'] = "-"
        df['idcopy'] = "-"
    else:
        df = pd.read_csv("./dataset/dataset_"+dataset+"_connections.csv", sep=";", dtype="string")
    rowsAdded = 0
    if os.path.exists("./dataset/authors/pubLiked_"+dataset+".csv"):
        df1 = pd.read_csv("./dataset/authors/pubLiked_"+dataset+".csv", sep = ";", dtype="string")
        if count != 0:
            df1 = df1.tail(count)
    else:
        df1 = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";", dtype="string") # default 
    logger.disabled = True
    utils.printProgressBar(0, df1.shape[0], prefix = ' Parsing:', length = 40)
    for index, row in df1.iterrows(): # users with open liked list
        try:
            tiktoks = api.userLiked(row['author_id'],row['author_secUid'],count=10000)
            if(len(tiktoks) > 0):
                df2 = utils.datasetHelper(tiktoks)
                #df2.to_csv("./dataset/test_"+str(uuid.uuid4().hex)+".csv",sep=";",index=False)
                for index1, row1 in df2.iterrows(): # liked tiktoks
                    if any(row1["desc"].lower().find("#"+elem_.lower()) != -1 for elem_ in list_of_tags) and (row1["id"] not in list(df["id"])):
                        row1['likedBy_id'] = "-"
                        row1['likedBy_secUid'] = "-"
                        row1['likedBy_uniqueId'] = "-"
                        row1['idcopy'] = "-"
                        df = df.append(row1, ignore_index=True)
                        rowsAdded += 1
                    if row1["id"] in list(df["id"]):
                        if df.loc[df['id'] == row1["id"], 'likedBy_id'].iloc[:].values[0] == '-': # if cell equals "-" (empty)
                            df.loc[df['id'] == row1["id"], 'likedBy_id'] = row["author_id"]
                            df.loc[df['id'] == row1["id"], 'likedBy_secUid'] = row["author_secUid"]
                            df.loc[df['id'] == row1["id"], 'likedBy_uniqueId'] = row["author_uniqueId"]
                        else:
                            df_temp = df.loc[df['id'] == row1["id"]] # a tiktok is liked by more than a user
                            df_temp['idcopy'] = df_temp['id']
                            df_temp['id'] = df_temp['id'] + "_" + str(uuid.uuid4().hex)
                            df_temp["likedBy_id"] = row["author_id"]
                            df_temp["likedBy_secUid"] = row["author_secUid"]
                            df_temp["likedBy_uniqueId"] = row["author_uniqueId"]
                            df = df.append([df_temp], ignore_index=True)
                            rowsAdded += 1
            utils.printProgressBar(index+1, df1.shape[0], prefix = ' Parsing:', length = 40)
        except:
            browser.clean_playwright()
            api.clean_up() # cleans api and restart it
            api = TikTokApi.get_instance(use_test_endpoints=True)
    logger.disabled = False
    print("\n\nSaving data...")
    df.to_csv("dataset/dataset_"+dataset+"_connections.csv", sep=';', index=False)
    return rowsAdded # restituisci il numero di righe aggiunte ad ogni iterazione

def buildDatasetByHashtag(api, hashtag, url_orig, _count=10000):
    df = pd.DataFrame()
    for tag in hashtag.split(","):
        try:
            tiktoks = api.byHashtag(tag.lower(), count=_count, custom_verifyFp="")
            print("Downloaded "+str(len(tiktoks)) + " for '"+tag+"'")
            df = df.append(utils.datasetHelper(tiktoks))
        except Exception as ex:
            print("Api failed downloading data for hashtag: '"+tag+"'\nPlease wait...checking for more tags...")
    _id = ""
    if url_orig:
        tiktok = api.getTikTokByUrl(url_orig)
        _id = tiktok["itemInfo"]["itemStruct"]["id"]
        if _id not in list(df["id"]):
            tiktokL = [tiktok["itemInfo"]["itemStruct"]]
            df = df.append(utils.datasetHelper(tiktokL), ignore_index = True)
    df['originalVideo'] = 0
    df.loc[df['id'] == _id, 'originalVideo'] = 1 # search for the original video and flag it
    df.drop_duplicates(subset="id", keep="first", inplace=True)
    df.to_csv("dataset/dataset_"+hashtag.split(",")[0]+".csv", sep=';', index=False)

def pubAuthList(api, dataset, rows=0): # returns dataset of users with public liked tiktok's list
    dataset = dataset.split(",")[0]
    if rows == 0:
        df = pd.read_csv("./dataset/dataset_"+dataset+".csv", sep=";")
    else:
        df = pd.read_csv("./dataset/dataset_"+dataset+"_connections.csv", sep=";")
        df = df.tail(rows)
    if os.path.exists("./dataset/authors/pubLiked_"+dataset+".csv"):
        df1 = pd.read_csv("./dataset/authors/pubLiked_"+dataset+".csv", sep = ";", dtype="string")
    else:
        df1 = pd.DataFrame({'author_id': [], 'author_secUid': [], 'author_uniqueId': []}, dtype="string")
    logger = logging.getLogger()
    count = 0
    logger.disabled = True
    counter = 1
    size = df.shape[0]
    for index, row in df.iterrows():
        try:
            print("Parsing: "+str(counter)+"/"+str(size))
            counter += 1
            if len(api.userLiked(row['author_id'],row['author_secUid'],count=1)) > 0:
                tempDict = {'author_id': row['author_id'], 'author_secUid': row['author_secUid'], 'author_uniqueId': row['author_uniqueId']}
                if row['author_uniqueId'] not in df1['author_uniqueId'].iloc[:].values:
                    df1 = df1.append(tempDict, ignore_index=True)
                    if rows != 0:
                        count += 1
            #if df1.shape[0] == 2: # subset of users
                #break         
        except:
            print("Recovery mode.")
            browser.clean_playwright()
            api.clean_up() # cleans api and restart it
            api = TikTokApi.get_instance(use_test_endpoints=True)
    logger.disabled = False
    #df1.drop_duplicates(subset='author_uniqueId', keep='first', inplace=True)
    df1.to_csv("dataset/authors/pubLiked_"+dataset+".csv", sep=";", index=False)
    return count