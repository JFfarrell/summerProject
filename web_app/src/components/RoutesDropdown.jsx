import { useQuery, gql } from "@apollo/client";
import { useState } from "react";

const ROUTES = gql`
  query {
    uniqueRoutes {
      id
      stopNum
      routeNum
    }
  }
`;

function  RoutesDropdown() {

  const { loading, error, data } = useQuery(ROUTES);
  const [routeSearch, setRouteSearch] = useState('');

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  function chooseRoute(route) {
    console.log(route)
  }

  const container = {
    width: "13vw",
    minWidth: "11rem",
  }
  const buttonContainer = {
    height: "10rem"
  };
  const button = {
    display: "block",
    width: "100%",
    height: "2rem",
    margin: "3% 0"
  };

  return (
    <div style={container}>
      <h3>Choose a Route</h3>
      <input type="text" placeholder="Search by route number" onChange={event => {setRouteSearch(event.target.value)}} />
      <div style={buttonContainer}>
        { data.uniqueRoutes.filter((val)=> {
          if (routeSearch === "") {
            return val
          } else if (val.routeNum.startsWith(routeSearch)) {
            return val
          } else {
            return null
          }
        }).slice(0, 8).map(({ id, routeNum }) => {
          return (
            <input type="button" style={button} key={id} value={routeNum} onClick={ () => {chooseRoute(routeNum)}}></input>
          )
        })}
      </div>
    </div>
  )
}

export default RoutesDropdown;