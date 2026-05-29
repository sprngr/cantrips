# Agent Skills Specification — Requirements Checklist

Source: https://agentskills.io/specification

## Directory structure

- [ ] Skill is a directory
- [ ] Contains `SKILL.md` file (required, case-insensitive)
- [ ] Optional directories: `scripts/`, `references/`, `assets/`
- [ ] No deeply nested reference chains (keep file references 1 level deep)

## Frontmatter — Required fields

- [ ] `name` present (1–64 chars, lowercase letters/digits/hyphens only)
- [ ] `name` does not start or end with hyphen
- [ ] `name` does not contain consecutive hyphens (`--`)
- [ ] `name` matches parent directory name
- [ ] `description` present (1–1024 chars, non-empty)
- [ ] `description` describes what the skill does AND when to use it
- [ ] `description` includes trigger keywords for agent identification

## Frontmatter — Optional fields (if present)

- [ ] `license` is a short name or reference to bundled file
- [ ] `compatibility` is 1–500 chars (only if skill has env requirements)
- [ ] `metadata` is a string→string map
- [ ] `allowed-tools` is space-separated (if present)
- [ ] No unknown frontmatter fields

## SKILL.md body

- [ ] Body is valid Markdown after frontmatter
- [ ] Contains step-by-step instructions
- [ ] Contains examples of inputs and outputs
- [ ] Contains edge case handling notes
- [ ] Total file under 500 lines / 5000 tokens

## Progressive disclosure

- [ ] Metadata (~100 tokens) is minimal and loadable at startup
- [ ] Instructions (<5000 tokens) contain core workflow
- [ ] Detailed content moved to `references/` files
- [ ] Agent told WHEN to load each reference file

## File references

- [ ] All file references use relative paths from skill root
- [ ] No deeply nested reference chains
