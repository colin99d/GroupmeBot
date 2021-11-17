"""Bot ESPN"""
__docformat__ = "numpy"
import os

import requests

# "&view=mDraftDetail&view=mLiveScoring&view=mMatchupScore&view=mPendingTransactions&view=mPositionalRatings&view=mSettings&view=modular&view=mNav&view=mMatchupScore"

base = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/"
year = "2021"
mid = "/segments/0/leagues/"
ESPN_leagueID = os.getenv("ESPN_leagueID")
tail = "?view=mTeam"
ESPN_SWID = os.getenv("ESPN_SWID")
ESPN_S2 = os.getenv("ESPN_S2")


def get_stat():
    tail = ""
    url = f"{base}{year}{mid}{ESPN_leagueID}{tail}"
    r = requests.get(url, cookies={"SWID": ESPN_SWID, "espn_s2": ESPN_S2})
    return r.json()


def team_stats():
    url = f"{base}{year}{mid}{ESPN_leagueID}{tail}"
    r = requests.get(url, cookies={"SWID": ESPN_SWID, "espn_s2": ESPN_S2})
    return r.json()["teams"]


def get_standings(*args) -> str:
    d = team_stats()
    d.sort(key=lambda x: x["record"]["overall"]["wins"], reverse=True)
    text = "Name\tW\tL\n"

    for t in d:
        gap = " " * (4 - len(t["abbrev"]))
        text += (
            f"{t['abbrev']}\t{t['record']['overall']['wins']}"
            f" {gap}{t['record']['overall']['losses']}\n"
        )

    return text


def win_chance(*args) -> str:
    d = team_stats()
    total = d[0]["record"]["overall"]["losses"]
    total += d[0]["record"]["overall"]["wins"]
    plyrs = []
    t_pts: float = 0
    t_wins: float = 0
    for p in d:
        pts = float(p["points"])
        ws = float(p["record"]["overall"]["wins"])
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
