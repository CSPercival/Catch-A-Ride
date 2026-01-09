import { map, addMarker, updateCrucialMarker } from '../map/state_handler.js';

const formParts = {
  carStartAddress: {
    input : document.getElementById("car-start-address"),
    feedback : document.getElementById("car-start-address-feedback")
  },
  ptStartAddress: {
    input : document.getElementById("pt-start-address"),
    feedback : document.getElementById("pt-start-address-feedback")
  },
  finishAddress: {
    input : document.getElementById("finish-address"),
    feedback : document.getElementById("finish-address-feedback")
  },
  submit : document.getElementById("address-input")
};

const formState = {
  ptStartAddress: {
    name : "",
    lat : null,
    lng : null,
    valid : false
  },
  carStartAddress: {
    name : "",
    lat : null,
    lng : null,
    valid : false
  },
  finishAddress: {
    name : "",
    lat : null,
    lng : null,
    valid : false
  },
};

export function updateInvalidAddress(coordinates){
   const invalidKey = Object.keys(formState).find(
    (key) => formState[key].valid === false && formParts[key].input 
  );
  if (invalidKey) {
    formParts[invalidKey].input.value = coordinates.lat + ", " + coordinates.lng;
    formParts[invalidKey].feedback.textContent = "Coordinates set from map click.";
    formParts[invalidKey].feedback.style.color = "orange";
    sendField(invalidKey);
  }
}

function sendField(key) {
  if(formParts[key].input.value == formState[key].name){
    return;
  }
  formState[key].name = formParts[key].input.value;
  formState[key].valid = false;
  fetch(window.APP_CONFIG.validateAddressUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ address: formParts[key].input.value })
  })
  .then(res => res.json())
  .then(data => {
    formParts[key].feedback.textContent = data.message;
    formParts[key].feedback.style.color = data.valid ? "green" : "red";
    if (data.valid) {
      formState[key].name = data.name;
      formState[key].lat = data.lat;
      formState[key].lng = data.lng;
      formState[key].valid = true;
      formParts[key].input.value = data.name;
      
      updateCrucialMarker(data.lat, data.lng, data.name, key === "carStartAddress" ? "carLandmark" : key === "ptStartAddress" ? "ptLandmark" : "finishLandmark");
    }
  });
}

function addListeners(key){
  if(formParts[key].input){
    formParts[key].input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        sendField(key);
      } 
    });
    formParts[key].input.addEventListener("blur", () => {
      sendField(key);
    });
  }
}

addListeners("carStartAddress");
addListeners("ptStartAddress");
addListeners("finishAddress");


formParts.submit.addEventListener("submit", (e) => {
  e.preventDefault();
  fetch(window.APP_CONFIG.submitFormUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formState)
  })
  .then(res => res.json())
  .then(data => {
    alert("Form submitted successfully!");
    console.log("Server response:", data);
  });
});