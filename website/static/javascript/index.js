var lat;
var long;
function sentlocation(){
    
    document.getElementById("loca").innerHTML='<input type="text" class="hidden_stuff" name="latitude" value='+lat+' >'+'<input type="text" class="hidden_stuff" name="longitude" value='+ long+'>'
}
function showLocation(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    lat=latitude;
    long=longitude;
   sentlocation()
   //alert("Latitude : " + latitude + " Longitude: " + longitude);
}
function errorHandler(err) {
   if(err.code == 1) {
      alert("Error: Access is denied!");
   } else if( err.code == 2) {
      alert("Error: Position is unavailable!");
   }
}
function getLocation(){
   if(navigator.geolocation){
      // timeout at 60000 milliseconds (60 seconds)
      var options = {timeout:60000};
      navigator.geolocation.getCurrentPosition
      (showLocation, errorHandler, options);
   } else{
      alert("Sorry, browser does not support geolocation!");
   }
}
getLocation();