import { useQuery, gql } from "@apollo/client";

const PREDICTIONS = gql`
  query {
    prediction (route:"37", direction:"inbound", day:"5", hour:"16", month:"7", rain:"4", temp:"9")
  }
`;

export default function ArrivalPredictions() {

  const { loading, error, data } = useQuery(PREDICTIONS);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error :(</div>;

  if (data) {
    console.log(data)
  }

  return (
    <div>got it</div>
  );
};