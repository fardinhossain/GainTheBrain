"use client";

import {
  ArrowUpDown,
  BrainCircuit,
  CalendarDays,
  FolderTree,
  Loader2,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  Tag,
} from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { MarkdownBlock } from "@/components/MarkdownBlock";
import type { Idea, IdeaCatalog } from "@/lib/ideas";

type IdeaWorkspaceProps = {
  catalog: IdeaCatalog;
};

type AskState = {
  status: "idle" | "loading" | "error" | "success";
  answer: string;
  error: string;
};

type SortKey = "newest" | "oldest" | "title";

const SORT_LABELS: Record<SortKey, string> = {
  newest: "Newest first",
  oldest: "Oldest first",
  title: "Title A-Z",
};

const ASK_HINTS = [
  "Summarize this idea in 3 lines",
  "What should I build first?",
  "What are the biggest risks?",
];

function normalize(value: string) {
  return value.toLowerCase();
}

function searchableText(idea: Idea) {
  return normalize(
    [
      idea.title,
      idea.collectionLabel,
      idea.folderLabel,
      idea.categoryText,
      idea.date,
      idea.difficulty,
      idea.path,
      idea.shortDescription,
      idea.sections.map((section) => `${section.title} ${section.markdown}`).join(" "),
    ].join(" "),
  );
}

export function IdeaWorkspace({ catalog }: IdeaWorkspaceProps) {
  const [query, setQuery] = useState("");
  const [collection, setCollection] = useState("all");
  const [folder, setFolder] = useState("all");
  const [sort, setSort] = useState<SortKey>("newest");
  const [selectedId, setSelectedId] = useState(catalog.projects[0]?.id || "");
  const [question, setQuestion] = useState("");
  const [askState, setAskState] = useState<AskState>({ status: "idle", answer: "", error: "" });

  const readerRef = useRef<HTMLElement | null>(null);
  const entryRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  // Stable log number per idea: oldest entry is #001, newest is the highest.
  const logNumbers = useMemo(() => {
    const map = new Map<string, number>();
    const total = catalog.projects.length;
    catalog.projects.forEach((idea, position) => {
      map.set(idea.id, total - position);
    });
    return map;
  }, [catalog.projects]);

  const latestId = catalog.projects[0]?.id || "";

  const folders = useMemo(() => {
    const values = new Map<string, string>();
    for (const idea of catalog.projects) {
      if (collection !== "all" && idea.collection !== collection) {
        continue;
      }
      values.set(idea.folder, idea.folderLabel);
    }
    return Array.from(values.entries()).sort((left, right) => left[1].localeCompare(right[1]));
  }, [catalog.projects, collection]);

  const filteredProjects = useMemo(() => {
    const search = normalize(query.trim());
    const matched = catalog.projects.filter((idea) => {
      if (collection !== "all" && idea.collection !== collection) {
        return false;
      }
      if (folder !== "all" && idea.folder !== folder) {
        return false;
      }
      return !search || searchableText(idea).includes(search);
    });

    const sorted = [...matched];
    if (sort === "oldest") {
      sorted.reverse();
    } else if (sort === "title") {
      sorted.sort((left, right) => left.title.localeCompare(right.title));
    }
    return sorted;
  }, [catalog.projects, collection, folder, query, sort]);

  const selectedIdea = useMemo(() => {
    return (
      filteredProjects.find((idea) => idea.id === selectedId) ||
      filteredProjects[0] ||
      null
    );
  }, [filteredProjects, selectedId]);

  // Keep a valid selection as filters change.
  useEffect(() => {
    if (selectedIdea && selectedIdea.id !== selectedId) {
      setSelectedId(selectedIdea.id);
    }
  }, [selectedIdea, selectedId]);

  // Reset the assistant whenever the active idea changes.
  useEffect(() => {
    setAskState({ status: "idle", answer: "", error: "" });
    setQuestion("");
  }, [selectedIdea?.id]);

  const latestDate = catalog.projects.find((idea) => idea.date)?.date || "-";
  const collectionOptions: Array<[string, string]> = [
    ["all", "All"],
    ["project-ideas", "Project Ideas"],
    ["ai-builders-congress", "AI Builders Congress"],
  ];

  function chooseCollection(value: string) {
    setCollection(value);
    setFolder("all");
  }

  function selectAndFocus(id: string) {
    setSelectedId(id);
    readerRef.current?.scrollTo({ top: 0, behavior: "smooth" });
  }

  function handleListKey(event: React.KeyboardEvent) {
    if (event.key !== "ArrowDown" && event.key !== "ArrowUp") {
      return;
    }
    event.preventDefault();
    if (!filteredProjects.length) {
      return;
    }
    const currentIndex = filteredProjects.findIndex((idea) => idea.id === selectedIdea?.id);
    const delta = event.key === "ArrowDown" ? 1 : -1;
    const nextIndex = Math.min(
      filteredProjects.length - 1,
      Math.max(0, (currentIndex < 0 ? 0 : currentIndex) + delta),
    );
    const next = filteredProjects[nextIndex];
    if (next) {
      setSelectedId(next.id);
      entryRefs.current[next.id]?.scrollIntoView({ block: "nearest" });
      entryRefs.current[next.id]?.focus();
    }
  }

  async function askAssistant(rawQuestion?: string) {
    const asked = (rawQuestion ?? question).trim();
    if (!asked || !selectedIdea) {
      return;
    }
    setQuestion(asked);
    setAskState({ status: "loading", answer: "", error: "" });
    try {
      const response = await fetch("/api/ideas/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: asked, ideaIds: [selectedIdea.id] }),
      });
      const body = (await response.json()) as { answer?: string; error?: string };
      if (!response.ok) {
        throw new Error(body.error || "The assistant could not answer.");
      }
      setAskState({ status: "success", answer: body.answer || "", error: "" });
    } catch (error) {
      setAskState({
        status: "error",
        answer: "",
        error: error instanceof Error ? error.message : "The assistant could not answer.",
      });
    }
  }

  return (
    <main className="app-shell">
      <header className="masthead">
        <div className="brand-mark">
          <span className="brand-glyph" aria-hidden="true">
            <BrainCircuit />
          </span>
          <div>
            <p className="eyebrow">Daily idea ledger</p>
            <h1>GainTheBrain</h1>
          </div>
        </div>
        <div className="stat-strip">
          <div className="stat">
            <span className="num">{catalog.totalProjects}</span>
            <span className="cap">Ideas logged</span>
          </div>
          <div className="stat">
            <span className="num live">
              <span className="pulse" aria-hidden="true" />
              {latestDate}
            </span>
            <span className="cap">Latest entry</span>
          </div>
          <div className="stat">
            <span className="num">{Object.keys(catalog.folders).length}</span>
            <span className="cap secure">Domains</span>
          </div>
        </div>
      </header>

      <div className="controls">
        <label className="search-box">
          <Search aria-hidden="true" />
          <span className="sr-only">Search ideas</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search titles, problems, features, stacks, domains..."
            type="search"
          />
        </label>
        <div className="sort-box">
          <ArrowUpDown aria-hidden="true" />
          <label htmlFor="sort">Sort</label>
          <select
            id="sort"
            value={sort}
            onChange={(event) => setSort(event.target.value as SortKey)}
          >
            {(Object.keys(SORT_LABELS) as SortKey[]).map((key) => (
              <option key={key} value={key}>
                {SORT_LABELS[key]}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="filters">
        <div className="filter-group">
          <span className="lbl">Collection</span>
          {collectionOptions.map(([value, label]) => (
            <button
              aria-pressed={collection === value}
              className="chip"
              key={value}
              onClick={() => chooseCollection(value)}
              type="button"
            >
              {label}
            </button>
          ))}
        </div>
        <div className="filter-group">
          <span className="lbl">Domain</span>
          <span className="select-inline">
            <FolderTree aria-hidden="true" />
            <span className="sr-only">Filter by domain</span>
            <select value={folder} onChange={(event) => setFolder(event.target.value)}>
              <option value="all">All domains</option>
              {folders.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </span>
        </div>
      </div>

      <div className="workspace">
        <aside className="ledger" aria-label="Idea ledger" onKeyDown={handleListKey}>
          <div className="ledger-head">
            <h2>The ledger</h2>
            <span className="count">
              {filteredProjects.length} / {catalog.totalProjects}
            </span>
          </div>
          <div className="ledger-scroll">
            {filteredProjects.map((idea) => {
              const num = logNumbers.get(idea.id) ?? 0;
              const active = selectedIdea?.id === idea.id;
              const isLatest = idea.id === latestId;
              return (
                <button
                  className={`entry ${active ? "active" : ""}`}
                  key={idea.id}
                  ref={(node) => {
                    entryRefs.current[idea.id] = node;
                  }}
                  onClick={() => selectAndFocus(idea.id)}
                  type="button"
                  aria-current={active ? "true" : undefined}
                >
                  <span className="entry-index" aria-hidden="true">
                    <span className="entry-num">#{String(num).padStart(3, "0")}</span>
                    <span className="entry-tick" />
                  </span>
                  <span className="entry-body">
                    <span className="entry-meta">
                      <span>{idea.date || "Undated"}</span>
                      <span className="dot" />
                      <span>{idea.collectionLabel}</span>
                      {isLatest && (
                        <span className="badge-live">
                          <span className="pulse" />
                          New
                        </span>
                      )}
                    </span>
                    <span className="entry-title">{idea.title}</span>
                    <span className="entry-tag">{idea.folderLabel}</span>
                  </span>
                </button>
              );
            })}
            {!filteredProjects.length && (
              <div className="empty-entry">
                <h3>Nothing matches yet</h3>
                <p>
                  Clear the search or switch domains. New ideas land here each time your
                  agent runs.
                </p>
              </div>
            )}
          </div>
        </aside>

        <section className="reader" aria-label="Selected idea" ref={readerRef} tabIndex={-1}>
          {selectedIdea ? (
            <>
              <div className="reader-head">
                <div className="reader-kicker">
                  <span className="mono">
                    #{String(logNumbers.get(selectedIdea.id) ?? 0).padStart(3, "0")}
                  </span>
                  <span className="k-accent">{selectedIdea.collectionLabel}</span>
                  <span>&middot;</span>
                  <span>{selectedIdea.categoryText}</span>
                </div>
                <h2>{selectedIdea.title}</h2>
                <div className="reader-badges">
                  <span>
                    <FolderTree aria-hidden="true" />
                    {selectedIdea.folderLabel}
                  </span>
                  <span>
                    <Tag aria-hidden="true" />
                    {selectedIdea.difficulty}
                  </span>
                  <span>
                    <CalendarDays aria-hidden="true" />
                    {selectedIdea.date || "No date"}
                  </span>
                </div>
                {selectedIdea.shortDescription && (
                  <p className="reader-summary">{selectedIdea.shortDescription}</p>
                )}
              </div>

              <div className="reader-scroll">
                <div className="assistant">
                  <div className="assistant-head">
                    <Sparkles aria-hidden="true" />
                    <div>
                      <h3>Ask about this idea</h3>
                      <p>
                        Runs server-side against this entry only. Your API key stays on the
                        server and never reaches the browser.
                      </p>
                    </div>
                  </div>
                  <div className="ask-row">
                    <input
                      value={question}
                      onChange={(event) => setQuestion(event.target.value)}
                      onKeyDown={(event) => {
                        if (event.key === "Enter") {
                          void askAssistant();
                        }
                      }}
                      placeholder="e.g. Draft a one-week MVP plan"
                      type="text"
                    />
                    <button
                      disabled={askState.status === "loading" || !question.trim()}
                      onClick={() => void askAssistant()}
                      type="button"
                    >
                      {askState.status === "loading" ? (
                        <Loader2 className="spin" aria-hidden="true" />
                      ) : (
                        <Send aria-hidden="true" />
                      )}
                      Ask
                    </button>
                  </div>
                  <div className="ask-hints">
                    {ASK_HINTS.map((hint) => (
                      <button
                        className="ask-hint"
                        key={hint}
                        onClick={() => void askAssistant(hint)}
                        type="button"
                        disabled={askState.status === "loading"}
                      >
                        {hint}
                      </button>
                    ))}
                  </div>
                  {askState.status === "success" && (
                    <p className="assistant-answer">{askState.answer}</p>
                  )}
                  {askState.status === "error" && (
                    <p className="assistant-error">{askState.error}</p>
                  )}
                </div>

                <div className="section-stack">
                  {selectedIdea.sections.map((section, index) => (
                    <article className="idea-section" key={section.title}>
                      <h3 data-index={String(index + 1).padStart(2, "0")}>{section.title}</h3>
                      <MarkdownBlock markdown={section.markdown} />
                    </article>
                  ))}
                  {!selectedIdea.sections.length && (
                    <article className="idea-section">
                      <p className="assistant-note">
                        This entry has no structured sections yet - the raw brief is still being
                        parsed from its README.
                      </p>
                    </article>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="empty-reader">
              <BrainCircuit aria-hidden="true" />
              <h2>No idea selected</h2>
              <p>
                Pick an entry from the ledger, or clear your filters to bring the archive back
                into view.
              </p>
            </div>
          )}
        </section>
      </div>

      <footer className="app-foot">
        <span>GainTheBrain &middot; private idea reader</span>
        <span className="secure-tag">
          <ShieldCheck aria-hidden="true" />
          AI key kept server-side
        </span>
      </footer>
    </main>
  );
}
