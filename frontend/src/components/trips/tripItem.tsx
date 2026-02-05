import { Trip } from "../../hooks/useFetchtrip";

type TripItemProps = {
  trip: Trip;
};

export const TripItem = ({ trip }: TripItemProps) => {
  return (
    <div className="flex flex-col justify-between h-full">
      <div>
        <h2 className="text-3xl font-semibold tracking-tight text-pretty text-white sm:text-4xl">
          {trip.name}!
        </h2>
        <p className="mt-6 text-lg/8 text-gray-400">{trip.description}</p>
        <p className="my-2 text-gray-400"> {trip.school_name}</p>
        <p className="my-2 text-gray-400">Destination: {trip.destination}</p>
        <p className="my-2 text-gray-400">
          Start Date: {new Date(trip.start_date || "").toDateString()}
        </p>
        <p className="my-2 text-gray-400">
          End Date: {new Date(trip.end_date || "").toDateString()}
        </p>
        <p className="my-2 text-gray-400">
          Price: ${(trip.price_in_cents! / 100).toFixed(2)}
        </p>
      </div>
      <div></div>
    </div>
  );
};
