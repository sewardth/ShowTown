/**
 * @file Functions to handle the musician page content
 */


function like_musician(mus_id){
  $.ajax({
    type: "POST",
    url: '/video_likes',
    dataType: 'json',
    data: {
      mus_id:mus_id
    }})
    .done(function(data, textStatus, xhr){
      // var entries = data.trending_data;



    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}