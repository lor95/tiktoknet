challenges = { "itookanap": 
                    {"name": "ITookANap",
                    "url": "https://www.tiktok.com/@gunnarolla/video/6816020939759815942"}, # original video
                "elpepe":
                    {"name":"elpepe",
                    "url":""},
                "ohnanachallenge":
                    {"name":"ohnanachallenge",
                    "url":"https://www.tiktok.com/@saffronbarker/video/6778137328499084549"},
                "makarenachallenge":
                    {"name":"makarenachallenge",
                     "url":""},
                "weirdsoundchallenge":
                    {"name":"weirdsoundchallenge",
                     "url":"https://www.tiktok.com/@angelbrown_19/video/6806305248223759622"},
                "copinesdancechallenge":
                    {"name":"copinesdancechallenge",
                     "url":"https://www.tiktok.com/@nicolesopogee/video/6906089727640816897"},
                "eatingchalk":
                    {"name":"eatingchalkasmr",
                     "url":""},
                "saltandicechallenge":
                    {"name":"saltandicechallenge",
                     "url":""},
                "trashbagchallenge":
                    {"name": "trashbagchallenge",
                     "url":""},
                "walkamile":
                    {"name":"walkamile",
                     "url":""},
               "silhouettechallenge":
                    {"name":"silhouettechallenge",
                     "url":""}
                # insert challenge here
            }
def getChallenge(challenge):
    return challenges[challenge.lower()]

def getChallengeList():
    return ', '.join(list(challenges.keys()))
