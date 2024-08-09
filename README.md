# English Dictionary Parser

**A Python script that parses an English dictionary in XML format and converts it into several useful formats.**


## About

This parser parses the dictionary from [GCIDE](https://www.ibiblio.org/webster/) in XML format and outputs it to [JSON format](output/eng_dictionary.json), [frequency list](output/eng_freqlist.csv), and [word list](output/eng_wordlist.txt).

## Output

> <strong style="font-size: large;">103,396 words collected</strong> <small>(as of 08/09/2024)</small>

| Resource | Format | Link |
| --- | --- | --- |
| Dictionary | json | [output/eng_dictionary.json](output/eng_dictionary.json) |
| Frequency list | csv | [output/eng_freqlist.csv](output/eng_freqlist.csv) |
| Word list | txt | [output/eng_wordlist.txt](output/eng_wordlist.txt) |


### JSON Dictionary

The JSON dictionary is structured as a list of words and its corresponding list of attributes. The attributes include part of speech, definition, etymology, classifications, synonyms, antonyms, example sentences, inflections, and sources. The entries are sorted alphabetically.

```json
[
    {
        "word": "The word itself",
        "attributes": [
            {
                "pos": "Simplified arts of speech",
                "definition": "The definition",
                "origin": "The etymology",
                "classification": "Any classification",
                "similar": [
                    "List of synonyms"
                ],
                "opposite": [
                    "List of antonyms"
                ],
                "examples": [
                    "List of example sentences that use the word"
                ],
                "inflections": [
                    "List of inflected forms"
                ],
                "sources": [
                    "List of sources"
                ]
            }
        ]
    },
]
```


### Frequency list

The frequency list is structured as a list of words and its corresponding frequency value derived from the [Leipzig Corpora Collection Dataset (2021 Wikipedia 100k corpus)](https://wortschatz.uni-leipzig.de/en/download/English). The list is sorted from highest to lowest frequency value.

```csv
the,101717
of,43438
in,37524
```


### Word list

The word list is simply the list of words sorted alphabetically.


## License

This project is licensed under the [Apache License](LICENSE).

---

For more information contact [maagmaandrian@gmail.com](mailto:maagmaandrian@gmail.com) with any additional questions or comments.