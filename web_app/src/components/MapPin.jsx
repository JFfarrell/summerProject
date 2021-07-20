function MapPin(props) {
  const { name } = props;
  const marker = {
    backgroundColor: "#000",
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
  const arrow = {
    display: "block",
    width: "0",
    height: "0",
    marginLeft: "-2rem",
    marginTop: "-3.65rem",
    borderLeft: "2rem solid transparent",
    borderRight: "2rem solid transparent",
    
    borderTop: "3rem solid lightgrey"
  }
  const boxContainer = {
    display: "block",
    backgroundColor: "lightgrey",
    marginLeft: "-8rem",
    marginTop: "-26rem",
    height: "23rem",
    width: "30rem"
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
  function togglePopup() {
    var box = document.getElementById("boxContainer");
    var arrow = document.getElementById("arrow");
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
        onClick={togglePopup}
      />
      <div
        style={arrow}
        id="arrow"

      />
      <div 
        style={boxContainer} 
        id="boxContainer"
      >
        <div style={header}>
          <h3>{name}</h3>
          <div>
            <p style={closeButton} onClick={togglePopup}>X</p>
          </div>
        </div>
        <hr />
        <p>arrival/departure time information here...</p>
      </div>
    </div>
  )
};

export default MapPin;