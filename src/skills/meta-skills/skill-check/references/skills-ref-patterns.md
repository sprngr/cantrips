# skills-ref Structural Patterns

Source: https://github.com/agentskills/agentskills/tree/main/skills-ref

Reference library for Agent Skills. Python-based CLI tool.

## Directory layout

```
skills-ref/
├── src/skills_ref/
│   ├── __init__.py
│   ├── validator.py      # core validation logic
│   ├── parser.py         # YAML frontmatter parsing
│   ├── models.py         # SkillProperties dataclass
│   ├── prompt.py         # <available_skills> XML generator
│   ├── errors.py         # ParseError, ValidationError
│   └── cli.py            # CLI entry point
├── tests/
├── pyproject.toml
└── README.md
```

## Validation rules implemented

From `validator.py`:

| Check | Rule |
|-------|------|
| SKILL.md exists | Directory contains SKILL.md or skill.md |
| Frontmatter starts | First 3 chars are `---` |
| Frontmatter closes | Second `---` present |
| name required | Present and non-empty string |
| name lowercase | No uppercase characters |
| name hyphens | No leading/trailing/consecutive hyphens |
| name valid chars | Only `[a-z0-9-]` |
| name length | 1–64 characters |
| name matches dir | Skill name == directory name |
| description required | Present and non-empty string |
| description length | 1–1024 characters |
| compatibility length | 1–500 characters (if present) |
| no unknown fields | Only allowed keys in frontmatter |

## Allowed frontmatter keys

```python
ALLOWED_FIELDS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
```

## Python API

```python
from skills_ref import validate, read_properties, to_prompt

problems = validate(Path("my-skill"))
props = read_properties(Path("my-skill"))
prompt = to_prompt([Path("skill-a"), Path("skill-b")])
```

## CLI

```bash
skills-ref validate path/to/skill
skills-ref read-properties path/to/skill
skills-ref to-prompt path/to/skill-a path/to/skill-b
```

## Pattern notes for audit

- Skills should follow this structure when they include `scripts/`
- Validation logic in `validator.py` is the source of truth for spec rules
- The `strictyaml` library is used for frontmatter parsing
- Error messages should match skills-ref error patterns for consistency
