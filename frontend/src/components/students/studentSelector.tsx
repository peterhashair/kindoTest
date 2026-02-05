import { useState, useRef, useEffect } from "react";
import { Student, useFetchStudent } from "../../hooks/useFetchStudent";
import NotFound from "../../pages/404";
import { useParentStore } from "../../stores/useParent";
import { StudentForm, StudentFormHandle } from "./studentForm";
import { DropdownInput } from "../forms/dropdownInput";
import { Modal } from "../modal/modal";
import { toast } from "react-hot-toast/headless";

type StudentSelectorProps = {
  setStudent: (student: Student) => void;
  student: Student | null;
};

export const StudentSelector = ({
  student,
  setStudent,
}: StudentSelectorProps) => {
  const [open, setOpen] = useState(false);
  const formRef = useRef<StudentFormHandle>(null);

  const parent = useParentStore((state) => state.parent);
  if (!parent) {
    return null;
  }
  const [StudentState, refetchStudents] = useFetchStudent(parent.id);

  if (StudentState.type === "loading") {
    return <div>Loading...</div>;
  }

  if (StudentState.type === "error") {
    return <NotFound />;
  }

  const handleSubmit = async (value: any) => {
    value.gender = value.gender.name;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/students`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...value,
            parent_ids: [parent.id],
          }),
        },
      );

      const result = await response.json();
      if (result.status !== "success" || !response.ok) {
        throw new Error(result.error || "Failed to add student");
      }
      toast.success("Student added successfully!");
      setStudent(result.data);
      setOpen(false);
      refetchStudents();
    } catch (e) {
      toast.error(
        (e as Error).message || "Failed to add student. Please try again.",
      );
    }
  };

  const handleSaveClick = () => {
    if (formRef.current) {
      formRef.current.submitForm();
    }
  };

  return (
    <div className="mt-10">
      {StudentState.data.length > 0 ? (
        <DropdownInput
          value={student ?? StudentState.data[0]}
          onChange={(value) => setStudent(value)}
          options={StudentState.data}
          displayValue={(value: { name: string }) => value.name}
        >
          <DropdownInput.Label>Select Student:</DropdownInput.Label>
          <DropdownInput.Dropdown>
            <DropdownInput.Button />
            <DropdownInput.Options />
          </DropdownInput.Dropdown>
        </DropdownInput>
      ) : (
        <div className="text-gray-400">No students found.</div>
      )}
      <button
        onClick={() => setOpen(true)}
        className="mt-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
      >
        Add Student
      </button>
      <Modal open={open} onClose={setOpen}>
        <Modal.Backdrop />
        <Modal.Panel>
          <Modal.Body>
            <StudentForm ref={formRef} onSubmit={handleSubmit} />
          </Modal.Body>
          <Modal.Footer>
            <button
              type="button"
              onClick={handleSaveClick}
              className="inline-flex w-full justify-center rounded-md bg-blue-500 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-400 sm:ml-3 sm:w-auto"
            >
              Save
            </button>
            <button
              type="button"
              data-autofocus
              onClick={() => setOpen(false)}
              className="mt-3 inline-flex w-full justify-center rounded-md bg-white/10 px-3 py-2 text-sm font-semibold text-white inset-ring inset-ring-white/5 hover:bg-white/20 sm:mt-0 sm:w-auto"
            >
              Cancel
            </button>
          </Modal.Footer>
        </Modal.Panel>
      </Modal>
    </div>
  );
};
