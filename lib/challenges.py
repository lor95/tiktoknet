challenges = { "itookanap": 
                {"name": "ITookANap",
                "url": "https://www.tiktok.com/@gunnarolla/video/6816020939759815942"}, # original video
                "elpepe":
                {"name":"elpepe",
                "url":""},
                "ohnanachallenge":
                {"name":"ohnanachallenge",
                "url":"https://vm.tiktok.com/ZMeA1fF7J/"}
                # insert challenge here
            }

def getChallenge(challenge):
    return challenges[challenge.lower()]
