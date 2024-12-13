import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ----------------------------
# Data and Configuration
# ----------------------------

CARD_VALUES = {
    "A": 1,
    "K": 10,
    "Q": 10,
    "J": 10,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
basic_strategy = {}


def set_actions(hand_type, player_totals, dealer_values, action):
    """
    Helper function to assign the given action to a range of player totals vs dealer upcards
    in the basic_strategy dictionary.
    """
    for pt in player_totals:
        for dv in dealer_values:
            basic_strategy[(hand_type, pt, dv)] = action


# ----------------------------
# Build the Basic Strategy Table
# ----------------------------
# HARD
set_actions("hard", range(4, 9), range(1, 11), "H")
set_actions("hard", [9], [3, 4, 5, 6], "D")
set_actions("hard", [9], [1, 2, 7, 8, 9, 10], "H")
set_actions("hard", [10], range(2, 10), "D")
set_actions("hard", [10], [1, 10], "H")
set_actions("hard", [11], range(2, 11), "D")
set_actions("hard", [12], [4, 5, 6], "S")
set_actions("hard", [12], [1, 2, 3, 7, 8, 9, 10], "H")
set_actions("hard", range(13, 17), range(2, 7), "S")
set_actions("hard", range(13, 17), [1, 7, 8, 9, 10], "H")
set_actions("hard", range(17, 22), range(1, 11), "S")

# SOFT
set_actions("soft", [13, 14], [5, 6], "D")
set_actions("soft", [13, 14], range(1, 5), "H")
set_actions("soft", [13, 14], [7, 8, 9, 10], "H")
set_actions("soft", [15, 16], [4, 5, 6], "D")
set_actions("soft", [15, 16], [1, 2, 3, 7, 8, 9, 10], "H")
set_actions("soft", [17], [3, 4, 5, 6], "D")
set_actions("soft", [17], [1, 2, 7, 8, 9, 10], "H")
set_actions("soft", [18], [2, 3, 4, 5, 6], "D")
set_actions("soft", [18], [7, 8], "S")
set_actions("soft", [18], [9, 10, 1], "H")
set_actions("soft", [19], range(1, 11), "S")
set_actions("soft", [20], range(1, 11), "S")
set_actions("soft", [21], range(1, 11), "S")

# PAIRS
set_actions("pair", [4, 6], [2, 3, 4, 5, 6, 7], "P")
set_actions("pair", [4, 6], [1, 8, 9, 10], "H")
set_actions("pair", [8], [5, 6], "P")
set_actions("pair", [8], [1, 2, 3, 4, 7, 8, 9, 10], "H")
set_actions("pair", [10], range(2, 10), "D")
set_actions("pair", [10], [1, 10], "H")
set_actions("pair", [12], [2, 3, 4, 5, 6], "P")
set_actions("pair", [12], [1, 7, 8, 9, 10], "H")
set_actions("pair", [14], [2, 3, 4, 5, 6, 7], "P")
set_actions("pair", [14], [1, 8, 9, 10], "H")
set_actions("pair", [16], range(1, 11), "P")
set_actions("pair", [18], [2, 3, 4, 5, 6, 8, 9], "P")
set_actions("pair", [18], [1, 7, 10], "S")
set_actions("pair", [20], range(1, 11), "S")

# ----------------------------
# Helper Functions
# ----------------------------


def hand_value(cards):
    """
    Calculate the best blackjack hand value given a list of cards.
    Aces count as 11 unless that would bust the hand, in which case they drop to 1.
    """
    total = 0
    aces = 0
    for c in cards:
        rank = c.upper()
        if rank == "A":
            aces += 1
            total += 11
        elif rank in ["K", "Q", "J", "10"]:
            total += 10
        else:
            total += int(rank)

    # Adjust for Aces if total > 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def is_soft_hand(cards):
    """
    Returns True if the hand is considered 'soft' (includes an Ace counting as 11).
    """
    val = hand_value(cards)
    ranks = [c.upper() for c in cards]
    if "A" in ranks:
        base_val = sum(CARD_VALUES[r] for r in ranks)
        return val != base_val
    return False


def hand_type(cards):
    """
    Determine if the player's hand is 'hard', 'soft', or a 'pair'.
    """
    ranks = [c.upper() for c in cards]
    if len(ranks) == 2 and ranks[0] == ranks[1]:
        return "pair"
    if is_soft_hand(cards):
        return "soft"
    return "hard"


def dealer_value(card):
    """
    Convert the dealer's upcard into its value for strategy lookup.
    """
    c = card.upper()
    if c in ["K", "Q", "J", "10"]:
        return 10
    elif c == "A":
        return 1
    else:
        return int(c)


def recommend_action(player_cards, dealer_upcard):
    p_val = hand_value(player_cards)

    # If player is over 21, they are busted, so no further action makes sense
    if p_val > 21:
        return "BUST"

    p_type = hand_type(player_cards)
    d_val = dealer_value(dealer_upcard)

    # If the player has more than 2 cards, don't allow double down (D)
    # Because double down is generally only allowed on the initial two-card hand.
    more_than_two_cards = len(player_cards) > 2

    ranks = [c.upper() for c in player_cards]
    # Special case: Pair of Aces always split
    if p_type == "pair" and ranks[0] == "A":
        return "P"

    key = (p_type, p_val, d_val)
    if key in basic_strategy:
        recommended = basic_strategy[key]
        # If recommended is "D" (Double) but player already hit, revert to "H" (Hit)
        if recommended == "D" and more_than_two_cards:
            recommended = "H"
        return recommended

    # Fallback logic if no entry in strategy table:
    if p_type == "hard":
        # With more than 2 cards, no double, just hit or stand
        return "H" if p_val < 12 else "S"
    elif p_type == "soft":
        return "H" if p_val < 18 else "S"
    else:  # pair
        return "H" if p_val < 12 else "S"


def update_count(seen_cards):
    """
    Update the running count based on seen cards using High-Low Counting.
    """
    count = 0
    for c in seen_cards:
        r = c.upper()
        if r in ["2", "3", "4", "5", "6"]:
            count += 1
        elif r in ["10", "J", "Q", "K", "A"]:
            count -= 1
    return count


def calculate_true_count(running_count, decks_remaining):
    """
    Calculate the true count by dividing running count by decks remaining.
    """
    if decks_remaining <= 0:
        return running_count
    return running_count / decks_remaining


def recommend_bet(chip_balance, min_bet, max_bet, true_count):
    """
    Simple betting strategy based on true count:
    - True count <= 0: Min bet
    - True count = 1: 2x min bet
    - True count = 2: 4x min bet
    - True count >= 3: 8x min bet
    Capped at max_bet.
    """
    if true_count <= 0:
        recommended = min_bet
    elif true_count == 1:
        recommended = min(2 * min_bet, max_bet)
    elif true_count == 2:
        recommended = min(4 * min_bet, max_bet)
    else:
        recommended = min(8 * min_bet, max_bet)

    # Ensure recommended bet does not exceed chip balance
    recommended = min(recommended, chip_balance)
    return recommended


def normalize_cards(input_str):
    """
    Normalize a comma-separated string of cards into a list of uppercase card ranks.
    Removes whitespace and ignores empty values.
    """
    return [c.strip().upper() for c in input_str.split(",") if c.strip()]


# ----------------------------
# GUI Application Class
# ----------------------------


class BlackjackAdvisorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Advisor")

        # Initialize a 6-deck shoe (6*4 of each rank = 24)
        self.shoe = {rank: 24 for rank in RANKS}
        self.running_count = 0.0

        # Main Frame
        frame = ttk.Frame(root, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        instructions = (
            "Steps to Use:\n"
            "1. Enter your cards and the dealer's up-card, then click 'Recommend Action'.\n"
            "2. If 'Hit' is recommended and you actually hit in real life, click 'Draw Card' to add the new card.\n"
            "3. After the round ends, enter any additional seen cards and click 'Record Round'.\n"
            "4. Use 'Recommend Bet' at any time for betting advice.\n"
            "5. 'Reset Shoe' starts fresh.\n\n"
            "Cards: A,2,3,...,J,Q,K. Case-insensitive."
        )
        ttk.Label(frame, text=instructions, wraplength=400).grid(
            row=0, column=0, columnspan=4, pady=(0, 10)
        )

        # Player Cards
        ttk.Label(frame, text="Your Cards (e.g. A,10):").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.player_cards_entry = ttk.Entry(frame, width=30)
        self.player_cards_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

        # Dealer Card
        ttk.Label(frame, text="Dealer Up-Card (e.g. 6):").grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        self.dealer_card_entry = ttk.Entry(frame, width=30)
        self.dealer_card_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=3)

        # Additional Seen Cards
        ttk.Label(frame, text="Additional Seen Cards (e.g. 4,9):").grid(
            row=3, column=0, sticky="e", padx=5, pady=5
        )
        self.seen_cards_entry = ttk.Entry(frame, width=30)
        self.seen_cards_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=3)

        # Chip Balance
        ttk.Label(frame, text="Chip Balance:").grid(
            row=4, column=0, sticky="e", padx=5, pady=5
        )
        self.chip_balance_entry = ttk.Entry(frame, width=30)
        self.chip_balance_entry.insert(0, "1000")
        self.chip_balance_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=3)

        # Min Bet
        ttk.Label(frame, text="Min Bet:").grid(
            row=5, column=0, sticky="e", padx=5, pady=5
        )
        self.min_bet_entry = ttk.Entry(frame, width=30)
        self.min_bet_entry.insert(0, "10")
        self.min_bet_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=3)

        # Max Bet
        ttk.Label(frame, text="Max Bet:").grid(
            row=6, column=0, sticky="e", padx=5, pady=5
        )
        self.max_bet_entry = ttk.Entry(frame, width=30)
        self.max_bet_entry.insert(0, "100")
        self.max_bet_entry.grid(row=6, column=1, padx=5, pady=5, columnspan=3)

        # Buttons
        action_btn = ttk.Button(
            frame, text="Recommend Action", command=self.on_recommend_action
        )
        action_btn.grid(row=7, column=0, padx=5, pady=10, sticky="e")

        bet_btn = ttk.Button(frame, text="Recommend Bet", command=self.on_recommend_bet)
        bet_btn.grid(row=7, column=1, padx=5, pady=10)

        record_btn = ttk.Button(
            frame, text="Record Round", command=self.on_record_round
        )
        record_btn.grid(row=7, column=2, padx=5, pady=10, sticky="w")

        draw_btn = ttk.Button(frame, text="Draw Card", command=self.on_draw_card)
        draw_btn.grid(row=7, column=3, padx=5, pady=10, sticky="w")

        reset_btn = ttk.Button(frame, text="Reset Shoe", command=self.on_reset_shoe)
        reset_btn.grid(row=8, column=0, padx=5, pady=10, sticky="e")

        help_btn = ttk.Button(frame, text="Help", command=self.show_help)
        help_btn.grid(row=8, column=1, padx=5, pady=10)

        self.result_label = ttk.Label(frame, text="", foreground="blue", wraplength=400)
        self.result_label.grid(row=9, column=0, columnspan=4, pady=10)

    def show_help(self):
        """
        Display the help instructions in a message box.
        """
        help_text = (
            "How to Use This Tool:\n\n"
            "1. Enter your initial cards and the dealer's card, click 'Recommend Action'.\n"
            "2. If 'Hit' is recommended and you actually hit, click 'Draw Card' to enter the new card.\n"
            "3. After the hand is done, enter any additional seen cards and click 'Record Round'.\n"
            "4. Use 'Recommend Bet' for betting advice.\n"
            "5. 'Reset Shoe' starts a new shoe.\n"
            "Cards: A,2,3,...,J,Q,K. Case-insensitive."
        )
        messagebox.showinfo("Help", help_text)

    def current_decks_remaining(self):
        """
        Calculate how many decks are remaining based on the cards left in the shoe.
        """
        cards_left = sum(self.shoe.values())
        return cards_left / 52.0

    def remove_from_shoe(self, card):
        """
        Remove one instance of the specified card from the shoe.
        Returns True on success, False if card not available.
        """
        card = card.upper()
        if card in self.shoe and self.shoe[card] > 0:
            self.shoe[card] -= 1
            return True
        return False

    def on_recommend_action(self):
        """
        Handler for the 'Recommend Action' button.
        Validates input and updates the recommendation label.
        """
        player_cards = normalize_cards(self.player_cards_entry.get())
        dealer_card = self.dealer_card_entry.get().strip().upper()

        if not player_cards or not dealer_card:
            self.result_label.config(
                text="Please enter both your cards and the dealer card."
            )
            return

        # Validate input cards
        for c in player_cards + [dealer_card]:
            if c not in CARD_VALUES and c != "A":
                self.result_label.config(text=f"Invalid card entered: {c}")
                return

        action = recommend_action(player_cards, dealer_card)
        action_text = {"H": "Hit", "S": "Stand", "D": "Double Down", "P": "Split"}.get(
            action, action
        )
        self.result_label.config(text=f"Recommended Action: {action_text}")

    def on_recommend_bet(self):
        """
        Handler for the 'Recommend Bet' button.
        Computes and displays a suggested betting amount based on the true count.
        """
        decks_remaining = self.current_decks_remaining()
        true_count = calculate_true_count(self.running_count, decks_remaining)

        # Validate numeric inputs
        try:
            chip_balance = float(self.chip_balance_entry.get().strip())
            min_bet = float(self.min_bet_entry.get().strip())
            max_bet = float(self.max_bet_entry.get().strip())
        except ValueError:
            self.result_label.config(
                text="Please enter valid numeric values for chip balance and bets."
            )
            return

        bet = recommend_bet(chip_balance, min_bet, max_bet, true_count)
        cards_left = sum(self.shoe.values())

        self.result_label.config(
            text=(
                f"Running Count: {self.running_count}, True Count: {true_count:.2f}\n"
                f"Recommended Bet: {bet}\n"
                f"Decks Remaining: {decks_remaining:.2f}, Cards Remaining: {cards_left}"
            )
        )

    def on_record_round(self):
        """
        Handler for the 'Record Round' button.
        Updates the shoe, running count, and clears fields for the next round.
        """
        player_cards = normalize_cards(self.player_cards_entry.get())
        dealer_card = self.dealer_card_entry.get().strip().upper()
        additional_cards = normalize_cards(self.seen_cards_entry.get())

        all_seen = player_cards + [dealer_card] + additional_cards

        # Validate all seen cards
        for c in all_seen:
            if c not in CARD_VALUES and c != "A":
                self.result_label.config(text=f"Invalid seen card: {c}")
                return

        # Remove seen cards from shoe
        for c in all_seen:
            if not self.remove_from_shoe(c):
                self.result_label.config(
                    text=(
                        f"Error: Tried to remove card {c} not available in shoe.\n"
                        "Check your inputs."
                    )
                )
                return

        # Update running count
        round_count_change = update_count(all_seen)
        self.running_count += round_count_change

        # Clear entries for next round
        self.player_cards_entry.delete(0, tk.END)
        self.dealer_card_entry.delete(0, tk.END)
        self.seen_cards_entry.delete(0, tk.END)

        decks_remaining = self.current_decks_remaining()
        true_count = calculate_true_count(self.running_count, decks_remaining)
        cards_left = sum(self.shoe.values())
        self.result_label.config(
            text=(
                f"Round Recorded.\n"
                f"Running Count: {self.running_count}, True Count: {true_count:.2f}\n"
                f"Decks Remaining: {decks_remaining:.2f}, Cards Remaining: {cards_left}"
            )
        )

    def on_draw_card(self):
        """
        Handler for the 'Draw Card' button.
        Prompts the user for the new card drawn and updates the player's hand.
        Then re-checks the recommended action.
        """
        new_card = simpledialog.askstring(
            "Draw Card", "Enter the new card (e.g. '5' or 'K'):"
        )
        if not new_card:
            return  # User cancelled

        new_card = new_card.strip().upper()

        # Validate the card
        if new_card not in CARD_VALUES and new_card != "A":
            messagebox.showerror("Invalid Card", f"{new_card} is not a valid card.")
            return

        # Update player's cards
        current_cards = normalize_cards(self.player_cards_entry.get())
        current_cards.append(new_card)
        # Update the entry field
        self.player_cards_entry.delete(0, tk.END)
        self.player_cards_entry.insert(0, ",".join(current_cards))

        # Automatically re-check the recommended action
        self.on_recommend_action()

    def on_reset_shoe(self):
        """
        Handler for 'Reset Shoe' button.
        Resets the shoe, counts, and input fields to initial values.
        """
        self.shoe = {rank: 24 for rank in RANKS}
        self.running_count = 0.0
        self.player_cards_entry.delete(0, tk.END)
        self.dealer_card_entry.delete(0, tk.END)
        self.seen_cards_entry.delete(0, tk.END)
        self.chip_balance_entry.delete(0, tk.END)
        self.chip_balance_entry.insert(0, "1000")
        self.min_bet_entry.delete(0, tk.END)
        self.min_bet_entry.insert(0, "10")
        self.max_bet_entry.delete(0, tk.END)
        self.max_bet_entry.insert(0, "100")

        decks_remaining = self.current_decks_remaining()
        cards_left = sum(self.shoe.values())
        self.result_label.config(
            text=f"Shoe reset. Counts cleared.\nDecks Remaining: {decks_remaining:.2f}, Cards Remaining: {cards_left}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackAdvisorGUI(root)
    root.mainloop()
