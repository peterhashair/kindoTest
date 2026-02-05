import { Trip } from "../../hooks/useFetchtrip";
import comingSoonImg from "../../assets/comingsoon.jpg";
import { formatTime } from "../../helpers/time";
import { useNavigate } from "react-router-dom";

type TripListProps = {
  trips: Trip[];
};

export const TripList = ({ trips }: TripListProps) => {
  const navigator = useNavigate();
  return (
    <div>
      <h2 className="sr-only">Products</h2>
      <div className="grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
        {trips.map((trip) => (
          <a
            key={trip.id}
            onClick={() => navigator(`/trips/${trip.id}`)}
            className="group"
          >
            <img
              src={comingSoonImg}
              alt={trip.name}
              className="h-55 w-full object-cover object-center group-hover:opacity-75"
            />
            <h3 className="mt-4 text-sm text-white">{trip.name}</h3>
            <p className="text-white">{formatTime(trip.start_date)}</p>
            <p className="mt-1 text-lg font-medium text-white">
              ${(trip.price_in_cents / 100).toFixed(2)}
            </p>
          </a>
        ))}
      </div>
    </div>
  );
};
