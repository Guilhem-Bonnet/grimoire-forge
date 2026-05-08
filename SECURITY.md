# Security Policy

## Scope

This policy covers the repository root, the Grimoire runtime assets, the web cockpit package, the Python framework and the governance artifacts that can influence tool execution or public release behavior.

## Reporting

Do not open a public issue for an undisclosed vulnerability.

Report it privately through one of these channels:

1. the private GitHub Security Advisory flow on the public repository when it is available;
2. the maintainer contact listed on the GitHub profile.

## Include in the report

- affected path or package;
- impact and expected attacker outcome;
- reproduction steps or a minimal proof;
- whether secrets, authz, file access or tool execution are involved;
- any mitigation already tested.

## High-priority classes

Treat the following as blocking security issues:

- prompt injection that can trigger tool execution;
- unauthorized filesystem access or data exfiltration;
- auth bypass on runtime write paths;
- supply-chain or packaging drift affecting release artifacts.

## Release gate

No public tag or release should proceed while an unresolved security issue affects an exposed write path, a host bridge permission boundary or a packaged artifact.
