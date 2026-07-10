<div align="center">

# 🧠 GainTheBrain

### *One carefully classified project idea every day*

[![Stars](https://img.shields.io/github/stars/fardinhossain/GainTheBrain?style=for-the-badge&logo=github&color=f5c542)](https://github.com/fardinhossain/GainTheBrain/stargazers)
[![Forks](https://img.shields.io/github/forks/fardinhossain/GainTheBrain?style=for-the-badge&logo=github&color=4287f5)](https://github.com/fardinhossain/GainTheBrain/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](LICENSE)
[![One Project Daily](https://img.shields.io/badge/One_Project-Daily-blueviolet?style=for-the-badge&logo=clockify&logoColor=white)](#-one-project-daily)

<br/>

**A curated, ever-growing collection of project ideas and domain-driven AI blueprints — built for developers, students, and builders who want to sharpen their skills by building.**

<br/>

[Explore Projects](#-project-ideas) · [AI Builders Congress](#-ai-builders-congress) · [Contribute](#-contributing)

---

</div>

---

## Daily Project Idea Agent Setup

This repository includes a Python agent that calls an OpenAI-compatible chat-completions API, generates exactly one unique project idea, saves it under the correct `project-ideas/` or `ai-builders-congress/` folder, and commits only when one new `README.md` is created.

### Local Setup

1. Create a local environment file:

```bash
cp .env.example .env
```

2. Fill in `.env`:

```env
AI_API_KEY=your_api_key
AI_API_URL=https://your-openai-compatible-endpoint/v1/chat/completions
AI_MODEL=your_model_name
GIT_COMMIT_NAME=Fardin Hossain
GIT_COMMIT_EMAIL=iamfardin.swe@gmail.com
GITHUB_BRANCH=main
SKIP_GIT_PUSH=true
```

3. Install dependencies and run:

```bash
pip install -r requirements.txt
python scripts/daily_project_agent.py
```

Local testing creates a real commit but does not push while `SKIP_GIT_PUSH=true`. After checking the generated idea, push it with:

```bash
git push origin main
```

GitHub contribution credit appears only after the commit is pushed to GitHub, and only if `GIT_COMMIT_EMAIL` is verified on your GitHub account.

### GitHub Actions Setup

Add these repository secrets in GitHub under **Settings -> Secrets and variables -> Actions**:

- `AI_API_KEY`
- `AI_API_URL`
- `AI_MODEL`
- `GIT_COMMIT_NAME`
- `GIT_COMMIT_EMAIL`

Set `GIT_COMMIT_NAME` and `GIT_COMMIT_EMAIL` to your GitHub profile name and a GitHub-verified email address. Commits only appear in your GitHub contribution graph when the commit author email is verified on that GitHub account.

The workflow at `.github/workflows/daily-project-agent.yml` runs every day at `03:17 UTC` (`09:17` in Bangladesh) and can also be started manually from the GitHub Actions tab. It validates all five secrets before running, so a configuration problem is named clearly in the job log.

### Troubleshooting a Failed Action

Open the failed run and expand **Validate agent secrets** or **Run daily project idea agent**. Common errors are:

- `Missing GitHub Actions secrets`: add every listed secret under **Settings -> Secrets and variables -> Actions**.
- `HTTP 401` or `HTTP 403`: replace `AI_API_KEY` with a valid key for the configured endpoint.
- `HTTP 404`: set `AI_API_URL` to the full chat-completions endpoint, usually ending in `/v1/chat/completions`.
- `HTTP 429`: the API account has reached a rate or credit limit.
- `Invalid category`, `duplicate`, or `invalid JSON`: the agent retries automatically up to three times.

<br/>

## 📖 What Is GainTheBrain?

**GainTheBrain** is an open-source project-idea archive designed to inspire you to build impactful software.

Whether you're a **Computer Science student** looking for your next capstone idea, a **full-stack developer** hunting for a weekend build, or an **AI enthusiast** eager to tackle a real-world problem — this repo has something for you.

Inside, you'll find:

| What You Get | Why It Matters |
|:---|:---|
| 🛠️ **Project Ideas** | Detailed, actionable project briefs across 14 categories — from AI/ML to IoT |
| 🏛️ **AI Builders Congress** | Domain-specific AI project blueprints organized by real-world industry verticals |

Every idea includes context, suggested tech stacks, difficulty levels, and real-world relevance — so you can go from *"What should I build?"* to *"Let's ship it"* in minutes.

<br/>

---

## 🗂️ Repository Structure

The repository is organized into two project collections. Click any folder to explore.

<br/>

### 🛠️ Project Ideas

> Actionable project briefs spanning beginner to advanced levels, organized by domain.

```
project-ideas/
```

| Folder | Domain | Description |
|:---|:---|:---|
| 📂 [`general-cs/`](project-ideas/general-cs/) | Computer Science | Algorithms, data structures, compilers, OS concepts |
| 📂 [`ai-ml/`](project-ideas/ai-ml/) | AI & Machine Learning | Neural networks, NLP, computer vision, reinforcement learning |
| 📂 [`full-stack/`](project-ideas/full-stack/) | Full-Stack Development | End-to-end apps with modern frontend and backend frameworks |
| 📂 [`software-engineering/`](project-ideas/software-engineering/) | Software Engineering | Design patterns, testing, CI/CD, architecture projects |
| 📂 [`web-development/`](project-ideas/web-development/) | Web Development | Responsive UIs, progressive web apps, browser APIs |
| 📂 [`mobile-app/`](project-ideas/mobile-app/) | Mobile App Development | Cross-platform and native mobile applications |
| 📂 [`cybersecurity/`](project-ideas/cybersecurity/) | Cybersecurity | Ethical hacking tools, encryption, vulnerability scanners |
| 📂 [`data-science/`](project-ideas/data-science/) | Data Science | Analytics dashboards, statistical models, data pipelines |
| 📂 [`cloud-devops/`](project-ideas/cloud-devops/) | Cloud & DevOps | Infrastructure-as-code, container orchestration, monitoring |
| 📂 [`iot-embedded/`](project-ideas/iot-embedded/) | IoT & Embedded Systems | Sensor networks, edge computing, hardware interfaces |
| 📂 [`blockchain/`](project-ideas/blockchain/) | Blockchain | Smart contracts, DeFi protocols, decentralized apps |
| 📂 [`productivity-tools/`](project-ideas/productivity-tools/) | Productivity Tools | Developer utilities, CLI tools, workflow automation |
| 📂 [`developer-tools/`](project-ideas/developer-tools/) | Developer Tools | CLIs, editor extensions, API tools, Git helpers, debugging tools |
| 📂 [`programming-education/`](project-ideas/programming-education/) | Programming Education | Coding practice, CS learning, exam preparation, teaching tools |

<br/>

### 🏛️ AI Builders Congress

> Industry-vertical AI project blueprints — real-world problem spaces where AI can make a tangible difference. Each "sphere" represents a domain of human activity, paired with project ideas that apply AI to solve meaningful challenges.

```
ai-builders-congress/
```

| Folder | Sphere | Focus Area |
|:---|:---|:---|
| 📂 [`foodsphere-ai/`](ai-builders-congress/foodsphere-ai/) | 🍽️ FoodSphere AI | Food supply chains, nutrition analytics, recipe generation |
| 📂 [`healthsphere-ai/`](ai-builders-congress/healthsphere-ai/) | 🏥 HealthSphere AI | Medical imaging, drug discovery, patient analytics |
| 📂 [`finsphere-ai/`](ai-builders-congress/finsphere-ai/) | 💰 FinSphere AI | Fraud detection, algorithmic trading, credit scoring |
| 📂 [`learnsphere-ai/`](ai-builders-congress/learnsphere-ai/) | 📚 LearnSphere AI | Adaptive learning, auto-grading, knowledge graphs |
| 📂 [`climatesphere-ai/`](ai-builders-congress/climatesphere-ai/) | 🌍 ClimateSphere AI | Carbon tracking, climate modeling, renewable energy optimization |
| 📂 [`civicsphere-ai/`](ai-builders-congress/civicsphere-ai/) | 🏛️ CivicSphere AI | Public policy analysis, civic engagement, governance tools |
| 📂 [`agrisphere-ai/`](ai-builders-congress/agrisphere-ai/) | 🌾 AgriSphere AI | Precision agriculture, crop disease detection, yield prediction |
| 📂 [`industrysphere-ai/`](ai-builders-congress/industrysphere-ai/) | 🏭 IndustrySphere AI | Predictive maintenance, quality control, supply chain AI |
| 📂 [`commercesphere-ai/`](ai-builders-congress/commercesphere-ai/) | 🛒 CommerceSphere AI | Recommendation engines, dynamic pricing, customer analytics |
| 📂 [`infrasphere-ai/`](ai-builders-congress/infrasphere-ai/) | 🏗️ InfraSphere AI | Smart cities, traffic optimization, structural health monitoring |

<br/>

---

## 🚀 How to Use This Repo

<table>
<tr>
<td width="60">🔍</td>
<td><strong>Browse by Interest</strong> — Navigate to a category or AI Builders Congress domain and explore its project briefs.</td>
</tr>
<tr>
<td>⭐</td>
<td><strong>Star &amp; Watch</strong> — Star this repo to bookmark it and click <strong>Watch → Custom → Releases</strong> to get notified when new content drops.</td>
</tr>
<tr>
<td>📥</td>
<td><strong>Clone &amp; Build</strong> — Pick a project idea, fork or clone the repo, and start building. Each idea is designed to be self-contained.</td>
</tr>
<tr>
<td>🏛️</td>
<td><strong>Think Big</strong> — Explore the AI Builders Congress for ambitious, industry-grade AI project blueprints.</td>
</tr>
</table>

```bash
# Clone the repository
git clone https://github.com/fardinhossain/GainTheBrain.git

# Open it up and start exploring
cd GainTheBrain
```

<br/>

---

## 🔄 One Project Daily

> [!NOTE]
> This repository adds **exactly one project idea per successful daily agent run**. The idea is saved under its most relevant `project-ideas/` category or `ai-builders-congress/` domain.

If the workflow is re-run after today's project has already been added, the agent exits without generating or committing another one.

Each file is timestamped so you can track what's new. Check back often — or watch the repo for release notifications.

<br/>

---

## 🤝 Contributing

Contributions are welcome and encouraged! Here's how you can help:

1. **🍴 Fork** this repository
2. **🌱 Create** a feature branch (`git checkout -b feature/amazing-idea`)
3. **✍️ Add** your content following the existing folder structure and formatting conventions
4. **📦 Commit** your changes (`git commit -m "Add: new AI/ML project idea"`)
5. **🚀 Push** to your branch (`git push origin feature/amazing-idea`)
6. **🔀 Open** a Pull Request with a clear description of what you've added

**Contribution ideas:**
- Submit a new project idea with a clear problem statement, tech stack, and difficulty level
- Propose a new AI Builders Congress sphere or expand an existing one
- Fix typos, improve formatting, or enhance existing content

> [!TIP]
> Please keep all content original. Use sources for research and inspiration, but write everything in your own words.

<br/>

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute the content in this repository, with attribution.

<br/>

---

<div align="center">

### 💡 *"The best way to predict the future is to build it."*

<br/>

**If this repo helps you learn, build, or stay informed — give it a ⭐**

Made with 🧠 by [Fardin Hossain](https://github.com/fardinhossain) and contributors

<br/>

[![Back to Top](https://img.shields.io/badge/⬆-Back_to_Top-lightgrey?style=flat-square)](#-gainthebrain)

</div>
