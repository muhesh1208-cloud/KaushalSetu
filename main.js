/**
 * KaushalSetu - Main UI JavaScript
 * Handles navigation, mobile drawer toggle, alert dismissal, and UI enhancements.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Menu Toggle
  const mobileToggle = document.getElementById('mobileNavToggle');
  const navLinks = document.getElementById('navLinks');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const isOpen = navLinks.classList.contains('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
    });
  }

  // Auto-dismiss alerts after 6 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-6px)';
      setTimeout(() => alert.remove(), 400);
    }, 6000);
  });
});

/**
 * Dismiss an alert card manually
 */
function dismissAlert(button) {
  const alert = button.closest('.alert');
  if (alert) {
    alert.style.transition = 'opacity 0.25s ease';
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 250);
  }
}
