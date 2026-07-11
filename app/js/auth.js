/*
==========================================
Inventory Management Authentication
==========================================
*/

const VALID_USERNAME = "admin";
const VALID_PASSWORD = "admin123";

/*
==========================================
Login
==========================================
*/

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        const error = document.getElementById("errorMessage");

        if (username === VALID_USERNAME && password === VALID_PASSWORD) {

            localStorage.setItem("loggedIn", "true");
            localStorage.setItem("username", username);

            window.location.href = "dashboard.html";

        } else {

            error.textContent = "Invalid username or password.";

        }

    });

}

/*
==========================================
Logout
==========================================
*/

const logoutBtn = document.getElementById("logoutBtn");

if (logoutBtn) {

    logoutBtn.addEventListener("click", function (event) {

        event.preventDefault();

        localStorage.removeItem("loggedIn");
        localStorage.removeItem("username");

        window.location.href = "login.html";

    });

}

/*
==========================================
Protect Dashboard / Inventory
==========================================
*/

const protectedPages = [
    "dashboard.html",
    "inventory.html"
];

const currentPage = window.location.pathname.split("/").pop();

if (protectedPages.includes(currentPage)) {

    if (localStorage.getItem("loggedIn") !== "true") {

        window.location.href = "login.html";

    }

}

/*
==========================================
Already Logged In
==========================================
*/

if (
    currentPage === "login.html" &&
    localStorage.getItem("loggedIn") === "true"
) {

    window.location.href = "dashboard.html";

}