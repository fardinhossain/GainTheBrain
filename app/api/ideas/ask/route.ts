import { NextResponse } from "next/server";
import { getIdeaCatalog, type Idea } from "@/lib/ideas";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type AskRequest = {
  question?: unknown;
  ideaIds?: unknown;
};

function errorResponse(message: string, status = 400) {
  return NextResponse.json({ error: message }, { status });
}

function normalizeQuestion(value: unknown) {
  if (typeof value !== "string") {
    return "";
  }
  return value.trim().slice(0, 1600);
}

function normalizeIdeaIds(value: unknown) {
  if (!Array.isArray(value)) {
    return [];
  }
  return value
    .filter((item): item is string => typeof item === "string")
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 8);
}

function ideaContext(ideas: Idea[]) {
  return ideas
    .map((idea) => {
      const sections = idea.sections
        .map((section) => `## ${section.title}\n${section.markdown}`)
        .join("\n\n");
      return [
        `# ${idea.title}`,
        `Collection: ${idea.collectionLabel}`,
        `Folder: ${idea.folderLabel}`,
        `Difficulty: ${idea.difficulty}`,
        `Date: ${idea.date || "Not provided"}`,
        `Path: ${idea.path}`,
        sections,
      ]
        .join("\n")
        .slice(0, 5000);
    })
    .join("\n\n---\n\n")
    .slice(0, 24000);
}

function readAssistantText(body: unknown) {
  if (!body || typeof body !== "object") {
    return "";
  }
  const choices = (body as { choices?: unknown }).choices;
  if (!Array.isArray(choices) || !choices.length) {
    return "";
  }
  const first = choices[0] as { message?: { content?: unknown } };
  const content = first.message?.content;
  if (typeof content === "string") {
    return content.trim();
  }
  if (Array.isArray(content)) {
    return content
      .map((part) => {
        if (part && typeof part === "object" && typeof (part as { text?: unknown }).text === "string") {
          return (part as { text: string }).text;
        }
        return "";
      })
      .join("\n")
      .trim();
  }
  return "";
}

export async function POST(request: Request) {
  let payload: AskRequest;
  try {
    payload = (await request.json()) as AskRequest;
  } catch {
    return errorResponse("Request body must be valid JSON.");
  }

  const question = normalizeQuestion(payload.question);
  if (question.length < 4) {
    return errorResponse("Ask a longer question about your ideas.");
  }

  const apiKey = process.env.AI_API_KEY?.trim();
  const apiUrl = process.env.AI_API_URL?.trim();
  const model = process.env.AI_MODEL?.trim();

  if (!apiKey || !apiUrl || !model) {
    return errorResponse(
      "The idea assistant is not configured. Set AI_API_KEY, AI_API_URL, and AI_MODEL on the server.",
      503,
    );
  }

  let parsedUrl: URL;
  try {
    parsedUrl = new URL(apiUrl);
  } catch {
    return errorResponse("AI_API_URL is not a valid URL.", 500);
  }

  if (!["http:", "https:"].includes(parsedUrl.protocol)) {
    return errorResponse("AI_API_URL must use http or https.", 500);
  }

  const catalog = await getIdeaCatalog();
  const requestedIds = normalizeIdeaIds(payload.ideaIds);
  const ideas =
    requestedIds.length > 0
      ? catalog.projects.filter((idea) => requestedIds.includes(idea.id))
      : catalog.projects.slice(0, 6);

  if (!ideas.length) {
    return errorResponse("No matching ideas were found for this question.");
  }

  const response = await fetch(apiUrl, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: "system",
          content:
            "You help the owner of GainTheBrain understand and compare their project ideas. Answer from the supplied Markdown only. If the answer is not in the context, say what is missing.",
        },
        {
          role: "user",
          content: `Question:\n${question}\n\nProject idea context:\n${ideaContext(ideas)}`,
        },
      ],
      temperature: 0.3,
    }),
    cache: "no-store",
  });

  if (!response.ok) {
    const detail = (await response.text()).replaceAll(apiKey, "[REDACTED]").slice(0, 300);
    return errorResponse(`AI provider returned ${response.status}: ${detail || "no details"}`, 502);
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch {
    return errorResponse("AI provider returned a non-JSON response.", 502);
  }

  const answer = readAssistantText(body);
  if (!answer) {
    return errorResponse("AI provider returned an empty answer.", 502);
  }

  return NextResponse.json(
    {
      answer,
      ideaIds: ideas.map((idea) => idea.id),
    },
    {
      headers: {
        "Cache-Control": "no-store",
      },
    },
  );
}
