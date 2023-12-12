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

let date = new Date();
// Get the year and month
let year = date.getFullYear();
let month = date.getMonth();

// Get the next month
function nextMonth() {
  // If the current month is December, the returned value will be 0
  if (month === 11) {
    year++;
    month = 0;
  } else {
    month++;
  }
  Calendar();
}

// Get the previous month
function prevMonth() {
  // If the current month is January, the returned value will be 11
  if (month === 0) {
    year--;
    month = 11;
  } else {
    month--;
  }
  Calendar();
}

function getMonth(month) {
  switch (month) {
    case 0:
      return "January";
    case 1:
      return "Febuary";
    case 2:
      return "March";
    case 3:
      return "April";
    case 4:
      return "May";
    case 5:
      return "June";
    case 6:
      return "July";
    case 7:
      return "August";
    case 8:
      return "September";
    case 9:
      return "October";
    case 10:
      return "November";
    case 11:
      return "December";
  }
}

// Calendar function
function generateCalendar(calendarData) {
  // Get the table body element
  const monthAndYear = document.getElementById("monthAndYear");
  monthAndYear.innerHTML = getMonth(month) + " " + year;
  const calendarBody = document.getElementById("calendar-body");
  // Clear the table body
  calendarBody.innerHTML = "";
  // Get the number of days in the current month
  const numDays = new Date(year, month + 1, 0).getDate();
  // Get the day of the week for the first day of the month
  const startDay = new Date(year, month, 1).getDay();
  // Start creating the calendar rows
  let row = document.createElement("tr");
  // Add empty cells for the days before the start day
  for (let i = 0; i < startDay; i++) {
    let cell = document.createElement("td");
    row.appendChild(cell);
  }
  // Add the days of the month
  for (let day = 1; day <= numDays; day++) {
    var eventName = "";
    var eventId = "";
    let cell = document.createElement("td");
    cell.innerHTML = "<b>" + day + "</b>";
    for (const event of calendarData) {
      let fullMonth = (month + 1).toString().padStart(2, "0");
      let fullDay = day.toString().padStart(2, "0");
      var cmp = year + "-" + fullMonth + "-" + fullDay;
      // let fullMonth = (month + 1).padStart(2, "0");
      // let fullDay = day.padStart(2, "0");
      // var cmp = year + "-" + (month + 1) + "-" + day.padStart(2, "0");
      console.log("cmp: ", cmp)
      console.log("date: ", event["date"])
      if (event["date"] === cmp) {
        var eventName = event["name"];
        var eventId = event["id"];
        if (eventName != "") {
          if (event.status === "made") {
            cell.innerHTML += "<br>" + "<a href=/event/" + eventId + "><div class=\"made\">" + eventName + "</div></a>";
          }
          if (event.status === "accepted") {
            cell.innerHTML += "<br>" + "<a href=/event/" + eventId + "><div class=\"accepted\">" + eventName + "</div></a>";
          }
          if (event.status === "invited") {
            cell.innerHTML += "<br>" + "<a href=/event/" + eventId + "><div class=\"invited\">" + eventName + "</div></a>";
          }
        }
      }
    }
    row.appendChild(cell);
    // Start a new row after every 7 cells
    if (row.children.length === 7) {
      calendarBody.appendChild(row);
      row = document.createElement("tr");
    }
  }
  // Add the remaining cells to the last row
  if (row.children.length > 0) {
    calendarBody.appendChild(row);
  }
}

// generate calendar
function Calendar() {
  // function to send ajax request to server to generate calendar data
  fetch('/calendar_data', {
    method: 'GET'
  })
    .then(response => response.json())
    .then(data => {
      // function to generate calendar
      generateCalendar(data);
    })
    .catch(error => {
      // Display an error message to the user
      console.error(error);
      alert('An error occurred while generating the calendar.');
    });
}

