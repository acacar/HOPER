# Preprocess

==TODO: Is this out of date, or in addition to the main readme?==

The aim of preprocess is extracting and editing the information of the xml files of the proteins.
Firstly, Uniprot database downloaded and the information of the subsections in the General annotation (Comments) was extracted.
Secondly, Pubmed references in the text were removed.
Finally, PubMed id’s and abstracts were parsed and saved.

## How to Run Preprocess

Step by step operation:

1. Download the Uniprot xml database: `https://www.uniprot.org/help/downloads`, unzip and place the **HOPER** file =TODO: Where?!?!=
1. Install dependencies(given below) =TODO: Did we not install them through conda?=
1. Edit the configuration file (Necessary adjustments (for example, giving the file location) =TODO: Which files? How?=
1. Run module main function i.e., `python preprocess_main.py`

### Dependencies

1. Python 3.7.3
2. Biopython 1.77 or greater

Output files will be created in the text_representations/preprocess/
