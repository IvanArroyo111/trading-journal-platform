document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('sidebarToggle');
  var sidebar = document.getElementById('sidebar');

  // Toggle sidebar expanded class on click
  if (toggle && sidebar) {
    toggle.onclick = function () {
      sidebar.classList.toggle('expanded');
    };
  }
});