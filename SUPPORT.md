# Support and Maintenance

Thank you for using **VAP2D (Vessel Analysis Program 2D)**. This document explains
how to get help and what you can expect from the maintainers.

## Getting help

| Need | Where to go |
| --- | --- |
| Report a bug | [Open a Bug report issue](https://github.com/sametkaya/vap2d/issues/new?template=bug_report.md) |
| Request a feature | [Open a Feature request issue](https://github.com/sametkaya/vap2d/issues/new?template=feature_request.md) |
| Usage / general question | Open an issue, or email the maintainer (skaya@fsm.edu.tr) |
| Retraining the deep learning model | See [`docs/RETRAINING.md`](docs/RETRAINING.md) |
| Batch / scripted processing | See [`docs/BATCH_PROCESSING.md`](docs/BATCH_PROCESSING.md) |

Before opening an issue, please:
1. Check the [README](README.md) and the documents in [`docs/`](docs/).
2. Search [existing issues](https://github.com/sametkaya/vap2d/issues?q=) to avoid duplicates.
3. Use the appropriate issue template and fill in the requested details (version,
   OS, installation method, input data, and detection method). Complete reports
   are resolved much faster.

## Maintenance policy

- **Status:** VAP2D is actively maintained as part of an ongoing academic research effort.
- **Maintainer:** Samet Kaya (corresponding author), Department of Computer Engineering,
  Fatih Sultan Mehmet Vakıf University. Contact: skaya@fsm.edu.tr.
- **Issue triage:** New issues are reviewed and labelled, normally within about two weeks.
  Response time may be longer during academic holidays; this is a best-effort, non-commercial
  support commitment.
- **Bug fixes:** Reproducible bugs are prioritised by severity. Please provide the
  information requested in the bug report template so the problem can be reproduced.
- **Releases:** Tagged releases on GitHub are mirrored to DockerHub
  (`sametkaya/vap2d`) and archived on Zenodo with a citable DOI.

## Contributing

Community contributions are welcome. To propose a change:
1. Fork the repository and create a feature branch.
2. Make your changes, keeping the code style consistent with the existing modules.
3. Open a Pull Request describing what changed and why. Pull requests are reviewed
   by the maintainer.

## License

VAP2D is released under the GNU General Public License v3.0 or later (GPLv3+).
See the [LICENSE](LICENSE) file for details.
