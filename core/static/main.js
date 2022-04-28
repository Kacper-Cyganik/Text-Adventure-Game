const textElement = document.getElementById("text");
const optionButtonsElement = document.getElementById("option-btns");

const gameData = JSON.parse(document.getElementById("game_data").textContent);
var textNodes = JSON.parse(mydata)

let state = {};

function startGame() {
  state = {};
  showTextNode(1);
}

function showTextNode(textNodeIndex) {
    const textNode = textNodes.find(textNode => textNode.id === textNodeIndex)
    textElement.innerText = textNode.text
    while (optionButtonsElement.firstChild) {
      optionButtonsElement.removeChild(optionButtonsElement.firstChild)
    }
  
    textNode.options.forEach(option => {
      if (showOption(option)) {
        const button = document.createElement('button')
        button.innerText = option.text
        button.classList.add('btn')
        button.addEventListener('click', () => selectOption(option))
        optionButtonsElement.appendChild(button)
      }
    })
  }

function showOption(option) {
  return true;
}

function selectOption(option) {}

startGame();
