window.addEventListener("scroll", function () {
    const nav = document.querySelector("nav");

    if (window.scrollY > 50) {
        nav.style.boxShadow = "0 6px 20px rgba(0,0,0,0.12)";
    } else {
        nav.style.boxShadow = "0 2px 10px rgba(0,0,0,0.05)";
    }
});

const navLinks = document.querySelectorAll(".nav-links a");

navLinks.forEach(link => {
    link.addEventListener("click", function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
            .scrollIntoView({
                behavior: "smooth"
            });
    });
});

const form = document.querySelector("form");
const successMessage = document.getElementById("success-message");

form.addEventListener("submit", function (e) {

    e.preventDefault();

    successMessage.style.display = "block";

    form.reset();

    setTimeout(() => {
        successMessage.style.display = "none";
    }, 3000);

});

const cards = document.querySelectorAll(".project-card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-10px)";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0)";
    });

});