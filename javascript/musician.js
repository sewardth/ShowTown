/**
 * @file Functions to handle the musician page content
 */


function like_musician(mus_id, vid_id){
  $.ajax({
    type: "POST",
    url: '/vote/likes',
    dataType: 'json',
    data: {
      mus_id:mus_id,
      vid_id:vid_id
    }})
    .done(function(data, textStatus, xhr){
      if(data.musician_likes){
        $('#mus_likes').html(data.musician_likes + data.musician_wins);
        $('#'+data.video_key).html(data.video_wins + data.video_likes);
      }

      else{
        location.reload(true);
      }



    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}