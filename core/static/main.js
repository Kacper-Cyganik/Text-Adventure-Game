const textElement = document.getElementById("text");
const optionButtonsElement = document.getElementById("option-btns");

const gameData = JSON.parse(document.getElementById("game_data").textContent);
var textNodes = JSON.parse(gameData)

let state = {};

function startGame() {
  state = {};
  showTextNode(1);
}

function showTextNode(textNodeIndex) {
  const textNode = textNodes.find((textNode) => textNode.id === textNodeIndex);
  textElement.innerText = textNode.text;
  while (optionButtonsElement.firstChild) {
    optionButtonsElement.removeChild(optionButtonsElement.firstChild);
  }

  textNode.options.forEach((option) => {
    if (showOption(option)) {
      const button = document.createElement("button");
      button.innerText = option.text;
      button.classList.add("btn");
      button.addEventListener("click", () => selectOption(option));
      optionButtonsElement.appendChild(button);
    }
  });
}

function showOption(option) {
  if (option.requiredState == null) {
    return true;
  }
  for (var propt in option.requiredState) {
    if (state.hasOwnProperty(propt) === false) {
      return false;
    } else if (state[propt] !== option.requiredState[propt]) {
      return false;
    }
  }
  return true;
}

function selectOption(option) {
  const nextTextNodeId = option.nextText;
  if (nextTextNodeId <= 0) {
    return startGame();
  }
  state = Object.assign(state, option.setState);
  showTextNode(nextTextNodeId);
}

startGame();
