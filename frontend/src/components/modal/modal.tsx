import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
  DialogTitle,
} from "@headlessui/react";
import { FC, ReactNode } from "react";

type ModalRootProps = {
  open: boolean;
  onClose: (value: boolean) => void;
  children: ReactNode;
};

const ModalRoot: FC<ModalRootProps> = ({ open, onClose, children }) => {
  return (
    <Dialog open={open} onClose={onClose} className="relative z-10">
      {children}
    </Dialog>
  );
};

const Backdrop: FC = () => {
  return (
    <DialogBackdrop
      transition
      className="fixed inset-0 bg-gray-900/50 transition-opacity data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in"
    />
  );
};

const Panel: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div className="flex min-h-full items-stretch justify-center text-center sm:items-center sm:p-0">
        <DialogPanel
          transition
          className="relative flex w-full transform flex-col text-left text-base transition sm:my-8 sm:max-w-lg"
        >
          {children}
        </DialogPanel>
      </div>
    </div>
  );
};

const Body: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="flex flex-grow flex-col overflow-y-auto bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4 sm:rounded-t-lg">
      {children}
    </div>
  );
};

const Footer: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="bg-gray-700/25 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6 sm:rounded-b-lg">
      {children}
    </div>
  );
};

export const Modal = Object.assign(ModalRoot, {
  Backdrop,
  Panel,
  Body,
  Footer,
  Title: DialogTitle,
});
