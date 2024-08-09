import concurrent.futures
import json
import os
import string
import sys
from html import unescape
from itertools import repeat
from bs4 import BeautifulSoup

from helpers import *


script_dir = os.path.dirname(os.path.realpath(__file__))


def parse_all(folder_path=os.path.join(script_dir, "data/gcide/"), auto_match=False):
    """Parses every dictionary entry from XML files to a list.

    Args:
        folder_path (str, optional): The path to the folder containing the XML files. Defaults to '<script_dir>/data/gcide/'.
        auto_match (bool, optional): Performs auto matching if True, does not if False. Defaults to False

    Returns:
        list: A list of dictionaries, each representing a dictionary entry containing:
            - 'word': The word
            - 'pos': Parts of Speech
            - 'definitions': List of definitions
            - 'origin': Origin or etymology
            - 'classification': Some classification
            - 'similar': List of similar words
            - 'opposite': List of opposite
            - 'examples': List of examples
            - 'inflections': List of inflections
            - 'sources': List of sources

    Notes:
        Data source: GCIDE_XML (https://www.ibiblio.org/webster/)
    """
    starting_letters = set(string.ascii_lowercase)

    dictionary = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(parse_letter, repeat(folder_path), starting_letters)

        for result in results:
            dictionary.extend(result)

    if auto_match:
        return auto_match_entries(dictionary)

    return dictionary


def parse_letter(folder_path, letter):
    """Parses every dictionary entry that starts with a specified letter from an XML file to a list.

    Args:
        folder (str): The path to the folder containing the XML files.
        letter (str): Any letter in the English alphabet.

    Returns:
        list: A list of dictionaries of the extracted dictionary entries.
    """
    letter = letter.strip().lower()

    with open(os.path.join(folder_path, f"gcide_{letter}.xml")) as in_file:
        content = in_file.read()

    soup = BeautifulSoup(content, "lxml")

    entries = soup.find_all("p")

    data = []

    for entry in entries:
        if new_entry := parse_entry(entry):

            # New word
            if new_entry["word"]:
                data.append(new_entry)

            # Previous word if word not present and there's a previous word
            elif len(data) >= 1:
                data[-1]["attributes"].extend(new_entry["attributes"])

    return data


def parse_entry(entry):
    """Parses a dictionary entry.

    Args:
        entry (bs4.BeautifulSoup): The dictionary entry.

    Returns:
        dict: A dictionary containing the word and its attributes.
    """
    # Find attributes
    if word_xml := entry.find("ent"):
        word = word_xml.text.strip()

        if not is_valid(word):
            return None

        print(word)
    else:
        word = None

    pos_xml = entry.find("pos")
    definitions_xml = entry.find_all("def")
    origin_xml = entry.find("ety")
    similar_xml = entry.find("syn")
    opposite_xml = entry.find("ant")
    sources_xml = entry.find_all("source")
    example_xml = entry.find("q") if entry.find("qex") else None

    # Convert and format attributes
    pos = format_pos(pos_xml.text.strip()) if pos_xml else None

    definitions = (
        [to_sentence(unescape(def_xml.text.strip())) for def_xml in definitions_xml]
        if definitions_xml
        else []
    )

    origin = unescape(origin_xml.text.strip(" []")) if origin_xml else None

    classification = None

    similar = (
        [
            word.strip().lower()
            for word in similar_xml.text.replace("Syn. --", "").strip().split(",")
            if " " not in word.strip()
        ]
        if similar_xml
        else []
    )

    opposite = (
        [
            word.strip().lower()
            for word in opposite_xml.text.strip().split(";")
            if " " not in word.strip()
        ]
        if opposite_xml
        else []
    )

    sources = [src_xml.text.strip() for src_xml in sources_xml] if sources_xml else []

    examples = [unescape(example_xml.text.strip())] if example_xml else []

    # Save attributes
    attributes = []
    for definition in definitions:
        attributes.append(
            {
                "pos": pos,
                "definition": definition,
                "origin": origin,
                "classification": classification,
                "similar": similar,
                "opposite": opposite,
                "examples": examples,
                "inflections": [],
                "sources": sources,
            }
        )

    new_entry = {"word": word, "attributes": attributes}

    return new_entry


def export(
    dictionary,
    out_path=os.path.join(script_dir, "output/eng_dictionary.json"),
    overwrite=False,
):
    """Exports a list of dictionaries representing a dictionary entry to a JSON file.

    Args:
        dictionary (list): A list of dictionaries, each representing a dictionary entry.
        out_path (str, optional): The path to the output JSON file. Defaults to '<script_dir>/output/eng_dictionary.json'
        overwrite (bool, optional): Overwrites existing output file if True, otherwise if False. Defaults to False.

    Returns:
        bool: True if successful, False otherwise.
    """
    print("Exporting...")

    if not overwrite and os.path.isfile(out_path):
        permit = None
        while permit not in ["y", "n"]:
            permit = input(f"{out_path} already exists.\n Overwrite? (Y/n) ").lower()
            if permit == "n":
                sys.exit("Terminated")

    with open(out_path, "w") as out_file:
        json.dump(dictionary, out_file, indent=4, ensure_ascii=False)

    print("Exported successfully.")

    return True


if __name__ == "__main__":
    export(parse_all())
