import { useState, useRef } from 'react';
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';
import { GoogleMap, DirectionsRenderer, DirectionsService } from '@react-google-maps/api';

// styles for places origin and destination search elements
const routeChoiceContainer = {
  margin: "0 0 0 3rem",
  display: "grid",
  gridTemplateColumns: "2fr 2fr 1fr"
};
const placesDropdown = {
  margin: "0 1rem",
};
const chooseRouteButton = {
  margin: "0 2rem",
};

// style for map
const containerStyle = {
  height: "50rem",
  margin: "3rem 5rem"
};

// position of map
const center = {
  lat: 53.34,
  lng: -6.26
};


export default function GoogleDirections() {

  // states for origin and destination values 
  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);

  // state for weather directions should be calculated yet
  const [calculate, setCalculate] = useState(false);

  // function triggered when origin and destination selected
  function calcRoute() {
    if (origin !== null && destination !== null) {
      setCalculate(true);
    };
  }

  // state for directions response
  const [response, setResponse] = useState(null);
  let count = useRef(0);

  // directions service options
  const DirectionsServiceOption = {
    destination: { placeId: origin.value.place_id },
    origin: { placeId: destination.value.place_id },
    travelMode: "TRANSIT",
  };

  // directions callback which sets response
  const directionsCallback = (response) => {
    console.log(response);

    if (response !== null && origin !== null && count.current < 2) {
      if (response.status === "OK") {
        count.current += 1;
        setResponse(response);
      } else {
        count.current = 0;
        console.log("response: ", response);
      }
    }
  };

  return (
    <div>
      <div style={routeChoiceContainer}>
        <div style={placesDropdown}>
          <GooglePlacesAutocomplete
            apiOptions={{ language: 'en-GB', region: 'ie' }}
            selectProps={{
              origin,
              onChange: setOrigin,
            }}
            autocompletionRequest={{
              bounds: [
                { lat: 53.66814524847642, lng: -6.713710391817202 },
                { lat: 53.11900451404619, lng: -5.971729440309045 }
              ],
              componentRestrictions: {
              country: ['ie'],
              }
            }}
          />
        </div>    
        <div style={placesDropdown}>
          <GooglePlacesAutocomplete
            apiOptions={{ language: 'en-GB', region: 'ie' }}
            selectProps={{
              destination,
              onChange: setDestination,
            }}
            autocompletionRequest={{
              bounds: [
                { lat: 53.66814524847642, lng: -6.713710391817202 },
                { lat: 53.11900451404619, lng: -5.971729440309045 }
              ],
              componentRestrictions: {
              country: ['ie'],
              }
            }}
          />
        </div>
        <button style={chooseRouteButton} onClick={calcRoute}>Calculate Route</button>
      </div>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={10}
      >
        {response !== null && (
          <DirectionsRenderer
            options={{
              directions: response,
            }}
          />
        )}
        {calculate && (
          <DirectionsService
            options={DirectionsServiceOption}
            callback={directionsCallback}
          />
        )}
      </GoogleMap>
    </div>
  )
};