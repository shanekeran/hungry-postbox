// Collapsed Mobile Navigation bar (Materialize)
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, { edge: "right"});
});
  
// User profile carousel (Materialize)
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.carousel');
    var instances = M.Carousel.init(elems, {});
  });

// Javascript for register and edit profile pages
const form = document.getElementsByTagName("form")
if (form) {
    // Date picker for registration form, displays over registration section.
    document.addEventListener('DOMContentLoaded', function() {
      let registrationSection = document.getElementById("registration")
        var elems = document.querySelectorAll('.datepicker');
        var instances = M.Datepicker.init(elems, {format: 'dd/mm/yyyy',
                                                  container: registrationSection, maxDate: new Date('01/01/2010'),
                                                  minDate: new Date('01/01/1930'), defaultDate: new Date('01/01/2000'),
                                                  yearRange: [1950, 2008]});
      });
    
    // Function to prevent register form returning inside envelope container after hover
    function remainOpen() {
      const form = document.getElementById("regForm");
      form.classList.add("letter-open")
      }
    
    // Multi step form, original code sourced from w3schools and modified (see README).
    var currentPage = 0;
    showPage(currentPage); // Display the current page

    function showPage(n) {
      // This function will display the specified form page while the others are hidden
      var pages = document.getElementsByClassName("form-page");
      pages[n].style.display = "block";
      // Prev/Next buttons
      if (n == 0) {
        document.getElementById("prevBtn").style.display = "none"; // On the first page, prev btn is hidden.
      } else {
        document.getElementById("prevBtn").style.display = "inline";
      }
      if (n == (pages.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "<span id='complete-form' class='valign-wrapper'>Register</span>"; // on the last page, this replaces the next icon.
      } else {
        document.getElementById("nextBtn").innerHTML = "<i class='fas fa-chevron-circle-right'></i>";
      }
      // ... and run a function that displays the correct page indicator:
      updateIndicators(n)
    }

    function nextPrev(n) {
      // This function will figure out which tab to display
      var pages = document.getElementsByClassName("form-page");
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
      var form, formInputs, valid = true;
      form = document.getElementsByClassName("form-page");
      formInputs = form[currentPage].getElementsByTagName("input");
      // A loop that checks every input field in the current tab:
      for (i = 0; i < formInputs.length; i++) {
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
      var indicator = document.getElementsByClassName("indicator");
      for (i = 0; i < indicator.length; i++) {
        indicator[i].className = indicator[i].className.replace(" active fas fa-dot-circle", "");
      }
      //... and adds the "active" class to the current step:
      indicator[n].className += " active fas fa-dot-circle";
    }


    // Shows URL input when user selects that they wish to customise their profile picture
    document.getElementById('customise-button').addEventListener('click', function() {
      var y = document.getElementsByClassName("customise")
      var x = document.getElementsByClassName("default")
      var j = document.getElementById("url")
      for (var i=0;i<y.length;i+=1){
        y[i].style.display = 'block';
      }
      for (var i=0;i<x.length;i+=1){
        x[i].style.display = 'none';
      }
      j.style.visibility = "visible" 
      document.getElementById("picture").value = ""  
      });
    
    // Hides URL input when user reselects the option to use the default profile picture
    document.getElementById('default-button').addEventListener('click', function() {
      var y = document.getElementsByClassName("customise")
      var x = document.getElementsByClassName("default")
      var j = document.getElementById("url")
      for (var i=0;i<y.length;i+=1){
        y[i].style.display = 'none';
      }
      for (var i=0;i<x.length;i+=1){
        x[i].style.display = 'block';
      }
      j.style.visibility = "hidden" 
      document.getElementById("picture").value = "../static/images/default-profile-pic.png" 
      });
}