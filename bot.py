# bot.py - LesPronoDuJBot PRO

import os
import time
import requests
import random
import pandas as pd

# ✅ Token Telegram depuis variable d'environnement
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("⚠️ TOKEN non défini dans Environment Variables !")

# ✅ Chat ID fixe
CHAT_ID = 2002767400  # remplace par ton chat_id

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

CSV_FILE = "valuebets.csv"

# Initialiser CSV si n'existe pas
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["match", "bet", "odds", "prob", "value", "stake"])
    df.to_csv(CSV_FILE, index=False)

# Fonction pour générer un prono simulé
def analyze_match(home, away):
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

# Envoyer message sur Telegram
def send_message(message):
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(BASE_URL, data=payload)
        print("✅ Message envoyé :", message)
    except Exception as e:
        print("❌ Erreur :", e)

# Liste de matchs simulés
MATCHES = [
    ("Team A", "Team B"),
    ("Team C", "Team D"),
    ("Team E", "Team F")
]

def main():
    while True:
        all_bets = []
        for home, away in MATCHES:
            bets = analyze_match(home, away)
            for bet in bets:
                msg = (f"🏟 {bet['match']}\n"
                       f"💰 Bet: {bet['bet']} | Odds: {bet['odds']}\n"
                       f"🎯 Prob: {bet['prob']}% | Value: {bet['value']}\n"
                       f"💵 Stake: {bet['stake']:.2f}€")
                send_message(msg)
                all_bets.append(bet)

        # Ajouter les pronos au CSV
        if all_bets:
            df = pd.DataFrame(all_bets)
            df.to_csv(CSV_FILE, mode="a", index=False, header=False)

        time.sleep(600)  # 10 minutes

if __name__ == "__main__":
    main()