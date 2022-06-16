import enum
from dataclasses import dataclass

from anki.collection import Collection


@dataclass
class PinyinTemplate:
    name: str
    qfmt: str
    afmt: str


class PinyinNotetype:
    NAME = "Pinyin With Audio"

    class Fields(enum.Enum):
        EN_FIELD = "English"
        PINYIN_FIELD = "Pinyin"
        AUDIO_FIELD = "Audio"

    TEMPLATES = [
        PinyinTemplate(
            name="Card 1",
            qfmt="{{English}}",
            afmt='{{FrontSide}}<hr id="answer">{{Pinyin}}{{Audio}}',
        ),
    ]

    def __init__(self, col: Collection):
        self.col = col

    def ensure_exists(self) -> None:
        notetype = self.col.models.by_name(self.NAME)
        if not notetype:
            self._add_notetype()

    def _add_notetype(self):
        notetype = self.col.models.new(self.NAME)
        for field_enum in self.Fields:
            field = self.col.models.new_field(field_enum.value)
            self.col.models.add_field(notetype, field)
        for template_info in self.TEMPLATES:
            template = self.col.models.new_template(template_info.name)
            template["qfmt"] = template_info.qfmt
            template["afmt"] = template_info.afmt
            self.col.models.add_template(notetype, template)
        self.col.models.save(notetype)
