/*
==========================================
Dashboard JavaScript
==========================================
*/

document.addEventListener("DOMContentLoaded", () => {

    updateProductCount();

    setupNavigation();

    displayLoggedInUser();

});


/*
==========================================
Display Logged-in User
==========================================
*/

function displayLoggedInUser() {

    const username = localStorage.getItem("username") || "Admin";

    const welcome = document.getElementById("welcomeMessage");

    if (welcome) {

        welcome.innerText = `Welcome, ${capitalize(username)}`;

    }

}


/*
==========================================
Update Product Count
==========================================
*/

function updateProductCount() {

    const countElement = document.getElementById("productCount");

    if (!countElement) return;

    const products = JSON.parse(localStorage.getItem("products")) || [];

    countElement.innerText = products.length;

}


/*
==========================================
Navigation
==========================================
*/

function setupNavigation() {

    const inventoryBtn = document.getElementById("inventoryBtn");

    if (inventoryBtn) {

        inventoryBtn.addEventListener("click", () => {

            window.location.href = "inventory.html";

        });

    }

}


/*
==========================================
Helper Function
==========================================
*/

function capitalize(text) {

    if (!text) return "";

    return text.charAt(0).toUpperCase() + text.slice(1);

}