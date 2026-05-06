import json
import os

a = input("Enter Name of Log File: ").strip()
if not a.endswith(".json"):
    a += ".json"
LOG_FILE = a

def view_history():
    if not os.path.exists(LOG_FILE):
        print(f"Error: {LOG_FILE} not found. Play the game first.")
        return

    with open(LOG_FILE, "r") as file:
        try:
            moves = json.load(file)
        except json.JSONDecodeError:
            print("Error: The JSON file is empty or corrupted.")
            return

    print("\n" + "=" * 40)
    print("📜 BUSINESS GAME MOVE HISTORY")
    print("=" * 40)

    if not moves:
        print("No moves recorded yet.")
        return

    for i, move in enumerate(moves, 1):
        print(f"\nMOVE #{i}")
        print(f"👤 Player: {move['player'].capitalize()}")
        print(f"🎲 Dice:   {move['roll']}")
        print(f"✅ Action: {move['action']}")

        if move["action"] == "sent_money":
            print(f"💸 Sent: {move['amount']} to {move['to']}")

        elif move["action"] == "took_money":
            print(f"🏦 Took: {move['amount']} from Bank")

        elif move["action"] == "no_action":
            print("⏭️ Skipped turn")

        elif move["action"] == "failed_twice_insufficient_balance":
            print("❌ Failed twice due to insufficient balance (turn lost)")

        elif move["action"] == "failed_bank_withdraw":
            print("❌ Tried to take more than bank balance (turn lost)")

        bal = move['balances']
        balance_str = " | ".join([f"{k.capitalize()}: {v}" for k, v in bal.items()])
        print(f"💰 Balances: {balance_str}")
        print("-" * 20)


if __name__ == "__main__":
    view_history()