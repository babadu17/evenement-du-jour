let stars = document.querySelectorAll(".star");
let resultat = document.getElementById("resultat");
let note = 0;

stars.forEach(star => {
  star.addEventListener("click", () => {
    note = star.getAttribute("data-value");
    resultat.innerText = "Note : " + note + " étoile(s)";
    stars.forEach(s => s.classList.remove("active"));
    for (let i = 0; i < note; i++) {
      stars[i].classList.add("active");
    }
  });
});
