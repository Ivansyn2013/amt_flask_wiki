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

let questions = quiz.questions;
let quizResult = [];
// let quizUrl = 'wiki/quiz_pass'

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
    let question_id = currentQuestion.question_id;

    questionElement.innerHTML = questionNo + ". " + currentQuestion.question;
    currentQuestion.answer.forEach(answer =>{
        const button = document.createElement('button')
        button.innerHTML = answer.text;
        button.classList.add("btn");
        answerButton.appendChild(button);
        if (answer.correct){
             button.dataset.correct = answer.correct;
        }
        button.question_id = question_id
        button.answer_id = answer.answer_id
        button.addEventListener("click", selectAnswer)

    })

}

function sendResult(data){
    fetch(quizUrl, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    })
        .then(responce => responce.json()
            .then(data => {
                console.log(data);
            }))
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
    oneResult = {
        "quiz_id" : quiz.id,
        "question_id" : selectedBtn.question_id,
        "answer_id" : selectedBtn.answer_id,
        "correct" : "",
    }

    if (isCorrect) {
        selectedBtn.classList.add("neutral");
        oneResult.correct = true
        score++;
    }else {
        selectedBtn.classList.add("neutral")
        oneResult.correct = false
    }
    Array.from(answerButton.children).forEach(button=>{
        if(button.dataset.correct === "true") {
            // button.classList.add("correct");
        }
        button.disabled = true;
    });

    quizResult.push(oneResult)
    nextButton.style.display = "block";

};

function showScore() {
    resetState();
    questionElement.innerHTML = `You score ${score} out of ${questions.length}!`
    nextButton.innerHTML = 'Завершить';
    nextButton.style.display = 'block';
    sendResult(quizResult)
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

