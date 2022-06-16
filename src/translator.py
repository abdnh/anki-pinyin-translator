from dataclasses import dataclass

from googletrans import Translator
from gtts import gTTS


@dataclass
class PinyinData:
    en_word: str
    pinyin: str
    audio: bytes


class PinyinTranslator:
    DEST_LANG = "zh-CN"

    def __init__(self) -> None:
        self.translator = Translator()

    def lookup(self, word: str, lang: str = "en") -> PinyinData:
        translated = self.translator.translate(word, src=lang, dest=self.DEST_LANG)
        tts = gTTS(translated.text, lang=self.DEST_LANG)
        return PinyinData(word, translated.pronunciation, next(tts.stream()))


if __name__ == "__main__":
    translator = PinyinTranslator()
    data = translator.lookup("red")
    print(data.en_word, data.pinyin)
    with open("test.mp3", "wb") as file:
        file.write(data.audio)
