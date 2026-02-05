import { BookingList } from "../components/booking/bookingList";
import { Layout } from "./_layout";

export const Booking = () => {
  return (
    <Layout>
      <h1 className="text-3xl font-bold text-white">Booking Page</h1>
      <p className="mt-4 text-lg text-gray-300">
        This is where you can manage your bookings.
      </p>
      <BookingList />
    </Layout>
  );
};
