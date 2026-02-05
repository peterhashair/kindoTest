import { Route, Routes } from "react-router-dom";
import "./index.css";
import Home from "./pages/home";
import { Trips } from "./pages/trips/index";
import { Trip } from "./pages/trips/id";
import { ProtectedRoute } from "./middleware/ProtectedRoute";
import { Booking } from "./pages/booking";
import NotFound from "./pages/404";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/trips" element={<Trips />} />
        <Route path="/trips/:id" element={<Trip />} />
        <Route path="/booking" element={<Booking />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
