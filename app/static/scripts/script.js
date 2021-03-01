const res = new XMLHttpRequest();

const drawBtn = document.querySelector('#draw_word');
const wordInput = document.querySelector('#put_word');
const checkBtn = document.querySelector('#check_input');
const counterRightGuess = document.querySelector('#counter_words');
const delBtns = document.querySelectorAll('.del_btn');
const testGenBtn = document.querySelector('#generate_test');
const testArea = document.querySelector('.test_area')
let transStore = [];
let eng_word = null;


const drawWord = (clear=true) => {
    if (clear) {
        drawBtn.nextElementSibling.remove();
    }
    res.open('POST', window.location.origin + '/get_random_word');
    res.send();
    res.onreadystatechange = () => {
        if (res.readyState == 4) {
            let word = document.createElement('span');
            word.setAttribute('class', 'eng_word');
            let jsonObj = JSON.parse(res.response);
            transStore = jsonObj.translates;
            eng_word = jsonObj.word;
            word.innerText = eng_word;
            drawBtn.insertAdjacentElement("afterend", word);
        };
    };
};

drawBtn.addEventListener('click', () => {
    drawWord();
});

checkBtn.addEventListener('click', () => {
    let answer = wordInput.value;
    if (transStore.indexOf(answer) > -1) {
        let counterValue = counterRightGuess.innerText;
        counterValue++;
        counterRightGuess.innerText = counterValue;
        drawWord();
    } else {
        console.log('nie git');
        console.log(transStore);
    }
});



window.addEventListener('DOMContentLoaded', () => {
    drawWord(false);
    delBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log(btn.parentElement.innerText.split(' ')[0]);
        });
    });
});