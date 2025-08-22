// List of actress names (from folder names)
const actressNames = [
  "Aya Asahina",   "Bindass Kavya",   "Choa"
];

// Utility to create safe file names with underscores
function toFileName(name) {
  return name.replace(/ /g, "_") + ".html";
}

function getFirstName(name) {
  return name.split(" ")[0].toLowerCase();
}

// Search Bar
const grid = document.getElementById('actressGrid');
if (grid) {
  // Add search bar
  const searchBar = document.createElement('input');
  searchBar.type = 'text';
  searchBar.placeholder = 'Search actresses...';
  searchBar.style = 'width: 100%; max-width: 400px; margin: 2rem auto 1rem auto; display: block; padding: 0.7rem 1rem; border-radius: 24px; border: none; font-size: 1.1rem; background: #23233a; color: #ffd700; box-shadow: 0 2px 8px #0006; outline: none;';
  grid.parentNode.insertBefore(searchBar, grid);

  function renderGrid(filter = "") {
    const filtered = actressNames.filter(name => name.toLowerCase().includes(filter.toLowerCase()));
    grid.innerHTML = filtered.map(name => {
      const firstName = getFirstName(name);
      const pngPath = `Avatar/${firstName}.png`;
      return `
        <div class="card">
          <a href="${toFileName(name)}">
            <img src="${pngPath}" alt="${name}">
            <div class="card-title">${name}</div>
          </a>
        </div>
      `;
    }).join('');
  }

  renderGrid();
  searchBar.addEventListener('input', e => renderGrid(e.target.value));
}

// Populate Navbar
const navbar = document.getElementById('navbar');
if (navbar) {
  navbar.innerHTML = actressNames.map(name => `<a href="${toFileName(name)}">${name}</a>`).join('');
}

// Fix double html/html/ in URL if present
if (window.location.pathname.match(/\/html\/html\//)) {
  window.location.pathname = window.location.pathname.replace('/html/html/', '/html/');
}