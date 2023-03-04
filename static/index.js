document.onreadystatechange = function () {
  if (document.readyState !== "complete") {
    document.querySelector("body").style.visibility = "hidden";
    document.querySelector("#loader").style.visibility = "visible";
  } else {
    document.querySelector("#loader").style.display = "none";
    document.querySelector("body").style.visibility = "visible";
  }
};

wh = window.innerHeight;
one = document.getElementById("one");
two = document.getElementById("two");
three = document.getElementById("three");
four = document.getElementById("four");
five = document.getElementById("five");
wh1 = wh / 2;
wh2 = wh + wh / 2;
wh3 = 2 * wh + wh / 2;
wh4 = 3 * wh + wh / 2;
window.onscroll = function () {
  if (window.scrollY < wh1) {
    one.classList.add("active");
    two.classList.remove("active");
    three.classList.remove("active");
    four.classList.remove("active");
    five.classList.remove("active");
    mybutton.style.display = "none";
    creator.style.bottom = "15px";
  } else if (window.scrollY > wh1 && window.scrollY < wh2) {
    two.classList.add("active");
    one.classList.remove("active");
    three.classList.remove("active");
    four.classList.remove("active");
    five.classList.remove("active");
    mybutton.style.display = "block";
    creator.style.bottom = "100px";
  } else if (window.scrollY > wh2 && window.scrollY < wh3) {
    three.classList.add("active");
    one.classList.remove("active");
    two.classList.remove("active");
    four.classList.remove("active");
    five.classList.remove("active");
    mybutton.style.display = "block";
    creator.style.bottom = "100px";
  } else if (window.scrollY > wh3) {
    four.classList.add("active");
    one.classList.remove("active");
    two.classList.remove("active");
    three.classList.remove("active");
    five.classList.remove("active");
    mybutton.style.display = "block";
    creator.style.bottom = "100px";
  } else if (window.scrollY > wh4) {
    five.classList.add("active");
    one.classList.remove("active");
    two.classList.remove("active");
    three.classList.remove("active");
    four.classList.remove("active");
    mybutton.style.display = "block";
    creator.style.bottom = "100px";
  }
};