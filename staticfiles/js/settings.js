document.addEventListener('DOMContentLoaded', function () {
  // Handle account deletion confirmation
  const form = document.getElementById('delete-account-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      // Show confirmation dialog before submitting the delete account form
      if (!confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        e.preventDefault();
      }
    });
  }
});