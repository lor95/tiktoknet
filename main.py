from TikTokApi import TikTokApi
import lib.tiktok_dataset as td

challenges = { "itookanap": 
                {"name": "ITookANap",
                "url": "https://www.tiktok.com/@gunnarolla/video/6816020939759815942"} # original video
                # insert challenge here
            }

api = TikTokApi.get_instance(use_test_endpoints=True)

td.buildDatasetByHashtag(api, challenges["itookanap"]["name"], challenges["itookanap"]["url"], 10000)
td.pubAuthList(api, challenges["itookanap"]["name"])
td.checkConnections(api, challenges["itookanap"]["name"])
td.ETL(challenges["itookanap"]["name"])