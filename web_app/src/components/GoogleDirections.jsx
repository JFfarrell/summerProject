import { useState, useRef } from 'react';
import { GoogleMap, DirectionsRenderer, DirectionsService } from '@react-google-maps/api';

const containerStyle = {
  height: "50rem",
  margin: "3rem 5rem"
};

const center = {
  lat: 53.34,
  lng: -6.26
};

const DirectionsServiceOption = {
  destination: { placeId: "ChIJa6XEGr0OZ0gRILjVsVwwPTg" },
  origin: { placeId: "ChIJz_6lJMoOZ0gRDHanHtH9zTs" },
  travelMode: "TRANSIT",
};

export default function GoogleDirections() {

  const [response, setResponse] = useState(null);
  let count = useRef(0);


  const directionsCallback = (response) => {
    console.log(response);

    if (response !== null && count.current < 2) {
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
      <DirectionsService
        options={DirectionsServiceOption}
        callback={directionsCallback}
      />
    </GoogleMap>
  )
};