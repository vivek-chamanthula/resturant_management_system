/* ----menu page start ---*/
const allSections = [
  "appetizers",
  "soups",
  "noodles",
  "maincourse",
  "starters",
  "biryanis",
  "curries",
  "tandoori",
  "pasta",
  "pizza",
  "grilled",
  "salads",
];
const chineseSelect = document.getElementById("categorySelect");
const indianSelect = document.getElementById("indianSelect");
const contiSelect = document.getElementById("continental_dropdown");
function hideAll() {
  allSections.forEach((id) => {
    document.getElementById(id).style.display = "none";
  });
}
function showSection(id) {
  document.getElementById(id).style.display = "grid";
}
chineseSelect.addEventListener("change", function () {
  hideAll();
  showSection(this.value);
});
indianSelect.addEventListener("change", function () {
  hideAll();
  showSection(this.value);
});
contiSelect.addEventListener("change", function () {
  hideAll();
  showSection(this.value);
});
hideAll();

function addToCart(itemId) {
  fetch(`/add-to-cart/${itemId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Item added to cart");
      }
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/* ----menu page end ---*/

/* ----cart page start ---*/
function updateQty(itemId, action) {
  fetch(`/update-qty/${itemId}/${action}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        location.reload();
      }
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
/* ----cart page end ---*/

/* ----order page start ---*/
function confirmOrder() {
  let customer = document.getElementById("customer").value.trim();
  let phone = document.getElementById("phone").value.trim();
  let table = document.getElementById("table").value.trim();

  if (!customer || !phone || !table) {
    alert("Please fill all details");
    return;
  }

  let rows = document.querySelectorAll(".order_row");
  let billItems = document.getElementById("billItems");
  let total = 0;
  let items = [];

  billItems.innerHTML = "";

  rows.forEach((row) => {
    let name = row.dataset.name;
    let price = Number(row.dataset.price);
    billItems.innerHTML += `<p>${name} - ₹${price}</p>`;
    items.push(name);
    total += price;
  });

  let now = new Date();
  let date = now.toLocaleDateString();
  let time = now.toLocaleTimeString();

  billItems.innerHTML += `
        <hr>
        <p><b>Date:</b> ${date}</p>
        <p><b>Time:</b> ${time}</p>
    `;

  document.getElementById("billTotal").innerText = "Total Amount: ₹" + total;

  document.getElementById("f_customer").value = customer;
  document.getElementById("f_phone").value = phone;
  document.getElementById("f_table").value = table;
  document.getElementById("f_date").value = date;
  document.getElementById("f_time").value = time;
  document.getElementById("f_items").value = items.join(", ");
  document.getElementById("f_total").value = total;

  document.getElementById("orderList").innerHTML = "<p>No Orders</p>";
  document.getElementById("generateBtn").style.display = "block";
}
/* ----order page end ---*/
