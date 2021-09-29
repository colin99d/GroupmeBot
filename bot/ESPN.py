import requests

#"&view=mDraftDetail&view=mLiveScoring&view=mMatchupScore&view=mPendingTransactions&view=mPositionalRatings&view=mSettings&view=modular&view=mNav&view=mMatchupScore"

base = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/"
year = "2021"
mid = "/segments/0/leagues/"
leagueID = "1659909443"
tail = "?view=mTeam"
SWID = "{01E541AA-E88F-4CFF-9978-CB5C2AB064BB}"
espn_s2 = "AECxO0pAyX7P4f55fN10Cf%2FgVHdoGXTkAlYQBxI4WBN0vYzOFipvz0zvt6gwIKkgpcVJK0CsCLf5tE1kNxzBNy%2FnNbZ3t9KnQjc8xCHrecZiOAr3zGU569IpRGGqIDZjzOF%2BKhTmDJbyI%2B7zDrTU2Bqs3C4uuDzvWtWnVq%2FgIHNUJ%2FvRiIc3bHdVRbBcY5s3ffi9mHTkZJiQruqNHggRyQjCfS8fv%2FQibP31tkkCx%2FtGmNHn2GOPFvjiuye4F%2B4STtdP9TnmGWN5D7HhCLdBvnqYp5KlPzj%2FwoSIwFdqH8qopg%3D%3D"

def team_stats():
    url = f"{base}{year}{mid}{leagueID}{tail}"
    r = requests.get(url, cookies={"SWID": SWID, "espn_s2":  espn_s2})
    return r.json()["teams"]

def get_standings():
    d = team_stats()
    d.sort(key=lambda x: x['record']['overall']['wins'], reverse=True)
    text = 'Name\tW\tL\n'

    for t in d:
        text += f"{t['abbrev']}\t{t['record']['overall']['wins']}\t{t['record']['overall']['losses']}\n"

    return text

def win_chance():
    d = team_stats()
    players = []
    total_pts = 0
    total_wins = 0
    for p in d:
        name = p["abbrev"]
        pts = float(p["points"])
        ws = int(p['record']['overall']['wins'])
        total_pts += pts
        total_wins += ws
        players.append([name, pts, ws])

    players_cln = []
    for plr in players:
        percent = plr[1]/total_pts * 0.5 + plr[2]/total_wins * 0.5
        percent = round(percent * 100,2)
        players_cln.append([plr[0], percent])

    players_cln.sort(key=lambda x: x[1], reverse=True)

    string = "Player's chance of winning:"
    for plr in players_cln:
        string += f"\n{plr[0]}\t{plr[1]}%"

    return string