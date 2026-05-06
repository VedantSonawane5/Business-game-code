"""If there is any error please sent email on vs05082013@gmail.com
   I myself will fix the error
   If you have some idia about this code then please email"""

import random
import json
import os

a = input("Enter Name of Log File: ").strip() # You gave to not make the File
if not a.endswith(".json"):
    a += ".json"
LOG_FILE = a

def log_move(move_data):
    history = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = []

    history.append(move_data)

    with open(LOG_FILE, "w") as file:
        json.dump(history, file, indent=4)


print("Welcome to the game")
print("It is a 2 player Business game")

player_one_name = input("Enter Player one name: ").lower().strip()
player_two_name = input("Enter Player two name: ").lower().strip()

if player_one_name == player_two_name:
    print("Names cannot be the same. Restart the game.")
    print("bro why are you naming each the player same do you wanted to play with your soul")
    exit()

data = {
    "player_one_name": player_one_name,
    "player_two_name": player_two_name,
    "player_one_money": 100000,
    "player_two_money": 100000,
    "bank_money": 500000,
}

def get_balance_key(player):
    if player == data["player_one_name"]:
        return "player_one_money"
    else:
        return "player_two_money"

def main(game, player):
    dice = random.randint(1, 6)
    print(f"\n{player.upper()}'s turn. Rolled: {dice}")

    balance_key = get_balance_key(player)
    print(f"Your balance: {game[balance_key]}")

    choice = input("Give (g), take (t), skip (n): ").lower().strip()

    amount_sent = 0
    amount_taken = 0
    target_name = "none"

    if choice == "g":
        attempts = 0

        while attempts < 2:
            try:
                amount_sent = int(input("Enter amount: "))

                if amount_sent <= 0:
                    print("Amount must be positive.")
                    attempts += 1
                    continue

                if amount_sent > game[balance_key]:
                    print("Not enough balance!")
                    attempts += 1

                    if attempts == 2:
                        print("Turn lost.")

                        log_move({
                            "player": player,
                            "roll": dice,
                            "action": "failed_twice_insufficient_balance",
                            "amount": amount_sent,
                            "from": player,
                            "to": "none",
                            "balances": {
                                game["player_one_name"]: game["player_one_money"],
                                game["player_two_name"]: game["player_two_money"],
                                "bank": game["bank_money"]
                            }
                        })
                        return
                    else:
                        print("Try again.")
                        continue

                break

            except ValueError:
                print("Invalid amount.")
                attempts += 1
                if attempts == 2:
                    print("Turn lost.")
                    return

        target = input("Give to Bank(b) or Player(p): ").lower().strip()

        if target == "b":
            game[balance_key] -= amount_sent
            game["bank_money"] += amount_sent
            target_name = "Bank"

        elif target == "p":
            if player == game["player_one_name"]:
                game["player_one_money"] -= amount_sent
                game["player_two_money"] += amount_sent
                target_name = game["player_two_name"]
            else:
                game["player_two_money"] -= amount_sent
                game["player_one_money"] += amount_sent
                target_name = game["player_one_name"]

    elif choice == "t":
        try:
            amount_taken = int(input("Enter amount to take from bank: "))

            if amount_taken <= 0:
                print("Amount must be positive.")
                return

            if amount_taken > game["bank_money"]:
                print("Bank does not have enough money! Turn lost.")

                log_move({
                    "player": player,
                    "roll": dice,
                    "action": "failed_bank_withdraw",
                    "amount": amount_taken,
                    "from": "bank",
                    "to": player,
                    "balances": {
                        game["player_one_name"]: game["player_one_money"],
                        game["player_two_name"]: game["player_two_money"],
                        "bank": game["bank_money"]
                    }
                })
                return

            if player == game["player_one_name"]:
                game["player_one_money"] += amount_taken
            else:
                game["player_two_money"] += amount_taken

            game["bank_money"] -= amount_taken
            target_name = player

        except ValueError:
            print("Invalid amount. Turn skipped.")
            return

    log_move({
        "player": player,
        "roll": dice,
        "action": (
            "sent_money" if choice == "g"
            else "took_money" if choice == "t"
            else "no_action"
        ),
        "amount": amount_sent if choice == "g" else amount_taken,
        "from": player if choice == "g" else "bank" if choice == "t" else "none",
        "to": target_name,
        "balances": {
            game["player_one_name"]: game["player_one_money"],
            game["player_two_name"]: game["player_two_money"],
            "bank": game["bank_money"]
        }
    })

def show_status(game):
    print("\n--- Game Status ---")
    print(f"{game['player_one_name']}: {game['player_one_money']}")
    print(f"{game['player_two_name']}: {game['player_two_money']}")
    print(f"Bank: {game['bank_money']}")
    print("-------------------")

def check_game_end(game):
    if game["player_one_money"] <= 0:
        print(f"\n{game['player_two_name']} wins! {game['player_one_name']} is bankrupt.")
        return True
    elif game["player_two_money"] <= 0:
        print(f"\n{game['player_one_name']} wins! {game['player_two_name']} is bankrupt.")
        return True
    return False

def started(game):
    with open(LOG_FILE, "w") as file:
        json.dump([], file)

    print("\nGame Start! Logging to", LOG_FILE)

    turn = 1

    while True:
        print(f"\n===== TURN {turn} =====")

        main(game, game["player_one_name"])
        show_status(game)
        if check_game_end(game):
            break

        main(game, game["player_two_name"])
        show_status(game)
        if check_game_end(game):
            break

        turn += 1

started(data)