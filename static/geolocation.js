//GOOGLE MAPS API

let map;
let marker;
let geocoder;
let responseDiv;
let response;
let fullAdressSpan = document.getElementById("full-address-span");

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 37.7749295, lng: -122.4194155 },
    mapTypeControl: false,
  });
  geocoder = new google.maps.Geocoder();

  const inputText = document.createElement("input");

  inputText.type = "text";
  inputText.placeholder = "Enter a location";

  const submitButton = document.createElement("input");

  submitButton.type = "button";
  submitButton.value = "Search";
  submitButton.classList.add("button", "button-primary");

  const clearButton = document.createElement("input");

  clearButton.type = "button";
  clearButton.value = "Clear";
  clearButton.classList.add("button", "button-secondary");
  response = document.createElement("pre");
  response.id = "response";
  response.innerText = "";
  responseDiv = document.createElement("div");
  responseDiv.id = "response-container";
  responseDiv.appendChild(response);

  const instructionsElement = document.createElement("p");

  instructionsElement.id = "instructions";
  instructionsElement.innerHTML =
    "<strong>Instructions</strong>: Enter an address in the textbox get the exact coordinates.";
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(inputText);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(submitButton);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(clearButton);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(instructionsElement);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(responseDiv);
  marker = new google.maps.Marker({
    map,
  });

  map.addListener("click", (e) => {
    geocode({ location: e.latLng });
  });

  submitButton.addEventListener("click", () =>
    geocode({ address: inputText.value })
  );

  clearButton.addEventListener("click", () => {
    clear();
  });
  clear();
}

function clear() {
  marker.setMap(null);
  responseDiv.style.display = "none";
}

function geocode(request) {
  clear();
  geocoder
    .geocode(request)
    .then((result) => {
      const { results } = result;
      map.setCenter(results[0].geometry.location);
      marker.setPosition(results[0].geometry.location);
      marker.setMap(map);
      responseDiv.style.display = "hidden";
      response.innerText = JSON.stringify(result, null, 2);

      console.log(JSON.parse(response.innerText).results);

      let locationlat = document.getElementById("lat");
      locationlat.value = JSON.parse(
        response.innerText
      ).results[0].geometry.location.lat;

      let locationlng = document.getElementById("lng");
      locationlng.value = JSON.parse(
        response.innerText
      ).results[0].geometry.location.lng;

      fullAdressSpan.innerText = "";

      let address = document.getElementById("address");
      address.value = `${
        JSON.parse(response.innerText).results[0].formatted_address
      }`;

      fullAdressSpan.innerText = `${
        JSON.parse(response.innerText).results[0].formatted_address
      }`;

      //Chosing the right elements.
      let city = document.getElementById("city");
      let state = document.getElementById("state");
      let country = document.getElementById("country");
      let zipcode = document.getElementById("zipcode");
      //Deleting previous values.
      city.value=''
      state.value=''
      country.value=''
      zipcode.value=''

      for (let i of JSON.parse(response.innerText).results[0]
        .address_components) {
        if (i.types.indexOf("locality") != -1) {
          city.value = i.long_name;
        }
        if (i.types.indexOf("administrative_area_level_1") != -1) {
          state.value = i.short_name;
        }
        if (i.types.indexOf("country") != -1) {
          country.value = i.short_name;
        }
        if (i.types.indexOf("postal_code") != -1) {
          zipcode.value = i.long_name;
        }

      }

      return results;
    })
    .catch((e) => {
      alert("Geocode was not successful for the following reason: " + e);
    });
}

window.initMap = initMap;
