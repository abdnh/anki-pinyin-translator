import csv
from typing import Generator, Sequence, Type

from anki.collection import Collection
from anki.decks import DeckId

from .notetype import PinyinNotetype
from .translator import PinyinTranslator


class PinyinImporter:
    def __init__(self, col: Collection, files: Sequence[str]):  # , did: DeckId
        self.col = col
        self.words: list[str] = []
        self._read_files(files)

    def _read_files(self, files: Sequence[str]) -> None:
        for file in files:
            with open(file, "r", newline="", encoding="utf-8") as stream:
                reader = csv.reader(stream)
                for row in reader:
                    self.words.append(row[0])

    def import_to_deck(
        self, did: DeckId, notetype_info: Type[PinyinNotetype]
    ) -> Generator[None, None, None]:
        translator = PinyinTranslator()
        notetype = self.col.models.by_name(notetype_info.NAME)
        for word in self.words:
            data = translator.lookup(word)
            note = self.col.new_note(notetype)
            note[notetype_info.Fields.EN_FIELD.value] = data.en_word
            note[notetype_info.Fields.PINYIN_FIELD.value] = data.pinyin
            audio_filename = self.col.media.write_data(
                f"{data.en_word}_pinyin.mp3", data.audio
            )
            note[notetype_info.Fields.AUDIO_FIELD.value] = f"[sound:{audio_filename}]"
            self.col.add_note(note, did)
            yield
