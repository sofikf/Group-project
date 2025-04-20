// Modal toggling
const btnPopup = document.querySelector('.btnLogin-popup');
const cover_box = document.querySelector('.cover_box');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const iconClose = document.querySelector('.icon-close');

function activateCoverBox(){
    cover_box.classList.add('active');
}

function deactivateCoverBox(){
    cover_box.classList.remove('active');
}

function activatePopup(){
    cover_box.classList.add('active-popup');
}

function deactivatePopup(){
    cover_box.classList.remove('active-popup');
}

registerLink.addEventListener('click', activateCoverBox);
loginLink.addEventListener('click', deactivateCoverBox);
btnPopup.addEventListener('click', activatePopup);
iconClose.addEventListener('click', deactivatePopup);

// Handle registration
const registerForm = document.getElementById("register-form");

if (registerForm) {
    registerForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(registerForm);

        try {
            const res = await fetch("/register", {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            if (data.success) {
                alert("✅ Registered! You can now log in.");
                deactivateCoverBox(); // switch back to login
            } else {
                alert("❌ " + data.message);
            }
        } catch (err) {
            alert("Something went wrong. Try again.");
        }
    });
}

// Handle login
const loginForm = document.getElementById("login-form");

if (loginForm) {
    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(loginForm);

        try {
            const res = await fetch("/login", {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            if (data.success) {
                alert("✅ Login successful!");
                deactivatePopup();
                location.reload(); // or redirect as needed
            } else {
                alert("❌ " + data.message);
            }
        } catch (err) {
            alert("Login error. Please try again.");
        }
    });
}

window.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/whoami");
        const data = await res.json();

        const nav = document.querySelector(".navigation ul");

        if (data.logged_in) {
            // Remove login button
            const loginBtn = document.querySelector(".btnLogin-popup");
            if (loginBtn) {
                loginBtn.parentElement.remove();
            }

            // Add Account link
            const li = document.createElement("li");
            li.innerHTML = `<a href="/account">Account</a>`;
            nav.appendChild(li);
        }
    } catch (err) {
        console.error("Could not check login status:", err);
    }
});
