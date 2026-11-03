# smart-internship-match

# Smart Internship Match

## Project Overview

Smart Internship Match is an AI-powered application designed to help students identify internship opportunities that match their skills and professional profiles.

The project uses job offer data, Large Language Models (LLMs), and a skill-matching algorithm to analyze internship opportunities and evaluate their relevance.

## Objectives

- Collect internship offers from the France Travail API.
- Extract technical and soft skills from job descriptions using a local LLM.
- Compare job requirements with a student's skills.
- Calculate a personalized matching score.
- Generate tailored CV paragraphs based on relevant job offers.
- Display matching results through an interactive dashboard.

## Project Architecture

```text
smart-internship-match/
├── .github/workflows/
├── data/
│   ├── profile/
│   └── offers/
├── scripts/
│   ├── fetch_offers.py
│   ├── extract_offers.py
│   ├── match_offers.py
│   └── draft_cv.py
├── output/cv_drafts/
├── docs/
│   ├── index.html
│   └── data/
└── README.md
```

## Technologies

- Python
- France Travail API
- Ollama
- Qwen3 8B
- GitHub Actions
- HTML, CSS and JavaScript

## Workflow

1. Fetch internship offers.
2. Extract skills using an LLM.
3. Match offers with the student's profile.
4. Calculate matching KPIs.
5. Generate tailored CV content.
6. Visualize results in a dashboard.

## Privacy

Personal profiles, raw offers and generated CV drafts must remain private. Only filtered and publishable matching results may be exposed through the dashboard.
