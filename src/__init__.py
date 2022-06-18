import functools
import os
import sys
from concurrent.futures import Future
from time import time

from aqt import gui_hooks, mw
from aqt.qt import *
from aqt.studydeck import StudyDeck
from aqt.utils import getFile, tooltip

ADDON_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(ADDON_DIR, "vendor"))

# pylint: disable=wrong-import-position
from .importer import PinyinImporter
from .notetype import PinyinNotetype


def on_import() -> None:
    files = getFile(
        mw,
        title="Choose CSV files to import",
        cb=None,
        key="pinyin_translator",
        filter="(*.csv *.txt)",
        multi=True,
    )
    if not files:
        return
    study_deck = StudyDeck(mw, title="Choose deck to import words to")
    deck = study_deck.name
    if not deck:
        return
    did = mw.col.decks.by_name(deck)["id"]
    importer = PinyinImporter(mw.col, files)
    total_words = len(importer.words)
    want_cancel = False

    def update_progress(i: int) -> None:
        nonlocal want_cancel
        want_cancel = mw.progress.want_cancel()
        mw.progress.update(f"Imported {i} words", value=i)

    def task() -> int:
        i = 0
        last_progress_update = time()
        for i, _ in enumerate(importer.import_to_deck(did, PinyinNotetype), start=1):
            if time() - last_progress_update >= 1.0:
                mw.taskman.run_on_main(functools.partial(update_progress, i=i + 1))
                if want_cancel:
                    break
                last_progress_update = time()
        return i

    def on_done(fut: Future) -> None:
        try:
            count = fut.result()
        finally:
            mw.progress.finish()
            mw.reset()
        tooltip(f"Imported {count} words", parent=mw)

    mw.progress.start(total_words, label="Importing words...", parent=mw)
    mw.taskman.run_in_background(task, on_done)


def on_init() -> None:
    action = QAction("Import English wordlist and generate Pinyin", mw)
    qconnect(action.triggered, on_import)
    mw.form.menuTools.addAction(action)
    PinyinNotetype.ensure_exists(mw.col)


gui_hooks.main_window_did_init.append(on_init)
