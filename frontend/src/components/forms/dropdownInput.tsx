import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
  Transition,
} from "@headlessui/react";
import {
  ComponentProps,
  createContext,
  FC,
  ReactNode,
  useContext,
} from "react";

type DropdownContextValue<T> = {
  value: T;
  onChange: (value: T) => void;
  options: T[];
  displayValue: (value: T) => string;
};

const DropdownContext = createContext<DropdownContextValue<any> | undefined>(
  undefined,
);

type DropdownInputRootProps<T> = {
  children: ReactNode;
  value: T;
  onChange: (value: T) => void;
  options: T[];
  displayValue: (value: T) => string;
};

const DropdownInputRoot = <T,>({
  children,
  value,
  onChange,
  options,
  displayValue,
}: DropdownInputRootProps<T>) => {
  return (
    <DropdownContext.Provider
      value={{ value, onChange, options, displayValue }}
    >
      <div className="sm:col-span-3">{children}</div>
    </DropdownContext.Provider>
  );
};

const useDropdownInput = () => {
  const context = useContext(DropdownContext);
  if (!context) {
    throw new Error(
      "useDropdownInput must be used within a DropdownInputProvider",
    );
  }
  return context;
};

const Label: FC<ComponentProps<"label">> = ({ children, ...props }) => {
  return (
    <label className="mb-2 block text-sm/6 font-medium text-white" {...props}>
      {children}
    </label>
  );
};

const Dropdown: FC<{ children: ReactNode }> = ({ children }) => {
  const { value, onChange } = useDropdownInput();
  return (
    <Listbox value={value} onChange={onChange}>
      <div className="relative mt-2">{children}</div>
    </Listbox>
  );
};

const Button: FC<ComponentProps<typeof ListboxButton>> = () => {
  const { value, displayValue } = useDropdownInput();
  return (
    <ListboxButton className="grid w-full cursor-default grid-cols-1 rounded-md bg-gray-800/50 py-1.5 pr-2 pl-3 text-left text-white outline-1 -outline-offset-1 outline-white/10 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-indigo-500 sm:text-sm/6">
      {displayValue(value)}
    </ListboxButton>
  );
};

const Options: FC<ComponentProps<typeof ListboxOptions>> = () => {
  const { options, displayValue } = useDropdownInput();
  return (
    <Transition
      leave="transition ease-in duration-100"
      leaveFrom="opacity-100"
      leaveTo="opacity-0"
    >
      <ListboxOptions className="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-gray-800 py-1 text-base outline-1 -outline-offset-1 outline-white/10 sm:text-sm">
        {options.map((option, index) => (
          <ListboxOption
            key={index}
            value={option}
            className="group relative cursor-default select-none py-2 pl-3 pr-9 text-white data-[focus]:bg-indigo-500"
          >
            <div className="ml-3 block truncate font-normal group-data-[selected]:font-semibold">
              {displayValue(option)}
            </div>
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Transition>
  );
};

export const DropdownInput = Object.assign(DropdownInputRoot, {
  Label,
  Dropdown,
  Button,
  Options,
});
