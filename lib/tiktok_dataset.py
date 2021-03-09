from TikTokApi import TikTokApi # api wrapper import https://github.com/davidteather/TikTok-Api
import pandas as pd
import json

api = TikTokApi.get_instance(use_test_endpoints=True)

def buildDatasetByHashtag(hashtag, _count):
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
