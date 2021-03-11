from TikTokApi import TikTokApi
import lib.tiktok_dataset as td

api = TikTokApi.get_instance(use_test_endpoints=True)

td.buildDatasetByHashtag(api, "ITookANap")
td.pubAuthList(api, "ITookANap")
