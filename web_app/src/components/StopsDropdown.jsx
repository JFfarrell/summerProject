import { useQuery, gql } from "@apollo/client";
import { useState } from "react";

const STOPS = gql`
  query {
    uniqueStops {
      id
      stopNum
      routeNum
    }
  }
`;

function  StopsDropdown() {

  const { loading, error, data } = useQuery(STOPS);
  const [stopSearch, setStopSearch] = useState('');

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <div>
      <input type="text" placeholder="Search by stop number" onChange={event => {setStopSearch(event.target.value)}} />
      { data.uniqueStops.filter((val)=> {
        if (stopSearch === "") {
          return val
        } else if (val.stopNum.includes(stopSearch)) {
          return val
        } else {
          return null
        }
      }).slice(0, 10).map(({ id, stopNum }) => {
        return (
          <div key={id}>
            <p>{stopNum}</p>
          </div>
        )
      })}
    </div>
  )
}

export default StopsDropdown;