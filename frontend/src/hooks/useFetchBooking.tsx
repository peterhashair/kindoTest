/// <reference types="vite/client" />

import { useState, useEffect, useCallback } from "react";
import toast from "react-hot-toast";

export type Booking = {
  id: string;
  total_in_cents: number;
  student_name: string;
  trip_name: string;
  status: string;
  created_at: string;
  school_id: string;
  updated_at: string;
};

export type BookingState =
  | { type: "loading" }
  | { type: "success"; data: Booking[] }
  | { type: "error"; error: Error };

export function useFetchBooking(parentId: string) {
  const [state, setState] = useState<BookingState>({
    type: "loading",
  });

  const fetchData = useCallback(async () => {
    setState({ type: "loading" });
    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/bookings/parent/${parentId}`,
      );
      const result = await response.json();

      if (result.status !== "success" || !response.ok) {
        throw new Error(result.error || "Failed to fetch bookings");
      }

      setState({ type: "success", data: result.data });
    } catch (e) {
      toast.error(
        (e as Error).message || "An error occurred while fetching bookings",
      );
      setState({ type: "error", error: e as Error });
    }
  }, [parentId]);

  useEffect(() => {
    if (parentId) {
      fetchData();
    }
  }, [parentId, fetchData]);

  return { state, refetch: fetchData };
}
