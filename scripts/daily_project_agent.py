#!/usr/bin/env python3
"""Daily project idea generator for GainTheBrain.

The agent creates exactly one original project idea, stores it in the correct
repository folder, and commits/pushes only when a new README.md was written.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from slugify import slugify


PROJECT_CATEGORIES = {
    "general-cs",
    "ai-ml",
    "full-stack",
    "software-engineering",
    "web-development",
    "mobile-app",
    "cybersecurity",
    "data-science",
    "cloud-devops",
    "iot-embedded",
    "blockchain",
    "productivity-tools",
    "developer-tools",
    "programming-education",
}

AI_BUILDERS_DOMAINS = {
    "foodsphere-ai",
    "healthsphere-ai",
    "finsphere-ai",
    "learnsphere-ai",
    "climatesphere-ai",
    "civicsphere-ai",
    "agrisphere-ai",
    "industrysphere-ai",
    "commercesphere-ai",
    "infrasphere-ai",
}

VALID_STORAGE_TYPES = {"general", "ai-builders-congress"}
VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}
REQUIRED_README_SECTIONS = [
    "## Category / Domain",
    "## Date",
    "## Short Description",
    "## Problem Statement",
    "## Proposed Solution",
    "## Target Users",
    "## Core Features",
    "## Advanced Features",
    "## AI/ML Integration",
    "## Suggested Tech Stack",
    "## Database Design",
    "## API Route Ideas",
    "## UI Pages",
    "## MVP Plan",
    "## Future Scope",
    "## Difficulty Level",
    "## Portfolio Value",
    "## Possible Monetization",
    "## Learning Outcomes",
]


class AgentError(RuntimeError):
    """Raised when the agent cannot safely complete its run."""


@dataclass(frozen=True)
class ExistingIdea:
    title: str
    slug: str
    path: str


@dataclass(frozen=True)
class ProjectIdea:
    title: str
    storage_type: str
    category_or_domain: str
    slug: str
    file_path: Path
    difficulty: str
    commit_message: str
    readme: str


def log(message: str) -> None:
    print(f"[daily-project-agent] {message}", flush=True)


def run_command(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a command with clear logging while keeping secrets out of output."""
    log(f"Running: {' '.join(args)}")
    result = subprocess.run(
        args,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    if check and result.returncode != 0:
        raise AgentError(f"Command failed with exit code {result.returncode}: {' '.join(args)}")
    return result


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def create_base_folders(root: Path) -> None:
    log("Ensuring base folders exist")
    for category in sorted(PROJECT_CATEGORIES):
        (root / "project-ideas" / category).mkdir(parents=True, exist_ok=True)
    for domain in sorted(AI_BUILDERS_DOMAINS):
        (root / "ai-builders-congress" / domain).mkdir(parents=True, exist_ok=True)


def read_title(readme_path: Path) -> str:
    try:
        for line in readme_path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    except OSError:
        return ""
    return readme_path.parent.name.replace("-", " ").title()


def scan_existing_ideas(root: Path) -> list[ExistingIdea]:
    log("Scanning existing project README.md files")
    ideas: list[ExistingIdea] = []
    for base_name in ("project-ideas", "ai-builders-congress"):
        base = root / base_name
        if not base.exists():
            continue
        for readme in sorted(base.glob("*/*/README.md")):
            ideas.append(
                ExistingIdea(
                    title=read_title(readme),
                    slug=readme.parent.name,
                    path=str(readme.relative_to(root)).replace("\\", "/"),
                )
            )
    log(f"Found {len(ideas)} existing project ideas")
    return ideas


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise AgentError(f"Missing required environment variable: {name}")
    return value


def clean_json_content(content: str) -> str:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def target_base_for(storage_type: str) -> str:
    return "ai-builders-congress" if storage_type == "ai-builders-congress" else "project-ideas"


def is_safe_relative_path(path: Path) -> bool:
    return not path.is_absolute() and ".." not in path.parts


def ensure_inside_allowed_roots(root: Path, target: Path) -> None:
    resolved = target.resolve()
    allowed_roots = [
        (root / "project-ideas").resolve(),
        (root / "ai-builders-congress").resolve(),
    ]
    if not any(resolved == allowed or allowed in resolved.parents for allowed in allowed_roots):
        raise AgentError(f"Refusing to write outside allowed content roots: {target}")


def normalize_idea(raw: dict[str, Any], root: Path) -> ProjectIdea:
    title = str(raw.get("title", "")).strip()
    storage_type = str(raw.get("storage_type", "")).strip()
    category_or_domain = str(raw.get("category_or_domain", "")).strip()
    raw_slug = str(raw.get("slug", "")).strip()
    difficulty = str(raw.get("difficulty", "")).strip()
    commit_message = str(raw.get("commit_message", "")).strip()
    readme = str(raw.get("readme", "")).strip()

    if not title:
        raise AgentError("AI response is missing title")
    if storage_type not in VALID_STORAGE_TYPES:
        raise AgentError(f"Invalid storage_type: {storage_type}")

    valid_folders = AI_BUILDERS_DOMAINS if storage_type == "ai-builders-congress" else PROJECT_CATEGORIES
    if category_or_domain not in valid_folders:
        raise AgentError(f"Invalid category_or_domain for {storage_type}: {category_or_domain}")

    slug = slugify(raw_slug or title)
    if not slug or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise AgentError(f"Invalid slug after sanitization: {raw_slug}")

    if difficulty not in VALID_DIFFICULTIES:
        raise AgentError(f"Invalid difficulty: {difficulty}")

    if not readme or not readme.startswith("# "):
        raise AgentError("AI response readme must be full Markdown beginning with '# '")
    missing_sections = [section for section in REQUIRED_README_SECTIONS if section not in readme]
    if missing_sections:
        raise AgentError(f"README is missing required sections: {', '.join(missing_sections)}")

    base = target_base_for(storage_type)
    generated_relative = Path(base) / category_or_domain / slug / "README.md"
    supplied_file_path = str(raw.get("file_path", "")).strip()
    if supplied_file_path:
        supplied = Path(supplied_file_path.replace("\\", "/"))
        if is_safe_relative_path(supplied) and supplied.as_posix() == generated_relative.as_posix():
            relative_path = supplied
        else:
            log("Ignoring unsafe or mismatched AI-supplied file_path; using generated target path")
            relative_path = generated_relative
    else:
        relative_path = generated_relative

    target_path = root / relative_path
    ensure_inside_allowed_roots(root, target_path)

    if not commit_message:
        commit_message = f"Add {category_or_domain} project idea: {title}"

    return ProjectIdea(
        title=title,
        storage_type=storage_type,
        category_or_domain=category_or_domain,
        slug=slug,
        file_path=target_path,
        difficulty=difficulty,
        commit_message=commit_message,
        readme=readme.rstrip() + "\n",
    )


def build_system_prompt() -> str:
    return """You are the GainTheBrain Daily Project Idea Agent.
Return valid JSON only. Do not wrap the JSON in Markdown.
Generate exactly one original, useful, portfolio-worthy project idea.
Follow the requested schema exactly and write a complete README.md.
Do not duplicate any existing title or slug provided by the user.
Use the classification rules to select storage_type and category_or_domain.
The README must be meaningful, specific, and immediately useful to a builder."""


def build_user_prompt(existing: list[ExistingIdea]) -> str:
    existing_payload = [
        {"title": idea.title, "slug": idea.slug, "path": idea.path}
        for idea in existing
    ]
    return f"""
Today is {date.today().isoformat()}.

Generate exactly one new project idea for the GainTheBrain open-source archive.

Existing project ideas to avoid:
{json.dumps(existing_payload, indent=2, ensure_ascii=False)}

Valid project-ideas folders:
{", ".join(sorted(PROJECT_CATEGORIES))}

Valid AI Builders Congress folders:
{", ".join(sorted(AI_BUILDERS_DOMAINS))}

AI Builders Congress domain rules:
- foodsphere-ai: food safety, food waste, nutrition, restaurant, food delivery, smart kitchen, food supply chain.
- healthsphere-ai: healthcare, symptoms, patient care, medicine, hospital, diagnosis support, health monitoring.
- finsphere-ai: finance, banking, budgeting, fraud detection, fintech, transaction analysis.
- learnsphere-ai: education, study assistant, exam preparation, course planning, skill development.
- climatesphere-ai: climate, disaster warning, environment, pollution, weather, carbon tracking.
- civicsphere-ai: citizen service, smart city, public complaint, government service, community problem solving.
- agrisphere-ai: agriculture, crop disease, farmer tools, soil, irrigation, smart farming.
- industrysphere-ai: factory, manufacturing, machine maintenance, industrial automation, production optimization.
- commercesphere-ai: e-commerce, retail, product recommendation, customer behavior, seller tools.
- infrasphere-ai: roads, bridges, buildings, transport infrastructure, urban planning, construction safety.

General project folder rules:
- ai-ml: AI, ML, LLM, computer vision, NLP, recommendation, prediction, automation.
- full-stack: SaaS, dashboard, marketplace, management platform, CRUD app, complete frontend + backend app.
- software-engineering: testing, debugging, CI/CD, code quality, architecture, documentation, engineering workflow.
- web-development: websites, frontend UI, web APIs, browser tools, web-based tools.
- mobile-app: Android, iOS, Flutter, React Native, mobile-first apps.
- cybersecurity: security, privacy, authentication, vulnerability detection, phishing detection, malware detection, secure coding.
- data-science: analytics, datasets, visualization, dashboards, data pipelines.
- cloud-devops: deployment, Docker, Kubernetes, serverless, cloud, monitoring, infrastructure, DevOps.
- iot-embedded: sensors, Arduino, ESP32, robotics, smart devices, hardware.
- blockchain: blockchain, smart contracts, Web3, dApps, crypto utilities.
- productivity-tools: routine, notes, tasks, link sharing, time management, workflow.
- developer-tools: CLI, VS Code extension, API tester, code generator, Git helper, debugging helper.
- programming-education: teaching programming, learning CS, exam preparation, code practice, student learning.
- general-cs: use only if nothing else matches.

Return JSON with this exact schema:
{{
  "title": "Project title",
  "storage_type": "general or ai-builders-congress",
  "category_or_domain": "exact folder name",
  "target_folder": "folder path where project should be saved",
  "slug": "lowercase-hyphen-project-slug",
  "file_path": "full README.md path",
  "difficulty": "Beginner or Intermediate or Advanced",
  "commit_message": "Add category/domain project idea: project title",
  "readme": "Full README.md content in Markdown"
}}

The README must include these headings:
# Project Title
## Category / Domain
## Date
## Short Description
## Problem Statement
## Proposed Solution
## Target Users
## Core Features
## Advanced Features
## AI/ML Integration
## Suggested Tech Stack
## Database Design
## API Route Ideas
## UI Pages
## MVP Plan
## Future Scope
## Difficulty Level
## Portfolio Value
## Possible Monetization
## Learning Outcomes
""".strip()


def call_ai_api(api_url: str, api_key: str, model: str, existing: list[ExistingIdea]) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(existing)},
        ],
        "temperature": 0.8,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(api_url, headers=headers, json=payload, timeout=90)
    if response.status_code >= 400:
        raise AgentError(f"AI_API request failed with HTTP {response.status_code}: {response.text[:500]}")
    try:
        body = response.json()
        content = body["choices"][0]["message"]["content"]
        return json.loads(clean_json_content(content))
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise AgentError(f"AI_API response did not contain valid JSON project data: {exc}") from exc


def validate_not_duplicate(idea: ProjectIdea, existing: list[ExistingIdea]) -> None:
    existing_slugs = {item.slug.lower() for item in existing}
    existing_titles = {item.title.strip().lower() for item in existing if item.title}
    if idea.slug.lower() in existing_slugs:
        raise AgentError(f"Duplicate slug: {idea.slug}")
    if idea.title.strip().lower() in existing_titles:
        raise AgentError(f"Duplicate title: {idea.title}")
    if idea.file_path.exists():
        raise AgentError(f"Target README.md already exists: {idea.file_path}")


def generate_project_idea(root: Path, existing: list[ExistingIdea]) -> ProjectIdea:
    api_key = require_env("AI_API_KEY")
    api_url = require_env("AI_API_URL")
    model = require_env("AI_MODEL")

    last_error: Exception | None = None
    for attempt in range(1, 4):
        log(f"Requesting project idea from AI_API, attempt {attempt}/3")
        try:
            raw_idea = call_ai_api(api_url, api_key, model, existing)
            idea = normalize_idea(raw_idea, root)
            validate_not_duplicate(idea, existing)
            return idea
        except Exception as exc:  # retries intentionally cover invalid JSON and duplicate ideas
            last_error = exc
            log(f"Attempt {attempt} failed: {exc}")
    raise AgentError(f"Unable to generate a valid unique project idea after 3 attempts: {last_error}")


def write_project_readme(idea: ProjectIdea) -> None:
    log(f"Writing new project README: {idea.file_path}")
    idea.file_path.parent.mkdir(parents=True, exist_ok=True)
    if idea.file_path.exists():
        raise AgentError(f"Refusing to overwrite existing file: {idea.file_path}")
    idea.file_path.write_text(idea.readme, encoding="utf-8")


def configure_git(root: Path) -> None:
    name = require_env("GIT_COMMIT_NAME")
    email = require_env("GIT_COMMIT_EMAIL")
    run_command(["git", "config", "user.name", name], cwd=root)
    run_command(["git", "config", "user.email", email], cwd=root)


def git_has_changes(root: Path, path: Path) -> bool:
    relative_path = str(path.relative_to(root)).replace("\\", "/")
    result = run_command(["git", "status", "--porcelain", "--", relative_path], cwd=root)
    return bool(result.stdout.strip())


def commit_and_push(root: Path, idea: ProjectIdea) -> None:
    branch = os.getenv("GITHUB_BRANCH", "main").strip() or "main"
    relative_path = str(idea.file_path.relative_to(root)).replace("\\", "/")

    run_command(["git", "status", "--short"], cwd=root)
    if not git_has_changes(root, idea.file_path):
        log("No new file changes detected; skipping commit and push")
        return

    configure_git(root)
    run_command(["git", "add", "--", relative_path], cwd=root)
    run_command(["git", "commit", "-m", idea.commit_message], cwd=root)
    run_command(["git", "push", "origin", f"HEAD:{branch}"], cwd=root)
    log(f"Success: created {relative_path}")
    log(f"Commit message: {idea.commit_message}")


def main() -> int:
    load_dotenv()
    root = repo_root()
    log(f"Repository root: {root}")

    try:
        create_base_folders(root)
        existing = scan_existing_ideas(root)
        idea = generate_project_idea(root, existing)
        write_project_readme(idea)
        commit_and_push(root, idea)
        return 0
    except AgentError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
