function parseQuestionNumber(label){
    let get_text = label.textContent.match(/\d+/);
    if (!get_text) {
        return undefined;
    };
    let number = parseInt(get_text[0]);
    return number;
};

function findNextDiv(element) {
    let nextElement = element.nextElementSibling;
    while (nextElement) {
        if (nextElement.tagName.toLowerCase() === 'div') {
            return nextElement;
        }
        nextElement = nextElement.nextElementSibling;
    }
    console.log("Next div after element not found")
    return null; // No div found
};

function addAnswer(element) {
    let parrent_div = element.parentElement;
    let copy_node = parrent_div.cloneNode(true);

    let number = copy_node.getElementsByTagName("span")[0];
    if (!number) {
        console.log('number element not found. ');
        return;
    };
    let numbretText = parseInt(number.textContent)
    number.textContent = numbretText + 1;
    copy_node.id = 'answerNumber' + `${number.textContent}`;

    if (numbretText > 7) {
        console.log("It is maximum numbers of answers")
        return;
    };
    parrent_div.insertAdjacentElement("afterend", copy_node);
    element.remove();
};

function addQuestion(element) {
    let answer = findNextDiv(element);
    let parrent_div = element.previousElementSibling;
    let new_button = element.cloneNode(true);
    let new_answer = answer.cloneNode(true);

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

        copy_quest_label.textContent = "Вопрос " + 2;
        copy_node.id = 'question2';

        answer.insertAdjacentElement('afterend', new_answer);
        answer.insertAdjacentElement('afterend', new_button)
        answer.insertAdjacentElement('afterend', copy_node);

    } else {
        let copy_node = parrent_div.cloneNode(true);
        let copy_quest_label = copy_node.getElementsByTagName("label")[0];
        let copy_question_number = parseQuestionNumber(copy_quest_label);
        copy_question_number += 1;
        copy_quest_label.textContent = "Вопрос " + copy_question_number;
        copy_node.id = 'question' + copy_question_number;

        answer.insertAdjacentElement('afterend', new_answer);
        answer.insertAdjacentElement('afterend', new_button);
        answer.insertAdjacentElement('afterend', copy_node);
    };

    element.remove();
};