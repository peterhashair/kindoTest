import { useParams } from "react-router-dom";
import { useFetchTrip } from "../../hooks/useFetchtrip";
import { Layout } from "../_layout";
import NotFound from "../404";
import { TripItem } from "../../components/trips/tripItem";
import { StudentSelector } from "../../components/students/studentSelector";
import { useState } from "react";
import { Student } from "../../hooks/useFetchStudent";
import { BookingModal } from "../../components/modal/bookingModal";

export const Trip = () => {
  const { id } = useParams<{ id: string }>();
  const [student, setStudent] = useState<Student | null>(null);

  if (!id) {
    return <NotFound />;
  }

  const TripState = useFetchTrip(id);

  if (TripState.type === "loading") {
    return <div>Loading...</div>;
  }

  if (TripState.type === "error") {
    return <NotFound />;
  }
  return (
    <Layout>
      <TripItem trip={TripState.data} />
      <StudentSelector setStudent={setStudent} student={student} />
      <BookingModal student={student} trip={TripState.data} />
    </Layout>
  );
};
