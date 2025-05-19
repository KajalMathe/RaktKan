document.addEventListener("DOMContentLoaded", function() {
    const passwordInput = document.getElementById("id_password");
    const confirmPasswordInput = document.getElementById("id_confirm_password");
  
    function validatePassword() {
      if (passwordInput.value !== confirmPasswordInput.value) {
        confirmPasswordInput.setCustomValidity("Passwords do not match.");
      } else {
        confirmPasswordInput.setCustomValidity("");
      }
    }
  
    if (passwordInput && confirmPasswordInput) {
      passwordInput.onchange = validatePassword;
      confirmPasswordInput.onkeyup = validatePassword;
    }
  });
  