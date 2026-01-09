// const car_address_input       = document.getElementById("car-start-address");
// const car_address_feedback    = document.getElementById("car-start-address-feedback");
// const pt_address_input        = document.getElementById("pt-start-address");
// const pt_address_feedback     = document.getElementById("pt-start-address-feedback");
// const finish_address_input    = document.getElementById("finish-address");
// const finish_address_feedback = document.getElementById("finish-address-feedback");

import { map, addMarker, updateCrucialMarker } from '../map/state_handler.js';

const form_parts = {
  car_start_address: {
    input : document.getElementById("car-start-address"),
    feedback : document.getElementById("car-start-address-feedback")
  },
  pt_start_address: {
    input : document.getElementById("pt-start-address"),
    feedback : document.getElementById("pt-start-address-feedback")
  },
  finish_address: {
    input : document.getElementById("finish-address"),
    feedback : document.getElementById("finish-address-feedback")
  },
  submit : document.getElementById("address-input")
};

const form_state = {
  pt_start_address: {
    name : "",
    lat : null,
    lon : null,
    valid : false
  },
  car_start_address: {
    name : "",
    lat : null,
    lon : null,
    valid : false
  },
  finish_address: {
    name : "",
    lat : null,
    lon : null,
    valid : false
  },
};

export function updateInvalidAddress(coordinates){
   const invalidKey = Object.keys(form_state).find(
    (key) => form_state[key].valid === false && form_parts[key].input 
  );
  if (invalidKey) {
    form_parts[invalidKey].input.value = coordinates.lng + ", " + coordinates.lat;
    form_parts[invalidKey].feedback.textContent = "Coordinates set from map click.";
    form_parts[invalidKey].feedback.style.color = "orange";
    sendField(invalidKey);
  }
}

function sendField(key) {
  if(form_parts[key].input.value == form_state[key].name){
    // console.log("Skipped", key);
    return;
  }
  form_state[key].name = form_parts[key].input.value;
  form_state[key].valid = false;
  // console.log("Not skipped", key);
  fetch(window.APP_CONFIG.validateAddressUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ address: form_parts[key].input.value })
  })
  .then(res => res.json())
  .then(data => {
    form_parts[key].feedback.textContent = data.message;
    form_parts[key].feedback.style.color = data.valid ? "green" : "red";
    if (data.valid) {
      form_state[key].name = data.name;
      form_state[key].lat = data.lat;
      form_state[key].lon = data.lon;
      form_state[key].valid = true;
      form_parts[key].input.value = data.name;
      
      updateCrucialMarker(data.lat, data.lon, data.name, key === "car_start_address" ? "carLandmark" : key === "pt_start_address" ? "ptLandmark" : "finishLandmark");
      // addMarker(data.lat, data.lon, data.name);
      // console.log("map:", map);
      // L.marker([data.lon, data.lat]).addTo(map);
      // { lat: 51.120671168668615, lng: 17.041908119820274 }
    }
  });
}

function add_listeners(key){
  if(form_parts[key].input){
    form_parts[key].input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault(); // prevent form submit
        sendField(key);
      } 
    });
    form_parts[key].input.addEventListener("blur", () => {
      sendField(key);
    });
  }
}

add_listeners("car_start_address");
add_listeners("pt_start_address");
add_listeners("finish_address");


form_parts.submit.addEventListener("submit", (e) => {
  e.preventDefault(); // stop normal POST

  // Optional: final validation check
  // if (!formState.start_address.valid) {
  //   alert("Please fix errors before submitting.");
  //   return;
  // }

  fetch(window.APP_CONFIG.submitFormUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form_state)
  })
  .then(res => res.json())
  .then(data => {
    alert("Form submitted successfully!");
    console.log("Server response:", data);
  });
});

// // When user presses Enter
// addressInput.addEventListener("keydown", (e) => {
//   if (e.key === "Enter") {
//     e.preventDefault(); // prevent form submit
//     sendField(addressInput.value);
//   }
// });

// // When user leaves the field
// addressInput.addEventListener("blur", () => {
//   sendField(addressInput.value);
// });