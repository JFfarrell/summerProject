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
    for (var i = 0; i < state.length; i++) {
    pins.push(
      <MapPin
        key={state[i].id}
        lat={state[i].latitude}
        lng={state[i].longitude}
        name={state[i].stopName}
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