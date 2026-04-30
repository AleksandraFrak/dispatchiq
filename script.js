const hamburger = document.querySelector('.hamburger');
const navList = document.querySelector('.nav-list');

hamburger.addEventListener('click', () => {
  const isOpen = navList.classList.toggle('active');
  hamburger.setAttribute('aria-expanded', isOpen);
});

const navLinks = document.querySelectorAll('.nav-list a');

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    navList.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
  });
});