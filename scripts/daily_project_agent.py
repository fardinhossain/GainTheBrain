#!/usr/bin/env python3
"""Generate, store, commit, and push exactly one unique project idea."""

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
from urllib.parse import urlparse

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
REQUIRED_README_SECTIONS = (
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
)


class AgentError(RuntimeError):
    """A safe, user-facing agent failure."""


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_url: str
    model: str
    git_name: str
    git_email: str
    branch: str
    skip_push: bool


@dataclass(frozen=True)
class ExistingIdea:
    title: str
    slug: str
    path: str
    project_date: str = ""


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


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings() -> Settings:
    required_names = (
        "AI_API_KEY",
        "AI_API_URL",
        "AI_MODEL",
        "GIT_COMMIT_NAME",
        "GIT_COMMIT_EMAIL",
    )
    values = {name: os.getenv(name, "").strip() for name in required_names}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise AgentError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Add them to .env locally or GitHub Actions repository secrets."
        )

    parsed_url = urlparse(values["AI_API_URL"])
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise AgentError("AI_API_URL must be a complete http:// or https:// chat-completions URL")

    branch = os.getenv("GITHUB_BRANCH", "main").strip() or "main"
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", branch) or ".." in branch or branch.startswith("-"):
        raise AgentError(f"Unsafe GITHUB_BRANCH value: {branch}")

    return Settings(
        api_key=values["AI_API_KEY"],
        api_url=values["AI_API_URL"],
        model=values["AI_MODEL"],
        git_name=values["GIT_COMMIT_NAME"],
        git_email=values["GIT_COMMIT_EMAIL"],
        branch=branch,
        skip_push=env_flag("SKIP_GIT_PUSH"),
    )


def run_command(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    log(f"Running: {' '.join(args)}")
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise AgentError(f"Could not run {args[0]}: {exc}") from exc

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
    log("Ensuring all project category and AI Builders Congress folders exist")
    for category in sorted(PROJECT_CATEGORIES):
        (root / "project-ideas" / category).mkdir(parents=True, exist_ok=True)
    for domain in sorted(AI_BUILDERS_DOMAINS):
        (root / "ai-builders-congress" / domain).mkdir(parents=True, exist_ok=True)


def read_title(readme_path: Path) -> str:
    try:
        for line in readme_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip().startswith("# "):
                return line.strip()[2:].strip()
    except OSError:
        pass
    return readme_path.parent.name.replace("-", " ").title()


def read_markdown_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if stripped.startswith("## "):
                return ""
            if stripped:
                return stripped
    return ""


def read_project_date(readme_path: Path) -> str:
    try:
        markdown = readme_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    value = read_markdown_section(markdown, "## Date")
    return value if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) else ""


def scan_existing_ideas(root: Path) -> list[ExistingIdea]:
    log("Scanning existing titles, slugs, and README.md paths")
    ideas: list[ExistingIdea] = []
    for base_name in ("project-ideas", "ai-builders-congress"):
        for readme in sorted((root / base_name).glob("*/*/README.md")):
            ideas.append(
                ExistingIdea(
                    title=read_title(readme),
                    slug=readme.parent.name,
                    path=readme.relative_to(root).as_posix(),
                    project_date=read_project_date(readme),
                )
            )
    log(f"Found {len(ideas)} existing project ideas")
    return ideas


def clean_json_content(content: str) -> str:
    cleaned = content.strip().lstrip("\ufeff")
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```\s*$", "", cleaned)
    return cleaned.strip()


def parse_json_object(content: str) -> dict[str, Any]:
    cleaned = clean_json_content(content)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        if start < 0:
            raise AgentError("AI response does not contain a JSON object")
        try:
            parsed, _ = json.JSONDecoder().raw_decode(cleaned[start:])
        except json.JSONDecodeError as exc:
            raise AgentError(f"AI response contains invalid JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise AgentError("AI response must be exactly one JSON object, not a list or scalar")
    return parsed


def extract_response_content(body: Any) -> str:
    try:
        message = body["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AgentError("AI_API response is missing choices[0].message") from exc

    parsed = message.get("parsed") if isinstance(message, dict) else None
    if isinstance(parsed, dict):
        return json.dumps(parsed)

    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, str) and content.strip():
        return content
    if isinstance(content, list):
        text_parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and isinstance(block.get("text"), str):
                text_parts.append(block["text"])
        if text_parts:
            return "\n".join(text_parts)
    raise AgentError("AI_API response message has no text content")


def target_base_for(storage_type: str) -> str:
    return "ai-builders-congress" if storage_type == "ai-builders-congress" else "project-ideas"


def ensure_inside_allowed_roots(root: Path, target: Path) -> None:
    resolved = target.resolve()
    allowed = ((root / "project-ideas").resolve(), (root / "ai-builders-congress").resolve())
    if not any(base in resolved.parents for base in allowed):
        raise AgentError(f"Refusing to write outside allowed project folders: {target}")


def normalize_idea(raw: dict[str, Any], root: Path) -> ProjectIdea:
    title = str(raw.get("title", "")).strip()
    storage_type = str(raw.get("storage_type", "")).strip().lower()
    category = str(raw.get("category_or_domain", "")).strip().lower()
    difficulty = str(raw.get("difficulty", "")).strip().title()
    readme = raw.get("readme", "")

    if not title or len(title) > 160:
        raise AgentError("AI response title is missing or longer than 160 characters")
    if storage_type not in VALID_STORAGE_TYPES:
        raise AgentError(f"Invalid storage_type: {storage_type or '<empty>'}")
    valid_folders = AI_BUILDERS_DOMAINS if storage_type == "ai-builders-congress" else PROJECT_CATEGORIES
    if category not in valid_folders:
        raise AgentError(f"Invalid category_or_domain for {storage_type}: {category or '<empty>'}")
    if difficulty not in VALID_DIFFICULTIES:
        raise AgentError(f"Invalid difficulty: {difficulty or '<empty>'}")
    if not isinstance(readme, str) or not readme.strip().startswith("# "):
        raise AgentError("AI response readme must be complete Markdown beginning with '# '")

    missing_sections = [section for section in REQUIRED_README_SECTIONS if section not in readme]
    if missing_sections:
        raise AgentError("README is missing sections: " + ", ".join(missing_sections))

    readme_date = read_markdown_section(readme, "## Date")
    expected_date = date.today().isoformat()
    if readme_date != expected_date:
        raise AgentError(f"README Date must be {expected_date}, received {readme_date or '<empty>'}")

    slug = slugify(str(raw.get("slug", "")).strip() or title, lowercase=True)
    if not slug or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise AgentError("AI response could not be converted to a safe lowercase slug")

    relative_path = Path(target_base_for(storage_type)) / category / slug / "README.md"
    supplied_path = str(raw.get("file_path", "")).strip().replace("\\", "/")
    if supplied_path and supplied_path != relative_path.as_posix():
        log("Ignoring mismatched AI-supplied file_path and using the classified path")

    supplied_folder = str(raw.get("target_folder", "")).strip().replace("\\", "/").rstrip("/")
    if supplied_folder and supplied_folder != relative_path.parent.as_posix():
        log("Ignoring mismatched AI-supplied target_folder and using the classified folder")

    file_path = root / relative_path
    ensure_inside_allowed_roots(root, file_path)
    commit_message = f"Add {category} project idea: {title}"
    return ProjectIdea(
        title=title,
        storage_type=storage_type,
        category_or_domain=category,
        slug=slug,
        file_path=file_path,
        difficulty=difficulty,
        commit_message=commit_message[:200],
        readme=readme.strip() + "\n",
    )


def canonical(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def validate_not_duplicate(idea: ProjectIdea, existing: list[ExistingIdea]) -> None:
    existing_slugs = {item.slug.lower() for item in existing}
    existing_titles = {canonical(item.title) for item in existing if item.title}
    if idea.slug.lower() in existing_slugs:
        raise AgentError(f"Duplicate slug: {idea.slug}")
    if canonical(idea.title) in existing_titles:
        raise AgentError(f"Duplicate title: {idea.title}")
    if idea.file_path.exists():
        raise AgentError(f"Target README.md already exists: {idea.file_path}")


def build_system_prompt() -> str:
    return """You are the GainTheBrain Daily Project Idea Agent.
Return valid JSON only, with exactly one project object and no Markdown fence.
Generate one original, practical, portfolio-worthy project idea.
Never reuse an existing title, slug, or substantially identical concept.
Choose the most accurate allowed folder and produce a detailed, buildable README."""


def build_user_prompt(existing: list[ExistingIdea], previous_error: str = "") -> str:
    existing_payload = [
        {
            "title": idea.title,
            "slug": idea.slug,
            "path": idea.path,
            "date": idea.project_date,
        }
        for idea in existing
    ]
    retry_note = f"\nThe previous response was rejected: {previous_error}\nGenerate a different valid idea." if previous_error else ""
    return f"""Today is {date.today().isoformat()}.

Generate exactly one new project idea for the GainTheBrain archive.{retry_note}

Existing ideas to avoid:
{json.dumps(existing_payload, ensure_ascii=False)}

For storage_type "general", category_or_domain must be one of:
{", ".join(sorted(PROJECT_CATEGORIES))}

Use storage_type "ai-builders-congress" when the idea strongly matches one of:
- foodsphere-ai: food safety, waste, nutrition, restaurants, kitchens, or food supply chains
- healthsphere-ai: healthcare, patients, medicine, hospitals, diagnosis support, or health monitoring
- finsphere-ai: banking, budgeting, fraud, fintech, or transaction analysis
- learnsphere-ai: education, study, exams, courses, or skill development
- climatesphere-ai: climate, disasters, environment, pollution, weather, or carbon
- civicsphere-ai: citizen services, smart cities, government, or community problems
- agrisphere-ai: crops, farmers, soil, irrigation, or smart farming
- industrysphere-ai: factories, manufacturing, maintenance, automation, or production
- commercesphere-ai: e-commerce, retail, recommendations, customers, or seller tools
- infrasphere-ai: roads, bridges, buildings, transport, planning, or construction safety

General classification guidance:
- ai-ml: ML, LLMs, vision, NLP, recommendation, prediction, or AI automation
- full-stack: SaaS, dashboards, marketplaces, management platforms, or complete web apps
- software-engineering: testing, CI/CD, quality, architecture, documentation, or engineering workflows
- web-development: frontend, browser tools, web APIs, or web-only utilities
- mobile-app: Android, iOS, Flutter, React Native, or mobile-first apps
- cybersecurity: security, privacy, authentication, vulnerabilities, phishing, or malware
- data-science: analytics, datasets, visualization, or data pipelines
- cloud-devops: deployment, containers, cloud, monitoring, infrastructure, or DevOps
- iot-embedded: sensors, Arduino, ESP32, robotics, smart devices, or hardware
- blockchain: smart contracts, Web3, dApps, or crypto utilities
- productivity-tools: notes, tasks, routines, time management, or personal workflows
- developer-tools: CLIs, editor extensions, API tools, generators, Git, or debugging tools
- programming-education: teaching code, CS study, exam preparation, or coding practice
- general-cs: only when no other category fits

Return this exact JSON shape:
{{
  "title": "Project title",
  "storage_type": "general or ai-builders-congress",
  "category_or_domain": "exact allowed folder name",
  "target_folder": "classified parent/project-slug",
  "slug": "lowercase-hyphen-project-slug",
  "file_path": "classified parent/project-slug/README.md",
  "difficulty": "Beginner or Intermediate or Advanced",
  "commit_message": "Add category/domain project idea: project title",
  "readme": "Full README.md content in Markdown"
}}

The readme value must include all headings below and meaningful content under every heading:
# Project Title
{chr(10).join(REQUIRED_README_SECTIONS)}
""".strip()


def call_ai_api(settings: Settings, existing: list[ExistingIdea], previous_error: str) -> dict[str, Any]:
    payload = {
        "model": settings.model,
        "messages": [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(existing, previous_error)},
        ],
        "temperature": 0.8,
    }
    headers = {"Authorization": f"Bearer {settings.api_key}", "Content-Type": "application/json"}
    try:
        response = requests.post(settings.api_url, headers=headers, json=payload, timeout=(15, 120))
    except requests.RequestException as exc:
        raise AgentError(f"AI_API network request failed: {exc}") from exc

    if not response.ok:
        detail = response.text.strip().replace(settings.api_key, "[REDACTED]")[:500]
        raise AgentError(f"AI_API returned HTTP {response.status_code}: {detail or 'no error body'}")
    try:
        body = response.json()
    except requests.JSONDecodeError as exc:
        raise AgentError("AI_API returned a non-JSON HTTP response") from exc
    return parse_json_object(extract_response_content(body))


def generate_project_idea(root: Path, settings: Settings, existing: list[ExistingIdea]) -> ProjectIdea:
    previous_error = ""
    for attempt in range(1, 4):
        log(f"Requesting exactly one project idea from AI_API (attempt {attempt}/3)")
        try:
            raw_idea = call_ai_api(settings, existing, previous_error)
            idea = normalize_idea(raw_idea, root)
            validate_not_duplicate(idea, existing)
            return idea
        except AgentError as exc:
            previous_error = str(exc)
            log(f"Attempt {attempt} rejected: {previous_error}")
    raise AgentError(f"Could not generate one valid unique idea after 3 attempts: {previous_error}")


def verify_git_repository(root: Path) -> None:
    result = run_command(["git", "rev-parse", "--show-toplevel"], cwd=root)
    if Path(result.stdout.strip()).resolve() != root.resolve():
        raise AgentError(f"Script is not running at the expected Git repository root: {root}")


def configure_git(root: Path, settings: Settings) -> None:
    run_command(["git", "config", "user.name", settings.git_name], cwd=root)
    run_command(["git", "config", "user.email", settings.git_email], cwd=root)


def write_project_readme(idea: ProjectIdea) -> None:
    log(f"Creating {idea.file_path}")
    idea.file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with idea.file_path.open("x", encoding="utf-8", newline="\n") as file:
            file.write(idea.readme)
    except FileExistsError as exc:
        raise AgentError(f"Refusing to overwrite existing file: {idea.file_path}") from exc


def commit_and_push(root: Path, settings: Settings, idea: ProjectIdea) -> None:
    relative_path = idea.file_path.relative_to(root).as_posix()
    status = run_command(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", relative_path],
        cwd=root,
    )
    if not status.stdout.strip():
        log("No new project file was detected; skipping commit and push")
        return

    run_command(["git", "add", "--", relative_path], cwd=root)
    staged = run_command(["git", "diff", "--cached", "--quiet", "--", relative_path], cwd=root, check=False)
    if staged.returncode == 0:
        log("Nothing was staged; skipping empty commit")
        return
    if staged.returncode != 1:
        raise AgentError("Could not inspect staged project file")

    run_command(["git", "commit", "-m", idea.commit_message, "--", relative_path], cwd=root)
    if settings.skip_push:
        log("SKIP_GIT_PUSH is enabled; the commit was created locally but not pushed")
    else:
        run_command(["git", "push", "origin", f"HEAD:{settings.branch}"], cwd=root)
    log(f"Success: created {relative_path}")
    log(f"Commit message: {idea.commit_message}")


def main() -> int:
    load_dotenv()
    root = repo_root()
    log(f"Repository root: {root}")
    try:
        settings = load_settings()
        verify_git_repository(root)
        configure_git(root, settings)
        create_base_folders(root)
        existing = scan_existing_ideas(root)
        today = date.today().isoformat()
        if any(idea.project_date == today for idea in existing):
            log(f"A project idea already exists for {today}; skipping generation and commit")
            return 0
        idea = generate_project_idea(root, settings, existing)
        write_project_readme(idea)
        commit_and_push(root, settings, idea)
        return 0
    except AgentError as exc:
        print(f"ERROR: {exc}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
