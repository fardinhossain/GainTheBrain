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

OFFLINE_IDEA_BANK = [
    {
        "title": "Local API Contract Drift Monitor",
        "storage_type": "general",
        "category_or_domain": "developer-tools",
        "difficulty": "Intermediate",
        "summary": "A CLI tool that compares saved OpenAPI snapshots against current local services and reports breaking API changes before they reach production.",
        "problem": "Small teams often change backend routes, request bodies, or response schemas without realizing that frontend apps, SDKs, or partner integrations depend on the old contract. Online API platforms can help, but developers also need a local-first workflow that works during offline development, hackathons, or restricted network environments.",
        "solution": "Build a local CLI that stores OpenAPI or JSON Schema snapshots in the repository, probes a running local API, compares the live schema against the baseline, and produces a human-readable drift report with severity levels. The tool can also generate Markdown changelogs for pull requests.",
        "users": "Backend developers, full-stack teams, API maintainers, QA engineers, and students learning API design.",
        "features": [
            "Snapshot and compare OpenAPI specifications",
            "Detect removed routes, changed status codes, renamed fields, and type changes",
            "Generate Markdown drift reports for commits or pull requests",
            "Support local mock servers and exported schema files",
            "Provide configurable rules for breaking versus non-breaking changes",
        ],
        "advanced": [
            "SDK compatibility scoring for TypeScript and Python clients",
            "Git hook integration before commit or push",
            "Offline HTML report with route-level diff visualization",
            "Schema history timeline for long-running projects",
        ],
        "tech_stack": "Python, Typer, Rich, jsonschema, pydantic, SQLite, pytest",
    },
    {
        "title": "Offline Study Path Generator",
        "storage_type": "general",
        "category_or_domain": "programming-education",
        "difficulty": "Beginner",
        "summary": "A local study planner that turns a programming topic into a structured roadmap using bundled curriculum templates instead of internet access.",
        "problem": "Students do not always have reliable internet, and many online learning paths are too broad or distracting. A focused offline planner can help learners choose what to study next, track progress, and practice consistently.",
        "solution": "Build a desktop or CLI app with local curriculum templates for topics like Python, data structures, web development, and databases. The app generates weekly plans, practice tasks, checkpoint quizzes, and project suggestions from local JSON files.",
        "users": "CS students, bootcamp learners, teachers, self-taught developers, and coding club mentors.",
        "features": [
            "Generate weekly study plans from local templates",
            "Track completed lessons, quizzes, and mini-projects",
            "Export progress reports as Markdown",
            "Support beginner, intermediate, and advanced tracks",
            "Store all data locally without login",
        ],
        "advanced": [
            "Spaced repetition review calendar",
            "Offline code challenge packs",
            "Teacher mode for assigning roadmaps to a class",
            "Import/export curriculum packs as JSON",
        ],
        "tech_stack": "Python, Textual or Tkinter, SQLite, Markdown, pytest",
    },
    {
        "title": "Personal Data Pipeline Sandbox",
        "storage_type": "general",
        "category_or_domain": "data-science",
        "difficulty": "Intermediate",
        "summary": "A local data engineering playground for building, testing, and documenting CSV-to-dashboard pipelines without cloud services.",
        "problem": "New data engineers often struggle to practice realistic pipelines because tutorials depend on cloud accounts, paid warehouses, or large datasets. A local sandbox can teach ingestion, validation, transformation, and visualization with reproducible examples.",
        "solution": "Create a project that ingests local CSV/JSON files, validates them, transforms them into analytical tables, and generates static charts plus a pipeline report. Everything runs from the command line and stores outputs in a local workspace.",
        "users": "Data science students, junior data engineers, analysts, and educators building classroom labs.",
        "features": [
            "Local dataset ingestion from CSV, JSON, and SQLite",
            "Validation rules for missing values, ranges, and schema mismatches",
            "Reusable transformation steps with dependency ordering",
            "Static chart generation and Markdown reporting",
            "Pipeline run history stored locally",
        ],
        "advanced": [
            "Data lineage graph",
            "Great Expectations-style quality checks",
            "Local scheduling with cron or Task Scheduler",
            "Plugin system for custom transformations",
        ],
        "tech_stack": "Python, pandas, DuckDB, SQLite, matplotlib, pytest",
    },
    {
        "title": "Container Readiness Checklist CLI",
        "storage_type": "general",
        "category_or_domain": "cloud-devops",
        "difficulty": "Intermediate",
        "summary": "A command-line checklist that audits Docker projects for common production-readiness issues before deployment.",
        "problem": "Many projects ship containers that work locally but fail in production because of missing health checks, large images, root users, hardcoded secrets, or weak build caching. Developers need a simple offline audit before pushing to CI.",
        "solution": "Build a CLI that scans Dockerfiles, compose files, and project metadata to produce a readiness score with practical fixes. The tool should work without contacting registries or cloud APIs.",
        "users": "Backend developers, DevOps learners, platform teams, and open-source maintainers.",
        "features": [
            "Dockerfile linting for security and image size issues",
            "Compose file checks for ports, volumes, and health checks",
            "Secret-pattern detection in local configuration files",
            "Readiness score with prioritized remediation steps",
            "Markdown report export",
        ],
        "advanced": [
            "Policy packs for different deployment targets",
            "GitHub Actions annotation output",
            "SBOM file detection and validation",
            "Before/after score comparison across commits",
        ],
        "tech_stack": "Python, PyYAML, Rich, pathlib, pytest",
    },
    {
        "title": "Clinic Queue Insight Simulator",
        "storage_type": "ai-builders-congress",
        "category_or_domain": "healthsphere-ai",
        "difficulty": "Intermediate",
        "summary": "An offline simulator that helps small clinics model patient queues, waiting times, and staffing changes before changing operations.",
        "problem": "Clinics often face long waiting times but lack enough historical data or software budget to test operational changes. A local simulator can help staff understand bottlenecks and experiment safely.",
        "solution": "Build a simulation tool where users define doctors, service counters, appointment slots, and walk-in rates. The system generates synthetic patient flows, predicts waiting time distributions, and recommends staffing adjustments.",
        "users": "Clinic administrators, public health students, hospital operations teams, and healthcare hackathon builders.",
        "features": [
            "Synthetic patient arrival and service-time generation",
            "Queue simulation for multiple counters or doctors",
            "Waiting time and utilization dashboards",
            "Scenario comparison for staffing and appointment rules",
            "Offline PDF or Markdown report generation",
        ],
        "advanced": [
            "ML-based wait time prediction from imported historical CSV data",
            "Triage-priority simulation",
            "What-if optimizer for staffing plans",
            "Privacy-first local data storage",
        ],
        "tech_stack": "Python, SimPy, pandas, scikit-learn, Streamlit, SQLite",
    },
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


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


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


def offline_readme(seed: dict[str, Any], title: str) -> str:
    today = date.today().isoformat()
    features = "\n".join(f"- {item}" for item in seed["features"])
    advanced = "\n".join(f"- {item}" for item in seed["advanced"])
    category = seed["category_or_domain"]
    return f"""# {title}

## Category / Domain

{category}

## Date

{today}

## Short Description

{seed["summary"]}

## Problem Statement

{seed["problem"]}

## Proposed Solution

{seed["solution"]}

## Target Users

{seed["users"]}

## Core Features

{features}

## Advanced Features

{advanced}

## AI/ML Integration

- Use lightweight anomaly detection or scoring models where useful, but keep the first version fully functional with deterministic local logic.
- Add optional local ML experiments later using imported CSV data and transparent evaluation metrics.
- Keep all user data local by default so the project remains usable without cloud services.

## Suggested Tech Stack

{seed["tech_stack"]}

## Database Design

| Table | Purpose |
|---|---|
| `projects` | Stores workspace-level project metadata and configuration. |
| `runs` | Tracks each execution, simulation, scan, or generation event. |
| `items` | Stores domain-specific records such as checks, lessons, routes, patients, or datasets. |
| `findings` | Captures generated recommendations, warnings, scores, and report entries. |
| `settings` | Stores local preferences and reusable presets. |

## API Route Ideas

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/health` | Check whether the local service is running. |
| `GET` | `/api/projects` | List local workspaces or project profiles. |
| `POST` | `/api/runs` | Start a new analysis, generation, scan, or simulation. |
| `GET` | `/api/runs/:id` | Read the result of one run. |
| `GET` | `/api/reports/:id` | Export a Markdown or JSON report. |

## UI Pages

1. **Dashboard** - Shows recent runs, key metrics, and next recommended actions.
2. **Workspace Setup** - Lets users configure local files, presets, and project settings.
3. **Run Detail** - Displays findings, warnings, scores, and generated outputs.
4. **History** - Helps users compare previous runs and track improvement over time.
5. **Settings** - Manages local preferences, export paths, and privacy controls.

## MVP Plan

| Phase | Duration | Deliverables |
|---|---|---|
| Phase 1 | Week 1 | CLI workflow, local configuration, and sample data. |
| Phase 2 | Week 2 | Core analysis engine and Markdown report output. |
| Phase 3 | Week 3 | SQLite persistence and history tracking. |
| Phase 4 | Week 4 | Simple UI, tests, documentation, and demo dataset. |

## Future Scope

- Add plugin support for custom rules and domain packs.
- Add richer visual reports for sharing with teams or teachers.
- Add optional cloud sync while keeping offline mode as the default.
- Add import/export bundles so users can move workspaces between machines.

## Difficulty Level

{seed["difficulty"]}

## Portfolio Value

This project demonstrates practical product thinking, local-first architecture, file handling, data modeling, testing, and user-focused reporting. It is strong portfolio material because it solves a real workflow problem without depending on paid services.

## Possible Monetization

- Offer paid domain-specific template packs.
- Provide a hosted collaboration version for teams.
- Sell support, customization, or classroom deployment services.
- Package advanced reporting as a professional edition.

## Learning Outcomes

- Practice building local-first software with clear boundaries.
- Learn how to design useful reports and actionable recommendations.
- Improve skills with Python packaging, testing, and structured data.
- Understand how to turn a narrow technical pain point into a complete product.
"""


def build_offline_raw_idea(existing: list[ExistingIdea]) -> dict[str, Any]:
    existing_slugs = {item.slug.lower() for item in existing}
    existing_titles = {item.title.strip().lower() for item in existing if item.title}
    today = date.today().isoformat()

    for offset in range(len(OFFLINE_IDEA_BANK) * 20):
        seed = OFFLINE_IDEA_BANK[(date.today().toordinal() + len(existing) + offset) % len(OFFLINE_IDEA_BANK)]
        title = seed["title"]
        slug = slugify(title)
        if slug in existing_slugs or title.lower() in existing_titles:
            title = f"{seed['title']} {today}"
            slug = slugify(title)
        if slug in existing_slugs or title.lower() in existing_titles:
            title = f"{seed['title']} Local Build {offset + 1}"
            slug = slugify(title)
        if slug in existing_slugs or title.lower() in existing_titles:
            continue

        base = target_base_for(seed["storage_type"])
        file_path = f"{base}/{seed['category_or_domain']}/{slug}/README.md"
        return {
            "title": title,
            "storage_type": seed["storage_type"],
            "category_or_domain": seed["category_or_domain"],
            "target_folder": f"{base}/{seed['category_or_domain']}/{slug}",
            "slug": slug,
            "file_path": file_path,
            "difficulty": seed["difficulty"],
            "commit_message": f"Add {seed['category_or_domain']} project idea: {title}",
            "readme": offline_readme(seed, title),
        }

    raise AgentError("Offline idea bank could not produce a unique project idea")


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
    if env_flag("OFFLINE_MODE"):
        log("OFFLINE_MODE is enabled; generating project idea without AI_API")
        raw_idea = build_offline_raw_idea(existing)
        idea = normalize_idea(raw_idea, root)
        validate_not_duplicate(idea, existing)
        return idea

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
    if env_flag("OFFLINE_MODE") or env_flag("SKIP_GIT_PUSH"):
        log("Skipping git push because OFFLINE_MODE or SKIP_GIT_PUSH is enabled")
        log(f"Success: created {relative_path}")
        log(f"Commit message: {idea.commit_message}")
        return
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
