from TikTokApi import TikTokApi
import lib.tiktok_dataset as td
import argparse
import os
import sys

parser = argparse.ArgumentParser(description = 'TikTok dataset generator.')
parser.add_argument('-rec', action = 'store', type = int,
                    help = 'Recovery mode',
                    metavar = '<recovery_mode>',
                    default = 0)
args = parser.parse_args()

challenges = { "itookanap": 
                {"name": "ITookANap",
                "url": "https://www.tiktok.com/@gunnarolla/video/6816020939759815942"} # original video
                # insert challenge here
            }

api = TikTokApi.get_instance(use_test_endpoints=True)

sys.argv = sys.argv[:1] 

if args.rec == 0:
    td.buildDatasetByHashtag(api, challenges["itookanap"]["name"], challenges["itookanap"]["url"], 10000)
try:
    td.pubAuthList(api, challenges["itookanap"]["name"], args.rec)
except Exception as ex:
    sys.argv.append("-rec")
    sys.argv.append(str(ex.args[0]))
    os.execv(sys.executable, [sys.executable] + sys.argv) # recovery mode
# recovery mode anche sotto??
td.checkConnections(api, challenges["itookanap"]["name"])
td.ETL(challenges["itookanap"]["name"])