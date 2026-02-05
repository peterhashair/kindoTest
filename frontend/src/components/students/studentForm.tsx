import { Formik, FormikProps } from "formik";
import { forwardRef, useImperativeHandle, useRef } from "react";
import * as Yup from "yup";
import { TextInput } from "../forms/textInput";
import { DropdownInput } from "../forms/dropdownInput";

const StudentValidationSchema = Yup.object().shape({
  name: Yup.string().required("Name is required"),
  dob: Yup.date()
    .required("Date of birth is required")
    .max(new Date(), "Date of birth cannot be in the future"),
  gender: Yup.object().shape({
    id: Yup.number().required(),
    name: Yup.string().required("Gender is required"),
  }),
});

type StudentFormValues = {
  name: string;
  dob: string;
  gender: { id: number; name: string };
};

type StudentFormProps = {
  onSubmit: (values: StudentFormValues) => void;
};

export type StudentFormHandle = {
  submitForm: () => void;
};

const genders = [
  { id: 1, name: "male" },
  { id: 2, name: "female" },
  { id: 3, name: "other" },
];

export const StudentForm = forwardRef<StudentFormHandle, StudentFormProps>(
  ({ onSubmit }, ref) => {
    const formikRef = useRef<FormikProps<StudentFormValues>>(null);

    useImperativeHandle(ref, () => ({
      submitForm: () => {
        if (formikRef.current) {
          formikRef.current.handleSubmit();
        }
      },
    }));

    return (
      <Formik
        innerRef={formikRef}
        initialValues={{ name: "", gender: genders[0], dob: "" }}
        validationSchema={StudentValidationSchema}
        onSubmit={(values, { setSubmitting }) => {
          onSubmit(values);
          setSubmitting(false);
        }}
      >
        {({
          values,
          handleChange,
          handleSubmit,
          setFieldValue,
          errors,
          touched,
        }) => (
          <form onSubmit={handleSubmit}>
            <div className="border-b border-white/10 pb-12">
              <h2 className="text-base/7 font-semibold text-white">
                Student Information
              </h2>
              <p className="mt-1 text-sm/6 text-gray-400">
                please provide the student's information for the booking.
              </p>
              <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                <TextInput id="name">
                  <TextInput.Label>name</TextInput.Label>
                  <TextInput.Field
                    name="name"
                    type="text"
                    autoComplete="name"
                    value={values.name}
                    onChange={handleChange}
                  />
                  {errors.name && touched.name ? (
                    <div className="text-red-500 text-sm mt-1">
                      {errors.name}
                    </div>
                  ) : null}
                </TextInput>
              </div>
              <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                <DropdownInput
                  value={values.gender}
                  onChange={(value) => setFieldValue("gender", value)}
                  options={genders}
                  displayValue={(value: { name: string }) => value.name}
                >
                  <DropdownInput.Label>gender</DropdownInput.Label>
                  <DropdownInput.Dropdown>
                    <DropdownInput.Button />
                    <DropdownInput.Options />
                  </DropdownInput.Dropdown>
                  {errors.gender && touched.gender ? (
                    <div className="text-red-500 text-sm mt-1">
                      {typeof errors.gender === "object"
                        ? errors.gender.name
                        : errors.gender}
                    </div>
                  ) : null}
                </DropdownInput>
              </div>
              <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                <TextInput id="dob">
                  <TextInput.Label>Date of Birth:</TextInput.Label>
                  <TextInput.Field
                    type="date"
                    name="dob"
                    value={values.dob}
                    onChange={handleChange}
                  />
                  {errors.dob && touched.dob ? (
                    <div className="text-red-500 text-sm mt-1">
                      {errors.dob}
                    </div>
                  ) : null}
                </TextInput>
              </div>
            </div>
          </form>
        )}
      </Formik>
    );
  },
);
