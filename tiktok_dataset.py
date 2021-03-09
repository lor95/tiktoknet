from TikTokApi import TikTokApi # api wrapper import https://github.com/davidteather/TikTok-Api
api = TikTokApi.get_instance(use_test_endpoints=True)

tiktoks=api.byHashtag("ITookANap",count=100000,custom_verifyFp="")

for tiktok in tiktoks:
    print(tiktok)
