function PlannerTab() {
  function calcRoute() {
    console.log("routing...")
  }
  return(
    <div>

      <h1>Plan your route</h1>
      <p>Enter an origin and destination and we will find the best route using the dublin bikes network</p>
      <br/>

      <input id="origin" placeholder="Origin" type="text" />
      <input id="destination" placeholder="Destination" type="text" />
      <button onClick={calcRoute}>Calculate Route</button>

      <div>map goes here</div>

    </div>
  )
}

export default PlannerTab;