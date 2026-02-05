import { Layout } from "../_layout";
import { useFetchTrip } from "../../hooks/useFetchtrip";
import { useParentStore } from "../../stores/useParent";
import { TripList } from "../../components/trips/tripList";

export const Trips = () => {
  const parent = useParentStore((state) => state.parent);
  const tripsState = useFetchTrip();

  if (tripsState.type === "loading") {
    return <div>Loading...</div>;
  }

  if (tripsState.type === "error") {
    return <div>Error: {tripsState.error.message}</div>;
  }

  return (
    <Layout>
      <div>
        <h2 className="text-3xl font-semibold tracking-tight text-pretty text-white sm:text-4xl">
          Hi, {parent?.name}!
        </h2>
        <p className="mt-6 text-lg/8 text-gray-400">
          Please select a trip from the list below to start:
        </p>
      </div>
      <TripList trips={tripsState.data} />
    </Layout>
  );
};
