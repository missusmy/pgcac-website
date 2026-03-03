function theme_apply() {
  'use strict';
  if (theme === 'light') {
    document.getElementById('btn-theme').innerHTML = '<i class="fas fa-moon"></i>';
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
  } else {
    document.getElementById('btn-theme').innerHTML = '<i class="fas fa-lightbulb"></i>';
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  }
}
theme_apply();
document.getElementById("form-theme").style.display = "block";
function theme_switch() {
  'use strict';
  if (theme === 'light') {
    theme = 'dark';
  } else {
    theme = 'light';
  }
  theme_apply();
}
let theme_OS = window.matchMedia('(prefers-color-scheme: light)');
theme_OS.addEventListener('change', function (e) {
  'use strict';
  if (e.matches) {
    theme = 'light';
  } else {
    theme = 'dark';
  }
  theme_apply();
});
// Ensure the body has top padding equal to the fixed navbar height
(function () {
  'use strict';
  var updatePadding = function () {
    var nav = document.querySelector('nav.navbar.no-shadow, nav.navbar.small-shadow');
    var body = document.querySelector('body.fullwidth');
    if (!nav || !body) return;
    var h = nav.offsetHeight || 0;
    body.style.paddingTop = h + 'px';
    // Expose navbar height as CSS variable for layout calculations
    document.documentElement.style.setProperty('--nav-height', h + 'px');
  };
  // Debounce resize handling
  var resizeTimer = null;
  var onResize = function () {
    if (resizeTimer) clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      updatePadding();
      resizeTimer = null;
    }, 100);
  };
  // Run on load and when DOM changes that might affect height
  window.addEventListener('load', updatePadding, { passive: true });
  window.addEventListener('resize', onResize, { passive: true });
  window.addEventListener('orientationchange', onResize, { passive: true });
  // Also run as soon as DOM is ready
  document.addEventListener('DOMContentLoaded', updatePadding);
}());

// Note: Scroll-blocking for the mobile navbar has been removed per request.