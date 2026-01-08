const addressInput = document.getElementById("start-address");
const feedback = document.getElementById("start-address-feedback");


function sendField(value) {
  fetch(validateAddressUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ address: value })
  })
  .then(res => res.json())
  .then(data => {
    feedback.textContent = data.message;
    feedback.style.color = data.valid ? "green" : "red";
  });
}

// When user presses Enter
addressInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault(); // prevent form submit
    sendField(addressInput.value);
  }
});

// When user leaves the field
addressInput.addEventListener("blur", () => {
  sendField(addressInput.value);
});