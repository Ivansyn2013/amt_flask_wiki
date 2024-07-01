function renderResponse(responceData) {
    //const renderConrtainer = document.getElementsByClassName('col-md-8 offset-md-2')[0]
    //renderConrtainer.innerHTML = responceData; // render text of responce in container
    document.body.innerHTML = responceData;
};

function sendFormData(data){
    let url = window.location.href;

    const xhr = new XMLHttpRequest();

    xhr.onload = function() {
    if (xhr.status === 200) {
        const response = xhr.responseText;
        console.log('Server response:', response);
        renderResponse(response);  // Call a function to render the response
    } else {
        console.error('Request failed with status:', xhr.status);
        // Handle error cases, e.g., show error message to user
    }
};

    xhr.onerror = function() {
        console.error('Request failed');
        // Handle network errors or other issues
    };

    xhr.ontimeout = function() {
        console.error('Request timed out');
        // Handle timeout situations
};


    xhr.open('POST', url, );  // Third parameter false makes the request synchronous
    xhr.setRequestHeader('Content-Type', 'application/json');  // Set appropriate headers if needed
    xhr.send(JSON.stringify(data));



};

function findAnswers(element){
    let answers = {};
    let nextElement = element.nextElementSibling;
    while (nextElement.id.includes('answer')) {
        let correct = nextElement.querySelector('#correct_answer')
        let answer_text = nextElement.querySelector('#answer')

        answers[nextElement.id] = {
            'correct' : correct.value,
            'text' : answer_text.value,
        }
        nextElement = nextElement.nextElementSibling;
    }
    return answers
};

function findNextDiv(element, find_tag = 'div') {
    let nextElement = element.parentElement.nextElementSibling;
    while (nextElement) {
        if (nextElement.tagName.toLowerCase() === find_tag) { //изменил для повтороного использовагия
            return nextElement;
        }
    }
    console.log("Next div after element not found")
    return null; // No div found
 };

function parseQuestionNumber(label){
    let get_text = label.textContent.match(/\d+/);
    if (!get_text) {
        return undefined;
    };
    let number = parseInt(get_text[0]);
    return number;
};

function findLastAnswer(element) {
    let nextElement = element.parentElement.nextElementSibling;
    let prevElement = null;

    while (nextElement) {
        if (nextElement.id.includes("answer")) {
            prevElement = nextElement;
        }

        nextElement = nextElement.nextElementSibling
    }
    return prevElement;


};

function addAnswer(element) {
    let parrent_div = element.parentElement;
    let copy_node = parrent_div.cloneNode(true);

    let number = copy_node.getElementsByTagName("span")[0];
    let key_field_answer = copy_node.getElementsByTagName("textarea")[0];
    let key_field_correct = copy_node.getElementsByTagName("input")[0];

    if (!number) {
        console.log('number element not found. ');
        return;
    };
    let numbretText = parseInt(number.textContent)
    number.textContent = numbretText + 1;
    copy_node.id = 'answerNumber' + `${number.textContent}`;
    key_field_answer.name = copy_node.id;
    key_field_correct.name = "correct_answer" + number.textContent;

    if (numbretText > 7) {
        console.log("It is maximum numbers of answers")
        return;
    };
    parrent_div.insertAdjacentElement("afterend", copy_node);
    element.remove();
};

function addQuestion(element) {
    let answer = findNextDiv(element);
    let parrent_div = element.parentElement;
    let new_button = element.cloneNode(true);
    let new_answer = answer.cloneNode(true);
    let last_answer = findLastAnswer(element);
    let question_button = document.getElementById("answerButton")
    let new_question_button = question_button.cloneNode(true);

    if (!answer) {
        return
    };

    let quest_label = parrent_div.getElementsByTagName("label")[0];
    let question_number = parseQuestionNumber(quest_label);

    if (!question_number) {
        quest_label.textContent = quest_label.textContent + " " + 1;
        parrent_div.id = 'question1';
        let copy_node = parrent_div.cloneNode(true);
        let copy_quest_label = copy_node.getElementsByTagName("label")[0];
        let key_field = copy_node.getElementsByTagName("textarea")[0];

        copy_quest_label.textContent = "Вопрос " + 2;
        copy_node.id = 'question2';
        key_field.name = 'question2';

        // copy_node.appendChild(new_button)
        last_answer.insertAdjacentElement('afterend', new_answer);
        // last_answer.insertAdjacentElement('afterend', new_button)
        last_answer.insertAdjacentElement('afterend', copy_node);

    } else {
        let copy_node = parrent_div.cloneNode(true);
        let copy_quest_label = copy_node.getElementsByTagName("label")[0];
        let copy_question_number = parseQuestionNumber(copy_quest_label);
        let key_field = copy_node.getElementsByTagName("textarea")[0];
        copy_question_number += 1;
        copy_quest_label.textContent = "Вопрос " + copy_question_number;
        copy_node.id = 'question' + copy_question_number;
        key_field.name = 'question' + copy_question_number;


        // copy_node.appendChild(new_question_button);
        last_answer.insertAdjacentElement('afterend', new_answer);
        // last_answer.insertAdjacentElement('afterend', new_button);
        last_answer.insertAdjacentElement('afterend', copy_node);

    };

    element.remove();
};

function createJsonForm(event) {
    event.preventDefault();

    const formData = {
        "questions" : {},
    };
    const quiz_name = document.getElementById("quiz_name");
    const quiz_threshold = document.getElementById("threshold");
    const quiz_department = document.getElementById("department");

    const questions = document.querySelectorAll('div[id^="quest"]');

    formData["quiz_name"] = quiz_name.value;
    formData["quiz_threshold"] = quiz_threshold.value;
    formData["quiz_department"] = quiz_department.value;


    questions.forEach(quest => {
        let answers = findAnswers(quest);
        let quest_text = quest.querySelector('textarea').value;

        formData.questions[quest.id] = {};
        formData.questions[quest.id].answers = answers;
        formData.questions[quest.id].text = quest_text;
    });

    sendFormData(formData);
    // return formData
};

