import re


def is_valid(word):
    """Validates a word based on specified patterns.
    The pattern dictates that the word must only contain of alphabet letters, apostrophes, hyphens, and periods.

    Args:
        word (str): Any word.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(re.match(r"^[a-zA-Z\'\-\.]+$", word))


def to_sentence(s):
    """Converts a string to sentence case.

    Args:
        s (str): Any string.

    Returns:
        str: The string in sentence case.
    """
    if not s:
        return None

    if len(s) > 1:
        s = s[0].upper() + s[1:]
        if s[-1] not in [".", "?", "!"]:
            s += "."

    return s


def format_pos(pos):
    """Formats a Parts of Speech (POS) tag into simpler forms.

    Args:
        pos (str): The POS tag.

    Returns:
        str/None: The formatted POS tag, if POS is provided, None otherwise.
    """
    if pos:
        formatted_pos = pos.lower()

        # Split multiple pos with delimiters
        if "&" in formatted_pos:
            formatted_pos = formatted_pos.split("&")[0].strip()
        if "and" in formatted_pos:
            formatted_pos = formatted_pos.split("and")[0].strip()
        if "or" in formatted_pos:
            formatted_pos = formatted_pos.split("or")[0].strip()
        if ";" in formatted_pos:
            formatted_pos = formatted_pos.split(";")[0].strip()
        if "," in formatted_pos:
            formatted_pos = formatted_pos.split(",")[0].strip()

        # Remove affixes
        formatted_pos = (
            formatted_pos.replace("prefix", "pfx")
            .replace("suffix", "sfx")
            .replace("infix", "ifx")
            .replace("pref", "pfx")
            .replace("suff", "sfx")
            .replace("infi", "ifx")
        )

        # Reformat proper nouns
        formatted_pos = formatted_pos.replace("pr.", "prop").replace(
            "prop. n.", "n prop"
        )

        # Remove singular/plural
        formatted_pos = formatted_pos.replace("sing.", "").replace("pl.", "")

        # Remove perspective
        formatted_pos = (
            formatted_pos.replace("3d", "")
            .replace("2d", "")
            .replace("1st", "")
            .replace("pers.", "")
            .replace("pres.", "")
        )

        # Reformat gender
        formatted_pos = formatted_pos.replace("masc. n.", "n masc").replace(
            "fem. n.", "n fem"
        )

        # Convert verb forms
        formatted_pos = (
            formatted_pos.replace("v. i.", "v")
            .replace("v. t.", "v")
            .replace("v. inf.", "v")
            .replace("prop. v.", "v")
            .replace("imperative", "imp")
            .replace("imp", "v")
            .replace("pret", "v")
            .replace("indic", "v")
        )

        # Convert adjective forms
        formatted_pos = (
            formatted_pos.replace("prop. a.", "adj")
            .replace("p. a.", "adj")
            .replace("pred. a.", "adj")
            .replace("pred. adj.", "adj")
            .replace("ads", "adj")
        )

        # Other
        formatted_pos = (
            formatted_pos.replace("pron.", "pro")
            .replace("interj", "intj")
            .replace("p. p.", "prep")
            .replace("abl", "adv")
            .replace("article", "art")
            .replace("definite", "def")
            .replace("strong", "")
            .replace("obs.", "")
        )

        # Remove periods and leading/trailing whitespace
        formatted_pos = formatted_pos.replace(".", " ")
        formatted_pos = formatted_pos.strip()

        # Other reformats
        if formatted_pos == "prop":
            formatted_pos = "n prop"
        if formatted_pos == "masc":
            formatted_pos = "n masc"
        if formatted_pos == "fem":
            formatted_pos = "n fem"

        if formatted_pos == "compar":
            formatted_pos = "adj compar"
        if formatted_pos == "superl":
            formatted_pos = "adj superl"

        # Convert delimiter to period instead of space
        formatted_pos = ".".join(formatted_pos.split()) + "."

        # Checks if there's other characters beside periods
        if len(formatted_pos.replace(".", "").strip()) < 1:
            return None

        return formatted_pos
    return None


def auto_match_entries(entries):
    """Ensures that all listed similar or opposite words of each dictionary entry has its own entry.

    Args:
        entries (list): A list of dictionary entries.

    Returns:
        list: A list of dictionary entries.
    """
    auto_matched_entries = []

    try:
        for entry in entries:
            print(entry["word"])

            for attribute in entry["attributes"]:
                if attribute.get("similar"):
                    for similar in attribute["similar"]:
                        if similar not in [fe["word"] for fe in entries]:
                            similar_entry = {
                                "word": similar,
                                "attributes": [
                                    {
                                        "definition": "",
                                        "pos": attribute["pos"],
                                        "origin": None,
                                        "classification": None,
                                        "sources": attribute["sources"],
                                        "similar": [
                                            entry["word"],
                                        ],
                                        "opposite": [],
                                        "examples": [],
                                    }
                                ],
                            }
                            auto_matched_entries.append(similar_entry)
                            print("added " + similar_entry["word"])
                        else:
                            similar_entry = list(
                                filter(
                                    lambda entry: entry["word"] == similar,
                                    entries,
                                )
                            )[0]
                            for attribute in similar_entry["attributes"]:
                                if entry["word"] not in attribute["similar"]:
                                    attribute["similar"].append(entry["word"])

                if attribute.get("opposite"):
                    for opposite in attribute["opposite"]:
                        if opposite not in [fe["word"] for fe in entries]:
                            opposite_entry = {
                                "word": opposite,
                                "attributes": [
                                    {
                                        "definition": "",
                                        "pos": attribute["pos"],
                                        "origin": None,
                                        "classification": None,
                                        "sources": attribute["sources"],
                                        "similar": [],
                                        "opposite": [
                                            entry["word"],
                                        ],
                                        "examples": [],
                                    }
                                ],
                            }
                            auto_matched_entries.append(opposite_entry)
                            print("added " + opposite_entry["word"])
                        else:
                            opposite_entry = list(
                                filter(
                                    lambda entry: entry["word"] == opposite,
                                    entries,
                                )
                            )[0]
                            for attribute in opposite_entry["attributes"]:
                                if entry["word"] not in attribute["opposite"]:
                                    attribute["opposite"].append(entry["word"])

    except KeyboardInterrupt:
        pass

    return auto_matched_entries
