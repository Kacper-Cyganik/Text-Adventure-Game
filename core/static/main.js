const textElement = document.getElementById("text");
const optionButtonsElement = document.getElementById("option-btns");

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

async function getGameData() {
  try {
    let res = await fetch("/game/get-current-game-state", {
      method: "GET",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
    });
    return await res.json();
  } catch (error) {
    console.log(error);
  }
}

async function updateSaveSlot(slot_id) {
  try {
    let res = await fetch("/game/update-save-slot", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ save_slot_id: slot_id }),
    });
    return await res.json();
  } catch (error) {
    console.log(error);
  }
}

async function getSaveSlots() {
  try {
    let res = await fetch("/game/get-save-slots", {
      method: "GET",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
    });
    return await res.json();
  } catch (error) {
    console.log(error);
  }
}

async function updateGameData(state, nextTextNodeId) {
  try {
    let res = await fetch("/game/update-game-state", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ next_node: nextTextNodeId, player_state: state }), //JavaScript object of data to POST
    });
    return await res.json();
  } catch (error) {
    console.log(error);
  }
  showTextNode();
}

async function showTextNode() {
  console.log("Trigger showTextNode");
  const gameData = await getGameData();
  // paragraph
  const currentParagraph = JSON.parse(gameData.paragraph);
  // character state
  var state = JSON.parse(gameData.character_state);

  textElement.innerText = currentParagraph.text;
  while (optionButtonsElement.firstChild) {
    optionButtonsElement.removeChild(optionButtonsElement.firstChild);
  }

  currentParagraph.options.forEach((option) => {
    if (showOption(state, option)) {
      const button = document.createElement("button");
      button.innerText = option.text;
      button.classList.add("btn");
      button.addEventListener("click", () => selectOption(state, option));
      optionButtonsElement.appendChild(button);
    }
  });
}

function showOption(state, option) {
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

async function showSaveSlotOptions() {
  const saveSlotData = await getSaveSlots();
  const saveSlots = JSON.parse(saveSlotData.saveSlotData);


  //
  textElement.innerText = "Choose save slot";
  while (optionButtonsElement.firstChild) {
    optionButtonsElement.removeChild(optionButtonsElement.firstChild);
  }
  saveSlots.forEach((text) => {
    const button = document.createElement("button");
    button.innerText = `Save: ${text.saveSlotId} \nLast played: ${text.lastModified}`;
    button.classList.add("btn-save-slot");
    button.addEventListener("click", () => updateSaveSlot(text.saveSlotId).then(showTextNode));
    optionButtonsElement.appendChild(button);
  });
}
async function selectOption(state, option) {
  const nextTextNodeId = option.nextText;

  if (nextTextNodeId <= 0) {
    console.log("lesser than 0" + nextTextNodeId);
    // End of the game
    await updateGameData({}, 1);
  } else {
    state = Object.assign(state, option.setState);
    await updateGameData(state, nextTextNodeId);
  }
  showTextNode();
}

// -------------------

showSaveSlotOptions();
