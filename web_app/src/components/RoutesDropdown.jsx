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

  return (
    <div>
      <input type="text" placeholder="Search by route number" onChange={event => {setRouteSearch(event.target.value)}} />
      { data.uniqueRoutes.filter((val)=> {
        if (routeSearch === "") {
          return val
        } else if (val.routeNum.includes(routeSearch)) {
          return val
        } else {
          return null
        }
      }).slice(0, 10).map(({ id, routeNum }) => {
        return (
          <div key={id}>
            <p>{routeNum}</p>
          </div>
        )
      })}
    </div>
  )
}

export default RoutesDropdown;