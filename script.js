
const grid = document.querySelector("#sticker-grid");

const stateNames = {
  AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas",
  CA: "California", CO: "Colorado", CT: "Connecticut", DE: "Delaware",
  FL: "Florida", GA: "Georgia", HI: "Hawaii", ID: "Idaho",
  IL: "Illinois", IN: "Indiana", IA: "Iowa", KS: "Kansas",
  KY: "Kentucky", LA: "Louisiana", ME: "Maine", MD: "Maryland",
  MA: "Massachusetts", MI: "Michigan", MN: "Minnesota",
  MS: "Mississippi", MO: "Missouri", MT: "Montana", NE: "Nebraska",
  NV: "Nevada", NH: "New Hampshire", NJ: "New Jersey",
  NM: "New Mexico", NY: "New York", NC: "North Carolina",
  ND: "North Dakota", OH: "Ohio", OK: "Oklahoma", OR: "Oregon",
  PA: "Pennsylvania", RI: "Rhode Island", SC: "South Carolina",
  SD: "South Dakota", TN: "Tennessee", TX: "Texas", UT: "Utah",
  VT: "Vermont", VA: "Virginia", WA: "Washington",
  WV: "West Virginia", WI: "Wisconsin", WY: "Wyoming"
};

const colors = [
  { code: "RED", label: "Red" },
  { code: "BLU", label: "Blue" },
  { code: "BLK", label: "Black" }
];

let samples = [];

function getStateNames(sku) {
  const parts = sku.split("-");
  return {
    a: stateNames[parts[1]] || parts[1],
    b: stateNames[parts[3]] || parts[3]
  };
}

// Animated hero sticker pile
let heroPileTimer = null;

function addHeroSticker() {
  const pile = document.querySelector("#hero-pile");

  if (!pile || !samples.length) return;

  const existingSkus = new Set(
    [...pile.querySelectorAll("img")].map(img => img.dataset.sku)
  );

  const available = samples.filter(
    item => !existingSkus.has(item.sku)
  );

  const item = available.length
    ? available[Math.floor(Math.random() * available.length)]
    : samples[Math.floor(Math.random() * samples.length)];

  const color = colors[Math.floor(Math.random() * colors.length)];

  const positions = [
    { left: 8, top: 28, angle: -8 },
    { left: 15, top: 36, angle: 5 },
    { left: 5, top: 40, angle: -3 },
    { left: 18, top: 23, angle: 9 },
    { left: 10, top: 34, angle: 3 },
    { left: 14, top: 43, angle: -6 },
    { left: 6, top: 22, angle: 7 }
  ];

  // Keep the pile from getting too crowded
  if (pile.children.length >= 7) {
    pile.firstElementChild.remove();
  }

  const position = positions[
  Math.floor(Math.random() * positions.length)
];

  const img = document.createElement("img");

  img.src = `/images/portfolio/${item.sku}-${color.code}.jpg`;
  img.alt = `${color.label} sticker`;
  img.dataset.sku = item.sku;
  img.draggable = false;

  img.style.left = `${position.left}%`;
  img.style.top = `${position.top}%`;
  img.style.setProperty("--angle", `${position.angle}deg`);
  img.style.zIndex = pile.children.length + 1;

  pile.appendChild(img);
}

function startHeroPile() {
  if (heroPileTimer) return;

  // Start with a few stickers already in the pile
  for (let i = 0; i < 4; i++) {
    setTimeout(addHeroSticker, i * 350);
  }

  // Add a new sticker every 2.4 seconds
  heroPileTimer = setInterval(addHeroSticker, 2400);
}

function render() {
  grid.innerHTML = samples.map(item => {
    const { a, b } = getStateNames(item.sku);

    const initialColor = colors[
      Math.floor(Math.random() * colors.length)
    ];

    return `
      <article class="sticker-card">
        <a
          href="/images/portfolio/${item.sku}-${initialColor.code}.jpg"
          target="_blank"
          rel="noopener"
          class="sticker-image-link"
          data-sku="${item.sku}"
          data-color="${initialColor.code}"
          aria-label="View ${initialColor.label} ${a} and ${b} sticker"
        >
          <img
            src="/images/thumbnails/${item.sku}-${initialColor.code}.jpg"
            alt="${initialColor.label} Don't ${a} My ${b} sticker"
            loading="lazy"
          >
        </a>
        <div class="card-meta">
          <span class="card-name">${a} / ${b}</span>
          <span class="card-sku">${item.sku}</span>
        </div>
      </article>
    `;
  }).join("");

  document.querySelector(".collection-bottom .mono").textContent =
    `SHOWING ${String(samples.length).padStart(2, "0")} OF 2,500 DESIGNS`;

  // Random color on hover
  document.querySelectorAll(".sticker-image-link").forEach(link => {
    const img = link.querySelector("img");
    const sku = link.dataset.sku;
    const originalColor = link.dataset.color;

    link.addEventListener("mouseenter", () => {
      const alternatives = colors.filter(
        color => color.code !== originalColor
      );

      const nextColor = alternatives[
        Math.floor(Math.random() * alternatives.length)
      ];

      img.src = `/images/thumbnails/${sku}-${nextColor.code}.jpg`;
      link.href = `/images/portfolio/${sku}-${nextColor.code}.jpg`;
    });

    link.addEventListener("mouseleave", () => {
      img.src = `/images/thumbnails/${sku}-${originalColor}.jpg`;
      link.href = `/images/portfolio/${sku}-${originalColor}.jpg`;
    });
  });
}

async function loadCatalog() {
  try {
    const response = await fetch("/catalog.json");

    if (!response.ok) {
      throw new Error(`Catalog request failed: ${response.status}`);
    }

    samples = await response.json();
    render();
    startHeroPile();
  } catch (error) {
    console.error("Could not load sticker catalog:", error);
    grid.innerHTML = "<p>Unable to load the sticker collection.</p>";
  }
}

// Mobile navigation
const menuButton = document.querySelector(".menu-toggle");
const nav = document.querySelector(".site-header nav");

menuButton.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute(
    "aria-label",
    open ? "Close navigation" : "Open navigation"
  );
});

nav.querySelectorAll("a").forEach(link => {
  link.addEventListener("click", () => {
    nav.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open navigation");
  });
});

loadCatalog();
