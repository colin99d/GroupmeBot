"""Bot ESPN"""
__docformat__ = "numpy"

import requests

# "&view=mDraftDetail&view=mLiveScoring&view=mMatchupScore&view=mPendingTransactions&view=mPositionalRatings&view=mSettings&view=modular&view=mNav&view=mMatchupScore"

base = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/"
year = "2021"
mid = "/segments/0/leagues/"
leagueID = "1659909443"
tail = "?view=mTeam"
SWID = "{01E541AA-E88F-4CFF-9978-CB5C2AB064BB}"
espn_s2 = (
    "AECxO0pAyX7P4f55fN10Cf%2FgVHdoGXTkAlYQBxI4WBN0vYzOFipvz0zvt6gwIKk"
    + "gpcVJK0CsCLf5tE1kNxzBNy%2FnNbZ3t9KnQjc8xCHrecZiOAr3zGU569IpRGGqI"
    + "DZjzOF%2BKhTmDJbyI%2B7zDrTU2Bqs3C4uuDzvWtWnVq%2FgIHNUJ%2FvRiIc3bH"
    + "dVRbBcY5s3ffi9mHTkZJiQruqNHggRyQjCfS8fv%2FQibP31tkkCx%2FtGmNHn2GO"
    + "PFvjiuye4F%2B4STtdP9TnmGWN5D7HhCLdBvnqYp5KlPzj%2FwoSIwFdqH8qopg%3"
    + "D%3D"
)


def get_stat():
    tail = ""
    url = f"{base}{year}{mid}{leagueID}{tail}"
    r = requests.get(url, cookies={"SWID": SWID, "espn_s2": espn_s2})
    return r.json()


def team_stats():
    url = f"{base}{year}{mid}{leagueID}{tail}"
    r = requests.get(url, cookies={"SWID": SWID, "espn_s2": espn_s2})
    return r.json()["teams"]


def get_standings() -> str:
    d = team_stats()
    d.sort(key=lambda x: x["record"]["overall"]["wins"], reverse=True)
    text = "Name\tW\tL\n"

    for t in d:
        gap = " " * (4 - len(t["abbrev"]))
        text += f"{t['abbrev']}\t{t['record']['overall']['wins']} {gap}{t['record']['overall']['losses']}\n"

    return text


def win_chance() -> str:
    d = team_stats()
    total = d[0]["record"]["overall"]["losses"] + d[0]["record"]["overall"]["wins"]
    plyrs = []
    t_pts = 0
    t_wins = 0
    for p in d:
        pts = float(p["points"])
        ws = int(p["record"]["overall"]["wins"])
        t_pts += pts
        t_wins += ws
        plyrs.append([p["abbrev"], pts, ws])

    if total > 9:
        return f"Winner is: {max(plyrs, key=lambda x: x[2])[0]}"
    most_wins = max(plyrs, key=lambda x: x[2])[2]
    games_left = 10 - total
    plyrs = list(filter(lambda x: x[2] + games_left >= most_wins, plyrs))

    plyrs_cln = [[x[0], (x[1] / t_pts * 0.5 + x[2] / t_wins * 0.5)] for x in plyrs]
    total_pts = sum(x[1] for x in plyrs_cln)
    players_cln = [[x[0], round((x[1] / total_pts) * 100, 2)] for x in plyrs_cln]
    players_cln.sort(key=lambda x: x[1], reverse=True)

    string = "Player's chance of winning:"
    for plr in players_cln:
        gap = " " * (4 - len(plr[0]))
        string += f"\n{plr[0]} {gap}{plr[1]}%"

    return string
