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

function previewImage(input) {
    const file = input.files[0];
    const preview = document.getElementById("preview");
    const uploadText = document.getElementById("uploadText");
    const cancelButton = document.getElementById("cancelButton");

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
            uploadText.style.display = "none";
            cancelButton.style.display = "inline-block";
        };
        reader.readAsDataURL(file);
    }
}

function cancelImage() {
    const imageInput = document.getElementById("imageInput");
    const preview = document.getElementById("preview");
    const uploadText = document.getElementById("uploadText");
    const cancelButton = document.getElementById("cancelButton");

    imageInput.value = "";
    preview.src = "";
    preview.style.display = "none";
    uploadText.style.display = "block";
    cancelButton.style.display = "none";
}

const checkbox = document.querySelector("input[name=is_staff_code_used]");
const codeDiv = document.getElementById("staff-code-input");
checkbox.addEventListener("change", function () {
    codeDiv.style.display = this.checked ? "block" : "none";
});

function togglePassword1() {
    const passwordInput = document.getElementById("parol1");
    const icon = document.querySelector(".toggle-password1");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.innerHTML = `<i class="fa-solid fa-eye-slash"></i>`;
    } else {
        passwordInput.type = "password";
        icon.innerHTML = `<i class="fa-solid fa-eye"></i>`;
    }
}
function togglePassword2() {
    const passwordInput = document.getElementById("parol2");
    const icon = document.querySelector(".toggle-password2");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.innerHTML = `<i class="fa-solid fa-eye-slash"></i>`;
    } else {
        passwordInput.type = "password";
        icon.innerHTML = `<i class="fa-solid fa-eye"></i>`;
    }
}
function togglePassword3() {
    const passwordInput = document.getElementById("parol_input");
    const icon = document.querySelector(".toggle-password3");

    if (passwordInput.type === "password") {
        icon.innerHTML = `<i class="fa-solid fa-eye-slash"></i>`;
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
        icon.innerHTML = `<i class="fa-solid fa-eye"></i>`;
    }
}