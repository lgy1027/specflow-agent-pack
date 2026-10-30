#!/usr/bin/env python3
"""Check pilot brief blocker-list structure, not its safety or factual validity."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^\s*(#{1,6})\s+(?:\d+[.)、]\s*)?启动阻断项(?:清单)?(?:\s*[（(].*[）)])?\s*$")
ID_RE = re.compile(r"(?<![A-Z0-9])B\d+(?![A-Z0-9])", re.IGNORECASE)
RANGE_RE = re.compile(
    r"(?<![A-Z0-9])B(\d+)\s*(?:–|—|－|-|~|～|…+|\.{2,}|至|到|to|through)\s*B(\d+)(?![A-Z0-9])",
    re.IGNORECASE,
)
OPEN_RANGE_RE = re.compile(
    r"(?<![A-Z0-9])B(\d+)\s*(?:–|—|－|-|~|～|…+|\.{2,}|至|到|to|through)\s*Bn(?![A-Z0-9])",
    re.IGNORECASE,
)
OPEN_LIST_RE = re.compile(r"B\d+(?:\s*[,，、]\s*B\d+)*\s*[,，、]?\s*(?:…+|\.{2,})\s*[,，、]?\s*Bn\b", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"待填写|待编号|待补充|替换为|\b(?:tbd|todo|n/?a)\b", re.IGNORECASE)
NONE_RE = re.compile(r"^(?:(?:当前(?:项目)?|本次(?:试点)?|本试点|试点)\s*)?(?:无(?:启动阻断项|阻断项)?|没有(?:启动阻断项|阻断项)?|未发现(?:启动阻断项|阻断项)?|none(?:\s+(?:startup\s+)?blockers?)?|n/?a)(?:\s*[（(].*[）)])?[。；;,.：:]?$", re.IGNORECASE)
ALIASES = {
    "id": {"id", "编号", "阻断项编号"},
    "issue": {"阻断事项", "事项", "阻断项", "问题", "blocker", "item"},
    "evidence": {"证据", "依据", "证据/待确认内容", "证据/待确认", "evidence"},
    "owner": {"责任角色", "责任人", "负责人", "责任方", "owner", "role"},
    "status": {"状态", "进度", "处理状态", "status"},
}


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def unsupported(message: str) -> int:
    print(f"UNSUPPORTED: {message}", file=sys.stderr)
    return 3


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().lower())


def canonical_header(value: str) -> str | None:
    normalized = normalize(value)
    return next((key for key, aliases in ALIASES.items() if normalized in {normalize(a) for a in aliases}), None)


def split_table_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [cell.replace(r"\|", "|").strip() for cell in cells]


def table_blocks(section: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    fenced = False
    for line in section:
        if line.strip().startswith(chr(96) * 3) or line.strip().startswith("~~~"):
            fenced = not fenced
        elif not fenced and line.strip().startswith("|"):
            current.append(line.strip())
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def visible_lines(lines: list[str]) -> list[str]:
    """Keep line positions but exclude fenced examples from validation."""
    visible: list[str] = []
    fenced = False
    for line in lines:
        if line.strip().startswith(chr(96) * 3) or line.strip().startswith("~~~"):
            fenced = not fenced
            visible.append("")
        else:
            visible.append("" if fenced else line)
    return visible


def extract_table_rows(section: list[str]) -> tuple[list[dict[str, str]] | None, str | None]:
    blocks = table_blocks(section)
    if not blocks:
        return None, None
    if len(blocks) > 1:
        return None, "multiple tables require manual review"
    table = blocks[0]
    header_cells = split_table_row(table[0])
    headers = [canonical_header(cell) for cell in header_cells]
    if any(header is None for header in headers) or len(set(headers)) != len(headers):
        return None, "table format unsupported; preserve the project format and use manual review"
    if not set(ALIASES).issubset(set(headers)):
        return None, "table format unsupported; preserve the project format and use manual review"
    if len(table) < 2 or not re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?", table[1]):
        return None, "table format unsupported; preserve the project format and use manual review"

    rows: list[dict[str, str]] = []
    for line in table[2:]:
        cells = split_table_row(line)
        if len(cells) != len(headers):
            return None, f"malformed blocker table row: {line}"
        rows.append({header: cell for header, cell in zip(headers, cells) if header})
    return rows, None


def extract_list_rows(section: list[str]) -> tuple[list[dict[str, str]], str | None]:
    rows = []
    for raw_line in section:
        line = raw_line.strip()
        while True:
            cleaned = re.sub(r"^(?:[-*+]\s+|\d+[.)、]\s*|\[\s*[xX ]\s*\]\s*|\(\d+\)\s*)", "", line, count=1)
            if cleaned == line:
                break
            line = cleaned
        line = re.sub(r"[*_]", "", line).strip()
        if not re.match(r"B\d+", line, re.IGNORECASE):
            continue
        if re.match(r"B\d+[\s,，、/]+B\d+", line, re.IGNORECASE):
            return rows, "split multiple blocker IDs into separate rows"
        id_match = re.match(r"B\d+", line, re.IGNORECASE)
        fields = {"id": id_match.group(0)}
        issue_text = line[id_match.end():].lstrip(" —-:：")
        issue_text = re.split(r"[|；;]", issue_text, maxsplit=1)[0].strip()
        if issue_text:
            fields["issue"] = issue_text
        for key, labels in {
            "issue": r"事项|阻断事项|问题",
            "evidence": r"证据(?:/待确认内容|/待确认)?|待确认内容|依据|待确认|evidence",
            "owner": r"责任角色|责任人|负责人|责任方|owner|role",
            "status": r"状态|进度|处理状态|status",
        }.items():
            match = re.search(rf"(?:{labels})\s*[:：=]\s*([^|；;]+)", line, re.IGNORECASE)
            if match:
                fields[key] = match.group(1).strip()
        rows.append(fields)
    return rows, None


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_pilot_brief.py <pilot-brief.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeError:
            text = raw.decode("utf-16")
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    lines = text.splitlines()
    scan_lines = visible_lines(lines)
    headings = [(i, HEADING_RE.match(line.strip().lstrip("\ufeff"))) for i, line in enumerate(scan_lines)]
    headings = [(i, match) for i, match in headings if match]
    if not headings:
        return unsupported("blocker section heading is not recognized; preserve the project format and use manual review")
    if len(headings) > 1:
        return unsupported("multiple blocker sections require manual review")

    heading_index, heading = headings[0]
    heading_level = len(heading.group(1))
    start = heading_index + 1
    end = next(
        (i for i in range(start, len(scan_lines))
         if (match := re.match(r"^\s*(#{1,6})\s+", scan_lines[i])) and len(match.group(1)) <= heading_level),
        len(lines),
    )
    section = scan_lines[start:end]
    non_table_lines = [
        re.sub(r"[*_]", "", re.sub(r"^\s*(?:[-*+]|\d+[.)、])\s*", "", line)).strip()
        for line in section if line.strip() and not line.strip().startswith("|")
    ]
    none_claim = any(NONE_RE.match(line.strip()) for line in non_table_lines)

    table_rows, error = extract_table_rows(section)
    if error:
        if "unsupported" in error or "multiple tables" in error:
            return unsupported(error)
        return fail(error)
    if table_rows is None:
        rows, error = extract_list_rows(section)
        if error:
            return fail(error)
    else:
        rows = table_rows

    if none_claim and rows:
        return fail("section says there are no blockers but also contains blocker entries")
    explicit_none = none_claim and not rows
    if not rows and not explicit_none:
        if any("|" in line for line in non_table_lines) or any(re.match(r"^\s*(?:[-*+]|\d+[.)、])", line) for line in section):
            return unsupported("blocker list format unsupported; preserve the project format and use manual review")
        if any(ID_RE.search(line) or RANGE_RE.search(line) or OPEN_RANGE_RE.search(line) for line in section):
            return fail("blocker IDs are referenced but no blocker rows are listed")
        return fail("blocker section is empty; state that there are no blockers or list each blocker")

    declared: set[str] = set()
    for row in rows:
        blocker_id = row.get("id", "").upper()
        if "待编号" in blocker_id or "待填写" in blocker_id:
            return fail("unreplaced blocker ID placeholder")
        if not re.fullmatch(r"B\d+", blocker_id):
            return unsupported(f"blocker ID format unsupported: {row.get('id', '')}; preserve the project format and use manual review")
        if blocker_id in declared:
            return fail(f"duplicate blocker ID: {blocker_id}")
        declared.add(blocker_id)
        for field in ("issue", "evidence", "owner", "status"):
            value = row.get(field, "").strip()
            empty_markers = {"", "-", "—", "–", "n/a", "na"}
            if field != "evidence":
                empty_markers.add("无")
            if (not value or PLACEHOLDER_RE.search(value) or value.lower() in empty_markers
                    or (field != "evidence" and re.search(r"待确认|待定|待更新", value))):
                return fail(f"{blocker_id} has a missing or placeholder {field} field")

    visible_text = "\n".join(scan_lines)
    prose_text = re.sub(r"`[^`]*`", "", visible_text)
    if OPEN_RANGE_RE.search(prose_text) or OPEN_LIST_RE.search(prose_text):
        return fail("replace unbounded ranges such as B1–Bn with explicit IDs")
    for match in RANGE_RE.finditer(prose_text):
        first, last = int(match.group(1)), int(match.group(2))
        if first > last or last - first > 99:
            return fail(f"invalid or oversized blocker ID range: {match.group(0)}")
    expanded = RANGE_RE.sub(
        lambda match: " ".join(
            f"B{i:0{len(match.group(1))}d}"
            for i in range(int(match.group(1)), int(match.group(2)) + 1)
        ),
        prose_text,
    )
    cited_lines = []
    for raw_line in expanded.splitlines():
        line = raw_line
        if re.search(r"启动阻断项|阻断项|blocker|前置条件|解除|关闭|未决|未解决|未关闭|待办|残余风险|附录|appendix|unresolved|outstanding|remain|pending|reference|引用|参考|见\s*B\d+", line, re.IGNORECASE):
            cited_lines.append(line)
    referenced = {value.upper() for line in cited_lines for value in ID_RE.findall(line)}
    missing = sorted(referenced - declared, key=lambda value: int(value[1:]))
    if missing:
        return fail("referenced blocker IDs are missing from the list: " + ", ".join(missing))

    print(f"PASS: file={path.resolve()} sha256={digest} blockers={len(declared)}; blocker-section structure and cited IDs only; no factual, approval, or safety validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
