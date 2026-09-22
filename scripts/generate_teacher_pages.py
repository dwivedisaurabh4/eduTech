from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "teacher-exams"

CONFIG = {
    "tgt": {
        "label": "TGT",
        "states": ["UP TGT", "Delhi TGT", "Haryana TGT", "Rajasthan TGT"],
        "subjects": ["Hindi", "Sanskrit", "English", "Mathematics", "Science", "Social Science", "GK/GS"],
    },
    "pgt": {
        "label": "PGT",
        "states": ["UP PGT", "Delhi PGT", "Haryana PGT", "Rajasthan PGT"],
        "subjects": ["Hindi", "Sanskrit", "English", "Mathematics", "Physics", "Chemistry", "Biology", "GK/GS"],
    },
    "primary": {
        "label": "Primary Teacher",
        "states": ["UP Primary", "Delhi Primary", "Haryana Primary", "Rajasthan Primary"],
        "subjects": ["Core Subjects", "GK/GS"],
    },
    "junior": {
        "label": "Junior Teacher",
        "states": ["UP Junior Teacher", "Delhi Junior Teacher", "Haryana Junior Teacher", "Rajasthan Junior Teacher"],
        "subjects": ["Hindi", "Sanskrit", "English", "Mathematics", "Science", "Social Science", "GK/GS"],
    },
}


def slug(value):
    return value.lower().replace("/", "-").replace(" ", "-")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def subject_page(exam, state, subject, kind):
    state_slug = slug(state)
    subject_slug = slug(subject)
    title = f"{subject} {kind}"
    other = "MCQ Test" if kind == "Notes" else "Notes"
    return f"""# {title}

**Breadcrumb:** Home > Teacher Exams > {exam['label']} > {state} > {subject} > {kind}

## {state} {subject}

This is the {kind.lower()} area for **{state} {subject}** preparation.

!!! note "Content template"
    Add verified, exam-specific content here. Keep this page focused on one revision task and include the notification or source date when details can change.

## Study checklist

- [ ] Match this topic with the official syllabus.
- [ ] Add concise explanations and examples.
- [ ] Add common mistakes and revision points.
- [ ] Review the linked {other.lower()} page.

[Go to {other}]({other.lower().replace(' ', '-')}.md)
"""


def subject_nav(exam, state, subject):
    state_slug = slug(state)
    subject_slug = slug(subject)
    base = f"teacher-exams/{slug(exam['label'])}/{state_slug}/{subject_slug}"
    if subject == "GK/GS" and exam["label"] in {"TGT", "PGT"}:
        return "    - सामान्य अध्ययन:\n      - नोट्स: notes/gs/index.md\n      - MCQ टेस्ट: mcq/gs-mcq.md"
    subject_label = "सामान्य अध्ययन" if subject == "GK/GS" else subject
    notes_label = "नोट्स" if subject == "GK/GS" else "Notes"
    mcq_label = "MCQ टेस्ट" if subject == "GK/GS" else "MCQ Test"
    return f"    - {subject_label}:\n      - {notes_label}: {base}/notes.md\n      - {mcq_label}: {base}/mcq-test.md"


def main():
    nav = []
    for key, exam in CONFIG.items():
        exam_slug = slug(exam["label"])
        write(ROOT / exam_slug / "index.md", f"""# {exam['label']}

Choose a state, then select a subject. Every subject follows the same path: **Notes -> MCQ Test**.

## Preparation guidance

Use the official notification as the source of truth for eligibility, syllabus, exam pattern, and dates. Add exam-specific guidance to the state and subject pages as the content grows.
""")
        exam_lines = [f"- {exam['label']}:", f"  - Overview: teacher-exams/{exam_slug}/index.md"]
        for state in exam["states"]:
            state_slug = slug(state)
            write(ROOT / exam_slug / state_slug / "index.md", f"""# {state}

Select a subject below. Each subject has **Notes** and **MCQ Test** pages.

**Breadcrumb:** Home > Teacher Exams > {exam['label']} > {state}
""")
            state_lines = [f"  - {state}:", f"    - Overview: teacher-exams/{exam_slug}/{state_slug}/index.md"]
            for subject in exam["subjects"]:
                subject_slug = slug(subject)
                folder = ROOT / exam_slug / state_slug / subject_slug
                write(folder / "notes.md", subject_page(exam, state, subject, "Notes"))
                write(folder / "mcq-test.md", subject_page(exam, state, subject, "MCQ Test"))
                state_lines.append(subject_nav(exam, state, subject))
            exam_lines.extend(state_lines)
        nav.extend(exam_lines)
    write(Path(__file__).with_name("teacher-nav.yml"), "\n".join(nav))

    config_path = Path(__file__).resolve().parents[1] / "mkdocs.yml"
    config = config_path.read_text(encoding="utf-8")
    start = "    # TEACHER_NAV_START"
    end = "    # TEACHER_NAV_END"
    start_index = config.index(start) + len(start)
    end_index = config.index(end)
    generated_lines = [f"    {part}" for line in nav for part in line.splitlines()]
    generated_nav = "\n" + "\n".join(generated_lines) + "\n    "
    config_path.write_text(config[:start_index] + generated_nav + config[end_index:], encoding="utf-8")


if __name__ == "__main__":
    main()
