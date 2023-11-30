// app.js
function changeProfilePicture() {
  // Open a file selection dialog for the user to choose a new profile picture
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.onchange = function(event) {
    const file = event.target.files[0];
    // Create a FormData object to send the file to the server
    const formData = new FormData();
    formData.append('profile_picture', file);
    // Send an AJAX request to the server to change the profile picture
    alert('Uploading profile picture...');
    fetch('/change_profile_picture', {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(result => {
        // Display a success message to the user
        alert(result);
        // Optionally, update the profile picture displayed on the page
        const profilePicture = document.getElementById('profile-picture');
        profilePicture.src = URL.createObjectURL(file);
      })
      .catch(error => {
        // Display an error message to the user
        console.error(error);
        alert('An error occurred while changing the profile picture.');
      });
  };
  input.click();
}

