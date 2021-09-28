import requests

#"&view=mDraftDetail&view=mLiveScoring&view=mMatchupScore&view=mPendingTransactions&view=mPositionalRatings&view=mSettings&view=modular&view=mNav&view=mMatchupScore"

def get_standings():
    base = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/"
    year = "2021"
    mid = "/segments/0/leagues/"
    leagueID = "1659909443"
    tail = "?view=mTeam"
    url = f"{base}{year}{mid}{leagueID}{tail}"

    r = requests.get(url,
                 cookies={"SWID": "{01E541AA-E88F-4CFF-9978-CB5C2AB064BB}",
                          "espn_s2": "AECxO0pAyX7P4f55fN10Cf%2FgVHdoGXTkAlYQBxI4WBN0vYzOFipvz0zvt6gwIKkgpcVJK0CsCLf5tE1kNxzBNy%2FnNbZ3t9KnQjc8xCHrecZiOAr3zGU569IpRGGqIDZjzOF%2BKhTmDJbyI%2B7zDrTU2Bqs3C4uuDzvWtWnVq%2FgIHNUJ%2FvRiIc3bHdVRbBcY5s3ffi9mHTkZJiQruqNHggRyQjCfS8fv%2FQibP31tkkCx%2FtGmNHn2GOPFvjiuye4F%2B4STtdP9TnmGWN5D7HhCLdBvnqYp5KlPzj%2FwoSIwFdqH8qopg%3D%3D" })
    d = r.json()["teams"]
    r.status_code

    d.sort(key=lambda x: x['record']['overall']['wins'], reverse=True)

    text = 'Name\tWins\tLosses\n'

    for t in d:
        text += f"{t['abbrev']}\t{t['record']['overall']['wins']}\t{t['record']['overall']['losses']}\n"

    return text