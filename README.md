# DNA Sequence Repeat Finder

This repository contains a Python script that processes DNA sequences by reading inputs from both plain text and FASTA files. It validates DNA sequences for the correct nucleotide characters (A, C, G, T) and identifies repeated substrings—specifically, consecutive identical nucleotides with a minimum repeat length of 2. The script is designed to handle both single DNA string inputs and multi-sequence FASTA files.

---

### Features

- **FASTA File Processing:**  
  Reads sequences from FASTA files where each sequence is preceded by a header (lines starting with `>`).

- **DNA Validation:**  
  Verifies that each DNA string contains only valid nucleotides (A, C, G, T).

- **Repeat Finder:**  
  Detects consecutive repeats in DNA sequences using Python's `itertools.groupby` and returns the start and end indices (0-based) of each repeated segment. If no repeats are found, `None` is returned.

- **Testing Suite:**  
  A set of pre-defined test cases using the function `check_example` validates various aspects of the pipeline:
  - Validates proper repeat detection.
  - Checks for duplicate sequences.
  - Handles errors such as empty or invalid DNA strings.

- **FASTA Test Case Generation:**  
  The function `generate_fasta_test_cases()` creates multiple FASTA test cases (including edge cases) and writes them to a file for further testing and performance evaluation.

- **Performance Considerations:**  
  The core repeat detection function operates in linear time (O(n)) with respect to the DNA sequence length. While efficient for small to moderate sequences, very long sequences or large FASTA files may pose memory constraints.

---

### Functions Overview

- **`read_fasta(file_path)`**  
  Reads a FASTA file and returns a list of DNA sequences (strings).

- **`is_valid_dna(dna_str)`**  
  Validates that the given DNA string contains only the nucleotides A, C, G, and T.

- **`find_repeats(dna_str)`**  
  Uses `itertools.groupby` to find and return a list of `[start, end]` pairs for repeated nucleotides in a DNA sequence. Returns `None` if no valid repeats (minimum length 2) are found.

- **`check_example(example_num, input_strings, expected_output)`**  
  Runs test cases by validating input strings, detecting duplicates, finding repeats, and comparing the actual output to the expected JSON-formatted output or error messages.

- **`process_fasta(file_path)`**  
  Processes a FASTA file by reading sequences, validating them, checking for duplicates, and identifying repeats. The results are returned as a dictionary.

- **`format_output(results)`**  
  Formats the output (results dictionary) as a JSON string.

- **`generate_fasta_test_cases()`**  
  Generates a set of FASTA test cases covering simple, duplicate, edge, and large sequence scenarios; saves these to a file named `fasta_test_cases.fasta`.

- **`main()`**  
  The main execution function that:
  - Runs pre-defined test cases.
  - Processes a FASTA file.
  - Prints formatted output.

---

### Requirements

- **Python Version:**  
  Python 3.x (recommended Python 3.7+)

- **Standard Libraries Used:**  
  - `json`
  - `re`
  - `itertools`
  - `random`

- **Additional Libraries:**  
  Although the core functionality uses standard libraries, you may integrate additional libraries (e.g., `pandas`) for extended functionalities.

---

### Usage

1. **Run the Script:**  
   To execute the script along with all the defined test cases and FASTA file processing, run:
   ```bash
   python your_script_name.py
