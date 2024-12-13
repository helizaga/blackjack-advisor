# Blackjack Advisor

This project provides a graphical tool to help you make better decisions at the Blackjack table. It recommends whether to hit, stand, double down, or split based on a commonly accepted "basic strategy." It can also track the cards that have been seen, maintain a running count using the High-Low method, and suggest betting amounts according to the current count.

**Please Note:**  
- This tool is for educational and practice purposes only.  
- Actual casino conditions may vary, and there's no guarantee of profit.

## Features

1. **Basic Strategy Recommendations:**  
   Enter your hand and the dealer’s up-card to see whether you should Hit (H), Stand (S), Double Down (D), or Split (P).

2. **Card Counting (High-Low):**  
   Keep track of seen cards. The tool updates the running count and calculates the "true count" based on how many decks are left.

3. **Bet Sizing Suggestions:**  
   Given your chip balance, min/max bet, and the true count, the tool suggests how much to wager.

4. **Easy-to-Use GUI:**  
   Built with Python's `tkinter` library, so you can interact with a clear and simple graphical interface.

## How It Works (Step-by-Step)

1. **Load and Run:**  
   Run the Python script. A window will appear with the inputs and buttons.

2. **Entering Your Cards:**  
   - Input your initial hand (e.g., `A,10`).
   - Input the dealer’s visible card (e.g., `6`).

3. **Get the Recommended Action:**  
   Click **"Recommend Action"** to see what the basic strategy suggests.

4. **Hitting and Drawing Cards:**  
   If the recommendation is to hit and you actually take another card, click **"Draw Card"** to enter the new card you received. The recommendation will update accordingly.

5. **Recording the Round:**  
   After the hand finishes, enter any other cards that were revealed during play (e.g., the dealer’s hole card and additional draws) and click **"Record Round"**. This updates the shoe and the running count.

6. **Bet Recommendations:**  
   Use **"Recommend Bet"** at any point to see how the true count affects the suggested wager size.

7. **Resetting the Shoe:**  
   When you want to start fresh (new shoe, new counts), click **"Reset Shoe"**.

## Requirements

- Python 3.x
- `tkinter` (usually included with most Python distributions)

No external dependencies are required besides tkinter.

## Installation and Running

1. **Clone or Download the Repo:**  
   Download the files or clone this repository to your machine.

2. **Run the Script:**  
   ```bash
   python3 blackjack_advisor.py
   ```
   Replace `blackjack_advisor.py` with the actual name of the Python file (if different).

3. **GUI Window Appears:**  
   Interact with the GUI as described in the steps above.

## Tips

- Make sure to enter cards in a comma-separated format (e.g., `A,10` or `4,9`).  
- Cards can be `A,2,3,...,10,J,Q,K` (not case-sensitive).  
- If you make a mistake with the input, the program will let you know which card is invalid.

## Disclaimer

This tool is a guide based on standard basic strategy and a simple card counting approach. Blackjack conditions vary by casino rules (e.g., dealer hits/stands on soft 17, number of decks, allowed doubles/splits, etc.). The suggestions here might not be optimal for every specific rule set.

Use this tool for practice and fun, not as a guarantee to win.
