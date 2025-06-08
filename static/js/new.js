const modal = document.getElementById('confirmModal');
const cancelBtn = document.getElementById('editConfirm');
const confirmBtn = document.getElementById('confirmSubmit');
const form = document.getElementById('booking_form');
const phoneInput = document.querySelector(".phone_input");


phoneInput.addEventListener("focus", function () {
    if (!phoneInput.value.startsWith("+998")) {
        phoneInput.value = "+998 ";
    }
});

phoneInput.addEventListener("input", function () {
    let input = phoneInput.value.replace(/\D/g, "");
    if (input.startsWith("998")) {
        input = input.substring(3);
    }

    let formattedNumber = "+998 ";
    if (input.length > 0) {
        formattedNumber += input.substring(0, 2);
    }
    if (input.length > 2) {
        formattedNumber += " " + input.substring(2, 5);
    }
    if (input.length > 5) {
        formattedNumber += " " + input.substring(5, 7);
    }
    if (input.length > 7) {
        formattedNumber += "-" + input.substring(7, 9);
    }

    phoneInput.value = formattedNumber;
});

phoneInput.addEventListener("keydown", function (event) {
    const position = phoneInput.selectionStart;
    if (position < 5 && event.key !== "Backspace") {
        event.preventDefault();
    }
});

phoneInput.addEventListener("blur", function () {
    if (phoneInput.value === "+998 ") {
        phoneInput.value = "";
    }
});

let allowSubmit = false;

form.addEventListener('submit', function (event) {
    if (!allowSubmit) {
        event.preventDefault();
        if (form.checkValidity()) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        } else {
            form.reportValidity();
        }
    }
});

cancelBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
});

confirmBtn.addEventListener('click', () => {
    allowSubmit = true;
    form.submit();
});


