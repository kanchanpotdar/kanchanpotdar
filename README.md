<div align="center">

![Kanchan Potdar — neon command center](./assets/neon-command-center.svg)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=20&duration=2600&pause=700&color=DAF561&center=true&vCenter=true&repeat=true&width=900&height=45&lines=%3E+training+models...;%3E+engineering+data+systems...;%3E+simulating+uncertainty...;%3E+shipping+reliable+AI...)](https://git.io/typing-svg)

[![Profile Views](https://komarev.com/ghpvc/?username=kanchanpotdar&label=PLAYERS+VISITED&color=DAF561&style=for-the-badge&abbreviated=true)](https://github.com/kanchanpotdar)
[![Followers](https://img.shields.io/github/followers/kanchanpotdar?label=ALLIES&style=for-the-badge&color=DAF561&labelColor=132441)](https://github.com/kanchanpotdar?tab=followers)
[![Repositories](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fusers%2Fkanchanpotdar&query=%24.public_repos&label=QUESTS&style=for-the-badge&color=DAF561&labelColor=132441)](https://github.com/kanchanpotdar?tab=repositories)

</div>

<div align="center">

<h1 align="center">KANCHAN POTDAR</h1>
<p align="center"><b>Applied AI Engineer · ML Researcher · Data Systems Builder</b></p>
<p align="center">IIT Kharagpur · Research at ISI Kolkata</p>
<p align="center"><i>Building AI systems that are grounded, measurable, and reliable.</i></p>

<p align="center">
  <a href="https://www.linkedin.com/in/kanchan-potdar-8b4762289">LinkedIn</a> ·
  <a href="mailto:kanchanpotdar15@gmail.com">Email</a> 
</p>

</div>

---
## `// OPERATOR PROFILE`

| | |
|---|---|
| **Education** | IIT Kharagpur |
| **Research** | Foundation models for prognostics (RUL), at ISI Kolkata under Prof. Tanmay Sen · Bachelor's thesis on low-resource speech recognition (Nyishi) |
| **Builds** | Agentic workflows, RAG, data pipelines, statistical simulation, APIs |
| **Experience** | EY GDS · University of Manchester · IIM Bodh Gaya · IBM |
| **Current focus** | Evaluation-first AI: systems that cite sources, reject what they can't answer, and report negative results honestly |

---

## `// RESEARCH LAB`

### Chronos-2 for Turbofan Remaining-Useful-Life Prediction
**ISI Kolkata** · under Prof. Tanmay Sen · NASA C-MAPSS FD001 · *ongoing*

**Question.** Does parameter-efficient fine-tuning (LoRA, and the Fisher-guided FARSS variant) improve a pretrained time-series foundation model (Amazon Chronos-2, ~120M parameters) at predicting engine remaining useful life, compared with keeping the backbone frozen and training only a small head?

**What I built**
- A Chronos-2 → RUL pipeline: 21 sensors as targets and 3 operating settings as covariates, feeding a temporal-then-sensor attention-pooling head (~102K parameters).
- A leakage-safe protocol: engine-level splits, with asserts that no engine appears in both train and validation.
- A resumable experiment harness covering a 33-run LoRA sweep, 3-fold engine-level cross-validation, and a FARSS re-implementation with numerical checks (adapter output preserved at initialisation).

**Results (100 official test engines)**

| Model | Test RMSE |
|---|--:|
| Mean-RUL baseline | 45.28 |
| Frozen Chronos-2 + mean-pool MLP (first experiment) | 26.21 |
| **Frozen Chronos-2 + temporal/sensor-attention head** | **14.47** (3-fold CV: 14.78 ± 0.43) |
| Best LoRA, single split | 14.95 |
| FARSS vs. uniform-rank control (30 epochs) | 15.83 vs. 15.74 |

**Findings**
- **A controlled negative result.** None of the 33 LoRA configurations nor FARSS beat the frozen baseline. A paired bootstrap over test engines shows the best LoRA runs are statistically indistinguishable from it.
- **Head design mattered more than backbone adaptation.** Moving from a flat head to the attention head cut RMSE by about 4 points.
- **A padding artefact.** Zero-padding the 23 shorter test engines corrupted predictions (RMSE 27.12 vs. 18.21 with native NaN-masking on identical weights).
- **Engineering safeguards.** An idempotent runner for interrupted GPU sessions, and a SHA-256 base-weight check after every adapter unload.

**Scope.** FD001 (single operating condition) only. The degradation-aware objective, multi-condition transfer, compression, and federated tasks are not yet done. These results are not evidence that LoRA fails in general.

---

### Low-Resource Dialect NLP: Awadhi & Bhojpuri
**IBM Research Labs** · May – August 2025

- Built a ~180K-line dialect–English parallel corpus using NLLB-200.
- Fine-tuned **Gemma-2-2B-IT** for translation and summarisation using domain-adaptive pre-training, supervised fine-tuning, and LoRA/QLoRA (Unsloth, 4-bit).
- Result: **+12.4 BLEU** improvement on a held-out set.

**Stack:** Hugging Face Transformers · PEFT (LoRA/QLoRA) · Unsloth · NLLB-200 · Python

### Nyishi Speech Recognition: Data Preparation
**Bachelor's Thesis Project (BTP)** · IIT Kharagpur · *ongoing, no model trained yet* · [`BTP` repo](https://github.com/kanchanpotdar/BTP)

**Question.** For Nyishi (ISO `njz`), a low-resource language of Arunachal Pradesh, is it better to fine-tune a speech model directly on the small dataset, or to go through an intermediate transfer step first? The planned comparison covers SraVaani, OmniASR, MMS, Whisper and IndicConformer, scored by character error rate.

**Current stage: making the data trustworthy before any training.**
- **Audited the public dataset.** Every file was downloaded at a pinned Hugging Face revision and verified against the Hub's size and SHA-256 (71 files OK, 0 bad). The audit found 25.8 h of audio in Dataset A, not the "200+ hours" its card states, and 1,067 clips whose transcript is the literal text `N/A`.
- **Found leakage in the published split.** It is not speaker-disjoint: 57 of 60 speaker IDs occur in more than one split. After merging 60 public IDs into 55 speaker groups, 52 groups still cross splits. Test scores on it would be inflated.
- **Built a versioned, non-destructive pipeline.** Each step writes a new master-table version (39 → 73 columns) and nothing is overwritten. The raw transcript is never modified. Problems become flags, not deleted rows.
- **Normalisation policy.** A 19-rule, reversible policy applied to IPA transcripts, with unconfirmed rules marked provisional pending linguistic review.
- **Automated quality flags.** Hard exclusions (empty or undecodable audio, missing transcript), manual-review signals (duration mismatch, unresolved symbols, suspected code-mixing) and eligibility, all written with SHA-256 provenance.
- **Human review in progress.** A 200-clip listening audit, followed by a speaker-disjoint train/validation/test split.

**Scope.** Dataset A (narration) only so far. Dataset B (YouTube) is untouched. The repository holds code and reports, not the audio or transcripts, because of the dataset's licence.

**Stack:** Python · pandas · PyArrow/Parquet · Hugging Face Hub · Jupyter

---

## `// FIELD OPERATIONS`

<!-- DRAFT: Phase 3. Describes patterns only; no client names or confidential specifics. -->

<details>
<summary><b>EY GDS · Technology Consulting Intern</b> · May – Jul 2026 · enterprise GenAI for IT demand management</summary>

<br>

Four builds, all around one idea: **LLM output that is grounded, validated and reviewed by a human before it affects anything.**

- **Demand Intake Assistant (PoC).** A field-aware assistant for a ~40-field IT demand intake form, exposed as an Azure Function (Python v2) calling GPT-4o. Answers come from a structured field-guidance mapping, and the system prompt forbids inventing dropdown values or rules.
- **ITDM AI Platform.** React + FastAPI + SQLAlchemy with three agents. Duplicate detection embeds demands and shortlists by cosine similarity (>0.60) before asking GPT-4o to reason on the top matches. Prioritisation uses a deterministic six-dimension weighted score (the LLM only writes the rationale). A BRD generator outputs a 14-section document as structured JSON.
- **Task King.** Extracts action items from meeting transcripts into schema-validated JSON (Pydantic), resolves relative deadlines against the call date, and scores each task for quality and duplicates. A reviewer approves each task, and the Azure DevOps step produces a dry-run preview only.
- **Model Router.** A Streamlit tool that discovers Azure OpenAI deployments at runtime via the Management API and logs latency, token usage and a prompt hash per call.

**Stack:** Azure OpenAI (GPT-4o, embeddings) · Azure Functions · FastAPI · Pydantic · React · Streamlit · Python

*Local and PoC builds; not described as production deployments.*

</details>

<details>
<summary><b>University of Manchester · Research Intern (SQUARE Programme)</b> · May – Jul 2026 · low-cost PM2.5 sensor calibration</summary>

<br>

**Question.** Low-cost PM2.5 sensors are cheap to deploy but need calibration against reference monitors. Which ML model calibrates best, and does a calibration transfer to sensors it has never seen?

- **Data engineering.** A hybrid OpenAQ pipeline (AWS S3 archive plus REST API v3, with deduplication) and Haversine pairing of sensors to the nearest reference monitor. A six-stage quality funnel took **72 candidate pairs down to 13 verified pairs** across nine Indian cities (~136,000 paired observations). The funnel also caught **7 government reference monitors mis-registered as low-cost sensors** in the public metadata.
- **Cleaning.** Physical-bounds screening and two-stage gap imputation, validated with three statistical checks. The target variable was never imputed.
- **Modelling.** Seven algorithms (OLS, Ridge, SVR, Random Forest, XGBoost, LightGBM, CatBoost) per sensor with chronological `TimeSeriesSplit`. A pooled CatBoost model with 70 Optuna trials. Ensembles. Leave-one-sensor-out testing. SHAP and partial-dependence explainability.
- **Result.** Network-mean calibration cut MAE from 38.8 to 24.19 µg/m³ (**~38% reduction**).
- **Findings.**
  - No single algorithm was statistically better (overlapping bootstrap CIs).
  - Random vs. chronological splitting gave a 30-point R² gap on the same model, so MAE is the primary metric.
  - Calibration **did not generalise** to unseen sensors (leave-one-sensor-out MAE 42.2 vs. 26.6 for seen sensors), likely due to hardware heterogeneity.

**Stack:** Python · scikit-learn · XGBoost · LightGBM · CatBoost · Optuna · SHAP · GeoPandas · OpenAQ

</details>

<details>
<summary><b>IIM Bodh Gaya · Research Intern</b> · May – Jun 2026 · fingerprint quality and matching</summary>

<br>

- Analysed **24,377 NIST SD302 fingerprint images**, relating **NFIQ2** quality scores to sensor type and demographic/acquisition metadata.
- Built a dependency-free NumPy/OpenCV replacement for the legacy NIST **Bozorth3** matcher, vectorising comparisons for a **~100× speedup**.
- Added a **RANSAC affine-transform** step to compensate for skin deformation, reducing EER from **37.46% to 31.36%**.
- Preprocessing included CLAHE, Gabor filtering, ROI extraction, binarisation and skeletonisation, plus a 2,000-image gold-standard enrolment gallery.

**Stack:** Python · OpenCV · NumPy · pandas

</details>

---

## `// ACTIVE QUESTS`

<table>
<tr>
<td width="50%" valign="top">

### 🧠 Level 04 · Financial Research Agent

Multi-agent LangGraph research pipeline with parallel analysis, bull/bear debate, deterministic scoring, model fallback and a human approval gate.

`LANGGRAPH` `PYDANTIC` `OLLAMA` `STREAMLIT`

[**ENTER QUEST →**](https://github.com/kanchanpotdar/Financial-Research-Agent)

</td>
<td width="50%" valign="top">

### 🏭 Level 04 · OpenAQ Medallion

Auditable Bronze → Silver → Gold PM2.5 pipeline validated on 3.3M measurements with PostgreSQL, reconciliation checks and 201 automated tests.

`PYTHON` `POSTGRESQL` `DOCKER` `PYTEST`

[**ENTER QUEST →**](https://github.com/kanchanpotdar/openaq_medallion)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📚 Level 03 · CFA Level 1 RAG

Fully local hybrid retrieval over CFA Level 1 curriculum PDFs with BGE-M3, Qdrant, cross-encoder reranking, grounded citations and a faithfulness guard.

`RAG` `QDRANT` `FASTAPI` `BGE-M3`

[**ENTER QUEST →**](https://github.com/kanchanpotdar/cfa-rag)

</td>
<td width="50%" valign="top">

### 🏏 Level 03 · Cricket Monte Carlo

Ball-by-ball T20 simulation using Markov transitions and Dirichlet-perturbed variance to estimate win probabilities and score distributions.

`MARKOV CHAINS` `MONTE CARLO` `PANDAS`

[**ENTER QUEST →**](https://github.com/kanchanpotdar/Monte-Carlo-Simulation-of-Cricket-Match-Outcomes)

</td>
</tr>
</table>

<div align="center">

[![Explore all quests](https://img.shields.io/badge/OPEN_QUEST_MAP-EXPLORE_ALL_REPOSITORIES-DAF561?style=for-the-badge&labelColor=132441)](https://github.com/kanchanpotdar?tab=repositories)

</div>

---

## `// SKILL TREE`

<div align="center">

### Core loadout

![Python](https://img.shields.io/badge/Python-132441?style=for-the-badge&logo=python&logoColor=DAF561)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-132441?style=for-the-badge&logo=postgresql&logoColor=DAF561)
![C++](https://img.shields.io/badge/C++-132441?style=for-the-badge&logo=cplusplus&logoColor=DAF561)
![Docker](https://img.shields.io/badge/Docker-132441?style=for-the-badge&logo=docker&logoColor=DAF561)
![Git](https://img.shields.io/badge/Git-132441?style=for-the-badge&logo=git&logoColor=DAF561)

### AI systems

![PyTorch](https://img.shields.io/badge/PyTorch-132441?style=for-the-badge&logo=pytorch&logoColor=DAF561)
![LangChain](https://img.shields.io/badge/LangChain-132441?style=for-the-badge&logo=langchain&logoColor=DAF561)
![FastAPI](https://img.shields.io/badge/FastAPI-132441?style=for-the-badge&logo=fastapi&logoColor=DAF561)
![Qdrant](https://img.shields.io/badge/Qdrant-132441?style=for-the-badge&logo=qdrant&logoColor=DAF561)
![Streamlit](https://img.shields.io/badge/Streamlit-132441?style=for-the-badge&logo=streamlit&logoColor=DAF561)
![Plotly](https://img.shields.io/badge/Plotly-132441?style=for-the-badge&logo=plotly&logoColor=DAF561)

</div>

---

## `// COMBAT STATS`

<div align="center">

<img height="190" src="https://github-readme-stats.vercel.app/api?username=kanchanpotdar&show_icons=true&include_all_commits=true&count_private=true&hide_border=false&border_color=DAF561&bg_color=132441&title_color=DAF561&text_color=F6F8FF&icon_color=DAF561&rank_icon=github" alt="Kanchan's GitHub stats" />
<img height="190" src="https://github-readme-stats.vercel.app/api/top-langs/?username=kanchanpotdar&layout=compact&langs_count=8&hide_border=false&border_color=DAF561&bg_color=132441&title_color=DAF561&text_color=F6F8FF" alt="Kanchan's top languages" />

<img src="https://streak-stats.demolab.com?user=kanchanpotdar&hide_border=false&border=DAF561&background=132441&stroke=DAF561&ring=DAF561&fire=DAF561&currStreakNum=F6F8FF&sideNums=F6F8FF&currStreakLabel=DAF561&sideLabels=DAF561&dates=91A8C6" alt="Kanchan's contribution streak" />

<img width="98%" src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=kanchanpotdar&theme=github_dark&title_color=DAF561&text_color=F6F8FF&bg_color=132441&border_color=DAF561&icon_color=DAF561&chart_color=DAF561&animation=sequence&duration=2" alt="Kanchan's contribution timeline" />

<img height="185" src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=kanchanpotdar&theme=github_dark&utcOffset=5.5&title_color=DAF561&text_color=F6F8FF&bg_color=132441&border_color=DAF561&icon_color=DAF561&chart_color=DAF561&animation=load" alt="Kanchan's productive coding time" />
<img height="185" src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=kanchanpotdar&theme=github_dark&title_color=DAF561&text_color=F6F8FF&bg_color=132441&border_color=DAF561&icon_color=DAF561&chart_color=DAF561&animation=load" alt="Kanchan's repositories by language" />

</div>

---

## `// CONTRIBUTION ARCADE`

<div align="center">

### `STAGE 01 — PAC-MAN`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kanchanpotdar/kanchanpotdar/output/pacman-contribution-graph-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kanchanpotdar/kanchanpotdar/output/pacman-contribution-graph.svg">
  <img alt="Pac-Man running through Kanchan's contribution graph" src="https://raw.githubusercontent.com/kanchanpotdar/kanchanpotdar/output/pacman-contribution-graph-dark.svg">
</picture>

<details>
<summary><b>🎮 LOAD BONUS STAGES</b></summary>
<br>

### `STAGE 02 — SNAKE`

<img src="https://raw.githubusercontent.com/kanchanpotdar/kanchanpotdar/output/neon-snake.svg" alt="Chartreuse snake eating Kanchan's contribution graph" />

### `STAGE 03 — BREAKOUT`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kanchanpotdar/kanchanpotdar/output/breakout-contribution-graph-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kanchanpotdar/kanchanpotdar/output/breakout-contribution-graph.svg">
  <img alt="Breakout playing across Kanchan's contribution graph" src="https://raw.githubusercontent.com/kanchanpotdar/kanchanpotdar/output/breakout-contribution-graph-dark.svg">
</picture>

</details>

</div>

---

## `// ACHIEVEMENT CABINET`

<div align="center">

[![Data Scale](https://img.shields.io/badge/DATA_BOSS-3.3M_ROWS-DAF561?style=for-the-badge&labelColor=132441)](https://github.com/kanchanpotdar/openaq_medallion)
[![Tests](https://img.shields.io/badge/QUALITY_GUARDIAN-201_TESTS-DAF561?style=for-the-badge&labelColor=132441)](https://github.com/kanchanpotdar/openaq_medallion)
[![Local AI](https://img.shields.io/badge/LOCAL_AI-4GB_GPU-DAF561?style=for-the-badge&labelColor=132441)](https://github.com/kanchanpotdar/cfa-rag)
[![Agentic AI](https://img.shields.io/badge/MULTI_AGENT-BULL_VS_BEAR-DAF561?style=for-the-badge&labelColor=132441)](https://github.com/kanchanpotdar/Financial-Research-Agent)

```text
╔═════════════════════════════════════════════════════════════╗
║  MISSION                                                     ║
║  Turn messy data and hard questions into systems that are   ║
║  useful, testable, explainable — and ready for the real world.║
╚═════════════════════════════════════════════════════════════╝
```

[![GitHub](https://img.shields.io/badge/CONNECT_ON_GITHUB-DAF561?style=for-the-badge&logo=github&logoColor=132441)](https://github.com/kanchanpotdar)

<sub>DESIGNED IN <code>#132441</code> MIDNIGHT BLUE × <code>#DAF561</code> CHARTREUSE</sub>

</div>

---

## `// TRANSMIT SIGNAL`

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LINKEDIN-DAF561?style=for-the-badge&logo=linkedin&logoColor=132441)](https://www.linkedin.com/in/kanchan-potdar-8b4762289)
[![Email](https://img.shields.io/badge/EMAIL-DAF561?style=for-the-badge&logo=gmail&logoColor=132441)](mailto:kanchanpotdar15@gmail.com)

</div>
