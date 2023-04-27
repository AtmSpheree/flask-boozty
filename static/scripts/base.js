const LOCAL_STORAGE_THEME_KEY = "toggle-bootstrap-theme";

const LOCAL_META_DATA_THEME = JSON.parse(
  localStorage.getItem(LOCAL_STORAGE_THEME_KEY)
);

const DARK_THEME_PATH = "https://bootswatch.com/4/cyborg/bootstrap.min.css";

const DARK_STYLE_LINK = document.getElementById("dark-theme-style");
const THEME_TOGGLER = document.getElementById("theme-toggler");
const GITHUB_LOGO_IMG = document.getElementById("github-logo");
const GITHUB_TEXT_IMG = document.getElementById("github-text");
const GITHUB_BUTTON = document.getElementById("github-button");
const GITHUB_LOGO_IMG_WHITE_PATH = "static/img/GitHub_Logo_White.png";
const GITHUB_TEXT_IMG_WHITE_PATH = "static/img/github-mark-white.png";
const GITHUB_LOGO_IMG_DARK_PATH = "static/img/GitHub_Logo.png";
const GITHUB_TEXT_IMG_DARK_PATH = "static/img/github-mark.png";

let isDark = LOCAL_META_DATA_THEME && LOCAL_META_DATA_THEME.isDark;

if (isDark) {
  enableDarkTheme();
} else {
  disableDarkTheme();
}

function toggleTheme() {
  isDark = !isDark;
  if (isDark) {
    enableDarkTheme();
  } else {
    disableDarkTheme();
  }
  const META = { isDark };
  localStorage.setItem(LOCAL_STORAGE_THEME_KEY, JSON.stringify(META));
}

function enableDarkTheme() {
  DARK_STYLE_LINK.setAttribute("href", DARK_THEME_PATH);
  THEME_TOGGLER.innerHTML = "Светлая";
  THEME_TOGGLER.className = "btn btn-outline-light btn-lg toggle_theme_btn";
  GITHUB_LOGO_IMG.setAttribute("src", GITHUB_LOGO_IMG_DARK_PATH);
  GITHUB_TEXT_IMG.setAttribute("src", GITHUB_TEXT_IMG_DARK_PATH);
}

function disableDarkTheme() {
  DARK_STYLE_LINK.setAttribute("href", "");
  THEME_TOGGLER.innerHTML = "Тёмная";
  THEME_TOGGLER.className = "btn btn-outline-dark btn-lg toggle_theme_btn";
  GITHUB_LOGO_IMG.setAttribute("src", GITHUB_LOGO_IMG_WHITE_PATH);
  GITHUB_TEXT_IMG.setAttribute("src", GITHUB_TEXT_IMG_WHITE_PATH);
}

function RedirectOnLinkWithScript(sender) {
  document.location.href = sender.getAttribute("href");
}
