// Background music control
const toggleBtn = document.getElementById("toggle-sound");
const bgMusic = document.getElementById("bg-music");

if (toggleBtn && bgMusic) {
  toggleBtn.addEventListener("click", () => {
    if (bgMusic.paused) {
      bgMusic.play();
      toggleBtn.textContent = "🔈 Sound ON";
    } else {
      bgMusic.pause();
      toggleBtn.textContent = "🔇 Sound OFF";
    }
  });
}

// Loader hide after animation
window.addEventListener("load", () => {
  const loader = document.getElementById("loader");
  if (loader) loader.style.display = "none";
});
