# Best Practices — Quality Guidelines Checklist

Source: https://agentskills.io/skill-creation/best-practices

## Grounding

- [ ] Skill is based on real expertise, not generic LLM knowledge
- [ ] Domain-specific context provided (API patterns, edge cases, conventions)
- [ ] Input/output formats documented
- [ ] Skill refined from real execution, not just theory

## Content quality

- [ ] Agent-specific content included, generic content omitted
- [ ] Each content piece passes "would agent get this wrong without it?" test
- [ ] Skill is a coherent unit of work (not too narrow, not too broad)
- [ ] Moderate detail level (not exhaustive, not sparse)
- [ ] Working example included

## Progressive disclosure

- [ ] SKILL.md under 500 lines / 5000 tokens
- [ ] Detailed reference material in `references/`
- [ ] Agent told WHEN to load each reference file
- [ ] Reference files are focused and small

## Instruction design

- [ ] Gotchas section for environment-specific edge cases
- [ ] Defaults provided, not menus of equal options
- [ ] Procedures taught, not one-off answers declared
- [ ] Specificity matches task fragility (flexible for variation, prescriptive for fragile ops)
- [ ] Validation loops present for multi-step workflows
- [ ] Checklists used for dependency tracking

## Script hygiene

- [ ] Scripts are self-contained or document dependencies
- [ ] Scripts include helpful error messages
- [ ] Scripts handle edge cases gracefully
- [ ] Repeated agent logic bundled into scripts

## Token efficiency

- [ ] No wasted explanation of concepts the agent already knows
- [ ] No redundant instructions across steps
- [ ] No instructions that don't apply to the current task
