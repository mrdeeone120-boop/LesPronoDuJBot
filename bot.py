import asyncio
import requests
from telegram import Bot
from bs4 import BeautifulSoup
import random

import os

TOKEN = os.getenv("TOKEN")
BOT_NAME = "LesPronoDuJBot"
BANKROLL = 1000

# ================= TELEGRAM =================
async def send(chat_id, msg):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=chat_id, text=msg)

def get_chat_id():
    # Chat ID fixe
    return 2002767400

# ================= SCRAPING FLASHSCORE =================
def get_matches():
    url = "https://www.flashscore.com/football/"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

    matches = []
    for m in soup.select(".event__match")[:10]:
        try:
            home = m.select_one(".event__participant--home").text
            away = m.select_one(".event__participant--away").text
            matches.append((home, away))
        except:
            continue
    return matches

# ================= LOGIQUE =================
def analyze_match(home, away):
    import random

    # Stats simulées mais cohérentes
    home_xg = random.uniform(1.0, 2.2)
    away_xg = random.uniform(0.8, 1.8)

    home_odds = random.uniform(1.5, 2.5)
    draw_odds = random.uniform(3.0, 4.0)
    away_odds = random.uniform(2.0, 3.5)

    total = home_xg + away_xg

    probs = {
        "home": home_xg / total,
        "away": away_xg / total,
        "draw": 0.25
    }

    pronos = []

    for outcome in ["home", "draw", "away"]:
        odds = locals()[f"{outcome}_odds"]
        prob = probs[outcome]

        value = (odds * prob) - 1

        if value > 0.05:
            kelly = ((odds * prob - 1) / (odds - 1))
            stake = max(0, kelly * 1000 * 0.5)

            pronos.append({
                "match": f"{home} vs {away}",
                "bet": outcome,
                "odds": round(odds, 2),
                "prob": round(prob * 100, 1),
                "value": round(value, 2),
                "stake": round(stake, 2)
            })

    return pronos

# ================= MAIN LOOP =================
async def main():
    chat_id = get_chat_id()
    matches = get_matches()

    found = 0

    for home, away in matches:
        p = analyze_match(home, away)
        if p:
            msg = (
                f"🔥 {BOT_NAME}\n"
                f"{p['match']}\n"
                f"🎯 Bet: {p['bet']}\n"
                f"📊 Prob: {p['prob']}%\n"
                f"💰 Odds: {p['odds']}\n"
                f"💎 Value: {p['value']}\n"
                f"💸 Stake: {p['stake']}€"
            )
            await send(chat_id, msg)
            found += 1

    if found == 0:
        await send(chat_id, "😴 Aucun value bet pour le moment")

asyncio.run(main())

import pandas as pd

# exemple après tes pronos
df = pd.DataFrame(all_pronos)  # ou ta liste de bets
df.to_csv("valuebets.csv", index=False)


import pandas as pd

# exemple liste de pronos
all_pronos = []

# quand tu crées un prono
all_pronos.append({
    "match": "PSG vs OM",
    "bet": "home",
    "odds": 1.8,
    "prob": 60,
    "value": 0.1,
    "stake": 20
})

# SAUVEGARDE CSV
df = pd.DataFrame(all_pronos)
df.to_csv("valuebets.csv", index=False)

print("CSV créé ✅")