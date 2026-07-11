import { IdeaWorkspace } from "@/components/IdeaWorkspace";
import { getIdeaCatalog } from "@/lib/ideas";

export const dynamic = "force-dynamic";

export default async function Home() {
  const catalog = await getIdeaCatalog();
  return <IdeaWorkspace catalog={catalog} />;
}
