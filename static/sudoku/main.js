var sideLength = 9;
var sol = 0;
var boxColor = "#8F1D21";
var nums = new Array(sideLength);
var sudoku = new Array(sideLength);
var uncompleteSudoku = new Array(sideLength);
var emptyCells = [];
var grid = document.querySelectorAll(".content");
var checkBtn = document.querySelector("#Check");
var newBtn = document.querySelector("#clear");
var board = document.getElementById("board");
var table = document.querySelector("table");
var message = document.getElementById("message");
let incorrectEntries = 0;
let initialEmptyBoxes = 0;
let correctEntries = 0;

document.addEventListener('DOMContentLoaded', function() {
    var startButton = document.getElementById('start');
    var stopButton = document.getElementById('stop');
    var checkButton = document.getElementById('check');
    var timerDisplay = document.getElementById('timer');
    var startTime, timerInterval;

    // Disable the input fields
    grid.forEach(function(content) {
        content.disabled = true;
    });

    startButton.addEventListener('click', function() {
        startTime = new Date().getTime();
        timerInterval = setInterval(updateTimer, 1000);

        // Enable the input fields
        grid.forEach(function(content) {
            content.disabled = false;
        });
    });

    stopButton.addEventListener('click', function() {
        clearInterval(timerInterval);

        // Disable the input fields
        grid.forEach(function(content) {
            content.disabled = true;
        });
    });

    checkButton.addEventListener('click', function() {
        grid.check();
    });

    function updateTimer() {
        var currentTime = new Date().getTime();
        var elapsedTime = currentTime - startTime;
        var hours = Math.floor(elapsedTime / 3600000);
        var minutes = Math.floor((elapsedTime % 3600000) / 60000);
        var seconds = Math.floor((elapsedTime % 60000) / 1000);
        timerDisplay.textContent = pad(hours) + ':' + pad(minutes) + ':' + pad(seconds);

        // Check if the game has been won
        if (grid.isWin()) {
            clearInterval(timerInterval);
        }
    }

    function pad(num) {
        return (num < 10 ? '0' : '') + num;
    }
});

grid.fill = function(){
    emptyCells = [];
    message.textContent = "Good Luck!";
    this.forEach(function(content, i){
        var row = Math.floor(i / 9);
        var col = i % 9;
        content.classList.remove("victory");
        if(uncompleteSudoku[row][col]){
            content.value = uncompleteSudoku[row][col];
            content.readOnly = "true";
            content.disabled = "true";
            content.classList.add("disabled");
            content.classList.remove("free");
        }
        else{
            content.row = row;
            content.col = col;
            emptyCells.push(content);
            content.value = "";
            content.readOnly = "";
            content.disabled = "";
            content.classList.add("free");
            content.classList.remove("disabled");
        }
    });
    initialEmptyBoxes = emptyCells.length;
    correctEntries = 0;
    document.getElementById('progress').textContent = `Progress: 0%`;
}
grid.setBoxes = function(){
    this.forEach(function(cell, i){
        var row = Math.floor(i / 9);
        var col = i % 9;
        if(row % 3 === 0){
            cell.style.borderTopColor = boxColor;
        }
        else if(row === 8){
            cell.style.borderBottomColor = boxColor;
        }
        if(col % 3 === 0){
            cell.style.borderLeftColor = boxColor;
        }
        else if(col === 8){
            cell.style.borderRightColor = boxColor;
        }
    });
}
grid.setFont = function(){
    var tableWidth = table.offsetWidth;
    grid.forEach(function(cell){
        cell.style.fontSize = tableWidth * 0.042 + "px";
    });
};
grid.isWin = function(){
    for(let i = 0; i < grid.length; i++){
        var row = Math.floor(i / 9);
        var col = i % 9;
        if(Number(grid[i].value) !== sudoku[row][col]) return false;
    }
    return true;
};
grid.colorRow = function(row){
    for(let i = row * 9; i < row * 9 + 9; i++){
        grid[i].classList.add("wrong");
    }
};
grid.colorCol = function(col){
    for(let i = col; i < col + 73; i += 9){
        grid[i].classList.add("wrong");
    }
};
grid.colorBox = function(rstart, cstart){
    for(let r = rstart; r < rstart + 3; r++){
        for(let c = cstart; c < cstart + 3; c++){
            var index = r * 9 + c;
            grid[index].classList.add("wrong");
        }
    }
};
grid.removeColor = function(){
    grid.forEach(function(cell){
        cell.classList.remove("wrong");
    });
};
grid.check = function(){
    var failMessage = "You have made mistakes as indicated in red!";
    grid.removeColor();
    message.textContent = "Fine! Keep Going";
    for(let i = 0; i < grid.length; i++){
        var row = Math.floor(i / 9);
        var col = i % 9;
        var num = Number(grid[i].value);
        var rstart = Math.floor(row / 3) * 3;
        var cstart = Math.floor(col / 3) * 3;
        if(num === 0 || grid[i].readOnly)continue;
        for(let j = row * 9 ; j < row  * 9 + sideLength; j++){
            if(grid[j] === grid[i])continue;
            if(num === Number(grid[j].value)){
                console.log("error in row", row);
                message.textContent = failMessage;
                grid.colorRow(row);
                incorrectEntries++;
                document.getElementById('incorrect-entries').textContent = 'Mistakes: ' + incorrectEntries;
            }
        }
        for(let j = col; j < col + 73; j += 9){
            if(grid[j] === grid[i])continue;
            if(num === Number(grid[j].value)){
                console.log("error in column", col);
                message.textContent = failMessage;
                grid.colorCol(col);
                incorrectEntries++;
                document.getElementById('incorrect-entries').textContent = 'Mistakes: ' + incorrectEntries;
            }
        }
        for(let r = rstart; r < rstart + 3; r++){
            for(let c = cstart ; c < cstart + 3; c++){
                var index = r * sideLength + c;
                if(grid[index] === grid[i])continue;
                if(num === Number(grid[index].value)){
                    console.log("error in box", row, col);
                    message.textContent = failMessage;
                    grid.colorBox(rstart, cstart);
                    incorrectEntries++;
                    document.getElementById('incorrect-entries').textContent = 'Mistakes: ' + incorrectEntries;
                }
            }
        }
    }
        const progress = document.getElementById('progress').innerText;
        const Mistakes = document.getElementById('incorrect-entries').innerText;
        const timer = document.getElementById('timer').innerText;

        fetch('/update_sudoku', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ progress: progress, Mistakes: Mistakes, timer:timer })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
};
grid.setEvents = function(){
    this.forEach(function(cell){
        cell.addEventListener("input", function(){
            if(grid.isWin()){
                victory();
            }
            if(isNaN(cell.value) || cell.value === ' '){
                cell.value = "";
            }
            // Increase the number of mistakes if the move is incorrect
            var row = cell.row;
            var col = cell.col;
            var num = Number(cell.value);
            if(num !== 0 && num !== sudoku[row][col]){
                incorrectEntries++;
                document.getElementById('incorrect-entries').textContent = 'Mistakes: ' + incorrectEntries;
            } else if (num === sudoku[row][col]) {
                if (!cell.classList.contains("correct")) {
                    cell.classList.add("correct");
                    correctEntries++;
                }
            } else if (cell.classList.contains("correct")) {
                cell.classList.remove("correct");
                correctEntries--;
            }
            let progress = (correctEntries / initialEmptyBoxes) * 100;
            document.getElementById('progress').textContent = `Progress: ${progress.toFixed(2)}%`;
        });
        cell.addEventListener("keypress", function(event){
            var emptyCellsIndex = emptyCells.indexOf(cell);
            switch (event.code) {
                case "ArrowRight":
                    emptyCellsIndex++;
                    if(emptyCellsIndex >= emptyCells.length){
                        emptyCellsIndex = 0;
                    }
                    emptyCells[emptyCellsIndex].focus();
                    break;
                case "ArrowLeft":
                    emptyCellsIndex--;
                    if(emptyCellsIndex < 0)emptyCellsIndex = emptyCells.length - 1;
                    emptyCells[emptyCellsIndex].focus();
                    break;
                case "ArrowUp":
                    for(let i = cell.row - 1; i >= 0 ; i--){
                        let index = i * 9 + cell.col;
                        if(!grid[index].disabled){
                            grid[index].focus();
                            break;
                        }
                    }
                    break;
                case "ArrowDown":
                    for(let i = cell.row + 1; i <= 8; i++){
                        let index = i * 9 + cell.col;
                        if(!grid[index].disabled){
                            grid[index].focus();
                            break;
                        }
                    }
                    break;
            }
            if((Number(event.key) >= 1 && Number(event.key) <= 9)){
                emptyCellsIndex++;
                if(emptyCellsIndex >= emptyCells.length){
                    emptyCellsIndex = 0;
                }
                if(Number(emptyCells[emptyCellsIndex].value) === 0)
                emptyCells[emptyCellsIndex].focus(); 
            }
        });
    });
    checkBtn.addEventListener("click", function() {
        grid.check();
    });
    newBtn.addEventListener("click", function() {
        startTime = new Date().getTime();
        clearInterval(timerInterval);

        // Disable the input fields
        grid.forEach(function(content) {
            content.disabled = true;
        });

        // Clear the timer display
        timerDisplay.textContent = '00:00:00';

        // Generate a new board
        game();
    });
};
grid.setGrid = function(){
    grid.fill();
    grid.setFont();
    grid.setBoxes();
};

// ________CODE_________
for(let i = 0; i < nums.length; i++){
    nums[i] = i + 1;
}
board.style.width = table.offsetWidth;
window.addEventListener("resize", function(){
    board.style.width = table.offsetWidth;
    grid.setFont();
})
game();
grid.setEvents();
// ________CODE_________

function game(){
    grid.removeColor();
    fillTable();
    setPlayableSudoku();
    grid.setGrid();
}
function victory(){
    console.log("Victory!!");
    message.textContent = "Good Job!"
    grid.forEach(function(cell){
        cell.classList.add("victory");
        cell.disabled = true;
    });
    clearInterval(timerInterval);
}
// fill the sudoku table
function fillTable(){
    makeArray(sudoku);
    for(let row  = 0; row < sudoku.length; row++){
        for(let col = 0; col < sudoku.length; col++){
            var cpy = nums.slice();
            if(!setValues(cpy, row, col)) {
                solveIssue(row, col);
                cpy = nums.slice();
                setValues(cpy, row, col);
            }
            var rand = Math.floor(Math.random() * cpy.length);
            sudoku[row][col] = cpy[rand];
        }
    }
    if(isValid()){
        // showsudoku(sudoku, p);
    }
    else{
        sudoku = new Array(sideLength);
        for(let i = 0 ; i < sideLength ; i++){
            sudoku[i] = new Array(sideLength);
        }
        fillTable();
    }
}
// showsudoku();
 function removeFromBox(arr, rowp, colp){
    var rStart = Math.floor(rowp / 3) * 3;
    var cStart = Math.floor(colp / 3) * 3;
    for(let row = rStart; row < rStart + 3; row++){
        for(let col = cStart; col < cStart + 3; col++){
            if(arr.indexOf(sudoku[row][col]) !== -1){
                arr.splice(arr.indexOf(sudoku[row][col]), 1);
            }
        }
    }
 }

 function showsudoku(arr, tableDisplay){
     var str = "";
     arr.forEach(function(row){
        row.forEach(function(square){
            if(square){
                str += square + "    ";
            }
            else str += "<span>E</span>" + "    ";
        });
        str += "<br>";
     });
     tableDisplay.innerHTML = str;
 }

 function removeFromRow(cpy, row){
    for(let i = 0; i < sideLength; i++){
        if(sudoku[row][i] === undefined) continue;
        if(cpy.indexOf(sudoku[row][i]) !== -1) {
            cpy.splice(cpy.indexOf(sudoku[row][i]), 1);
        }
    }
 }

 function removeFromUp(cpy, row, col){
    for(let i = 0; i < row; i++){
        if(cpy.indexOf(sudoku[i][col]) !== -1){
            cpy.splice(cpy.indexOf(sudoku[i][col]), 1);
        }
    }
 }
 function solveIssue(row, col){
    var solved = false;
    var values = [];
    takeFromUp(values, row, col);
    takeFromBox(values, row, col);
    console.log(values, row, col);
    for(let c = col - 1; c >= 0; c--){
        var valuesCpy = values.slice();
        if(valuesCpy.indexOf(sudoku[row][c]) !== -1) continue;
        if(!setValues(valuesCpy, row, c)) continue;
        var rand = Math.floor(Math.random() * valuesCpy.length);
        sudoku[row][c] = valuesCpy[rand];
        solved = true;
    }
    return solved;
 }

 function takeFromUp(arr, row, col){
    for(let i = 0; i < row; i++){
        if(arr.indexOf(sudoku[i][col]) === -1){
            arr.push(sudoku[i][col]);
        }
    }
 }

 function takeFromBox(arr, rowp, colp){
    var rStart = Math.floor(rowp / 3) * 3;
    var cStart = Math.floor(colp / 3) * 3;
    for(let row = rStart; row < rStart + 3; row++){
        if(row === rowp) continue;
        for(let col = cStart; col < cStart + 3; col++){
            if(arr.indexOf(sudoku[row][col]) === -1 && sudoku[row][col] !== undefined){
                arr.push(sudoku[row][col]);
            }
        }
    }
 }

 function setValues(cpy, row, col){
    removeFromRow(cpy, row);
    removeFromUp(cpy, row, col);
    removeFromBox(cpy, row, col);
    if(cpy[0] === undefined){
        return false;
    }
    return true;
 }

 function isValid(){
    for(let row = 0; row < sideLength; row++){
        for(let col = 0; col < sideLength; col++){
            if(sudoku[row][col] === undefined) return false;
        }
    }
    return true;
 }
 function makeArray(array){
    for(let i = 0 ; i < sideLength ; i++){
        array[i] = new Array(sideLength);
    }
 }

 function setPlayableSudoku(){
    makeArray(uncompleteSudoku);
    for(let row = 0; row < sideLength; row++){
        for(let col = 0; col < sideLength; col++){
            uncompleteSudoku[row][col] = undefined;
        }
    }
    // for(let i = 0; i < 3; i++){
    //     fillRandCell();
    // }
    // showsudoku(uncompleteSudoku, uncomplete);
    var array = new Array(sideLength);
    makeArray(array);
    array = makeCopy(array);
    while(solve(array)){
        sol = 0;
        fillRandCell();
        array = makeCopy(array);
    }
    // showsudoku(uncompleteSudoku, uncomplete);
 }

 function fillRandCell(){
    var randrow = Math.floor(Math.random()  * sideLength);
    var randcol = Math.floor(Math.random()  * sideLength);
    uncompleteSudoku[randrow][randcol] = sudoku[randrow][randcol];
    uncompleteSudoku[8 - randrow][8 - randcol] = sudoku[8 - randrow][8 - randcol];
    console.log("im here");
 }

 function solve(arr){
    var row;
    var col;
    if(!findUnassigned()){
        sol++;
        return sol > 1 ;
    }
    for(let i = 1; i <= 9; i++){
        if(isSafe(arr, row, col, i)){
            arr[row][col] = i;
            if(solve(arr)) return true;

            arr[row][col] = undefined;
        }
    }
    return false;

    function findUnassigned(){
        for(let rowp = 0; rowp < sideLength; rowp++){
            for(let colp = 0; colp < sideLength; colp++){
                if(arr[rowp][colp] === undefined){
                   row = rowp;
                   col = colp;
                   return true; 
                }
            }
        }
        return false;
     }
 }

 function isSafe(arr, row, col, num){
    for(let i = 0; i < sideLength; i++){
        if(arr[row][i] === num || arr[i][col] === num) return false;
    }
    var rStart = Math.floor(row / 3) * 3;
    var cStart = Math.floor(col / 3) * 3;
    for(let r = rStart; r < 3; r++){
        for(let c = cStart; c < 3; c++){
            if(arr[r][c] === num) return false;
        }
    }
    return true;
 }
 function makeCopy(array){
    for(let row = 0; row < sideLength; row++){
        for(let col = 0; col < sideLength; col++){
            array[row][col] = uncompleteSudoku[row][col];
        }
    }
    return array;
 }