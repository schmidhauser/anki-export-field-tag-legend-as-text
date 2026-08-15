# Copyright (C) 2026 Andreas U. Schmidhauser
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import date
from pathlib import Path
import re

from aqt import mw
from aqt.qt import QAction, QApplication, QFileDialog, qconnect
from aqt.utils import showWarning, tooltip


HTML_COMMENT_PATTERN = re.compile(r"<!--(.*?)-->", re.DOTALL)


def configured_options() -> tuple[str, str, str]:
    config = mw.addonManager.getConfig(__name__) or {}

    location = config.get("location")

    if not isinstance(location, dict):
        raise ValueError(
            'The "location" setting must contain a note type and card type.'
        )

    note_type = location.get("note_type")
    card_type = location.get("card_type")
    marker = config.get("marker")

    if not isinstance(note_type, str) or not note_type.strip():
        raise ValueError(
            'The "location.note_type" setting must be a non-empty string.'
        )

    if not isinstance(card_type, str) or not card_type.strip():
        raise ValueError(
            'The "location.card_type" setting must be a non-empty string.'
        )

    if not isinstance(marker, str) or not marker.strip():
        raise ValueError(
            'The "marker" setting must be a non-empty string.'
        )

    return note_type, card_type, marker


def extract_legend(front_template: str, marker: str) -> str:
    occurrences = front_template.count(marker)

    if occurrences == 0:
        raise ValueError(
            "The configured marker was not found in the front template."
        )

    if occurrences > 1:
        raise ValueError(
            "The configured marker occurs more than once in the front template."
        )

    for match in HTML_COMMENT_PATTERN.finditer(front_template):
        comment = match.group(1)

        if marker in comment:
            return comment.strip()

    raise ValueError(
        "The configured marker was found, but it is not inside "
        "a complete HTML comment."
    )


def prepare_legend() -> str | None:
    if mw.col is None:
        showWarning("No collection is open.", parent=mw)
        return None

    try:
        note_type_name, card_type_name, marker = configured_options()
    except ValueError as error:
        showWarning(str(error), parent=mw)
        return None

    note_type = mw.col.models.by_name(note_type_name)

    if note_type is None:
        showWarning(
            f'Note type "{note_type_name}" was not found.',
            parent=mw,
        )
        return None

    card_type = next(
        (
            template
            for template in note_type.get("tmpls", [])
            if template.get("name") == card_type_name
        ),
        None,
    )

    if card_type is None:
        showWarning(
            f'Card type "{card_type_name}" was not found '
            f'in note type "{note_type_name}".',
            parent=mw,
        )
        return None

    front_template = card_type.get("qfmt")

    if not isinstance(front_template, str):
        showWarning(
            f'Could not read the front template of card type '
            f'"{card_type_name}".',
            parent=mw,
        )
        return None

    try:
        return extract_legend(front_template, marker)
    except ValueError as error:
        showWarning(str(error), parent=mw)
        return None


def on_copy() -> None:
    text = prepare_legend()

    if text is None:
        return

    clipboard = QApplication.clipboard()

    if clipboard is None:
        showWarning("Could not access the system clipboard.", parent=mw)
        return

    clipboard.setText(text)

    tooltip(
        "Copied Field and Tag Legend",
        parent=mw,
    )


def on_save() -> None:
    text = prepare_legend()

    if text is None:
        return

    default_filename = (
        f"anki-field-tag-legend-{date.today().isoformat()}.txt"
    )
    default_path = Path.home() / default_filename

    filename, _selected_filter = QFileDialog.getSaveFileName(
        mw,
        "Save Field and Tag Legend as Text",
        str(default_path),
        "Text Files (*.txt)",
    )

    if not filename:
        return

    path = Path(filename)

    if not path.suffix:
        path = path.with_suffix(".txt")

    try:
        path.write_bytes(text.encode("utf-8"))
    except OSError as error:
        showWarning(
            f"Could not save the file:\n{error}",
            parent=mw,
        )
        return

    tooltip(
        "Saved Field and Tag Legend",
        parent=mw,
    )


def apply_shortcuts(config: dict) -> None:
    shortcut_copy = config.get("shortcut_copy", "")
    shortcut_save = config.get("shortcut_save", "")

    copy_action.setShortcut(
        shortcut_copy if isinstance(shortcut_copy, str) else ""
    )
    save_action.setShortcut(
        shortcut_save if isinstance(shortcut_save, str) else ""
    )


copy_action = QAction("Copy Field and Tag Legend as Text", mw)
save_action = QAction("Save Field and Tag Legend as Text…", mw)

qconnect(copy_action.triggered, on_copy)
qconnect(save_action.triggered, on_save)

config = mw.addonManager.getConfig(__name__) or {}
apply_shortcuts(config)

mw.addonManager.setConfigUpdatedAction(__name__, apply_shortcuts)

mw.form.menuTools.addAction(copy_action)
mw.form.menuTools.addAction(save_action)
