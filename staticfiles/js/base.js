const nav = document.querySelector("nav"),
  profile = document.querySelector(".account");

const nav_open = () => {
  nav.classList.toggle("open");
};

const createColor = () => {
  const hexArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F'];
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += hexArray[Math.floor(Math.random() * 16)];
  }
  return color;
};

color = createColor()

localStorage.setItem("color", color)

profile.style.background = `${localStorage.getItem("color")}`