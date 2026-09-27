# Research Sources

These sources informed the 2026-08-21 repository, documentation, product-process, and security redesign.

## Product And Documentation

- [Roadmap.sh Product Design](https://roadmap.sh/): supplied roadmap covering success definition, discovery, problem framing, prioritization, risk, experience design, validation, engineering constraints, launch, scaling, and measurement. The downloaded PDF is retained in private LocalWeave research storage and is not redistributed with the repository.
- [Diátaxis](https://diataxis.fr/): separates tutorials, how-to guides, reference, and explanation according to the reader's need.
- [C4 Model](https://c4model.com/): system-context and container/component views for communicating architecture at appropriate levels.

## Python Project Structure

- [Python Packaging User Guide: src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/): supports an installable `src/` package and prevents accidental imports from the working tree.
- [Python Packaging User Guide: pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/): defines project metadata, supported Python versions, dependencies, optional dependencies, scripts, and licensing.
- [Python Packaging User Guide: packaging projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/): baseline project layout with README, `pyproject.toml`, `src`, and tests.

## Privacy And Secure Development

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html): credentials should not be hardcoded or committed, and access should be minimized and auditable.
- [OWASP LLM Excessive Agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency.html): minimize tool functionality, permissions, and autonomy; avoid open-ended tools; require human approval for high-impact actions.
- [OWASP LLM Improper Output Handling](https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM05_ImproperOutputHandling): treat model output as untrusted and validate it before downstream execution.
- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf): document security requirements and decisions, protect software artifacts, produce well-secured software, and respond to residual vulnerabilities.
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir/): separates user configuration, durable data, state, cache, and runtime files.

## Operational Principles

- [The Twelve-Factor App](https://12factor.net/): explicit dependencies, configuration separated from code, build/run separation, disposability, and logs as operational streams. LocalWeave adopts the relevant principles without pretending a local desktop agent is a cloud service.
