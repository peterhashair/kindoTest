import { useFetchParent, Parent } from "../../hooks/useFetchParent";
import { useParentStore } from "../../stores/useParent";
import { useNavigate } from "react-router-dom";

const parentPhotos = [
  "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  "https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  "https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
];

export default function ParentList() {
  const navigate = useNavigate();
  const parentsState = useFetchParent();
  const setParent = useParentStore((state) => state.setParent);

  if (parentsState.type === "loading") {
    return <div>Loading...</div>;
  }

  if (parentsState.type === "error") {
    return <div>Error: {parentsState.error.message}</div>;
  }

  const onParentSelectClick = (parent: Parent) => {
    setParent(parent);
    navigate("/trips");
  };

  return (
    <ul
      role="list"
      className="grid gap-x-8 gap-y-12 sm:grid-cols-2 sm:gap-y-16 xl:col-span-2"
    >
      {parentsState.data.map((parent, index) => (
        <li
          key={parent.id}
          className="hover:scale-105 transition-transform cursor-pointer"
          onClick={() => onParentSelectClick(parent)}
        >
          <div className="flex items-center gap-x-6">
            <img
              alt=""
              src={parentPhotos[index % parentPhotos.length]}
              className="size-16 rounded-full outline-1 -outline-offset-1 outline-white/10"
            />

            <div>
              <h3 className="text-base/7 font-semibold tracking-tight text-white">
                {parent.name}
              </h3>
              <p className="text-sm/6 font-semibold text-indigo-400">
                {parent.email}
              </p>
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
}
