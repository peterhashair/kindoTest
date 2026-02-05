/// <reference types="vite/client" />

import { useState, useEffect, useCallback } from "react";
import toast from "react-hot-toast";

export type Student = {
  id: number;
  name: string;
  gender: string;
  dob: string;
};

export type StudentState =
  | { type: "loading" }
  | { type: "success"; data: Student[] }
  | { type: "error"; error: Error };

export const useFetchStudent = (id: string): [StudentState, () => void] => {
  const [state, setState] = useState<StudentState>({ type: "loading" });

  const fetchData = useCallback(async () => {
    setState({ type: "loading" });
    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/students/parent/${id}`,
      );

      const result = await response.json();
      if (result.status !== "success" || !response.ok) {
        throw new Error(result.error || "Failed to fetch students");
      }
      setState({ type: "success", data: result.data });
    } catch (e) {
      toast.error(
        (e as Error).message || "An error occurred while fetching students",
      );
      setState({ type: "error", error: e as Error });
    }
  }, [id]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return [state, fetchData];
};
