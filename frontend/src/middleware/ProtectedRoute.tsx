import { useEffect } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import { useParentStore } from "../stores/useParent";

export const ProtectedRoute = () => {
  const parent = useParentStore((state) => state.parent);
  const navigate = useNavigate();

  useEffect(() => {
    if (!parent) {
      navigate("/");
    }
  }, [parent, navigate]);

  if (!parent) {
    return null; // or a loading spinner
  }

  return <Outlet />;
};
