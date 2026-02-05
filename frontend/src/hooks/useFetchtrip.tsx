/// <reference types="vite/client" />

import { useState, useEffect } from "react";
import toast from "react-hot-toast";

export type Trip = {
  id: number;
  name: string;
  description: string;
  destination: string;
  school_id: string;
  price_in_cents: number;
  start_date: string;
  end_date: string;
  published: boolean;
  school_name: string;
};

export type TripState<T extends Trip | Trip[]> =
  | { type: "loading" }
  | { type: "success"; data: T }
  | { type: "error"; error: Error };

export function useFetchTrip(id: string): TripState<Trip>;
export function useFetchTrip(): TripState<Trip[]>;
export function useFetchTrip(id?: string): TripState<Trip | Trip[]> {
  const [state, setState] = useState<TripState<Trip | Trip[]>>({
    type: "loading",
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/trips${id ? `/${id}` : ""}`,
        );

        const result = await response.json();

        if (result.status !== "success" || !response.ok) {
          throw new Error(result.error || "Failed to fetch trip(s)");
        }

        setState({ type: "success", data: result.data });
      } catch (e) {
        toast.error(
          (e as Error).message || "An error occurred while fetching trip(s)",
        );
        setState({ type: "error", error: e as Error });
      }
    };

    fetchData();
  }, [id]);

  return state;
}
