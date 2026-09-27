# Repository development instructions

MessMind is a learner-friendly Python project built one tested milestone at a time.

- Read `ROADMAP.md` and `progress.json` before daily work. Implement the next incomplete milestone; keep the UI, changelog and progress file aligned.
- Prefer small, readable Python modules and standard-library solutions. Keep Streamlit presentation separate from calculations and persistence.
- Use Python 3.12 and the dependencies in `requirements.txt`. Document dependency changes.
- Run `python -m unittest discover -s tests -v` before publishing code. Verify meaningful acceptance criteria, not only implementation details.
- Test storage using temporary databases. Never overwrite or commit a user's real meal database.
- Preserve validation, demo isolation, explicit shortage accounting and weighted metrics.
- Keep synthetic evidence labelled. Do not invent model accuracy, avoided waste, savings, citations or test results.
- Do not force-push, erase unrelated changes, add paid services or deploy the app without an explicit request.
- If a milestone is blocked, report the blocker and retain the existing completion state.
