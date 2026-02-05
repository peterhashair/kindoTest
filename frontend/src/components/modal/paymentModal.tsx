import { useRef } from "react";
import { Modal } from "./modal";
import { Trip } from "../../hooks/useFetchtrip";
import { TripItem } from "../trips/tripItem";
import { useParentStore } from "../../stores/useParent";
import {
  PaymentForm,
  PaymentFormHandle,
  PaymentFormValues,
} from "../forms/paymentForm";
import toast from "react-hot-toast";
import { Booking } from "../../hooks/useFetchBooking";

type PaymentModalProps = {
  student: { name: string };
  trip?: Trip;
  booking: Booking | null;
  open: boolean;
  onClose: () => void;
};

export const PaymentModal = ({
  student,
  trip,
  booking,
  open,
  onClose,
}: PaymentModalProps) => {
  const parent = useParentStore((state) => state.parent);
  const paymentFormRef = useRef<PaymentFormHandle>(null);

  const handleCheckout = async (values: PaymentFormValues) => {
    const toastId = toast.loading("Processing payment...");
    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/payments/process`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: (booking!.total_in_cents / 100).toFixed(2),
            activity_id: booking!.id,
            student_name: student.name,
            parent_name: parent?.name,
            school_id: booking!.school_id,
            card_number: values.cardNumber,
            expiry_date: values.expiryDate,
            cvv: values.cvc,
          }),
        },
      );

      const result = await response.json();

      if (result.status !== "success" || !response.ok) {
        throw new Error(result.error || "Payment failed. Please try again.");
      }

      toast.success("Payment processed successfully!", { id: toastId });
      onClose();
    } catch (e: any) {
      toast.error(e.message || "An unexpected error occurred.", {
        id: toastId,
      });
    }
  };

  const handlePayClick = () => {
    paymentFormRef.current?.submitForm();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Modal.Backdrop />
      <Modal.Panel>
        <Modal.Body>
          {trip && <TripItem trip={trip} />}
          <p className="mt-4 text-gray-400">Attend Students: {student.name}</p>
          <div className="mt-4 mb-4 border-t border-gray-300"></div>
          <PaymentForm ref={paymentFormRef} onSubmit={handleCheckout} />
        </Modal.Body>
        <Modal.Footer>
          <button
            type="button"
            onClick={handlePayClick}
            className="inline-flex w-full justify-center rounded-md bg-blue-500 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-400 sm:ml-3 sm:w-auto"
          >
            pay now
          </button>
          <button
            type="button"
            data-autofocus
            onClick={onClose}
            className="mt-3 inline-flex w-full justify-center rounded-md bg-white/10 px-3 py-2 text-sm font-semibold text-white inset-ring inset-ring-white/5 hover:bg-white/20 sm:mt-0 sm:w-auto"
          >
            Cancel
          </button>
        </Modal.Footer>
      </Modal.Panel>
    </Modal>
  );
};
