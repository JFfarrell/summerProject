import { useQuery, gql } from "@apollo/client";

const PREDICTIONS = gql`
  query Prediction($route: String!, $direction: String!, $day: String!, $hour: String!, $month: String!, $stopNum: String!){
    prediction (route:$route, direction:$direction, day:$day, hour:$hour, month:$month, rain:"4", temp:"9", listSize: 10, stopNum: $stopNum)
  }
`;

export default function ArrivalPredictions(props) {

  const table = {
    border: '1px solid black',
    borderCollapse: 'collapse',
    margin: '0 0 0 3rem'
  };

  const header = {
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

  const { route, direction, stopNum, destination} = props;

  let output = [];

  const { loading, error, data } = useQuery(PREDICTIONS, {
    variables: { route, direction, day, hour, month, stopNum },
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error :(</div>;

  if (data) {
    // first the string returned has to be maniupulated to turn into an array
    let predictionString = data.prediction;
    predictionString = predictionString.replace("[", "");
    predictionString = predictionString.replace("]", "");
    predictionString = predictionString.replace(new RegExp("'", 'g'), "");
    predictionString = predictionString.replace(new RegExp(",", 'g'), "");
    let predictions = predictionString.split(" ")
    // for each bus arrivng, push table row
    predictions.forEach((val)=>{
      output.push(
      <tr key={destination+val}>
        <td style={items}>{destination}</td>
        <td style={items}>{val}</td>
      </tr>
      )
      });
  }

  return (
    <div>
      <table style={table}>
        <thead>
          <tr>
            <th style={header}>Destination</th>
            <th style={header}>Expected Time</th>
          </tr>
        </thead>
        <tbody>
          {output}
        </tbody>
      </table>
    </div>
  );
};