/// <reference types="vite/client" />

import { useState, useEffect } from "react";
import toast from "react-hot-toast";

export type Parent = {
  id: string;
  name: string;
  email: string;
};

export type ParentState =
  | { type: "loading" }
  | { type: "success"; data: Parent[] }
  | { type: "error"; error: Error };

export const useFetchParent = () => {
  const [state, setState] = useState<ParentState>({ type: "loading" });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/parents`,
        );

        const result = await response.json();

        if (result.status !== "success") {
          throw new Error(result.error || "Failed to fetch parents");
        }

        setState({ type: "success", data: result.data });
      } catch (e) {
        setState({ type: "error", error: e as Error });
      }
    };

    fetchData();
  }, []);

  return state;
};
