import {
  createContext,
  useContext,
  ComponentProps,
  FC,
  ReactNode,
} from "react";

type TextInputContextValue = {
  id?: string;
};

const TextInputContext = createContext<TextInputContextValue | undefined>(
  undefined,
);

type TextInputRootProps = {
  children: ReactNode;
  id?: string;
};

const TextInputRoot: FC<TextInputRootProps> = ({ children, id }) => {
  return (
    <TextInputContext.Provider value={{ id }}>
      <div className="sm:col-span-3">{children}</div>
    </TextInputContext.Provider>
  );
};

const useTextInput = () => {
  const context = useContext(TextInputContext);
  if (!context) {
    throw new Error("useTextInput must be used within a TextInputProvider");
  }
  return context;
};

const Label: FC<ComponentProps<"label">> = ({ children, ...props }) => {
  const { id } = useTextInput();
  return (
    <label
      htmlFor={id}
      className="mb-2 block text-sm/6 font-medium text-white"
      {...props}
    >
      {children}
    </label>
  );
};

const Field: FC<ComponentProps<"input">> = ({ ...props }) => {
  const { id } = useTextInput();
  return (
    <input
      id={id}
      className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
      {...props}
    />
  );
};

export const TextInput = Object.assign(TextInputRoot, { Label, Field });
