
//==================================
// HELPER FUNCTIONS
//==================================

// Sum up all elements in an array
function sumArray(array) {
    var sum = 0,
        i = 0;
    for (i = 0; i < array.length; i++) {
        sum += array[i];
    }
    return sum;
}

// Check element existence
function isInArray(element, array) {
    if (array.indexOf(element) > -1) {
        return true;
    }
    return false;
}

// Shuffle an array using the Fisher-Yates (Durstenfeld) shuffle algorithm
function shuffleArray(array) {
    var counter = array.length,
        temp,
        index;
    while (counter > 0) {
        index = Math.floor(Math.random() * counter);
        counter--;
        temp = array[counter];
        array[counter] = array[index];
        array[index] = temp;
    }
    return array;
}

// Generate a random integer between min and max
function intRandom(min, max) {
    var rand = min + Math.random() * (max + 1 - min);
    return Math.floor(rand);
}


//==================================
// GLOBAL VARIABLES
//==================================

var mode = 0, // 0 for single player, 1 for two players
    moves = 0,
    winner = 0,
    x = 1, // player X identifier
    o = 3, // player O identifier
    player = x, // current player
    computer = o, // computer identifier
    whoseTurn = x, // track whose turn is it
    gameOver = false,
    score = {
        ties: 0,
        player1: 0,
        player2: 0
    },
    xText = "×", // text for player X
    oText = "o", // text for player O
    playerText = xText, // current player's text
    computerText = oText, // computer's text
    myGrid = null; // the game grid


//==================================
// GRID OBJECT
//==================================

// Grid constructor
function Grid() {
    this.cells = new Array(9);
}

// Get free cells in an array
// Returns an array of indices in the original Grid.cells array, not the values
// of the array elements
// Their values can be accessed as Grid.cells[index]
Grid.prototype.getFreeCellIndices = function () {
    var i = 0,
        resultArray = [];
    for (i = 0; i < this.cells.length; i++) {
        if (this.cells[i] === 0) {
            resultArray.push(i);
        }
    }

    return resultArray;
};

// Get a row (accepts 0, 1, or 2 as argument)
// Returns the values of a specified row
Grid.prototype.getRowValues = function (index) {
    if (index !== 0 && index !== 1 && index !== 2) {
        console.error("Wrong arg for getRowValues!");
        return undefined;
    }
    var i = index * 3;
    return this.cells.slice(i, i + 3);
};

// Get a row (accepts 0, 1, or 2 as argument)
// Return the indices of the cells in a specified row
Grid.prototype.getRowIndices = function (index) {
    if (index !== 0 && index !== 1 && index !== 2) {
        console.error("Wrong arg for getRowIndices!");
        return undefined;
    }
    var row = [];
    index = index * 3;
    row.push(index);
    row.push(index + 1);
    row.push(index + 2);
    return row;
};

// Return the values of a specified column
Grid.prototype.getColumnValues = function (index) {
    if (index !== 0 && index !== 1 && index !== 2) {
        console.error("Wrong arg for getColumnValues!");
        return undefined;
    }
    var i, column = [];
    for (i = index; i < this.cells.length; i += 3) {
        column.push(this.cells[i]);
    }
    return column;
};

// Return the indices of the cells in a specified column
Grid.prototype.getColumnIndices = function (index) {
    if (index !== 0 && index !== 1 && index !== 2) {
        console.error("Wrong arg for getColumnIndices!");
        return undefined;
    }
    var i, column = [];
    for (i = index; i < this.cells.length; i += 3) {
        column.push(i);
    }
    return column;
};

// arg 0: from top-left
// arg 1: from top-right
// Return the values of a specified diagonal
Grid.prototype.getDiagValues = function (arg) {
    var cells = [];
    if (arg !== 1 && arg !== 0) {
        console.error("Wrong arg for getDiagValues!");
        return undefined;
    } else if (arg === 0) {
        cells.push(this.cells[0]);
        cells.push(this.cells[4]);
        cells.push(this.cells[8]);
    } else {
        cells.push(this.cells[2]);
        cells.push(this.cells[4]);
        cells.push(this.cells[6]);
    }
    return cells;
};

// Return the indices of the cells in a specified diagonal
Grid.prototype.getDiagIndices = function (arg) {
    if (arg !== 1 && arg !== 0) {
        console.error("Wrong arg for getDiagIndices!");
        return undefined;
    } else if (arg === 0) {
        return [0, 4, 8];
    } else {
        return [2, 4, 6];
    }
};

// Identify a cell that can complete two in a row for a given player or computer
Grid.prototype.getFirstWithTwoInARow = function (agent) {
    if (agent !== computer && agent !== player) {
        console.error("Function getFirstWithTwoInARow accepts only player or computer as argument.");
        return undefined;
    }
    var sum = agent * 2,
        freeCells = shuffleArray(this.getFreeCellIndices());

    // Check rows, columns, and diagonals for a possible win
    for (var i = 0; i < freeCells.length; i++) {
        for (var j = 0; j < 3; j++) {
            var rowV = this.getRowValues(j);
            var rowI = this.getRowIndices(j);
            var colV = this.getColumnValues(j);
            var colI = this.getColumnIndices(j);
            if (sumArray(rowV) == sum && isInArray(freeCells[i], rowI)) {
                return freeCells[i];
            } else if (sumArray(colV) == sum && isInArray(freeCells[i], colI)) {
                return freeCells[i];
            }
        }

        // Check diagonals separately as there are only two
        for (j = 0; j < 2; j++) {
            var diagV = this.getDiagValues(j);
            var diagI = this.getDiagIndices(j);
            if (sumArray(diagV) == sum && isInArray(freeCells[i], diagI)) {
                return freeCells[i];
            }
        }
    }
    return false; // Return false if no actionable cell is found
};

// Reset the grid
Grid.prototype.reset = function () {
    for (var i = 0; i < this.cells.length; i++) {
        this.cells[i] = 0;
    }
    return true;
};

//==================================
// MAIN FUNCTIONS
//==================================

// Initialize the game setup
function initialize() {
    myGrid = new Grid(); // Create a new grid instance
    moves = 0; // Reset move count
    winner = 0; // Reset winner
    gameOver = false; // Reset game status to not over
    whoseTurn = player; // Set the initial turn

    for (var i = 0; i <= myGrid.cells.length - 1; i++) {
        myGrid.cells[i] = 0;
    }
    // Show options after a slight delay
    setTimeout(showOptions, 500);
}

document.addEventListener('DOMContentLoaded', function() {
    initialize();
});

// Toggle between player X and O
function switchPlayer() {
    if (player === x) {
        player = o;
        playerText = oText; // Set the text to 'O'
    } else {
        player = x;
        playerText = xText; // Set the text back to 'X'
    }
    // Update whoseTurn
    whoseTurn = player
}

// Handle cell click during gameplay
function cellClicked(id) {
    console.log("cell clicked", id)

    // Extract cell index
    var idName = id.toString();
    var cell = parseInt(idName[idName.length - 1]);

    // Access the DOM element corresponding to the clicked cell
    var cellElement = document.getElementById(id);

    if (myGrid.cells[cell] > 0 || whoseTurn !== player || gameOver) {
        return false; // Indicate the click had no effect
    }

    // Increment the move count with each valid click
    moves += 1;

    // Update the HTML of the cell
    // with the appropriate player's symbol and apply a class for CSS styling
    if (player === x) { // Check if the current player is 'x'
        cellElement.innerHTML = xText; // Set the cell's content to the symbol for 'x'
        cellElement.classList.add("x"); // Add class 'x' for specific styling
    } else if (player === o) { // Check if the current player is 'o'
        cellElement.innerHTML = oText; // Set the cell's content to the symbol for 'o'
        cellElement.classList.add("o"); // Add class 'o' for specific styling
    }

    // Randomly rotate the symbol for aesthetic purposes
    var rand = Math.random();
    if (rand < 0.3) {
        document.getElementById(id).style.transform = "rotate(180deg)";
    } else if (rand > 0.6) {
        document.getElementById(id).style.transform = "rotate(90deg)";
    }

    // Set the cursor to default after a move is made
    cellElement.style.cursor = "default";

    // Update the game's data structure to reflect the current state of the cell
    myGrid.cells[cell] = player;

    // Check for a winner if enough moves have been made
    if (moves >= 5) {
        winner = checkWin();
    }

    // Determine the next steps based on game mode and current game state
    if (winner === 0) { // No winner
        if (mode === 0) { // Single player mode
            whoseTurn = computer;
            makeComputerMove(); // Computer makes its move
        } else { // Multi player mode
            switchPlayer(); // Switch to the other player
        }
    }
    return true; // Indicate successful handling of the click
}

// Restart the game
function restartGame(ask) {
    // Reset game variables
    gameOver = false;
    moves = 0;
    winner = 0;
    whoseTurn = x;

    // Clears all cells in the grid
    myGrid.reset();

    // Iterate over each cell in the game board
    for (var i = 0; i <= 8; i++) {
        var cellElement = document.getElementById('cell' + i); // Get cell's ID
        cellElement.innerHTML = ""; // Clear the content of the cell
        cellElement.style.cursor = "pointer"; // Reset the cursor to pointer to indicate clickable
        cellElement.style.transform = ""; // Remove any rotation applied to the cells
        cellElement.classList.remove("x", "o", "win-color"); // Remove all classes that might have been added
    }
}

// The logic of the Computer
function makeComputerMove() {
    // Check if the game is already over. If it is, exit the function
    if (gameOver) {
        return false;
    }

    var cell = -1, // Store the chosen cell index
        myArr = [], // Store potential move indices
        corners = [0,2,6,8]; // Indices of corner cells

    // More strategic consideration if three or more moves have been made
    if (moves >= 3) {
        // Try to find a winning move
        cell = myGrid.getFirstWithTwoInARow(computer);

        // If no winning move, try to block the player's winning move
        if (cell === false) {
            cell = myGrid.getFirstWithTwoInARow(player);
        }

        // If no threats, try a strategic position
        if (cell === false) {
            if (myGrid.cells[4] === 0) {
                cell = 4; // Prefer center position
            } else {
                myArr = myGrid.getFreeCellIndices();
                cell = myArr[intRandom(0, myArr.length - 1)];
            }
        }

        // If the computer controls the center and it is the third move
        if (moves == 3 && myGrid.cells[4] == computer) {
            if (myGrid.cells[7] == player && (myGrid.cells[0] == player || myGrid.cells[2] == player)) {
                myArr = [6,8];
                cell = myArr[intRandom(0,1)];
            }
            else if (myGrid.cells[5] == player && (myGrid.cells[0] == player || myGrid.cells[6] == player)) {
                myArr = [2,8];
                cell = myArr[intRandom(0,1)];
            }
            else if (myGrid.cells[3] == player && (myGrid.cells[2] == player || myGrid.cells[8] == player)) {
                myArr = [0,6];
                cell = myArr[intRandom(0,1)];
            }
            else if (myGrid.cells[1] == player && (myGrid.cells[6] == player || myGrid.cells[8] == player)) {
                myArr = [0,2];
                cell = myArr[intRandom(0,1)];
            }
        } else if (moves == 3 && myGrid.cells[4] == player) { // If the player controls the center and it is the third move
            if (myGrid.cells[2] == player && myGrid.cells[6] == computer) {
                cell = 8;
            }
            else if (myGrid.cells[0] == player && myGrid.cells[8] == computer) {
                cell = 6;
            }
            else if (myGrid.cells[8] == player && myGrid.cells[0] == computer) {
                cell = 2;
            }
            else if (myGrid.cells[6] == player && myGrid.cells[2] == computer) {
                cell = 0;
            }
        }
    } else if (moves === 1 && myGrid.cells[4] == player) { // If the player played center, play one of the corners
        cell = corners[intRandom(0,3)];
    } else {
        if (myGrid.cells[4] === 0) { // Choose the center of the board if possible
            cell = 4;
        } else {
            myArr = myGrid.getFreeCellIndices();
            cell = myArr[intRandom(0, myArr.length - 1)];
        }
    }

    var id = "cell" + cell.toString();

    // Set the innerHTML of the chosen cell to the computer's symbol
    document.getElementById(id).innerHTML = computerText;
    // Change the cursor to default, indicate that the cell can no longer be interacted
    document.getElementById(id).style.cursor = "default";

    // Randomize rotation of marks on the board
    var rand = Math.random();
    if (rand < 0.3) {
        document.getElementById(id).style.transform = "rotate(180deg)";
    } else if (rand > 0.6) {
        document.getElementById(id).style.transform = "rotate(90deg)";
    }

    myGrid.cells[cell] = computer; // Reflect that the computer has taken the chosen cell
    moves += 1; // Increment the move counter

    // If at least 5 moves have been made in total, check the winner
    if (moves >= 5) {
        winner = checkWin();
    }

    // No winner, switch turn
    if (winner === 0 && !gameOver) {
        whoseTurn = player;
    }
}

// Increment scores
function incrementScore(playerWon) {
        if (mode === 0) {  // Single-player mode
            if (playerWon) {
                score.player1++;  // Increment Player's score
            } else {
                score.player2++;  // Increment Computer's score
            }
        } else {  // Two-player mode
            if (playerWon) {
                score.player1++;  // Increment Player 1's score
            } else {
                score.player2++;  // Increment Player 2's score
            }
        }
    }

// Check winner
function checkWin() {
    winner = 0;

    // Loop through indices to check rows, columns, and diagonals for a win condition
    for (var i = 0; i <= 2; i++) {
        var combinations = [
            myGrid.getRowValues(i), // Extract values from the ith row
            myGrid.getColumnValues(i), // Extract values from the ith column
            ...(i <= 1 ? [myGrid.getDiagValues(i)] : []) // Extract diagonal values only for the first two indices
        ];

        // Iterate over each combination of row, column, or diagonal values
        for (var combo of combinations) {
            // Check if all elements in a combination are the same and greater than zero
            if (combo[0] > 0 && combo[0] == combo[1] && combo[0] == combo[2]) {
                var playerWon = combo[0] !== computer;
                incrementScore(playerWon); // Update the score based on who won
                winner = playerWon ? player : computer; // Set the winner

                // Determine the indices of the winning cells
                var tmpAr = (combinations.indexOf(combo) == 0) ? myGrid.getRowIndices(i) :
                            (combinations.indexOf(combo) == 1) ? myGrid.getColumnIndices(i) :
                            myGrid.getDiagIndices(i);

                // Highlight the winning cells
                for (var j = 0; j < tmpAr.length; j++) {
                    var str = "cell" + tmpAr[j];
                    document.getElementById(str).classList.add("win-color");
                }

                setTimeout(endGame, 1000, winner);
                return winner;
            }
        }
    }

    // If the board is full and no winner, it is a tie
    if (myGrid.getFreeCellIndices().length === 0) {
        winner = 'tie'; // Set the game result as a tie
        score.ties++; // Increment the tie count in the scoreboard
        endGame(winner);
        return winner;
    }

    // If no winner or tie, return the default winner value, here is 0
    return winner;
}

// Display the winner
function announceWinner(text) {
    // Set the text to display the winner
    document.getElementById("winText").innerHTML = text;
    // Make the winner announcement modal visible
    document.getElementById("winAnnounce").style.display = "block";
    setTimeout(closeModal, 1400, "winAnnounce");
}

// Display the options dialog
function showOptions() {
    // Make the options dialog visible
    document.getElementById("optionsDlg").style.display = "block";
}

// Handle the selection of game options
function getOptions() {
    // Close the options modal dialog
    document.getElementById("optionsDlg").style.display = "none";

    // Determine if it is a single player or two players game
    if (document.getElementById("r0").checked) {
        mode = 0; // Set the mode to single player if the radio button with id "r0" is checked
    } else {
        mode = 1;
    }

    // Update the labels on the scoreboard based on the game mode
    if (mode === 0) { // Single player mode
        document.getElementById('score_player1_label').textContent = 'Player';
        document.getElementById('score_player2_label').textContent = 'Computer';
    } else { // Two players mode
        document.getElementById('score_player1_label').textContent = 'Player 1';
        document.getElementById('score_player2_label').textContent = 'Player 2';
    }
}

// Close a modal dialog based on the ID of the modal
function closeModal(id) {
    document.getElementById(id).style.display = "none";
}

// Handle the end of the game, display the result and reset the game
function endGame(who) {
    // Check if the game is in single player or two players mode
    if (mode === 0) { // Single player mode
        if (who == player) {
            announceWinner("Congratulations, you won!");
        } else if (who == computer) {
            announceWinner("Computer wins!");
        } else {
            announceWinner("It's a tie!");
        }
    } else { // Two players mode
        if (who == x) {
            announceWinner("Player 1 won!");
        } else if (who == o) {
            announceWinner("Player 2 won!");
        } else {
            announceWinner("It's a tie!");
        }
    }

    gameOver = true; // Indicate the game has ended
    whoseTurn = 0; // Indicate no current turn
    moves = 0; // Reset the move counter
    winner = 0; // Reset the winner

    // Update the scoreboard
    document.getElementById("player1_score").innerHTML = score.player1;
    document.getElementById("tie_score").innerHTML = score.ties;
    document.getElementById("player2_score").innerHTML = score.player2;

    setTimeout(restartGame, 800);
}