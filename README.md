# PulseNote

Local-first CLI tool that turns your Git commit history into clean, professional standup notes and weekly digests.

**Built by Mourad.Soltani**

## Features
- Generate daily standup from last 24h commits
- Weekly summary mode
- Interactive prompts for "today" and "blockers"
- Outputs Markdown, Slack, or plain text
- Works across multiple local repositories
- Zero external APIs — everything stays on your machine
- Health checks and unit tests included

## Installation
```bash
pip install -e .
# or
python -m pip install .
```

## Usage
```bash
pulsenote standup          # daily
pulsenote standup --format slack
pulsenote week             # last 7 days
pulsenote --help
```

## Requirements
- Python 3.9+
- Git installed and available in PATH
- Local Git repositories

## Development
```bash
pip install -e ".[dev]"
pytest
```

## License
MIT — see LICENSE

Built by Mourad.Soltani
