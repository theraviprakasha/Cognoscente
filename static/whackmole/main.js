const cursor = document.querySelector('.cursor');
const holes = [...document.querySelectorAll('.hole')];
const scoreEl = document.querySelector('.score span');
const accuracyEl = document.querySelector('.accuracy span');
const reactionTimeEl = document.querySelector('.reaction-time span');
const durationEl = document.querySelector('.duration');
let score = 0;
let totalActions = 0;
let reactionTimes = [];
let successfulHits = 0;
let gameInterval, stopwatchInterval, elapsedMilliseconds = 0;
const sound = new Audio("http://127.0.0.1:5000/static/whackmole/assets/smash.mp3");
let gameActive = false;
let startTime;

function run() {
    if (!gameActive) return;

    const i = Math.floor(Math.random() * holes.length);
    const hole = holes[i];
    let timer = null;

    const img = document.createElement('img');
    img.classList.add('mole');
    img.src = 'http://127.0.0.1:5000/static/whackmole/assets/mole.png';

    img.addEventListener('click', () => {
        if (!gameActive) return;

        score += 10;
        totalActions += 1;
        const reactionTime = new Date() - startTime;
        reactionTimes.push(reactionTime);
        successfulHits++;
        updateDisplay();
        updateReactionTimeDisplay();
        sound.play();
        img.src = 'http://127.0.0.1:5000/static/whackmole/assets/mole-whacked.png';
        clearTimeout(timer);
        setTimeout(() => {
            hole.removeChild(img);
            run();
        }, 500);
    });

    hole.appendChild(img);

    timer = setTimeout(() => {
        if (!gameActive) return;

        totalActions += 1;
        updateDisplay();
        hole.removeChild(img);
        run();
    }, 1500);

}

function updateDisplay() {
    const accuracy = totalActions > 0 ? ((score / 10) / totalActions * 100).toFixed(2) : 0;

    scoreEl.textContent = score.toString().padStart(2, '0');
    accuracyEl.textContent = `${accuracy}%`;
}

function updateReactionTimeDisplay() {
    const averageReactionTime = successfulHits > 0 ?
        (reactionTimes.reduce((sum, time) => sum + time, 0) / successfulHits).toFixed(2) / 1000 : 0;

    reactionTimeEl.textContent = `${averageReactionTime}s`;
}

function updateDuration() {
    const now = new Date();
    elapsedMilliseconds = now - startTime;
    const minutes = Math.floor(elapsedMilliseconds / 60000).toString().padStart(2, '0');
    const seconds = Math.floor((elapsedMilliseconds % 60000) / 1000).toString().padStart(2, '0');
    durationEl.textContent = `DURATION: ${minutes}:${seconds}`;
}

function startGame() {
    gameActive = true;
    score = 0;
    totalActions = 0;
    successfulHits = 0;
    reactionTimes = [];
    startTime = new Date();
    elapsedMilliseconds = 0; 
    updateDisplay();
    run();
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
    gameInterval = setInterval(updateDuration, 1000);
}

function stopGame() {
    gameActive = false;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    clearInterval(gameInterval);
    clearInterval(stopwatchInterval); 
    const moles = document.querySelectorAll('.mole');
    moles.forEach(mole => mole.parentNode.removeChild(mole));
    updateReactionTimeDisplay();
}

document.getElementById('startBtn').addEventListener('click', () => {
    startGame();
    stopwatchInterval = setInterval(updateDuration, 1000);
});

document.getElementById('stopBtn').addEventListener('click', () => {
    const duration = durationEl.innerText;
    const score = document.getElementById('score').innerText;
    const accuracy = document.getElementById('accuracy').innerText;
    const reactionTime = document.getElementById('reactionTime').innerText;
  
    fetch('/update_whackmole', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ score: score, accuracy: accuracy,  reactionTime: reactionTime, duration:duration})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
    stopGame();
    clearInterval(stopwatchInterval);
});

window.addEventListener('mousemove', e => {
    cursor.style.top = e.pageY + 'px';
    cursor.style.left = e.pageX + 'px';
});

window.addEventListener('mousedown', () => {
    cursor.classList.add('active');
});

window.addEventListener('mouseup', () => {
    cursor.classList.remove('active');
});