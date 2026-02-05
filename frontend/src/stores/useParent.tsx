import { create } from "zustand";
import { Parent } from "../hooks/useFetchParent";

type ParentState = {
  parent: Parent | null;
  setParent: (parent: Parent) => void;
};

export const useParentStore = create<ParentState>((set) => ({
  parent: null,
  setParent: (parent) => set({ parent }),
}));
