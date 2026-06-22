#!/usr/bin/env python3
"""Render MeikiKai popup sample states to PNG files for UI review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PyQt6.QtWidgets import QApplication  # noqa: E402

from meikikai.dictionary.lookup import DictionaryEntry, KanjiEntry  # noqa: E402
from meikikai.gui.popup import Popup  # noqa: E402


class DummyLock:
    def acquire(self):
        pass

    def release(self):
        pass


class DummyState:
    screen_lock = DummyLock()


def vocab(
    written_form: str,
    reading: str,
    glosses: list[str],
    pos: tuple[str, ...] = (),
    tags: tuple[str, ...] = (),
    freq: int = 999_999,
    deconj: tuple[str, ...] = (),
) -> DictionaryEntry:
    return DictionaryEntry(
        id=1,
        written_form=written_form,
        reading=reading,
        senses=[{"glosses": glosses, "pos": list(pos), "tags": list(tags)}],
        freq=freq,
        deconjugation_process=deconj,
    )


def mockup_entries() -> list[DictionaryEntry | KanjiEntry]:
    return [
        DictionaryEntry(
            id=1,
            written_form="誘う",
            reading="さそう",
            senses=[
                {
                    "glosses": [
                        "to invite",
                        "to ask (someone to do)",
                        "to call (for)",
                        "to take (someone) along",
                    ],
                    "pos": ["v5u", "vt"],
                    "tags": [],
                },
                {
                    "glosses": ["to tempt", "to lure", "to entice", "to seduce"],
                    "pos": ["v5u", "vt"],
                    "tags": [],
                },
                {
                    "glosses": [
                        "to induce (tears, laughter, sleepiness, etc.)",
                        "to arouse (e.g. sympathy)",
                        "to provoke",
                    ],
                    "pos": ["v5u", "vt"],
                    "tags": [],
                },
            ],
            freq=832,
            deconjugation_process=("誘われる", "passive", "('a' stem)"),
        ),
        DictionaryEntry(
            id=2,
            written_form="誘う",
            reading="いざなう",
            senses=[
                {
                    "glosses": [
                        "to invite",
                        "to ask (someone to do)",
                        "to call (for)",
                        "to take (someone) along",
                    ],
                    "pos": ["v5u"],
                    "tags": [],
                },
                {
                    "glosses": ["to tempt", "to lure", "to entice", "to seduce"],
                    "pos": ["v5u"],
                    "tags": [],
                },
            ],
            freq=999_999,
            deconjugation_process=(),
        ),
        KanjiEntry(
            character="誘",
            meanings=["entice", "lead", "tempt", "invite", "ask", "call for"],
            readings=["ユウ", "さそ.う", "いざな.う"],
            examples=[
                {"w": "誘う", "r": "さそう", "m": "to invite"},
                {"w": "誘い", "r": "さそい", "m": "invitation"},
                {"w": "誘導", "r": "ゆうどう", "m": "guidance"},
            ],
            components=[{"c": "言", "m": "say"}, {"c": "秀", "m": "excel"}],
        ),
    ]


def long_entries() -> list[DictionaryEntry]:
    return [
        vocab(
            "取り戻させられなかった",
            "とりもどさせられなかった",
            [
                "to take back",
                "to regain",
                "to recover something that was lost",
                "to restore something to a previous state",
                "to make someone recover",
                "to be unable to cause someone to take something back",
            ],
            pos=("v5s", "vt"),
            tags=("usually written using kana alone", "transitive verb", "long sample tag"),
            freq=12345,
            deconj=(
                "取り戻させられなかった",
                "negative",
                "past",
                "potential",
                "causative",
                "passive",
                "('a' stem)",
            ),
        )
    ]


def nature_entries() -> list[DictionaryEntry | KanjiEntry]:
    return [
        DictionaryEntry(
            id=20,
            written_form="自然",
            reading="しぜん",
            senses=[
                {
                    "glosses": ["nature", "spontaneity", "naturally", "in due course"],
                    "pos": ["n", "adj-no", "adv"],
                    "tags": [],
                },
            ],
            freq=724,
            deconjugation_process=(),
        ),
        KanjiEntry(
            character="自",
            meanings=["oneself", "self", "from"],
            readings=["ジ", "シ", "みずか.ら", "おの.ずから"],
            examples=[
                {"w": "自分", "r": "じぶん", "m": "oneself"},
                {"w": "自然", "r": "しぜん", "m": "nature"},
                {"w": "自由", "r": "じゆう", "m": "freedom"},
            ],
            components=[{"c": "目", "m": "eye"}],
        ),
        KanjiEntry(
            character="然",
            meanings=["so", "if so", "in that case", "well"],
            readings=["ゼン", "ネン", "しか", "しか.り"],
            examples=[
                {"w": "自然", "r": "しぜん", "m": "nature"},
                {"w": "当然", "r": "とうぜん", "m": "natural; obvious"},
                {"w": "全然", "r": "ぜんぜん", "m": "not at all"},
            ],
            components=[{"c": "灬", "m": "fire"}, {"c": "月", "m": "moon; flesh"}, {"c": "犬", "m": "dog"}],
        ),
    ]


def tall_entries() -> list[DictionaryEntry | KanjiEntry]:
    return [
        DictionaryEntry(
            id=10,
            written_form="か",
            reading="か",
            senses=[
                {"glosses": ["question particle", "indicates a question", "marks doubt", "used at sentence end", "whether"], "pos": ["prt"], "tags": []},
                {"glosses": ["or", "alternatively", "some", "one of"], "pos": ["prt"], "tags": []},
                {"glosses": ["indicates uncertainty", "maybe", "perhaps", "I wonder"], "pos": ["prt"], "tags": []},
                {"glosses": ["emphasis", "surprise", "disbelief"], "pos": ["prt"], "tags": []},
                {"glosses": ["archaic exclamation", "poetic ending"], "pos": ["prt"], "tags": ["archaism"]},
            ],
            freq=42,
            deconjugation_process=(),
        ),
        vocab("蚊", "か", ["mosquito"], pos=("n",), freq=6400),
        vocab("課", "か", ["lesson", "section", "department", "division", "counter for lessons"], pos=("n",), freq=7100),
        vocab("可", "か", ["passable", "acceptable", "permitted", "approval"], pos=("n",), freq=12200),
        vocab("化", "か", ["-ization", "action of making something", "change into", "influence"], pos=("suf",), freq=2300),
        KanjiEntry(
            character="可",
            meanings=["can", "passable", "mustn't", "should not", "do not"],
            readings=["カ", "べ.き", "べ.し"],
            examples=[
                {"w": "可能", "r": "かのう", "m": "possible"},
                {"w": "許可", "r": "きょか", "m": "permission"},
                {"w": "可愛い", "r": "かわいい", "m": "cute"},
            ],
            components=[{"c": "口", "m": "mouth"}, {"c": "丁", "m": "street"}],
        ),
    ]


def render(entries: list[DictionaryEntry | KanjiEntry], output: Path) -> tuple[int, int]:
    app = QApplication.instance() or QApplication([])
    popup = Popup(DummyState())
    popup._set_entries(entries)
    popup.show()
    app.processEvents()
    image = popup.grab()
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(output))
    return popup.size().width(), popup.size().height()


def render_switch(output: Path) -> tuple[int, int]:
    app = QApplication.instance() or QApplication([])
    popup = Popup(DummyState())
    for entries in (mockup_entries(), long_entries(), mockup_entries(), long_entries()):
        popup._set_entries(entries)
        popup.show()
        app.processEvents()
    image = popup.grab()
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(output))
    return popup.size().width(), popup.size().height()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a MeikiKai popup sample PNG.")
    parser.add_argument(
        "case",
        nargs="?",
        choices=("mockup", "long", "switch", "tall", "nature"),
        default="mockup",
        help="Sample state to render. Default: mockup.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output PNG path. Default: /tmp/meikikai_popup_<case>.png",
    )
    args = parser.parse_args()

    output = args.output or Path(f"/tmp/meikikai_popup_{args.case}.png")
    if args.case == "mockup":
        width, height = render(mockup_entries(), output)
    elif args.case == "long":
        width, height = render(long_entries(), output)
    elif args.case == "tall":
        width, height = render(tall_entries(), output)
    elif args.case == "nature":
        width, height = render(nature_entries(), output)
    else:
        width, height = render_switch(output)

    print(f"Rendered {args.case} popup to {output} ({width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
