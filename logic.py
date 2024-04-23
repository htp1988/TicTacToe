"use strict";

// Bind Esc key to closing the modal dialog
document.onkeypress = function (evt) {
    evt = evt || window.event;
    var modal = document.getElementsByClassName("modal")[0];
    if (evt.keyCode === 27) {
        modal.style.display = "none";
    }
};

// When the user clicks anywhere outside of the modal dialog, close it
window.onclick = function (evt) {
    var modal = document.getElementsByClassName("modal")[0];
    if (evt.target === modal) {
        modal.style.display = "none";
    }
};

//==================================
// HELPER FUNCTIONS
//==================================
function sumArray(array) {
    var sum = 0,
        i = 0;
    for (i = 0; i < array.length; i++) {
        sum += array[i];
    }
    return sum;
}

function isInArray(element, array) {
    if (array.indexOf(element) > -1) {
        return true;
    }
    return false;
}

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

function intRandom(min, max) {
    var rand = min + Math.random() * (max + 1 - min);
    return Math.floor(rand);
}

// GLOBAL VARIABLES
var mode = 0,
    moves = 0,
    winner = 0,
    x = 1,
    o = 3,
    player = x,
    computer = o,
    whoseTurn = x,
    gameOver = false,
    score = {
        ties: 0,
        player1: 0,
        player2: 0
    },
    xText = "×",
    oText = "o",
    playerText = xText,
    computerText = oText,
    myGrid = null;


//==================================
// GRID OBJECT
//==================================

// Grid constructor
//=================
function Grid() {
    this.cells = new Array(9);
}

// Grid methods
//=============

// Get free cells in an array.
// Returns an array of indices in the original Grid.cells array, not the values
// of the array elements.
// Their values can be accessed as Grid.cells[index].
Grid.prototype.getFreeCellIndices = function () {
    var i = 0,
        resultArray = [];
    for (i = 0; i < this.cells.length; i++) {
        if (this.cells[i] === 0) {
            resultArray.push(i);
        }
    }
    // console.log("resultArray: " + resultArray.toString());
    // debugger;
    return resultArray;
};

// Get a row (accepts 0, 1, or 2 as argument).
// Returns the values of the elements.
Grid.prototype.getRowValues = function (index) {
    if (index !== 0 && index !== 1 && index !== 2) {
        console.error("Wrong arg for getRowValues!");
        return undefined;
    }
    var i = index * 3;
    return this.cells.slice(i, i + 3);
};

// Get a row (accepts 0, 1, or 2 as argument).
// Returns an array with the indices, not their values.
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

// get a column (values)
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

// get a column (indices)
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

// get diagonal cells
// arg 0: from top-left
// arg 1: from top-right
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

// get diagonal cells
// arg 0: from top-left
// arg 1: from top-right
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

// Get first index with two in a row (accepts computer or player as argument)
Grid.prototype.getFirstWithTwoInARow = function (agent) {
    if (agent !== computer && agent !== player) {
        console.error("Function getFirstWithTwoInARow accepts only player or computer as argument.");
        return undefined;
    }
    var sum = agent * 2,
        freeCells = shuffleArray(this.getFreeCellIndices());
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
        for (j = 0; j < 2; j++) {
            var diagV = this.getDiagValues(j);
            var diagI = this.getDiagIndices(j);
            if (sumArray(diagV) == sum && isInArray(freeCells[i], diagI)) {
                return freeCells[i];
            }
        }
    }
    return false;
};

Grid.prototype.reset = function () {
    for (var i = 0; i < this.cells.length; i++) {
        this.cells[i] = 0;
    }
    return true;
};

//==================================
// MAIN FUNCTIONS
//==================================

// executed when the page loads
function initialize() {
    myGrid = new Grid();
    moves = 0;
    winner = 0;
    gameOver = false;
    whoseTurn = player; // default, this may change
    for (var i = 0; i <= myGrid.cells.length - 1; i++) {
        myGrid.cells[i] = 0;
    }
    // setTimeout(assignRoles, 500);
    setTimeout(showOptions, 500);
    // debugger;
}

function switchPlayer() {
    // Switch the 'player' between 'x' and 'o'
    if (player === x) {
        player = o;
        playerText = oText; // Set the text to 'O'
    } else {
        player = x;
        playerText = xText; // Set the text back to 'X'
    }
    // Update whoseTurn to the new player
    whoseTurn = player
}

// executed when player clicks one of the table cells
function cellClicked(id) {
    // The last character of the id corresponds to the numeric index in Grid.cells:
    var idName = id.toString();
    var cell = parseInt(idName[idName.length - 1]);
    var cellElement = document.getElementById(id); // Define cellElement here

    if (myGrid.cells[cell] > 0 || whoseTurn !== player || gameOver) {
        // cell is already occupied or something else is wrong
        return false;
    }
    moves += 1;

    // Update the cell with the player's symbol and apply the corresponding class
    if (player === x) { // Assuming x represents player X
        cellElement.innerHTML = xText; // Assuming xText is 'X'
        cellElement.classList.add("x");
    } else if (player === o) { // Assuming o represents player O
        cellElement.innerHTML = oText; // Assuming oText is 'O'
        cellElement.classList.add("o");
    }

    // randomize orientation (for looks only)
    var rand = Math.random();
    if (rand < 0.3) {
        document.getElementById(id).style.transform = "rotate(180deg)";
    } else if (rand > 0.6) {
        document.getElementById(id).style.transform = "rotate(90deg)";
    }

    cellElement.style.cursor = "default";
    myGrid.cells[cell] = player;
    // Test if we have a winner:
    if (moves >= 5) {
        winner = checkWin();
    }
    if (winner === 0) {
        if (mode === 0) { // If single-player mode, computer makes a move
            whoseTurn = computer;
            makeComputerMove();
        } else { // If multi-player mode, switch to the other player
            switchPlayer(); // You need to implement switchPlayer() if not already done
        }
    }
    return true;
}

// Executed when player hits restart button.
// ask should be true if we should ask users if they want to play as X or O
function restartGame(ask) {
    if (ask && moves > 0) {
        var response = confirm("Are you sure you want to start over?");
        if (response === false) {
            return;
        }
    }
    gameOver = false;
    moves = 0;
    winner = 0;
    whoseTurn = x;
    myGrid.reset();

    for (var i = 0; i <= 8; i++) {
        var cellElement = document.getElementById('cell' + i);
        cellElement.innerHTML = "";
        cellElement.style.cursor = "pointer";
        cellElement.style.transform = ""; // Remove any rotation applied to the cells
        cellElement.classList.remove("x", "o", "win-color"); // Clear all relevant classes
    }
    if (ask) {
        setTimeout(showOptions, 200);
    } else if (whoseTurn === computer && mode === 0) {
        setTimeout(makeComputerMove, 800);
    }
}

// The logic of the Computer
function makeComputerMove() {
    // debugger;
    if (gameOver) {
        return false;
    }
    var cell = -1,
        myArr = [],
        corners = [0,2,6,8];
    if (moves >= 3) {
        cell = myGrid.getFirstWithTwoInARow(computer);
        if (cell === false) {
            cell = myGrid.getFirstWithTwoInARow(player);
        }
        if (cell === false) {
            if (myGrid.cells[4] === 0) {
                cell = 4;
            } else {
                myArr = myGrid.getFreeCellIndices();
                cell = myArr[intRandom(0, myArr.length - 1)];
            }
        }
        // Avoid a catch-22 situation:
        if (moves == 3 && myGrid.cells[4] == computer && player == x) {
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
        }
        else if (moves == 3 && myGrid.cells[4] == player && player == x) {
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
    } else if (moves === 1 && myGrid.cells[4] == player) {
        // if player is X and played center, play one of the corners
        cell = corners[intRandom(0,3)];
    } else if (moves === 2 && myGrid.cells[4] == player && computer == x) {
        // if player is O and played center, take two opposite corners
        if (myGrid.cells[0] == computer) {
            cell = 8;
        }
        else if (myGrid.cells[2] == computer) {
            cell = 6;
        }
        else if (myGrid.cells[6] == computer) {
            cell = 2;
        }
        else if (myGrid.cells[8] == computer) {
            cell = 0;
        }
    } else if (moves === 0 && intRandom(1,10) < 8) {
        // if computer is X, start with one of the corners sometimes
        cell = corners[intRandom(0,3)];
    } else {
        // choose the center of the board if possible
        if (myGrid.cells[4] === 0) {
            cell = 4;
        } else {
            myArr = myGrid.getFreeCellIndices();
            cell = myArr[intRandom(0, myArr.length - 1)];
        }
    }
    var id = "cell" + cell.toString();
    // console.log("computer chooses " + id);
    document.getElementById(id).innerHTML = computerText;
    document.getElementById(id).style.cursor = "default";
    // randomize rotation of marks on the board to make them look
    // as if they were handwritten
    var rand = Math.random();
    if (rand < 0.3) {
        document.getElementById(id).style.transform = "rotate(180deg)";
    } else if (rand > 0.6) {
        document.getElementById(id).style.transform = "rotate(90deg)";
    }
    myGrid.cells[cell] = computer;
    moves += 1;
    if (moves >= 5) {
        winner = checkWin();
    }
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

// Check if the game is over and determine winner
function checkWin() {
    winner = 0;

    // rows, columns, diagonals
    for (var i = 0; i <= 2; i++) {
        var combinations = [
            myGrid.getRowValues(i),
            myGrid.getColumnValues(i),
            ...(i <= 1 ? [myGrid.getDiagValues(i)] : [])
        ];

        for (var combo of combinations) {
            if (combo[0] > 0 && combo[0] == combo[1] && combo[0] == combo[2]) {
                var playerWon = combo[0] !== computer;
                incrementScore(playerWon);
                winner = playerWon ? player : computer;

                var tmpAr = (combinations.indexOf(combo) == 0) ? myGrid.getRowIndices(i) :
                            (combinations.indexOf(combo) == 1) ? myGrid.getColumnIndices(i) :
                            myGrid.getDiagIndices(i);

                for (var j = 0; j < tmpAr.length; j++) {
                    var str = "cell" + tmpAr[j];
                    document.getElementById(str).classList.add("win-color");
                }

                setTimeout(endGame, 1000, winner);
                return winner;
            }
        }
    }

    // If the board is full and no winner, it's a tie
    if (myGrid.getFreeCellIndices().length === 0) {
        winner = 'tie';
        score.ties++;
        endGame(winner);
        return winner;
    }

    return winner;
}

function announceWinner(text) {
    document.getElementById("winText").innerHTML = text;
    document.getElementById("winAnnounce").style.display = "block";
    setTimeout(closeModal, 1400, "winAnnounce");
}

function showOptions() {
  document.getElementById("optionsDlg").style.display = "block";
}

function updateScoreboardLabels() {
  if (mode === 0) {
    // Single-player mode
    document.getElementById('score_player1_label').textContent = 'Player';
    document.getElementById('score_player2_label').textContent = 'Computer';
  } else {
    // Two-player mode
    document.getElementById('score_player1_label').textContent = 'Player 1';
    document.getElementById('score_player2_label').textContent = 'Player 2';
  }
}

// Call the right function when the Play button is clicked
function getOptions() {
    // Close the options modal dialog
    document.getElementById("optionsDlg").style.display = "none";

    // Determine if it's a single-player or multi-player game
    if (document.getElementById("r0").checked) {
        mode = 0;
    } else {
        mode = 1;
    }

    updateScoreboardLabels();
}

function closeModal(id) {
    document.getElementById(id).style.display = "none";
}

function endGame(who) {
    if (mode === 0) {
        if (who == player) {
            announceWinner("Congratulations, you won!");
        } else if (who == computer) {
            announceWinner("Computer wins!");
        } else {
            announceWinner("It's a tie!");
        }
    } else {
        if (who == x) {
            announceWinner("Player 1 won!");
        } else if (who == o) {
            announceWinner("Player 2 won!");
        } else {
            announceWinner("It's a tie!");
        }
    }

    gameOver = true;
    whoseTurn = 0;
    moves = 0;
    winner = 0;

    // Update the scoreboard correctly
    document.getElementById("player1_score").innerHTML = score.player1;
    document.getElementById("tie_score").innerHTML = score.ties;
    document.getElementById("player2_score").innerHTML = score.player2;

    for (var i = 0; i <= 8; i++) {
        var id = "cell" + i.toString();
        document.getElementById(id).style.cursor = "default";
    }
    setTimeout(restartGame, 800);
}




'''''''''''''''''''''''''''''''''''''''''''''''''''''''

<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic-tac-toe</title>
    <link rel="stylesheet" href="static/styles.css">
    <link href="https://fonts.googleapis.com/css?family=Indie+Flower" rel="stylesheet">
  </head>
  <body onload="initialize()">
    <h1>Tic-Tac-Toe</h1>
    <table id="table_game">
      <tr>
        <td class="td_game"><div id="cell0" onclick="cellClicked(this.id)" class="fixed"></div></td>
        <td class="td_game"><div id="cell1" onclick="cellClicked(this.id)" class="fixed"></div></td>
        <td class="td_game"><div id="cell2" onclick="cellClicked(this.id)" class="fixed"></div></td>
      </tr>
      <tr>
        <td class="td_game"><div id="cell3" onclick="cellClicked(this.id)" class="fixed"></div></td>
        <td class="td_game"><div id="cell4" onclick="cellClicked(this.id)" class="fixed"></div></td>
        <td class="td_game"><div id="cell5" onclick="cellClicked(this.id)" class="fixed"></div></td>
      </tr>
      <tr>
        <td class="td_game"><div id="cell6" onclick="cellClicked(this.id)" class="fixed"></div></td>
        <td class="td_game"><div id="cell7" onclick="cellClicked(this.id)" class="fixed"></div></td>
        <td class="td_game"><div id="cell8" onclick="cellClicked(this.id)" class="fixed"></div></td>
      </tr>
    </table>
    <div id="restart" title="Start new game" onclick="restartGame(true)"><span style="vertical-align:top;position:relative;top:-10px">#</span></div>
    <table>
      <tr>
        <th class="th_list" id="score_player1_label">Player</th>
        <th class="th_list" style="padding-right:10px;padding-left:10px" id="score_draws_label">Draws</th>
        <th class="th_list" id="score_player2_label">Computer</th>
      </tr>
      <tr>
        <td class="td_list" id="player1_score">0</td>
        <td class="td_list" style="padding-right:10px;padding-left:10px" id="tie_score">0</td>
        <td class="td_list" id="player2_score">0</td>
      </tr>
    </table>
    <!-- The modal dialog for announcing the winner -->
    <div id="winAnnounce" class="modal">
      <!-- Modal content -->
      <div class="modal-content">
        <span class="close" onclick="closeModal('winAnnounce')">×</span>
        <p id="winText"></p>
      </div>
    </div>
    <!-- The dialog for getting feedback from the user -->
    <div id="userFeedback" class="modal">
      <!-- Modal content -->
      <div class="modal-content">
        <p id="questionText"></p>
        <p><button id="yesBtn">Yes</button> <button id="noBtn">No</button></p>
      </div>
    </div>
    <!-- The options dialog -->
    <div id="optionsDlg" class="modal">
      <!-- Modal content -->
      <div class="modal-content">
        <h2>How would you like to play?</h2>
          <h3>Player:</h3>
          <label><input type="radio" name="player" id="r0" value="0">1 Player </label>
          <label><input type="radio" name="player" id="r1" value="1" checked>2 Player</label><br>
          <p><button id="okBtn" onclick="getOptions()">Play</button></p>
      </div>
    </div>
    <script src="static/script.js"></script>
  </body>
</html>