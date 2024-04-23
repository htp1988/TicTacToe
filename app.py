from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Define the root route '/' that renders and returns the 'index.html' template when accessed
@app.route('/')
def index():
    return render_template('index.html')

'''
# Initialize the game board as a list of 9 spaces to represent an empty tic-tac-toe board
board = [" " for _ in range(9)]
# Set the initial current player to 'X'
current_player = "X"

def check_winner(board, player):
    # Define win conditions
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
        (0, 4, 8), (2, 4, 6)             # Diagonal
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

@app.route('/move', methods=['POST'])
def move():
    global current_player
    index = request.json['index']
    if 0 <= index < 9 and board[index] == " ":
        board[index] = current_player
        winner = check_winner(board, current_player)
        game_over = winner or " " not in board
        current_player = "O" if current_player == "X" else "X"
        return jsonify(move=index, player=board[index], winner=winner, game_over=game_over, next_player=current_player)
    return jsonify(error="Invalid move"), 400

@app.route('/reset', methods=['POST'])
def reset():
    global board, current_player
    board = [" " for _ in range(9)]
    current_player = "X"
    return jsonify(message="Game reset", next_player=current_player)
'''

if __name__ == '__main__':
    app.run(debug=True)
