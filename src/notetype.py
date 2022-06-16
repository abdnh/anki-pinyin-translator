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

    @classmethod
    def ensure_exists(cls, col: Collection) -> None:
        notetype = col.models.by_name(cls.NAME)
        if not notetype:
            cls._add_notetype(col)

    @classmethod
    def _add_notetype(cls, col: Collection) -> None:
        notetype = col.models.new(cls.NAME)
        for field_enum in cls.Fields:
            field = col.models.new_field(field_enum.value)
            col.models.add_field(notetype, field)
        for template_info in cls.TEMPLATES:
            template = col.models.new_template(template_info.name)
            template["qfmt"] = template_info.qfmt
            template["afmt"] = template_info.afmt
            col.models.add_template(notetype, template)
        col.models.save(notetype)
