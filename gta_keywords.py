import random as r

gta_keywords = {
    "Company":(
        "R*",
        "Rockstar",
        "Sam Houser",
        "T2",
        "Take-Two",
        "Take-Two interactive",
        "Strauss Zelnick"
    ),
    "Release":(
        "upload",
        "drop",
        "show",
        "release",
        "announce"
    ),
    "Title":(
        "GTA",
        "Gta",
        "Grand Theft Auto"
    ),
    "Number":(
        "6",
        "VI",
        "six"
    ),
    "Timeline":(
        "tomorrow",
        "next week",
        "this month",
        "next month",
        "this decade",
        "before the heat death of the universe",
        "in your lifetime"
    ),
    "Random timeline":(
        lambda:f"in {r.randint(2,30)} days",
        lambda:f"in {r.randint(2,15)} weeks",
        lambda:f"in {r.randint(2,12)} months",
        lambda:f"in {r.randint(2,10)} years",
        lambda:f"in {r.randint(2024,2027)}"
    ),
    "Affirmation":(
        "for sure",
        "surely",
        "trust me",
        "my uncle works at rockstar",
        "on god",
        "100%"
    ),
    "Bro":(
        "bro",
        "dude",
        "brother"
    ),
    "Denial":(
        "no, bruh",
        "LIES",
        "untrue",
        "Strauss Zelnick whispered me that",
        "Insider info from Sam Houser",
        "MrBossFTW told me so",
        "Not sure if this is true"
        #"couldn't be further from the truth"
    )
}