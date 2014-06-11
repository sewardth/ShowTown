/**
 * @file Functions common to all pages and jQuery initialization.
 */
 
$(document).ready(function() {
  switch(location.pathname){
    case '/':
      init_page()
      break;
    case '/trending':
      init_page()
      break;
    case '/venues':
      init_page()
      break;
    case '/find_musicians':
      init_page()
      break;
  }
});

// Stick here persistent objects such as dialogs.
var global = {};

/**
 * Objects to fill in pulldowns and get keys for AJAX calls
 */
var gig_offers = {'With Gigs':'with', 'Without Gigs':'without', Either:'either'};
// var genres = {alt:'Alternative', blues:'Blues', classical:'Classical', country:'Country', dance:'Dance',
//   easy_listening:'Easy Listening', electronic:'Electronic', hip_hop_rap:'Hip-Hop/Rap', industrial:'Industrial',
//   instrumental:'Instrumental', jazz:'Jazz', pop:'Pop', rock:'Rock', singer_songwriter:'Singer/Songwriter', vocal:'Vocal'};
var venue_types = {bar:'Bar', coffee_shop:'Coffee Shop', concert_house:'Concert House'};
// var states = {Michigan:'MI', California:'CA', Florida:'FL'}
