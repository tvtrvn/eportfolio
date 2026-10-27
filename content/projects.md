title: Projects
nav: Projects
eyebrow: E — Projects
description: Selected software projects by Thinh Tran, tagged with the undergraduate competencies they demonstrate.
---
# Projects

<p class="lede">Selected work, each tagged with the undergraduate competencies it demonstrates.</p>

<div class="card" markdown="1">
### AI Workflow System, built on Claude Code

The project I'm proudest of. It makes me feel like I can take on anything, and it keeps me caught up with a field that changes every week.

A personal AI system I designed and direct. Its core is a job-application pipeline of 14 custom skills that analyzes a posting, tailors a resume, and fact-checks every claim against a verified record of my own experience. If the audit finds a claim it can't trace to evidence, the pipeline refuses to package the application. Hooks and a file-based memory carry rules and project state between sessions, and scheduled agents keep an application tracker up to date.

<p class="stack">Claude Code · custom skills · hooks · scheduled agents · Python</p>
<p class="links">Private repository, walkthrough available on request.</p>

<ul class="tags"><li>Critical Thinking and Problem Solving</li><li>Initiative and Entrepreneurship</li><li>Curiosity and Imagination</li></ul>

**Why these tags:** the fact-check gate is a design decision about how the system should fail; I started it and built it on my own; and I keep extending it as the tools change.
</div>

<div class="card" markdown="1">
### Pho Ginger Online Ordering Platform

A production ordering platform for a Toronto restaurant: a customer storefront and a private staff dashboard, built and maintained by me as the sole developer. It includes a self-serve menu manager so the owner can make changes without a developer, and it serves real customers every day.

<p class="stack">Next.js · React · TypeScript · MongoDB · Prisma · Redis · Vercel · Playwright</p>
<p class="links"><a href="https://gingercuisine.ca">Live site</a> · <a href="https://github.com/tvtrvn/gingercuisine-app">Code on GitHub</a></p>

<ul class="tags"><li>Effective Oral and Written Communication</li><li>Initiative and Entrepreneurship</li><li>Critical Thinking and Problem Solving</li></ul>

**Why these tags:** I turned a non-technical owner's needs into a written requirements document; it's real software that a business depends on, built and maintained by me as the sole developer; and I designed the whole system.
</div>

<div class="card" markdown="1">
### Portfolio Analytics Dashboard

A full-stack analytics platform for four simulated investment portfolios. A NumPy engine computes 11 financial metrics from first principles (including Sharpe ratio, maximum drawdown, beta and value at risk), served through 18 REST endpoints over an 8-table PostgreSQL schema.

<p class="stack">React · TypeScript · Redux Toolkit · Python · FastAPI · PostgreSQL · NumPy</p>
<p class="links"><a href="https://github.com/tvtrvn/portfolio-analytics-dashboard">Code on GitHub</a></p>

<ul class="tags"><li>Accessing and Analyzing Information</li><li>Critical Thinking and Problem Solving</li></ul>

**Why these tags:** every metric is implemented from its mathematical definition rather than a library call, and the data model came from working out which questions the dashboard has to answer.
</div>

<div class="card" markdown="1">
### Historical Trade Scenario Simulator

A simulator for "what if I had invested" questions: lump-sum and dollar-cost-averaging scenarios with benchmark comparisons, drawdown charts and a trade ledger. Market data falls back through three sources so it keeps working when a provider fails, and 76 automated tests cover the finance logic, security and data providers.

<p class="stack">React · TypeScript · Python · FastAPI · PostgreSQL · Docker · GitHub Actions</p>
<p class="links"><a href="https://historical-trade-sim.vercel.app">Live site</a> · <a href="https://github.com/tvtrvn/historical-trade-sim">Code on GitHub</a></p>

<ul class="tags"><li>Critical Thinking and Problem Solving</li><li>Accessing and Analyzing Information</li></ul>

**Why these tags:** the fallback chain was designed around how real data providers fail, and the test suite is how I prove the numbers are right.
</div>

