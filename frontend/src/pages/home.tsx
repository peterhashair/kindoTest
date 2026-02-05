import ParentList from "../components/parents/parentList";
import { Layout } from "./_layout";

export default function Home() {
  return (
    <Layout>
      <div>
        <h2 className="text-3xl font-semibold tracking-tight text-pretty text-white sm:text-4xl">
          Welcome to Kindo Test!
        </h2>
        <p className="mt-6 text-lg/8 text-gray-400">
          Please select a parent from the list below to start:
        </p>
      </div>
      <ParentList />
    </Layout>
  );
}
