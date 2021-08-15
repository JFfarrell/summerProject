import { useQuery, gql } from "@apollo/client";

// const PREDICTIONS = gql`
//   query StopPrediction($stopNum: String!, $day: String!, $month: String!, $hour: String!) {
//     stopPredictions (stopNum:$stopNum, day:$day, month:$month, hour:$hour, rain:"1", temp:"15") 
//   }
// `;

const PREDICTIONS = gql`
  query {
    stopPredictions (stopNum:"198", day:"4", month:"8", hour:"18", rain:"1", temp:"15") 
  }
`;

export default function MapPin(props) {

  const { destination, stopName, stopNum, markerColor, openPopup } = props;

  const table = {
    border: '1px solid black',
    borderCollapse: 'collapse',
    margin: '0 0 0 3rem'
  };

  const tableHeader = {
    backgroundColor: 'black',
    color: 'white',
    padding: '0.4rem 5rem 0.6rem 1rem',
    textAlign: 'left',
    whiteSpace: 'nowrap'
  };

  const items = {
    padding: '0.25rem 5rem 0.4rem 1rem',
    textAlign: 'left',
    whiteSpace: 'nowrap'
  };

  let today = new Date();
  let day = String(today.getDay()-1);
  let hour = String(today.getHours());
  let month = String(today.getMonth()+1);

  const { loading, error, data } = useQuery(PREDICTIONS, {
    variables: { stopNum, day, month, hour },
  });

  let prediction = [];

  if (loading) {
    prediction = "Loading..."
  }
  if (error) {
    prediction = "Error :("
  } 
  if (data) {
    // first the string returned has to be maniupulated to turn into an array
    let predictionString = data.stopPredictions.replace(new RegExp("'", 'g'), "\"");
    let predictionObject = JSON.parse(predictionString);
    prediction = predictionObject
    console.log(prediction)
  }

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
        {/* {data
          ? <table style={table}>
              <thead>
                <tr>
                  <th style={tableHeader}>Route</th>
                  <th style={tableHeader}>Destination</th>
                  <th style={tableHeader}>Expected Time</th>
                </tr>
              </thead>
              <tbody>
                {prediction.map((val) => (
                  <tr key={val}>
                    <td style={items}>{val}</td>
                    <td style={items}>{destination}</td>
                    <td style={items}>{prediction[val]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          : <div>{prediction}</div>
        } */}
      </div>
    </div>
  )
};