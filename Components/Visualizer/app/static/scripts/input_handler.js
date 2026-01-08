// const car_address_input       = document.getElementById("car-start-address");
// const car_address_feedback    = document.getElementById("car-start-address-feedback");
// const pt_address_input        = document.getElementById("pt-start-address");
// const pt_address_feedback     = document.getElementById("pt-start-address-feedback");
// const finish_address_input    = document.getElementById("finish-address");
// const finish_address_feedback = document.getElementById("finish-address-feedback");

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
  car_start_address: {
    name : "",
    lat : null,
    lon : null
  },
  pt_start_address: {
    name : "",
    lat : null,
    lon : null
  },
  finish_address: {
    name : "",
    lat : null,
    lon : null
  },
};


function sendField(key) {
  if(form_parts[key].input.value == form_state[key].name){
    console.log("Skipped", key);
    return;
  }
  console.log("Not skipped", key);
  fetch(validateAddressUrl, {
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
      form_parts[key].input.value = data.name;
      console.log("map:", map);
      L.marker([data.lon, data.lat]).addTo(map);
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

  fetch(submitFormUrl, {
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