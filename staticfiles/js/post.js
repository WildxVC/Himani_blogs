var index = 0;
var slides = document.getElementsByClassName("slides");
var dot = document.getElementsByClassName("dot");

function changeSlide() {

    if (index < 0) {
        index = slides.length - 1;
    }

    if (index > slides.length - 1) {
        index = 0;
    }

    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        dot[i].classList.remove("active");
    }

    slides[index].style.display = "block";
    dot[index].classList.add("active");

    index++;

    setTimeout(changeSlide, 3000);

}

changeSlide();