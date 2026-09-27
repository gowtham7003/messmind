# Daily development procedure

The requested working style is automatic daily development: implement, test and commit one useful milestone per run. The schedule must be created separately after the new repository is reachable. No automation has been installed by this source package.

Suggested schedule: once each evening around 7 PM Asia/Kolkata. Start with Day 2 on the first scheduled run after repository setup. Finish after Day 14. The run can use the connected GitHub tools or an authorized checkout.

## Run procedure

1. Read the repository's current default branch, `AGENTS.md`, `progress.json`, `ROADMAP.md` and relevant source. Do not rely on an old workspace or a remembered commit.
2. If Day 14 is already complete, make no changes and report completion.
3. Implement the next incomplete milestone. Preserve all user changes. Keep data migrations backward compatible. Use synthetic examples and temporary test databases.
4. Add or update meaningful tests for the milestone's acceptance criteria. Run `python -m unittest discover -s tests -v` and any relevant model evaluation. Capture the outcome honestly.
5. Update the roadmap, progress record, changelog and visible UI progress when the milestone passes. Document what a learner should inspect and how to try the feature.
6. Commit the complete change set with a message such as `feat(day-02): add validated meal editing`. Use a single coherent commit when possible. Before changing a branch ref, verify it has not moved; preserve concurrent changes and never force-push.
7. Return the commit link, the implemented feature, test results, next milestone and any limitation. Do not claim a commit happened until the remote confirms it.

If permissions, dependencies, data or tests block completion, report the blocker. Keep the milestone pending. A failed run must not create an empty commit or mark unfinished work complete.

## Data and modeling expectations

- Record aggregate meal counts only. Do not collect personal diner details.
- Keep database files, credentials, environment files and real imported meal data out of Git.
- Synthetic data is suitable for demos and pipeline tests, not proof of accuracy or operational savings.
- Include unserved requests in demand. Served meals alone underestimate demand when food runs out.
- Use chronological evaluation and ensure features are available before the predicted meal.
- Keep a transparent baseline, especially when data is sparse. Show the number of observations and known limitations.
- Any hosting, paid API, notification to another person, external data transfer or expansion beyond the roadmap requires a separate user request.
