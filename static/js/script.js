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

  // Date picker for registration form
  document.addEventListener('DOMContentLoaded', function() {
      var elems = document.querySelectorAll('.datepicker');
      var instances = M.Datepicker.init(elems, {format: 'dd/mm/yyyy'});
    });
  
    var currentPage = 0; // Current tab is set to be the first tab (0)
    showPage(currentPage); // Display the current tab

  function showPage(n) {
    // This function will display the specified tab of the form ...
    var page = document.getElementsByClassName("form-page");
    page[n].style.display = "block";
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
      document.getElementById("prevBtn").style.display = "none";
    } else {
      document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (page.length - 1)) {
      document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
      document.getElementById("nextBtn").innerHTML = "Next";
    }
    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(n)
  }

  function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("form-page");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentPage].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentPage = currentPage + n;
    // if you have reached the end of the form... :
    if (currentPage >= x.length) {
      //...the form gets submitted:
      document.getElementById("regForm").submit();
      return false;
    }
    // Otherwise, display the correct tab:
    showPage(currentPage);
  }

  function validateForm() {
    // This function deals with validation of the form fields
    var form, formInputs, i, valid = true;
    form = document.getElementsByClassName("form-page");
    formInputs = form[currentPage].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < formInputs.length; i++) {
      // If a field is empty...
      if (formInputs[i].value == "") {
        // add an "invalid" class to the field:
        formInputs[i].className += " invalid";
        // and set the current valid status to false:
        valid = false;
      }
    }
    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentPage].className = " step finish fas fa-check-circle";
    }
    
    return valid; // return the valid status
  }

  function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
      x[i].className = x[i].className.replace(" active fas fa-dot-circle", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active fas fa-dot-circle";
  }