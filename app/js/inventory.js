/*
=========================================
Inventory Management
=========================================
*/

// Default Products

const defaultProducts = [
    {
        id: 1,
        name: "Laptop",
        qty: 5,
        price: 85000
    },
    {
        id: 2,
        name: "Mouse",
        qty: 25,
        price: 500
    },
    {
        id: 3,
        name: "Keyboard",
        qty: 15,
        price: 1200
    }
];


// Initialize localStorage

if (!localStorage.getItem("products")) {

    localStorage.setItem(
        "products",
        JSON.stringify(defaultProducts)
    );

}

let products = JSON.parse(localStorage.getItem("products"));


// HTML Elements

const tableBody = document.getElementById("productTableBody");

const modal = document.getElementById("productModal");

const modalTitle = document.getElementById("modalTitle");

const addBtn = document.getElementById("addProductBtn");

const saveBtn = document.getElementById("saveProductBtn");

const cancelBtn = document.getElementById("cancelBtn");

const searchInput = document.getElementById("searchInput");


// =====================================
// Render Products
// =====================================

function renderProducts(productList = products) {

    tableBody.innerHTML = "";

    productList.forEach(product => {

        tableBody.innerHTML += `
        <tr>

            <td>${product.id}</td>

            <td>${product.name}</td>

            <td>${product.qty}</td>

            <td>${product.price}</td>

            <td>

                <button
                    class="btn btn-warning"
                    onclick="editProduct(${product.id})">

                    Edit

                </button>

                <button
                    class="btn btn-danger"
                    onclick="deleteProduct(${product.id})">

                    Delete

                </button>

            </td>

        </tr>
        `;

    });

}

renderProducts();


// =====================================
// Open Modal
// =====================================

addBtn.addEventListener("click", () => {

    modal.style.display = "block";

    modalTitle.innerText = "Add Product";

    document.getElementById("productId").value = "";

    document.getElementById("productName").value = "";

    document.getElementById("productQty").value = "";

    document.getElementById("productPrice").value = "";

});


// =====================================
// Cancel
// =====================================

cancelBtn.addEventListener("click", () => {

    modal.style.display = "none";

});


// =====================================
// Save Product
// =====================================

saveBtn.addEventListener("click", () => {

    const id = document.getElementById("productId").value;

    const name = document.getElementById("productName").value.trim();

    const qty = Number(document.getElementById("productQty").value);

    const price = Number(document.getElementById("productPrice").value);


    if (!name || qty <= 0 || price <= 0) {

        alert("Please enter valid values.");

        return;

    }


    if (id === "") {

        const newProduct = {

            id: products.length
                ? products[products.length - 1].id + 1
                : 1,

            name,
            qty,
            price

        };

        products.push(newProduct);

    }

    else {

        const index = products.findIndex(
            p => p.id == id
        );

        products[index].name = name;
        products[index].qty = qty;
        products[index].price = price;

    }


    localStorage.setItem(
        "products",
        JSON.stringify(products)
    );

    renderProducts();

    modal.style.display = "none";

});


// =====================================
// Edit Product
// =====================================

function editProduct(id) {

    const product = products.find(
        p => p.id == id
    );

    modal.style.display = "block";

    modalTitle.innerText = "Edit Product";

    document.getElementById("productId").value = product.id;

    document.getElementById("productName").value = product.name;

    document.getElementById("productQty").value = product.qty;

    document.getElementById("productPrice").value = product.price;

}


// =====================================
// Delete Product
// =====================================

function deleteProduct(id) {

    if (!confirm("Delete this product?")) {

        return;

    }

    products = products.filter(
        p => p.id != id
    );

    localStorage.setItem(
        "products",
        JSON.stringify(products)
    );

    renderProducts();

}


// =====================================
// Search
// =====================================

searchInput.addEventListener("keyup", () => {

    const keyword = searchInput.value.toLowerCase();

    const filtered = products.filter(product =>

        product.name
            .toLowerCase()
            .includes(keyword)

    );

    renderProducts(filtered);

});