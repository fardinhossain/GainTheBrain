import importlib.util
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "daily_project_agent.py"
SPEC = importlib.util.spec_from_file_location("daily_project_agent", SCRIPT)
agent = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = agent
SPEC.loader.exec_module(agent)


def valid_readme(title="Fresh Idea"):
    sections = "\n\n".join(
        f"{heading}\n\n{date.today().isoformat() if heading == '## Date' else 'Meaningful content.'}"
        for heading in agent.REQUIRED_README_SECTIONS
    )
    return f"# {title}\n\n{sections}\n"


def valid_raw(**changes):
    raw = {
        "title": "Fresh Idea",
        "storage_type": "general",
        "category_or_domain": "developer-tools",
        "target_folder": "project-ideas/developer-tools/fresh-idea",
        "slug": "fresh-idea",
        "file_path": "project-ideas/developer-tools/fresh-idea/README.md",
        "difficulty": "Intermediate",
        "commit_message": "ignored unsafe model message",
        "readme": valid_readme(),
    }
    raw.update(changes)
    return raw


def test_settings():
    return agent.Settings(
        api_key="secret",
        api_url="https://example.test/v1/chat/completions",
        model="test-model",
        git_name="Fardin Hossain",
        git_email="iamfardin.swe@gmail.com",
        branch="main",
        skip_push=False,
    )


class AgentTests(unittest.TestCase):
    def test_parses_fenced_json_object(self):
        parsed = agent.parse_json_object('```json\n{"title": "One"}\n```')
        self.assertEqual(parsed, {"title": "One"})

    def test_rejects_multiple_ideas(self):
        with self.assertRaises(agent.AgentError):
            agent.parse_json_object('[{"title": "One"}, {"title": "Two"}]')

    def test_classifies_path_from_validated_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            idea = agent.normalize_idea(valid_raw(file_path="../../outside/README.md"), root)
            expected = root / "project-ideas" / "developer-tools" / "fresh-idea" / "README.md"
            self.assertEqual(idea.file_path, expected)
            self.assertEqual(idea.commit_message, "Add developer-tools project idea: Fresh Idea")

    def test_ai_builders_congress_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = valid_raw(
                storage_type="ai-builders-congress",
                category_or_domain="agrisphere-ai",
                slug="crop-scout",
                title="Crop Scout",
                readme=valid_readme("Crop Scout"),
            )
            idea = agent.normalize_idea(raw, root)
            self.assertEqual(
                idea.file_path,
                root / "ai-builders-congress" / "agrisphere-ai" / "crop-scout" / "README.md",
            )

    def test_rejects_duplicate_title_after_normalization(self):
        with tempfile.TemporaryDirectory() as directory:
            idea = agent.normalize_idea(valid_raw(), Path(directory))
            existing = [agent.ExistingIdea("Fresh-Idea!", "another-slug", "some/README.md")]
            with self.assertRaises(agent.AgentError):
                agent.validate_not_duplicate(idea, existing)

    def test_exclusive_write_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            idea = agent.normalize_idea(valid_raw(), Path(directory))
            agent.write_project_readme(idea)
            with self.assertRaises(agent.AgentError):
                agent.write_project_readme(idea)

    def test_reads_project_date_for_daily_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(valid_readme(), encoding="utf-8")
            self.assertEqual(agent.read_project_date(readme), date.today().isoformat())

    def test_rejects_readme_with_wrong_date(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = valid_raw(readme=valid_readme().replace(date.today().isoformat(), "2000-01-01"))
            with self.assertRaises(agent.AgentError):
                agent.normalize_idea(raw, Path(directory))

    def test_non_fast_forward_push_rebases_and_retries_once(self):
        rejected = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr="[rejected] non-fast-forward"
        )
        succeeded = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            idea = agent.normalize_idea(valid_raw(), root)
            with patch.object(agent, "run_command", side_effect=[rejected, succeeded, succeeded]) as run:
                with patch.object(agent, "scan_existing_ideas", return_value=[]):
                    self.assertTrue(agent.push_with_rebase_retry(root, test_settings(), idea))
        self.assertEqual(run.call_count, 3)

    def test_free_deepseek_fallback_runs_after_primary_exhausts_retries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            settings = agent.Settings(
                api_key="gemini-key",
                api_url="https://gemini.example/chat/completions",
                model="gemini-model",
                git_name="Fardin Hossain",
                git_email="iamfardin.swe@gmail.com",
                branch="main",
                skip_push=True,
                openrouter_api_key="openrouter-key",
            )
            responses = [
                agent.AgentError("Gemini unavailable"),
                agent.AgentError("Gemini unavailable"),
                agent.AgentError("Gemini unavailable"),
                valid_raw(),
            ]
            with patch.object(agent, "call_ai_api", side_effect=responses) as call:
                idea = agent.generate_project_idea(root, settings, [])
        self.assertEqual(idea.title, "Fresh Idea")
        self.assertEqual(call.call_count, 4)
        self.assertEqual(
            call.call_args_list[-1].kwargs["provider_name"],
            "OpenRouter DeepSeek fallback",
        )
        self.assertEqual(
            call.call_args_list[-1].kwargs["model"],
            "deepseek/deepseek-chat-v3.1:free",
        )

    def test_load_settings_accepts_open_router_api_key_alias(self):
        environment = {
            "AI_API_KEY": "gemini-key",
            "AI_API_URL": "https://gemini.example/chat/completions",
            "AI_MODEL": "gemini-model",
            "GIT_COMMIT_NAME": "Fardin Hossain",
            "GIT_COMMIT_EMAIL": "iamfardin.swe@gmail.com",
            "OPEN_ROUTER_API_KEY": "openrouter-alias-key",
        }
        with patch.dict(agent.os.environ, environment, clear=True):
            settings = agent.load_settings()
        self.assertEqual(settings.openrouter_api_key, "openrouter-alias-key")
        self.assertEqual(
            settings.openrouter_api_url,
            "https://openrouter.ai/api/v1/chat/completions",
        )
        self.assertEqual(
            settings.openrouter_model, "deepseek/deepseek-chat-v3.1:free"
        )

    def test_openai_compatible_response_contract(self):
        class Response:
            ok = True
            status_code = 200
            text = ""

            @staticmethod
            def json():
                import json

                return {"choices": [{"message": {"content": json.dumps(valid_raw())}}]}

        settings = agent.Settings(
            api_key="secret",
            api_url="https://example.test/v1/chat/completions",
            model="test-model",
            git_name="Fardin Hossain",
            git_email="iamfardin.swe@gmail.com",
            branch="main",
            skip_push=True,
        )
        with patch.object(agent.requests, "post", return_value=Response()) as post:
            result = agent.call_ai_api(settings, [], "")
        self.assertEqual(result["title"], "Fresh Idea")
        self.assertEqual(post.call_args.kwargs["json"]["model"], "test-model")

    def test_api_error_redacts_key(self):
        class Response:
            ok = False
            status_code = 401
            text = "invalid key secret-value"

        settings = agent.Settings(
            api_key="secret-value",
            api_url="https://example.test/v1/chat/completions",
            model="test-model",
            git_name="Fardin Hossain",
            git_email="iamfardin.swe@gmail.com",
            branch="main",
            skip_push=True,
        )
        with patch.object(agent.requests, "post", return_value=Response()):
            with self.assertRaises(agent.AgentError) as raised:
                agent.call_ai_api(settings, [], "")
        self.assertNotIn("secret-value", str(raised.exception))
        self.assertIn("[REDACTED]", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
