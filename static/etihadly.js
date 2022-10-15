$(document).ready(function(){

    $("#re-parse").click(function(){
      $('#editor').find('span').remove();
      var divContent = $('#editor').text();
      //alert(divContent);
      alert(divContent);
    });
  });
