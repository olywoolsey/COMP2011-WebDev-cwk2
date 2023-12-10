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

function generateUserList() {
  fetch('/get_users')
    .then(response => response.json())
    .then(data => {
      var users = data.users;
      var userListElement = document.getElementById('userList');

      users.forEach(function(user) {
        var li = document.createElement('li');
        li.textContent = user;
        userListElement.appendChild(li);
      });
    })
    .catch(error => {
      console.error('Error retrieving users', error);
    });
}

function sendUserList() {
  var userList = document.getElementById('userList').getElementsByTagName('li');
  var selectedUsers = [];

  for (var i = 0; i < userList.length; i++) {
    selectedUsers.push(userList[i].textContent);
  }

  fetch('/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ users: selectedUsers })
  })
    .then(response => {
      if (response.ok) {
        console.log('Users sent successfully');
      } else {
        console.error('Error sending users');
      }
    })
    .catch(error => {
      console.error('Error sending users', error);
    });
}
