import { NextResponse } from "next/server";
import { getIdeaCatalog } from "@/lib/ideas";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function GET() {
  const catalog = await getIdeaCatalog();
  return NextResponse.json(catalog, {
    headers: {
      "Cache-Control": "no-store",
    },
  });
}
