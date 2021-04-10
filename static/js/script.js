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