import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const IDEA_ROOTS = [
  {
    base: "project-ideas",
    directory: "project-ideas",
  },
  {
    base: "ai-builders-congress",
    directory: "ai-builders-congress",
  },
] as const;

type ReadmeFile = {
  absolutePath: string;
  relativePath: string;
};

const COLLECTION_LABELS: Record<string, string> = {
  "project-ideas": "Project Ideas",
  "ai-builders-congress": "AI Builders Congress",
};

const FOLDER_LABELS: Record<string, string> = {
  "general-cs": "General CS",
  "ai-ml": "AI / ML",
  "full-stack": "Full-Stack",
  "software-engineering": "Software Engineering",
  "web-development": "Web Development",
  "mobile-app": "Mobile App",
  cybersecurity: "Cybersecurity",
  "data-science": "Data Science",
  "cloud-devops": "Cloud and DevOps",
  "iot-embedded": "IoT and Embedded",
  blockchain: "Blockchain",
  "productivity-tools": "Productivity Tools",
  "developer-tools": "Developer Tools",
  "programming-education": "Programming Education",
  "foodsphere-ai": "FoodSphere AI",
  "healthsphere-ai": "HealthSphere AI",
  "finsphere-ai": "FinSphere AI",
  "learnsphere-ai": "LearnSphere AI",
  "climatesphere-ai": "ClimateSphere AI",
  "civicsphere-ai": "CivicSphere AI",
  "agrisphere-ai": "AgriSphere AI",
  "industrysphere-ai": "IndustrySphere AI",
  "commercesphere-ai": "CommerceSphere AI",
  "infrasphere-ai": "InfraSphere AI",
};

const SECTION_ALIASES: Record<string, string[]> = {
  category: ["Category / Domain", "Category", "Domain", "Challenge Type"],
  date: ["Date"],
  shortDescription: ["Short Description", "AI-Powered Solution"],
  problemStatement: ["Problem Statement"],
  proposedSolution: ["Proposed Solution", "AI-Powered Solution"],
  targetUsers: ["Target Users"],
  coreFeatures: ["Core Features"],
  advancedFeatures: ["Advanced Features"],
  aiIntegration: ["AI/ML Integration", "AI Model / API Idea"],
  techStack: ["Suggested Tech Stack"],
  databaseDesign: ["Database Design"],
  apiRoutes: ["API Route Ideas", "API Routes"],
  uiPages: ["UI Pages"],
  mvpPlan: ["MVP Plan", "MVP Development Plan"],
  futureScope: ["Future Scope"],
  difficulty: ["Difficulty Level"],
  portfolioValue: ["Portfolio Value", "Why This Project is Useful"],
  monetization: ["Possible Monetization"],
  learningOutcomes: ["Learning Outcomes"],
  realWorldImpact: ["Real-World Impact"],
  datasetIdea: ["Dataset Idea"],
  showcase: ["Final Showcase Presentation Idea"],
};

const DETAIL_SECTION_ORDER = [
  ["Problem Statement", "problemStatement"],
  ["Proposed Solution", "proposedSolution"],
  ["Target Users", "targetUsers"],
  ["Core Features", "coreFeatures"],
  ["Advanced Features", "advancedFeatures"],
  ["AI / ML Integration", "aiIntegration"],
  ["Suggested Tech Stack", "techStack"],
  ["Database Design", "databaseDesign"],
  ["API Route Ideas", "apiRoutes"],
  ["UI Pages", "uiPages"],
  ["MVP Plan", "mvpPlan"],
  ["Future Scope", "futureScope"],
  ["Portfolio Value", "portfolioValue"],
  ["Possible Monetization", "monetization"],
  ["Learning Outcomes", "learningOutcomes"],
  ["Real-World Impact", "realWorldImpact"],
  ["Dataset Idea", "datasetIdea"],
  ["Final Showcase", "showcase"],
] as const;

export type IdeaSection = {
  title: string;
  markdown: string;
};

export type Idea = {
  id: string;
  title: string;
  collection: string;
  collectionLabel: string;
  folder: string;
  folderLabel: string;
  categoryText: string;
  date: string;
  difficulty: string;
  slug: string;
  path: string;
  shortDescription: string;
  body: string;
  sections: IdeaSection[];
};

export type IdeaCatalog = {
  generatedAt: string;
  totalProjects: number;
  collections: Record<string, number>;
  folders: Record<string, number>;
  projects: Idea[];
};

function headingKey(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "");
}

function slugToLabel(value: string) {
  if (FOLDER_LABELS[value]) {
    return FOLDER_LABELS[value];
  }
  return value
    .split("-")
    .map((part) => (part === "ai" ? "AI" : part.charAt(0).toUpperCase() + part.slice(1)))
    .join(" ");
}

function repairText(value: string) {
  return value.replace(/^\uFEFF/, "");
}

function splitMarkdownSections(markdown: string) {
  let title = "";
  const sections = new Map<string, string>();
  let currentHeading = "";
  let buffer: string[] = [];

  function flush() {
    if (currentHeading) {
      sections.set(headingKey(currentHeading), buffer.join("\n").trim());
    }
  }

  for (const line of markdown.split(/\r?\n/)) {
    if (line.startsWith("# ")) {
      flush();
      title = line.slice(2).trim();
      currentHeading = "";
      buffer = [];
      continue;
    }
    if (line.startsWith("## ")) {
      flush();
      currentHeading = line.slice(3).trim();
      buffer = [];
      continue;
    }
    if (currentHeading) {
      buffer.push(line);
    }
  }

  flush();
  return { title, sections };
}

function resolveSection(sections: Map<string, string>, aliases: string[]) {
  for (const alias of aliases) {
    const value = sections.get(headingKey(alias));
    if (value) {
      return value.trim();
    }
  }
  return "";
}

async function safeReadDir(target: string) {
  try {
    return await readdir(target, { withFileTypes: true });
  } catch {
    return [];
  }
}

async function collectReadmes() {
  const readmes: ReadmeFile[] = [];
  const root = process.cwd();

  for (const ideaRoot of IDEA_ROOTS) {
    const absoluteDir = path.join(root, ideaRoot.directory);
    const folders = await safeReadDir(absoluteDir);
    for (const folder of folders) {
      if (!folder.isDirectory()) {
        continue;
      }
      const folderPath = path.join(absoluteDir, folder.name);
      const projects = await safeReadDir(folderPath);
      for (const project of projects) {
        if (!project.isDirectory()) {
          continue;
        }
        readmes.push({
          absolutePath: path.join(folderPath, project.name, "README.md"),
          relativePath: `${ideaRoot.base}/${folder.name}/${project.name}/README.md`,
        });
      }
    }
  }

  return readmes.sort((left, right) => left.relativePath.localeCompare(right.relativePath));
}

async function buildIdea(readme: ReadmeFile): Promise<Idea | null> {
  let markdown: string;
  try {
    markdown = repairText(await readFile(readme.absolutePath, "utf8"));
  } catch {
    return null;
  }

  const relativePath = readme.relativePath;
  const parts = relativePath.split("/");
  const [collection, folder, slug] = parts;
  if (!collection || !folder || !slug || parts[3] !== "README.md") {
    return null;
  }

  const { title, sections } = splitMarkdownSections(markdown);
  const categoryText = resolveSection(sections, SECTION_ALIASES.category) || slugToLabel(folder);
  const date = resolveSection(sections, SECTION_ALIASES.date);
  const shortDescription = resolveSection(sections, SECTION_ALIASES.shortDescription);
  const difficulty = resolveSection(sections, SECTION_ALIASES.difficulty) || "Not specified";

  const detailSections = DETAIL_SECTION_ORDER.map(([sectionTitle, key]) => ({
    title: sectionTitle,
    markdown: resolveSection(sections, SECTION_ALIASES[key]),
  })).filter((section) => section.markdown);

  return {
    id: `${collection}/${folder}/${slug}`,
    title: title || slugToLabel(slug),
    collection,
    collectionLabel: COLLECTION_LABELS[collection] || slugToLabel(collection),
    folder,
    folderLabel: slugToLabel(folder),
    categoryText,
    date,
    difficulty,
    slug,
    path: relativePath,
    shortDescription,
    body: markdown,
    sections: detailSections,
  };
}

export async function getIdeas() {
  const readmes = await collectReadmes();
  const ideas = (await Promise.all(readmes.map((readme) => buildIdea(readme)))).filter(
    (idea): idea is Idea => Boolean(idea),
  );

  return ideas.sort((left, right) => {
    const byDate = right.date.localeCompare(left.date);
    if (byDate !== 0) {
      return byDate;
    }
    return left.title.localeCompare(right.title);
  });
}

export async function getIdeaCatalog(): Promise<IdeaCatalog> {
  const projects = await getIdeas();
  const collections: Record<string, number> = {};
  const folders: Record<string, number> = {};

  for (const idea of projects) {
    collections[idea.collectionLabel] = (collections[idea.collectionLabel] || 0) + 1;
    folders[idea.folderLabel] = (folders[idea.folderLabel] || 0) + 1;
  }

  return {
    generatedAt: new Date().toISOString(),
    totalProjects: projects.length,
    collections,
    folders,
    projects,
  };
}
