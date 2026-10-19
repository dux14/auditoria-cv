# AI engineer CV skeleton (English, single column)

Single column. No tables for layout, text boxes, icons, skill bars or photo. Nothing in
header or footer (contact lives in the body). Standard system font, 10-12 pt. 1 page
(2 only if the second page is at least half full and relevant). Reverse-chronological.
Section order: header, summary, skills, experience, selected projects, education, links.
Every number and tool below must map to the evidence register or be marked USER-ATTESTED.
All `<...>` are placeholders: fill with real data or delete the line. No invented numbers.

---

FIRST LAST
`<Target title: e.g. AI Quality / Agent Evaluation Engineer | Applied AI Engineer>`
City, Country | email@domain.com | +00 000 000 0000 | linkedin.com/in/`<handle>` | github.com/`<handle>`
`<Optional, if relevant: Open to relocation to <country> | Work authorization: <honest statement>>`

SUMMARY
`<Target title>` with `<X>` years in `<domain>`. `<Core stack named exactly as in the target postings>`. `<One verifiable proof: shipped artifact + how it was measured>`.

SKILLS
Agents & tool use: `<MCP, tool schemas, agent SDK / framework>`
Evals & quality: `<pytest, Playwright, eval framework, LLM-as-judge, golden datasets>`
Languages: `<Python, TypeScript>`
CI / Infra / Observability: `<GitHub Actions, tracing tool, Docker>`
(Only tools you can explain in two minutes without an IDE.)

EXPERIENCE

Job Title (as the employer granted it) | Company | City | Mon YYYY - Mon YYYY
- `<Verb>` + `<artifact you owned>` + `<how it was measured: dataset / grader / gate>` + `<before -> after, verified or attested>` + `<stack>`
- `<Agent-assisted workflow: what the agent does, what a human reviews, which gates block merges>`
- `<QA-to-eval translation: regression suite -> regression evals, flaky tests -> non-determinism handling, triage -> failure taxonomy>`

Job Title | Company | City | Mon YYYY - Mon YYYY
- ...

SELECTED PROJECTS
`<Project name>` | `<repo URL>` | `<live demo or one-command run>`
- Problem, key design decision, eval result, failure cases found. `<2-3 projects max>`

EDUCATION
`<Degree>` | `<Institution>` | `<Year or "expected Mon YYYY">`

CERTIFICATIONS (optional; one line, only if held and relevant)
`<Exact name>` | `<Issuer>` | `<Year>`

LANGUAGES
`<Language (level, certificate if any)>`

LINKS
`<GitHub>` | `<write-up on an eval or MCP design>` | `<portfolio>` (plain-text URLs)

---

Export notes:
- Build a real DOCX, then export the PDF from it. Open the PDF, select all, copy: if the
  text does not copy, an ATS cannot read it either. Never export as an image.
- Run `python3 scripts/parse_check.py CV.pdf` and read the `.ats.txt`.
- File name: `First-Last-Role.pdf`.
- No hidden text, ever. Do not claim a title the employer did not grant.
