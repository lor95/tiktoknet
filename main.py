from TikTokApi import TikTokApi
import lib.tiktok_dataset as td
import lib.challenges as challenge
import argparse

parser = argparse.ArgumentParser(description = 'TikTok dataset generator.')
parser.add_argument('--challenge', '-c', action = 'store', type = str,
                    help = 'Challenge hashtag',
                    metavar = '<challenge>',
                    default = "itookanap")
parser.add_argument('--loop', '-l', action = 'store', type = int,
                    help = 'Check for more tiktoks (keep searching for users with public tiktok liked\'s list)',
                    metavar = '<loop>',
                    default = 0)
args = parser.parse_args()

challenge = challenge.getChallenge(args.c)

api = TikTokApi.get_instance(use_test_endpoints=True)

td.buildDatasetByHashtag(api, challenge["name"], challenge["url"], 10000)
td.pubAuthList(api, challenge["name"])
rows = td.checkConnections(api, challenge["name"])
while rows != 0 and args.l: # conditional loop
    count = td.pubAuthList(api, challenge["name"], rows)
    if count == 0:
        break
    else:
        rows = td.checkConnections(api, challenge["name"], count)
td.ETL(challenge["name"])
