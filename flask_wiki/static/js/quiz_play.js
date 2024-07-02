// const questions = [
//     {
//         question: 'qweqwe',
//         answer: [
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: true},
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: false},
//         ]
//     },
//     {
//         question: 'second 2',
//         answer: [
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: true},
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: false},
//         ]
//     },
//     {
//         question: 'second 2',
//         answer: [
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: true},
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: false},
//         ]
//     },
//     {
//         question: 'second 2',
//         answer: [
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: true},
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: false},
//         ]
//     },
//     {
//         question: 'second 2',
//         answer: [
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: true},
//             {text: 'asdasd', correct: false},
//             {text: 'asdasd', correct: false},
//         ]
//     },
// ];

let questions = quiz.questions

const questionElement = document.getElementById('question') //h2
const answerButton = document.getElementById('answer-buttons') //div
const nextButton = document.getElementById('next-btn') //button

let curretQuestionIndex = 0;
let score = 0;

function startQuiz() {
    curretQuestionIndex = 0;
    score = 0;
    nextButton.innerHTML = "Далее";
    showQuestion();
}

function showQuestion() {
    resetState();
    let currentQuestion = questions[curretQuestionIndex];
    let questionNo = curretQuestionIndex + 1;
    questionElement.innerHTML = questionNo + ". " + currentQuestion.question;
    currentQuestion.answer.forEach(answer =>{
        const button = document.createElement('button')
        button.innerHTML = answer.text;
        button.classList.add("btn");
        answerButton.appendChild(button);
        if (answer.correct){
             button.dataset.correct = answer.correct;
        }
        button.addEventListener("click", selectAnswer)

    })

}

function sendResult(){

};

function resetState() {
    nextButton.style.display = "none";
    while(answerButton.firstChild) {
        answerButton.removeChild(answerButton.firstChild)
    }
};

function selectAnswer(event) {
    const selectedBtn = event.target;
    const isCorrect = selectedBtn.dataset.correct === "true";
    if (isCorrect) {
        selectedBtn.classList.add("correct")
        score++;
    }else {
        selectedBtn.classList.add("incorrect")
    }
    Array.from(answerButton.children).forEach(button=>{
        if(button.dataset.correct === "true") {
            button.classList.add("correct");
        }
        button.disabled = true;
    });
    nextButton.style.display = "block";

};

function showScore() {
    resetState();
    questionElement.innerHTML = `You score ${score} out of ${questions.length}!`
    nextButton.innerHTML = 'Завершить';
    nextButton.style.display = 'block';
    nextButton.addEventListener('click', ()=>{
      location.assign(indexUrl);
    });
};
function handleNextButton(){
    curretQuestionIndex++;
    if (curretQuestionIndex < questions.length) {
        showQuestion();
    }
    else {
        showScore();
    }
};

function showJson() {
    let jsonData = JSON.parse('{{ quiz | tojson | safe}}');
    console.log(jsonData);
};

nextButton.addEventListener('click',(e)=> {
    if (curretQuestionIndex < questions.length) {
        handleNextButton();
    } else {
        startQuiz();
    }
});

showQuestion();

