const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let filter = searchInput.value.toLowerCase();
        let cards = document.querySelectorAll(".card");

        cards.forEach(function(card){

            let productName = card.querySelector("h3").textContent.toLowerCase();

            if(productName.includes(filter)){
                card.style.display = "";
            }
            else{
                card.style.display = "none";
            }

        });

    });

}

function filterProducts(category){

    let cards = document.querySelectorAll(".card");

    cards.forEach(function(card){

        if(category === "all"){
            card.style.display = "";
        }
        else{

            if(card.dataset.category === category){
                card.style.display = "";
            }
            else{
                card.style.display = "none";
            }

        }

    });

}

document.querySelectorAll(".wish-btn").forEach(function(button){

    button.addEventListener("click", function(){

        let product = {

            name: this.dataset.name,
            price: Number(this.dataset.price),
            image: this.dataset.image

        };

        let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];

        wishlist.push(product);

        localStorage.setItem("wishlist", JSON.stringify(wishlist));

        alert(product.name + " added to wishlist ❤️");

    });

});

document.querySelectorAll(".cart-btn").forEach(function(button){

    button.addEventListener("click", function(){

        let product = {

            name: this.dataset.name,
            price: Number(this.dataset.price),
            image: this.dataset.image,
            quantity: 1

        };

        let cart = JSON.parse(localStorage.getItem("cart")) || [];

        let existing = cart.find(item => item.name === product.name);

        if(existing){

            existing.quantity++;

        }
        else{

            cart.push({

                name: product.name,
                price: Number(product.price),
                image: product.image,
                quantity: 1

            });

        }

        localStorage.setItem("cart", JSON.stringify(cart));

        alert(product.name + " added to cart 🛒");

    });

});

const cakeForm = document.getElementById("cakeForm");

if(cakeForm){

    cakeForm.addEventListener("submit", function(e){

        e.preventDefault();

        let msg = document.getElementById("successMessage");

        if(msg){
            msg.style.display = "block";
        }

        cakeForm.reset();

    });

}

function toggleText(){

    let text = document.getElementById("moreText");

    if(text){
        text.classList.toggle("hidden");
    }

}