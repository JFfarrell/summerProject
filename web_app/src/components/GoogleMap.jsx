import GoogleMapReact from 'google-map-react';
import MapPin from "./MapPin"
import { useContext } from "react";
import { StationsContext } from "../contexts/stations"

const GOOGLE_API_KEY = process.env.REACT_APP_GOOGLE_API_KEY;

export default function SimpleMap(){
  const defaultProps = {
    center: {
      lat: 53.34,
      lng: -6.26
    },
    zoom: 11
  };

  const [ state ] = useContext(StationsContext)

  var pins = [];

  if (state) {
    if (state[0].length > 1) {
      state[0].forEach((stop) => {
          pins.push(
            <MapPin
              key={stop.stopNum}
              lat={stop.latitude}
              lng={stop.longitude}
              name={stop.stopName}
            />
          )
      });
    } else {
      pins.push(
        <MapPin
          key={state[0].stopNum}
          lat={state[0].latitude}
          lng={state[0].longitude}
          name={state[0].stopName}
        />
      )
    }
  }

  return (
    <div style={{ height: '100%', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: GOOGLE_API_KEY }}
        defaultCenter={defaultProps.center}
        defaultZoom={defaultProps.zoom}
      >
        {pins}
      </GoogleMapReact>
    </div>
  );
}