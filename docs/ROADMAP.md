# Development roadmap

This roadmap records intended work, not completed features.

## Phase 0 — Foundation
- [ ] Establish repository conventions and project structure.
- [ ] Define supported platforms and Python/runtime requirements.
- [ ] Select architecture boundaries and configuration strategy.
- [ ] Add formatting, linting, type-checking, and test tooling.
- [ ] Add a minimal application entry point and health checks.

## Phase 1 — Assistant core
- [ ] Define request, response, event, and cancellation contracts.
- [ ] Implement provider interfaces and configuration.
- [ ] Add structured logging and error handling.
- [ ] Add unit tests for core orchestration.

## Phase 2 — Voice
- [ ] Select speech-to-text and text-to-speech interfaces.
- [ ] Implement audio input/output lifecycle.
- [ ] Add wake-word handling and interruption support.
- [ ] Test latency, device selection, and recovery.

## Phase 3 — Tools and perception
- [ ] Define a permission-aware tool registry.
- [ ] Add desktop interaction behind explicit controls.
- [ ] Add screen capture and visual understanding.
- [ ] Add browser and research workflows.
- [ ] Add file and document tools.

## Phase 4 — Memory and workflows
- [ ] Define user-controlled memory storage and deletion.
- [ ] Add reusable workflows and scheduled tasks.
- [ ] Add audit history for actions and external integrations.

## Phase 5 — Interface and integrations
- [ ] Build the desktop interface and activity view.
- [ ] Add settings, connections, files, and memory screens.
- [ ] Add integrations incrementally with least-privilege permissions.

## Release readiness
- [ ] Security and dependency review.
- [ ] Automated tests and supported-platform checks.
- [ ] Installation and update documentation.
- [ ] Backup, recovery, and troubleshooting documentation.
