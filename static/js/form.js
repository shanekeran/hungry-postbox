// Javascript for register / edit profile form

// Date picker for registration form, displays over registration section.
document.addEventListener('DOMContentLoaded', function() {
  let registrationSection = document.getElementById("registration");
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, {format: 'dd/mm/yyyy',
                                              container: registrationSection, maxDate: new Date('01/01/2010'),
                                              minDate: new Date('01/01/1930'), defaultDate: new Date('01/01/2000'),
                                              yearRange: [1950, 2008]});
});

// Function to prevent register form returning inside envelope container after hover
function remainOpen() {
  const registerForm = document.getElementById("regForm");
  registerForm.classList.add("letter-open");
  }

// Multi step form, original code sourced from w3schools and modified (see README).
let currentPage = 0;
showPage(currentPage); // Display the current page

function showPage(n) {
  // This function will display the specified form page while the others are hidden
  let pages = document.getElementsByClassName("form-page");
  pages[n].style.display = "block";
  
  // Prev/Next buttons
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none"; // On the first page, prev btn is hidden.
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (pages.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "<span id='complete-form' class='valign-wrapper'>Submit</span>"; // on the last page, this replaces the next icon.
  } else {
    document.getElementById("nextBtn").innerHTML = "<i class='fas fa-chevron-circle-right'></i>";
  }
  // ... and run a function that displays the correct page indicator:
  updateIndicators(n);
}

function nextPrev(n) {
  // This function will figure out which tab to display
  let pages = document.getElementsByClassName("form-page");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  pages[currentPage].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentPage = currentPage + n;
  // if you have reached the end of the form... :
  if (currentPage >= pages.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showPage(currentPage);
}

function validateForm() {
  // This function deals with validation of the form fields
  let form, formInputs, valid = true;
  form = document.getElementsByClassName("form-page");
  formInputs = form[currentPage].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (let i = 0; i < formInputs.length; i++) {
    // If a field is empty: valid is set to false to prevent user from advancing.
    if (formInputs[i].value == "" || formInputs[i].validity.tooShort) {
      valid = false;
        if(formInputs[i].id =="picture"){
          valid=true; // picture field is permitted to be empty if default picture is chosen.
        }
    }
  }
  // If the valid status is true, the user can advance and a visual tick icon is displayed on progress bar.
  if (valid) {
      document.getElementsByClassName("indicator")[currentPage].className = " indicator finish fas fa-check-circle";
  }
  
  return valid; // return the valid status
}

function updateIndicators(n) {
  // Removes the "active" class off all steps...
  let indicator = document.getElementsByClassName("indicator");
  for ( let i = 0; i < indicator.length; i++) {
    indicator[i].className = indicator[i].className.replace(" active fas fa-dot-circle", "");
  }
  //... and adds the "active" class to the current step:
  indicator[n].className += " active fas fa-dot-circle";
}

// Shows URL input when user selects that they wish to customise their profile picture
const customiseButton = document.getElementById("customise-button");
let optionB = document.getElementsByClassName("customise");
let optionA = document.getElementsByClassName("default");
let input = document.getElementById("url");

if(customiseButton){  
  customiseButton.addEventListener('click', function() {
    let i;
    for (i=0;i<optionB.length;i+=1){
      optionB[i].style.display = 'block';
    }
    for (i=0;i<optionA.length;i+=1){
      optionA[i].style.display = 'none';
    }
    input.style.visibility = "visible" ;
    document.getElementById("picture").value = ""  ;
  });
}

// Hides URL input when user reselects the option to use the default profile picture
const defaultButton = document.getElementById('default-button');
if(defaultButton){
  defaultButton.addEventListener('click', function() {
    let i;
    for (i=0;i<optionB.length;i+=1){
      optionB[i].style.display = 'none';
    }
    for (i=0;i<optionA.length;i+=1){
      optionA[i].style.display = 'block';
    }
    input.style.visibility = "hidden" ;
    document.getElementById("picture").value = "https://i.imgur.com/8MovaTk.png";
    });
}

// Edit profile
const changeButton = document.getElementById('change-button');
if(changeButton){
  changeButton.addEventListener('click', function() {
    let i;
    for (i=0;i<optionB.length;i+=1){
      optionB[i].style.display = 'block';
    }
    for (i=0;i<optionA.length;i+=1){
      optionA[i].style.display = 'none';
    }
    input.style.visibility = "visible" ;
    document.getElementById("picture").value = "";
  });
}