import { useState } from "react";
import { formatTime } from "../../helpers/time";
import { Booking, useFetchBooking } from "../../hooks/useFetchBooking";
import { PaymentModal } from "../modal/paymentModal";
import { useParentStore } from "../../stores/useParent";

const getStatusClass = (status: string) => {
  switch (status.toLowerCase()) {
    case "confirmed":
      return "bg-green-500/10 text-green-400 ring-green-500/20";
    case "pending":
      return "bg-yellow-500/10 text-yellow-400 ring-yellow-500/20";
    case "cancelled":
      return "bg-red-500/10 text-red-400 ring-red-500/20";
    default:
      return "bg-gray-500/10 text-gray-400 ring-gray-500/20";
  }
};

export const BookingList = () => {
  const [open, setOpen] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);
  const parent = useParentStore((state) => state.parent);

  const { state: bookingState, refetch } = useFetchBooking(parent!.id);
  const bookings = bookingState.type === "success" ? bookingState.data : [];
  const onClose = () => {
    setOpen(false);
    refetch();
  };

  const onPayNowClick = (booking: Booking) => {
    setSelectedBooking(booking);
    setOpen(true);
  };
  return (
    <div>
      {bookings.length === 0 ? (
        <p className="text-center text-gray-400">You have no bookings yet.</p>
      ) : (
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {bookings.map((booking) => (
            <div
              key={booking.id}
              className="group relative flex flex-col overflow-hidden rounded-lg border border-white/10 bg-gray-800/50 hover:bg-gray-800/80 transition-colors duration-300"
            >
              <div className="flex flex-1 flex-col space-y-4 p-6">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-white">
                    {booking.trip_name}
                  </h3>
                  <p className="mt-2 text-sm text-gray-400">
                    For {booking.student_name}
                  </p>
                </div>
                <div className="border-t border-white/10 pt-4">
                  <p className="text-sm text-gray-400">
                    Booked on: {formatTime(booking.created_at)}
                  </p>
                </div>
              </div>
              <div className="flex items-center justify-between border-t border-white/10 bg-gray-900/50 p-4">
                <p className="text-lg font-medium text-white">
                  ${(booking.total_in_cents / 100).toFixed(2)}
                </p>
                <span
                  className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${getStatusClass(
                    booking.status,
                  )}`}
                >
                  {booking.status}
                </span>
              </div>
              <div className="border-t border-white/10 bg-gray-900/50 p-4">
                <button
                  onClick={() => onPayNowClick(booking)}
                  type="button"
                  disabled={booking.status !== "pending"}
                  className="w-full justify-center rounded-md bg-blue-500 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-400 disabled:bg-gray-500 disabled:cursor-not-allowed"
                >
                  {booking.status !== "pending"
                    ? "no payment required"
                    : "pay now"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      <PaymentModal
        open={open}
        onClose={onClose}
        student={{
          name: selectedBooking?.student_name || "",
        }}
        booking={selectedBooking}
      />
    </div>
  );
};
