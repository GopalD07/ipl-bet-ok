"""
IPL 2026 Bet Tracker — Flask Backend
Storage: Supabase (Postgres via supabase-py)
Full 70-match league schedule included.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set as environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TEAMS = {
    "Royal Challengers Bengaluru": {"abbr":"RCB","color":"#EC1C24"},
    "Sunrisers Hyderabad":         {"abbr":"SRH","color":"#F7A721"},
    "Mumbai Indians":              {"abbr":"MI", "color":"#005DA0"},
    "Kolkata Knight Riders":       {"abbr":"KKR","color":"#3A225D"},
    "Rajasthan Royals":            {"abbr":"RR", "color":"#EA1A85"},
    "Chennai Super Kings":         {"abbr":"CSK","color":"#F9CD05"},
    "Punjab Kings":                {"abbr":"PBKS","color":"#ED1B24"},
    "Gujarat Titans":              {"abbr":"GT", "color":"#1C1C57"},
    "Lucknow Super Giants":        {"abbr":"LSG","color":"#A72B2A"},
    "Delhi Capitals":              {"abbr":"DC", "color":"#0078BC"},
}

def mi(no,date,day,time,home,away,venue):
    h,a=TEAMS[home],TEAMS[away]
    return {"match":no,"date":date,"day":day,"time":time,
            "home":home,"away":away,"venue":venue,
            "home_abbr":h["abbr"],"away_abbr":a["abbr"],
            "home_color":h["color"],"away_color":a["color"]}

IPL_SCHEDULE = [
    # ── PHASE 1 (Mar 28 – Apr 12) ──────────────────────────────────────────
    mi(1, "2026-03-28","Sat","7:30 PM","Royal Challengers Bengaluru","Sunrisers Hyderabad","Bengaluru"),
    mi(2, "2026-03-29","Sun","7:30 PM","Mumbai Indians","Kolkata Knight Riders","Mumbai"),
    mi(3, "2026-03-30","Mon","7:30 PM","Rajasthan Royals","Chennai Super Kings","Guwahati"),
    mi(4, "2026-03-31","Tue","7:30 PM","Punjab Kings","Gujarat Titans","New Chandigarh"),
    mi(5, "2026-04-01","Wed","7:30 PM","Lucknow Super Giants","Delhi Capitals","Lucknow"),
    mi(6, "2026-04-02","Thu","7:30 PM","Kolkata Knight Riders","Sunrisers Hyderabad","Kolkata"),
    mi(7, "2026-04-03","Fri","7:30 PM","Chennai Super Kings","Punjab Kings","Chennai"),
    mi(8, "2026-04-04","Sat","3:30 PM","Delhi Capitals","Mumbai Indians","Delhi"),
    mi(9, "2026-04-04","Sat","7:30 PM","Gujarat Titans","Rajasthan Royals","Ahmedabad"),
    mi(10,"2026-04-05","Sun","3:30 PM","Sunrisers Hyderabad","Lucknow Super Giants","Hyderabad"),
    mi(11,"2026-04-05","Sun","7:30 PM","Royal Challengers Bengaluru","Chennai Super Kings","Bengaluru"),
    mi(12,"2026-04-06","Mon","7:30 PM","Kolkata Knight Riders","Punjab Kings","Kolkata"),
    mi(13,"2026-04-07","Tue","7:30 PM","Rajasthan Royals","Mumbai Indians","Guwahati"),
    mi(14,"2026-04-08","Wed","7:30 PM","Delhi Capitals","Gujarat Titans","Delhi"),
    mi(15,"2026-04-09","Thu","7:30 PM","Kolkata Knight Riders","Lucknow Super Giants","Kolkata"),
    mi(16,"2026-04-10","Fri","7:30 PM","Rajasthan Royals","Royal Challengers Bengaluru","Guwahati"),
    mi(17,"2026-04-11","Sat","3:30 PM","Punjab Kings","Sunrisers Hyderabad","New Chandigarh"),
    mi(18,"2026-04-11","Sat","7:30 PM","Chennai Super Kings","Delhi Capitals","Chennai"),
    mi(19,"2026-04-12","Sun","3:30 PM","Lucknow Super Giants","Gujarat Titans","Lucknow"),
    mi(20,"2026-04-12","Sun","7:30 PM","Mumbai Indians","Royal Challengers Bengaluru","Mumbai"),
    # ── PHASE 2 (Apr 13 – May 24) ──────────────────────────────────────────
    mi(21,"2026-04-13","Mon","7:30 PM","Sunrisers Hyderabad","Rajasthan Royals","Hyderabad"),
    mi(22,"2026-04-14","Tue","7:30 PM","Chennai Super Kings","Kolkata Knight Riders","Chennai"),
    mi(23,"2026-04-15","Wed","7:30 PM","Royal Challengers Bengaluru","Lucknow Super Giants","Bengaluru"),
    mi(24,"2026-04-16","Thu","7:30 PM","Mumbai Indians","Punjab Kings","Mumbai"),
    mi(25,"2026-04-17","Fri","7:30 PM","Gujarat Titans","Kolkata Knight Riders","Ahmedabad"),
    mi(26,"2026-04-18","Sat","3:30 PM","Royal Challengers Bengaluru","Delhi Capitals","Bengaluru"),
    mi(27,"2026-04-18","Sat","7:30 PM","Sunrisers Hyderabad","Chennai Super Kings","Hyderabad"),
    mi(28,"2026-04-19","Sun","3:30 PM","Kolkata Knight Riders","Rajasthan Royals","Kolkata"),
    mi(29,"2026-04-19","Sun","7:30 PM","Punjab Kings","Lucknow Super Giants","New Chandigarh"),
    mi(30,"2026-04-20","Mon","7:30 PM","Gujarat Titans","Mumbai Indians","Ahmedabad"),
    mi(31,"2026-04-21","Tue","7:30 PM","Sunrisers Hyderabad","Delhi Capitals","Hyderabad"),
    mi(32,"2026-04-22","Wed","7:30 PM","Lucknow Super Giants","Rajasthan Royals","Lucknow"),
    mi(33,"2026-04-23","Thu","7:30 PM","Mumbai Indians","Chennai Super Kings","Mumbai"),
    mi(34,"2026-04-24","Fri","7:30 PM","Royal Challengers Bengaluru","Gujarat Titans","Bengaluru"),
    mi(35,"2026-04-25","Sat","3:30 PM","Delhi Capitals","Punjab Kings","Delhi"),
    mi(36,"2026-04-25","Sat","7:30 PM","Rajasthan Royals","Sunrisers Hyderabad","Jaipur"),
    mi(37,"2026-04-26","Sun","3:30 PM","Gujarat Titans","Chennai Super Kings","Ahmedabad"),
    mi(38,"2026-04-26","Sun","7:30 PM","Lucknow Super Giants","Kolkata Knight Riders","Lucknow"),
    mi(39,"2026-04-27","Mon","7:30 PM","Delhi Capitals","Royal Challengers Bengaluru","Delhi"),
    mi(40,"2026-04-28","Tue","7:30 PM","Punjab Kings","Rajasthan Royals","New Chandigarh"),
    mi(41,"2026-04-29","Wed","7:30 PM","Mumbai Indians","Sunrisers Hyderabad","Mumbai"),
    mi(42,"2026-04-30","Thu","7:30 PM","Gujarat Titans","Royal Challengers Bengaluru","Ahmedabad"),
    mi(43,"2026-05-01","Fri","7:30 PM","Rajasthan Royals","Delhi Capitals","Jaipur"),
    mi(44,"2026-05-02","Sat","7:30 PM","Chennai Super Kings","Mumbai Indians","Chennai"),
    mi(45,"2026-05-03","Sun","3:30 PM","Sunrisers Hyderabad","Kolkata Knight Riders","Hyderabad"),
    mi(46,"2026-05-03","Sun","7:30 PM","Gujarat Titans","Punjab Kings","Ahmedabad"),
    mi(47,"2026-05-04","Mon","7:30 PM","Mumbai Indians","Lucknow Super Giants","Mumbai"),
    mi(48,"2026-05-05","Tue","7:30 PM","Delhi Capitals","Chennai Super Kings","Delhi"),
    mi(49,"2026-05-06","Wed","7:30 PM","Sunrisers Hyderabad","Punjab Kings","Hyderabad"),
    mi(50,"2026-05-07","Thu","7:30 PM","Lucknow Super Giants","Royal Challengers Bengaluru","Lucknow"),
    mi(51,"2026-05-08","Fri","7:30 PM","Delhi Capitals","Kolkata Knight Riders","Delhi"),
    mi(52,"2026-05-09","Sat","7:30 PM","Rajasthan Royals","Gujarat Titans","Jaipur"),
    mi(53,"2026-05-10","Sun","3:30 PM","Chennai Super Kings","Lucknow Super Giants","Chennai"),
    mi(54,"2026-05-10","Sun","7:30 PM","Royal Challengers Bengaluru","Mumbai Indians","Raipur"),
    mi(55,"2026-05-11","Mon","7:30 PM","Punjab Kings","Delhi Capitals","Dharamshala"),
    mi(56,"2026-05-12","Tue","7:30 PM","Gujarat Titans","Sunrisers Hyderabad","Ahmedabad"),
    mi(57,"2026-05-13","Wed","7:30 PM","Royal Challengers Bengaluru","Kolkata Knight Riders","Raipur"),
    mi(58,"2026-05-14","Thu","7:30 PM","Punjab Kings","Mumbai Indians","Dharamshala"),
    mi(59,"2026-05-15","Fri","7:30 PM","Lucknow Super Giants","Chennai Super Kings","Lucknow"),
    mi(60,"2026-05-16","Sat","7:30 PM","Kolkata Knight Riders","Gujarat Titans","Kolkata"),
    mi(61,"2026-05-17","Sun","3:30 PM","Punjab Kings","Royal Challengers Bengaluru","Dharamshala"),
    mi(62,"2026-05-17","Sun","7:30 PM","Delhi Capitals","Rajasthan Royals","Delhi"),
    mi(63,"2026-05-18","Mon","7:30 PM","Chennai Super Kings","Sunrisers Hyderabad","Chennai"),
    mi(64,"2026-05-19","Tue","7:30 PM","Rajasthan Royals","Lucknow Super Giants","Jaipur"),
    mi(65,"2026-05-20","Wed","7:30 PM","Kolkata Knight Riders","Mumbai Indians","Kolkata"),
    mi(66,"2026-05-21","Thu","7:30 PM","Chennai Super Kings","Gujarat Titans","Chennai"),
    mi(67,"2026-05-22","Fri","7:30 PM","Sunrisers Hyderabad","Royal Challengers Bengaluru","Hyderabad"),
    mi(68,"2026-05-23","Sat","7:30 PM","Lucknow Super Giants","Punjab Kings","Lucknow"),
    mi(69,"2026-05-24","Sun","3:30 PM","Mumbai Indians","Rajasthan Royals","Mumbai"),
    mi(70,"2026-05-24","Sun","7:30 PM","Kolkata Knight Riders","Delhi Capitals","Kolkata"),
]

# ── SUPABASE HELPERS ──────────────────────────────────────────────────────

def get_config(match_no):
    res = supabase.table("match_configs").select("*").eq("match_no", match_no).execute()
    if res.data:
        return res.data[0]
    row = {"match_no": match_no, "home_wallet": 0, "away_wallet": 0, "result": "pending"}
    supabase.table("match_configs").insert(row).execute()
    return row

def upsert_config(match_no, **kwargs):
    existing = supabase.table("match_configs").select("match_no").eq("match_no", match_no).execute()
    if existing.data:
        supabase.table("match_configs").update(kwargs).eq("match_no", match_no).execute()
    else:
        supabase.table("match_configs").insert({"match_no": match_no, **kwargs}).execute()

def get_bets(match_no, side=None):
    q = supabase.table("bets").select("*").eq("match_no", match_no).order("id")
    if side:
        q = q.eq("side", side)
    return q.execute().data or []

# ── STATS ─────────────────────────────────────────────────────────────────

def compute_match_stats(config, home_bets, away_bets):
    def ts(bets):
        placed = sum(float(b["placed"]) for b in bets)
        win    = sum(float(b["win"])    for b in bets)
        avg    = (win/placed) if placed>0 else 0
        return {"count":len(bets),"placed":round(placed,4),"win":round(win,4),
                "avg_odd":round(avg,4),"profit":round(win-placed,4)}
    home = ts(home_bets)
    away = ts(away_bets)
    total = home["placed"] + away["placed"]
    hw = float(config.get("home_wallet") or 0)
    aw = float(config.get("away_wallet") or 0)
    result = config.get("result","pending")
    if result=="home": net_pnl = round(home["win"]-total,4)
    elif result=="away": net_pnl = round(away["win"]-total,4)
    else: net_pnl = 0
    return {"home":home,"away":away,"total_placed":round(total,4),
            "home_wallet":hw,"away_wallet":aw,
            "home_wallet_left":round(hw-home["placed"],4),
            "away_wallet_left":round(aw-away["placed"],4),
            "result":result,"net_pnl":net_pnl}

def compute_global_analytics():
    all_configs = supabase.table("match_configs").select("*").execute().data or []
    all_bets    = supabase.table("bets").select("*").execute().data or []
    bmap = {}
    for b in all_bets:
        mn=b["match_no"]; bmap.setdefault(mn,{"home":[],"away":[]})
        bmap[mn][b["side"]].append(b)
    total_placed=all_net=0; wins=losses=pending=0
    cumulative=[]; running=0; team_pnl={}
    for cfg in all_configs:
        mn=cfg["match_no"]; bb=bmap.get(mn,{"home":[],"away":[]})
        stats=compute_match_stats(cfg,bb["home"],bb["away"])
        total_placed+=stats["total_placed"]; result=stats["result"]
        if result=="pending": pending+=1
        else:
            running+=stats["net_pnl"]; all_net+=stats["net_pnl"]
            wins+=1 if stats["net_pnl"]>=0 else 0
            losses+=0 if stats["net_pnl"]>=0 else 1
            cumulative.append({"label":f"M{mn}","value":round(running,4)})
        match_info=next((m for m in IPL_SCHEDULE if m["match"]==mn),None)
        if match_info:
            for side,team in [("home",match_info["home"]),("away",match_info["away"])]:
                s=stats[side]; team_pnl.setdefault(team,{"placed":0,"win":0,"bets":0})
                team_pnl[team]["placed"]+=s["placed"]; team_pnl[team]["win"]+=s["win"]
                team_pnl[team]["bets"]+=s["count"]
    roi=(all_net/total_placed*100) if total_placed>0 else 0
    return {"total_placed":round(total_placed,2),"net_pnl":round(all_net,2),
            "roi":round(roi,2),"wins":wins,"losses":losses,"pending":pending,
            "win_rate":round(wins/max(wins+losses,1)*100,1),
            "cumulative_pnl":cumulative,"team_pnl":team_pnl}

# ── ROUTES ────────────────────────────────────────────────────────────────

@app.route("/")
def health():
    return jsonify({"status":"ok","matches":len(IPL_SCHEDULE)})

@app.route("/schedule")
def get_schedule():
    today=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return jsonify([dict(m,is_today=m["date"]==today,is_past=m["date"]<today) for m in IPL_SCHEDULE])

@app.route("/match/<int:match_no>")
def get_match(match_no):
    config=get_config(match_no)
    hb=get_bets(match_no,"home"); ab=get_bets(match_no,"away")
    stats=compute_match_stats(config,hb,ab)
    mi_info=next((m for m in IPL_SCHEDULE if m["match"]==match_no),None)
    return jsonify({"match_info":mi_info,"doc":{"home_bets":hb,"away_bets":ab,
        "home_wallet":config.get("home_wallet",0),"away_wallet":config.get("away_wallet",0),
        "result":config.get("result","pending")},"stats":stats})

@app.route("/match/<int:match_no>/wallet",methods=["PUT"])
def set_wallet(match_no):
    b=request.json
    upsert_config(match_no,home_wallet=float(b.get("home_wallet",0)),
                  away_wallet=float(b.get("away_wallet",0)),result="pending")
    config=get_config(match_no)
    stats=compute_match_stats(config,get_bets(match_no,"home"),get_bets(match_no,"away"))
    return jsonify({"stats":stats})

@app.route("/match/<int:match_no>/bet",methods=["POST"])
def add_bet(match_no):
    b=request.json; side=b.get("side")
    placed=float(b.get("placed",0)); win=float(b.get("win",0))
    if side not in ("home","away"): return jsonify({"error":"side: home or away"}),400
    if placed<=0: return jsonify({"error":"placed > 0"}),400
    if win<0:     return jsonify({"error":"win >= 0"}),400
    get_config(match_no)
    new_bet={"match_no":match_no,"side":side,"placed":placed,"win":win,
             "odd":round(win/placed,4) if placed>0 else 0,
             "created_at":datetime.now(timezone.utc).isoformat()}
    ins=supabase.table("bets").insert(new_bet).execute()
    saved=ins.data[0] if ins.data else new_bet
    config=get_config(match_no)
    stats=compute_match_stats(config,get_bets(match_no,"home"),get_bets(match_no,"away"))
    return jsonify({"bet":saved,"stats":stats}),201

@app.route("/match/<int:match_no>/bet/<side>/<int:bet_id>",methods=["DELETE"])
def delete_bet(match_no,side,bet_id):
    if side not in ("home","away"): return jsonify({"error":"bad side"}),400
    supabase.table("bets").delete().eq("id",bet_id).eq("match_no",match_no).execute()
    config=get_config(match_no)
    stats=compute_match_stats(config,get_bets(match_no,"home"),get_bets(match_no,"away"))
    return jsonify({"stats":stats})

@app.route("/match/<int:match_no>/result",methods=["PUT"])
def settle_match(match_no):
    b=request.json; result=b.get("result")
    if result not in ("home","away","void","pending"):
        return jsonify({"error":"result: home/away/void/pending"}),400
    upsert_config(match_no,result=result)
    config=get_config(match_no)
    stats=compute_match_stats(config,get_bets(match_no,"home"),get_bets(match_no,"away"))
    analytics=compute_global_analytics()
    return jsonify({"stats":stats,"analytics":analytics})

@app.route("/analytics")
def get_analytics():
    analytics=compute_global_analytics()
    all_configs=supabase.table("match_configs").select("*").execute().data or []
    all_bets=supabase.table("bets").select("*").execute().data or []
    bmap={}
    for bet in all_bets:
        mn=bet["match_no"]; bmap.setdefault(mn,{"home":[],"away":[]})
        bmap[mn][bet["side"]].append(bet)
    all_matches=[]
    for cfg in all_configs:
        mn=cfg["match_no"]; bb=bmap.get(mn,{"home":[],"away":[]})
        stats=compute_match_stats(cfg,bb["home"],bb["away"])
        mi_info=next((m for m in IPL_SCHEDULE if m["match"]==mn),None)
        all_matches.append({"match_no":str(mn),"match_info":mi_info,"stats":stats,
            "doc":{"home_bets":bb["home"],"away_bets":bb["away"],
                   "home_wallet":cfg.get("home_wallet",0),
                   "away_wallet":cfg.get("away_wallet",0),
                   "result":cfg.get("result","pending")}})
    return jsonify({"analytics":analytics,"matches":all_matches})

@app.route("/reset",methods=["POST"])
def reset():
    supabase.table("bets").delete().neq("id",0).execute()
    supabase.table("match_configs").delete().neq("match_no",0).execute()
    return jsonify({"message":"Reset"})

if __name__=="__main__":
    port=int(os.environ.get("PORT",5050))
    debug=os.environ.get("FLASK_ENV","production")!="production"
    app.run(host="0.0.0.0",port=port,debug=debug)
