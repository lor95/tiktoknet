from TikTokApi import TikTokApi
import pandas as pd

api = TikTokApi.get_instance(use_test_endpoints=True)

def checkAvLikedPerc(hashtag): # prints tiktok liked list availability
    counter = 0
    df = pd.read_csv("./dataset/dataset_"+hashtag+".csv", sep=";")
    for index, row in df.iterrows():
        counter += len(api.userLiked(row['author_id'],row['author_secUid'],count=1))
    print("\n\nAvailability: " + str(round((counter/df.shape[0])*100, 2)) + "% (" + str(counter) + "/" + str(df.shape[0]) + ")")