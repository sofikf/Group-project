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
                location.reload();
            } else {
                alert("❌ " + data.message);
            }
        } catch (err) {
            alert("Login error. Please try again.");
        }
    });
}

// Replace login button with Account dropdown if user is logged in
window.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/whoami", {
            credentials: "include"
        });
        const data = await res.json();

        const nav = document.querySelector(".navigation ul");

        if (data.logged_in) {
            const loginBtn = document.querySelector(".btnLogin-popup");
            if (loginBtn) loginBtn.parentElement.remove();

            const li = document.createElement("li");
            li.innerHTML = `
                <div class="dropdown" style="position: relative;">
                    <button class="dropbtn" style="background: none; border: none; color: white; cursor: pointer;">
                        ${data.username} ▾
                    </button>
                    <div class="dropdown-content" style="
                        display: none;
                        position: absolute;
                        right: 0;
                        background-color: white;
                        min-width: 140px;
                        box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
                        z-index: 1000;
                        border-radius: 4px;
                    ">
                        <a href="/account" style="display: block; padding: 10px; color: black; text-decoration: none;">Profile</a>
                        <a href="/dashboard" style="display: block; padding: 10px; color: black; text-decoration: none;">Dashboard</a>
                        <a href="#" id="logout-link" style="display: block; padding: 10px; color: black; text-decoration: none;">Logout</a>
                    </div>
                </div>
            `;
            nav.appendChild(li);

            // Hover toggle
            const dropdown = li.querySelector(".dropdown");
            const dropdownContent = li.querySelector(".dropdown-content");

            dropdown.addEventListener("mouseenter", () => {
                dropdownContent.style.display = "block";
            });

            dropdown.addEventListener("mouseleave", () => {
                dropdownContent.style.display = "none";
            });

            // Handle logout via JavaScript
            document.getElementById("logout-link").addEventListener("click", async (e) => {
                e.preventDefault();
                await fetch("/logout", {
                    method: "GET",
                    credentials: "include"
                });
                window.location.reload();
            });
        }
    } catch (err) {
        console.error("Login check failed:", err);
    }
});
