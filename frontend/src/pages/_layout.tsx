import { Button } from "@headlessui/react";
import { useLocation, useNavigate } from "react-router-dom";

export const Layout = ({ children }: { children: React.ReactNode }) => {
  const navigator = useNavigate();
  const location = useLocation();

  return (
    <div className="bg-gray-900 py-24 sm:py-32 min-h-screen">
      <div className="mx-auto grid max-w-7xl gap-20 px-6 lg:px-8 relative">
        {location.pathname !== "/" && (
          <div className="absolute top-6 right-6 flex gap-4">
            <Button
              className="text-white cursor-pointer mt-3 inline-flex justify-center rounded-md bg-white/10 px-3 py-2 text-sm font-semibold text-white inset-ring inset-ring-white/5 hover:bg-white/20 "
              onClick={() => navigator(-1)}
            >
              Back
            </Button>
            <Button
              className="text-white cursor-pointer right-6 mt-3 inline-flex justify-center rounded-md bg-white/10 px-3 py-2 text-sm font-semibold text-white inset-ring inset-ring-white/5 hover:bg-white/20 "
              onClick={() => navigator("/booking")}
            >
              All your books
            </Button>
          </div>
        )}
        {children}
      </div>
    </div>
  );
};
