const toggleNav = () => {
  // console.log("clicked");
  document.getElementById("main-nav").classList.toggle("open-nav");
};

document.getElementById("close-icon").addEventListener("click", toggleNav);

document.getElementById("hamburg").addEventListener("click", toggleNav);
