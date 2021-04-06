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
                "walkamile":
                    {"name":"walkamile",
                     "url":""},
                "silhouettechallenge":
                    {"name":"silhouettechallenge",
                     "url":""},
                "badchallenge":
                    {"name":"badchallenge",
                     "url":""},
                "eatingchallenge":
                    {"name":"eatingchallenge",
                     "url":""},
                "kissyourpetchallenge":
                    {"name":"kissyourpetchallenge",
                     "url":"https://www.tiktok.com/@foopydrip/video/6922985431424437510"},
                "emojichallenge":
                    {"name":"emojichallenge",
                     "url":""},
                "flexibilitychallenge":
                    {"name":"flexibilitychallenge",
                     "url":"https://www.tiktok.com/@ayushishukla098/video/6546886448757347328"},
                "bussitchallenge":
                    {"name":"bussitchallenge",
                     "url":""},
                "dominochallenge":
                    {"name":"dominochallenge",
                     "url":"https://www.tiktok.com/@stilestefanbae/video/6905779244845092098"},
                "popcornkaraoke":
                    {"name":"popcornkaraoke",
                     "url":""},
                "boredinthehouse":
                    {"name":"boredinthehouse",
                     "url":"https://www.tiktok.com/@curtisroach/video/6800471860761971974"},
                "beautifulpeople":
                    {"name":"beautifulpeople",
                     "url":"https://www.tiktok.com/@daniloantonelli/video/6716795433986952454"},
                "savagechallenge":
                    {"name":"savagechallenge",
                     "url":""},
                "savagelove":
                    {"name":"savagelove",
                     "url":""},
                "plankchallenge":
                    {"name":"plankchallenge",
                     "url":""},
                "levelupchallenge":
                    {"name":"levelupchallenge",
                     "url":"https://www.tiktok.com/@jelinuh/video/6580863052575411461"},
                "makemomsmile":
                    {"name":"MakeMomSmile",
                    "url":""},
                "makeupchallenge":
                    {"name":"makeupchallenge",
                     "url":""}
                # insert challenge here
            }

def getChallenge(challenge):
    return challenges[challenge.lower()]

def getChallengeList():
    return ', '.join(list(challenges.keys())) 

 
