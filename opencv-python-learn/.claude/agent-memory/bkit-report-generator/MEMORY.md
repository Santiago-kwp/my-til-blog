# Report Generator Memory

## Project: opencv-python-learn

### Pattern: Design vs Implementation Variance

When generating PDCA completion reports, always evaluate whether design-vs-implementation differences are:
- **Improvements** (code is better): Document as positive and recommend design update
- **Regressions** (code misses spec): Flag as issues requiring fixes
- **Neutral** (different but equivalent): Document transparently

Example: `pitch-angle-image-size-correction` changed math model from symmetric (design) to asymmetric (implementation) — this was an improvement because:
- Asymmetric model is mathematically more general
- Handles real camera geometry (camera position != calendar center height)
- Symmetric case is a special case when `alpha_top = -alpha_bot`

### Key Report Sections (Korean Project)

1. **개요** (Overview) - Use Korean for project name, English for metric labels
2. **품질 지표** (Quality Metrics) - Always include:
   - Design Match Rate (from analysis.md)
   - Architecture Compliance
   - Convention Compliance
   - Overall score
3. **완료 항목** (Completed Items) - List all FR/NFR with checkboxes
4. **경험과 교훈** (Lessons Learned) - Keep/Problem/Try format
5. **PDCA 체크리스트** (PDCA Checklist) - Verify all 5 phases marked complete

### Template Structure for Korean Projects

Use this table structure for quality metrics (always have 4 score rows):

```
| 메트릭 | 값 | 상태 |
├─ 설계 일치도: X% (from analysis.md)
├─ 아키텍처: Y% (from analysis.md)
├─ 규칙 준수: Z% (from analysis.md)
└─ 전체: (X+Y+Z)/3 (Overall)
```

### Test Results Formatting

Always display full pytest output when 100% of tests pass:
```
$ pytest path/to/test_file.py -v
✅ test_name_1  PASS
...
Total: N tests | Passed: N (100%) | Failed: 0 (0%)
```

This demonstrates quality and reproducibility.

### File Path Patterns (Project-Specific)

- Implementation files: `Practices/{feature_name}.py`
- Test files: `Practices/test_{feature_name}.py`
- Analysis notebooks: `Practices/{feature_name}_analysis.ipynb`
- Reports: `docs/04-report/features/{feature_name}.report.md`

