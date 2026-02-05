import { useState, useRef } from "react";
import { Trip } from "../../hooks/useFetchtrip";
import { Student } from "../../hooks/useFetchStudent";
import { useParentStore } from "../../stores/useParent";
import { PaymentModal } from "./paymentModal";
import toast from "react-hot-toast";
import { Booking } from "../../hooks/useFetchBooking";

type BookingModalProps = {
  student: Student | null;
  trip: Trip;
};

export const BookingModal = ({ student, trip }: BookingModalProps) => {
  const parent = useParentStore((state) => state.parent);
  const [open, setOpen] = useState(false);
  const [booking, setBooking] = useState<Booking | null>(null);

  if (!student) {
    return (
      <button
        disabled={true}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed mt-4"
      >
        Book Trip
      </button>
    );
  }

  const onBookingClick = async () => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/bookings`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            student_id: student.id,
            trip_id: trip.id,
            parent_id: parent?.id,
          }),
        },
      );
      const result = await response.json();

      if (!response.ok || result.status !== "success") {
        throw new Error(
          result.error.messaage ||
            "Failed to create booking. Please try again.",
        );
      }

      setBooking(result.data);
      setOpen(true);
    } catch (e) {
      toast.error(
        (e as Error).message || "Failed to create booking. Please try again.",
      );
    }
  };

  return (
    <>
      <button
        onClick={onBookingClick}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer mt-4"
      >
        Book Trip
      </button>
      <PaymentModal
        open={open}
        onClose={() => setOpen(false)}
        student={student}
        trip={trip}
        booking={booking}
      />
    </>
  );
};
