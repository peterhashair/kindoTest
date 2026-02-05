import { forwardRef, useImperativeHandle, useRef } from "react";
import { Formik, FormikProps } from "formik";
import * as Yup from "yup";
import { TextInput } from "./textInput";

export type PaymentFormValues = {
  cardName: string;
  cardNumber: string;
  expiryDate: string;
  cvc: string;
};

type PaymentFormProps = {
  onSubmit: (values: PaymentFormValues) => void;
};

export type PaymentFormHandle = {
  submitForm: () => void;
};

const PaymentValidationSchema = Yup.object().shape({
  cardName: Yup.string().required("Name on card is required"),
  cardNumber: Yup.string()
    .matches(/^[0-9]{16}$/, "Card number must be 16 digits")
    .required("Card number is required"),
  expiryDate: Yup.string()
    .matches(
      /^(0[1-9]|1[0-2])\/?([0-9]{2})$/,
      "Invalid expiry date format (MM/YY)",
    )
    .required("Expiry date is required"),
  cvc: Yup.string()
    .matches(/^[0-9]{3,4}$/, "CVC must be 3 or 4 digits")
    .required("CVC is required"),
});

export const PaymentForm = forwardRef<PaymentFormHandle, PaymentFormProps>(
  ({ onSubmit }, ref) => {
    const formikRef = useRef<FormikProps<PaymentFormValues>>(null);

    useImperativeHandle(ref, () => ({
      submitForm: () => {
        formikRef.current?.handleSubmit();
      },
    }));

    return (
      <Formik
        innerRef={formikRef}
        initialValues={{
          cardName: "",
          cardNumber: "",
          expiryDate: "",
          cvc: "",
        }}
        validationSchema={PaymentValidationSchema}
        onSubmit={onSubmit}
      >
        {({ values, handleChange, handleSubmit, errors, touched }) => (
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div className="col-span-full">
                <TextInput id="cardName">
                  <TextInput.Label>Name on card</TextInput.Label>
                  <TextInput.Field
                    name="cardName"
                    type="text"
                    autoComplete="cc-name"
                    value={values.cardName}
                    onChange={handleChange}
                  />
                </TextInput>
                {errors.cardName && touched.cardName ? (
                  <div className="text-red-500 text-sm mt-1">
                    {errors.cardName}
                  </div>
                ) : null}
              </div>

              <div className="col-span-full">
                <TextInput id="cardNumber">
                  <TextInput.Label>Card number</TextInput.Label>
                  <TextInput.Field
                    name="cardNumber"
                    type="text"
                    autoComplete="cc-number"
                    value={values.cardNumber}
                    onChange={handleChange}
                  />
                </TextInput>
                {errors.cardNumber && touched.cardNumber ? (
                  <div className="text-red-500 text-sm mt-1">
                    {errors.cardNumber}
                  </div>
                ) : null}
              </div>

              <div className="sm:col-span-3">
                <TextInput id="expiryDate">
                  <TextInput.Label>Expiration date (MM/YY)</TextInput.Label>
                  <TextInput.Field
                    name="expiryDate"
                    type="text"
                    autoComplete="cc-exp"
                    value={values.expiryDate}
                    onChange={handleChange}
                  />
                </TextInput>
                {errors.expiryDate && touched.expiryDate ? (
                  <div className="text-red-500 text-sm mt-1">
                    {errors.expiryDate}
                  </div>
                ) : null}
              </div>

              <div className="sm:col-span-3">
                <TextInput id="cvc">
                  <TextInput.Label>CVC</TextInput.Label>
                  <TextInput.Field
                    name="cvc"
                    type="text"
                    autoComplete="cc-csc"
                    value={values.cvc}
                    onChange={handleChange}
                  />
                </TextInput>
                {errors.cvc && touched.cvc ? (
                  <div className="text-red-500 text-sm mt-1">{errors.cvc}</div>
                ) : null}
              </div>
            </div>
          </form>
        )}
      </Formik>
    );
  },
);
