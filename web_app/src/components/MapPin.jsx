import ArrivalPredictions from "./ArrivalPredictions";
import { useEffect } from "react";

let prediction;

export default function MapPin(props) {

  const { lineId, direction, destination, lng, lat, stopName, stopNum, irishName, departureSchedule, markerColor, openPopup } = props;

  useEffect(() => {
    prediction = <ArrivalPredictions 
      key={stopNum}
      route={lineId}
      direction={direction}
      stopNum={stopNum}
      destination={destination}
    />;
  }, [direction, lineId, stopNum, destination]);

  const marker = {
    backgroundColor: markerColor,
    cursor: 'pointer',
    position: "absolute",
    top: "0",
    left: "0",
    width: "18px",
    height: "18px",
    border: "2px solid #fff",
    borderRadius: "100%",
    userSelect: "none",
    transform: "translate(-50%, -50%)"
  };
  var arrow = {
    display: "none",
    width: "0",
    height: "0",
    marginLeft: "-2rem",
    marginTop: "-3.65rem",
    borderLeft: "2rem solid transparent",
    borderRight: "2rem solid transparent",
    borderTop: "3rem solid lightgrey",
    position: "absolute",
    zIndex: "3"
  };
  var boxContainer = {
    display: "none",
    backgroundColor: "lightgrey",
    marginLeft: "-8rem",
    marginTop: "-28rem",
    height: "25rem",
    width: "30rem",
    position: "absolute",
    zIndex: "3",
    borderRadius: "50px"
  };
  const header = {
    paddingTop: "0.5rem",
    fontSize: "1.4rem",
    display: "grid",
    gridTemplateColumns: "5fr 1fr"
  };
  const closeButton = {
    cursor: 'pointer',
  };

  // if openPopup prop is true, then ensure the marker renders with popup open
  if (openPopup) {
    arrow = {
      display: "block",
      width: "0",
      height: "0",
      marginLeft: "-2rem",
      marginTop: "-3.65rem",
      borderLeft: "2rem solid transparent",
      borderRight: "2rem solid transparent",
      borderTop: "3rem solid lightgrey",
      position: "absolute",
      zIndex: "3"
    };
    boxContainer = {
      display: "block",
      backgroundColor: "lightgrey",
      marginLeft: "-8rem",
      marginTop: "-28rem",
      height: "25rem",
      width: "30rem",
      position: "absolute",
      zIndex: "3",
      borderRadius: "50px"
    };
  }

  function togglePopup(n) {
    // this function handles the opening of a popup for the stop clicked

    // close already open popups
    var boxClass = document.getElementsByClassName("boxContainer");
    var arrowClass = document.getElementsByClassName("arrow");
    for (let i = 0; i < boxClass.length; i++) {
      if (boxClass[i].style.display === "block") {
        boxClass[i].style.display = "none";
        arrowClass[i].style.display = "none"
      }
    };

    // open this popup
    var box = document.getElementById(n+"-boxContainer");
    var arrow = document.getElementById(n+"-arrow");
    if (box.style.display === "none") {
      box.style.display = "block";
      arrow.style.display = "block";
    } else {
      box.style.display = "none";
      arrow.style.display = "none";
    }
  }

  return(
    <div>
      <div 
        style={marker}
        onClick={() => togglePopup(stopName)}
      />
      <div
        style={arrow}
        className={"arrow"}
        id={stopName+"-arrow"}

      />
      <div 
        style={boxContainer} 
        className={"boxContainer"}
        id={stopName+"-boxContainer"}
      >
        <div style={header}>
          <h3>{stopName}</h3>
          <div>
            <p style={closeButton} onClick={() => togglePopup(stopName)}>X</p>
          </div>
        </div>
        {prediction}
      </div>
    </div>
  )
};