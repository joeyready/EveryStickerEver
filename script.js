const samples = [
  {a:"CALIFORNIA",b:"TEXAS",sku:"D-CA-M-TX"},
  {a:"NEW YORK",b:"OREGON",sku:"D-NY-M-OR"},
  {a:"FLORIDA",b:"COLORADO",sku:"D-FL-M-CO"},
  {a:"ALASKA",b:"HAWAII",sku:"D-AK-M-HI"},
  {a:"ILLINOIS",b:"MONTANA",sku:"D-IL-M-MT"},
  {a:"NEW JERSEY",b:"ARIZONA",sku:"D-NJ-M-AZ"}
];
let activeColor = "red";
const grid = document.querySelector("#sticker-grid");
const render = () => {
  grid.innerHTML = samples.map((item,index) => `
    <article class="sticker-card">
      <div class="sticker sticker-${activeColor}">
        <span class="sticker-small">A FRIENDLY REMINDER</span>
        <strong>DON’T<br>${item.a}<br>MY ${item.b}</strong>
        <span class="sticker-bottom">✳ &nbsp; KEEP IT BETWEEN THE LINES &nbsp; ✳</span>
      </div>
      <div class="card-meta"><span class="card-name">${item.a} / ${item.b}</span><span class="card-sku">${item.sku}</span></div>
    </article>`).join("");
};
document.querySelectorAll(".swatch").forEach(button => {
  button.addEventListener("click", () => {
    activeColor = button.dataset.color;
    document.querySelectorAll(".swatch").forEach(swatch => {
      const selected = swatch === button;
      swatch.classList.toggle("active", selected);
      swatch.setAttribute("aria-pressed", String(selected));
    });
    render();
  });
});
const menuButton = document.querySelector(".menu-toggle");
const nav = document.querySelector(".site-header nav");
menuButton.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
});
nav.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
  nav.classList.remove("open");
  menuButton.setAttribute("aria-expanded","false");
}));
render();