import json
import re
from itertools import groupby

# Summary:
# 
# This Python script reads DNA sequences from test inputs and FASTA files, validates 
# them, and identifies repeated substrings of consecutive identical nucleotides (minimum 
# repeat length = 2). It handles both single DNA string inputs and multi-sequence FASTA 
# files. Key functions include:
#
# 1. `read_fasta(file_path)`: Reads a FASTA file and returns a dictionary of sequence names and DNA sequences.
# 2. `is_valid_dna(dna_str)`: Ensures the DNA string contains only valid nucleotides (A, C, G, T).
#
# 3. `find_repeats(dna_str)`: Identifies consecutive identical nucleotides and returns their start and end indices (0-based).
# The function uses `groupby` from `itertools` to group consecutive identical nucleotides 
# in a DNA sequence. It records the start and end positions (0-based indexing) of each 
# repeat group. If no repeats (minimum length of 2) are found, it returns `None`. Otherwise, 
# it returns a list of [start, end] pairs.
#
# Performance Summary:
# The function operates in linear time, O(n), where n is the length of the DNA sequence, 
# since it processes each nucleotide once. It's efficient for short to moderate sequences, 
# but performance could degrade with extremely long sequences due to its need to process 
# the entire string in memory.
#
#
# 4. `check_example(example_num, input_strings, expected_output)`: Runs test cases by validating input DNA strings, detecting duplicates, finding repeats, and comparing actual and expected outputs.
# 5. `process_fasta(file_path)`: Processes a FASTA file, validates sequences, checks for duplicates, and finds repeats, returning the result as a JSON string.
# 6. `main()`: Executes predefined test cases and processes a FASTA file.
#
# Input File Format:
#    The input is a standard FASTA file with sequence names prefixed by '>' and DNA 
#    sequences on the following lines. Example:
#    >sequence_1
#    ATCGGGGACGA
#
# Indexing:
#    0-based indexing is used throughout, where the first character of the sequence 
#    is at index 0.
#
# Overall Performance:
# Efficient for small to moderate-sized DNA sequences. Handles small and medium FASTA files quickly, 
# though larger files might impact memory due to in-memory sequence storage. 
# Repeated file reads and processing may slow performance with large datasets or complex repeats.
#
# Limitations:
# Large FASTA files may strain memory, and the `find_repeats` function may slow down for very long sequences with extensive repeats.
#
# Potential Improvements:
# 1. **Memory Optimization**: For very large FASTA files, consider processing sequences in chunks or streaming the input file instead of loading everything into memory.
# 2. **Parallel Processing**: If handling multiple sequences, parallelizing the `find_repeats` function across sequences can improve performance.
# 3. More FASTA error handling for any potential errors in a FASTA files.


def read_fasta(file_path):
    """Reads a FASTA file and returns a list of sequences."""
    sequences = []
    current_sequence = ""
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if current_sequence:
                    sequences.append(current_sequence)
                current_sequence = ""
            else:
                current_sequence += line
    
    if current_sequence:
        sequences.append(current_sequence)
    
    return sequences

def is_valid_dna(dna_str):
    """Checks if the DNA string contains only valid nucleotides (A, C, G, T)."""
    return re.fullmatch(r'[ACGT]*', dna_str.upper()) is not None

def find_repeats(dna_str):
    """Finds repeated substrings of consecutive identical characters in a DNA string."""
    repeats = []
    for k, g in groupby(enumerate(dna_str), key=lambda x: x[1]):
        group = list(g)
        if len(group) >= 2: #Minimum repeat set to two. 
            start = group[0][0]
            end = group[-1][0]
            repeats.append([start, end])
    return repeats if repeats else None

#


def check_example(example_num, input_strings, expected_output):
    """Runs a test case and compares the actual output to the expected output."""
    print(f"Running Example #{example_num}:")
    # Normalize and validate DNA strings
    dna_strings = []
    dna_set = set()
    error_message = None
    for dna in input_strings:
        dna_upper = dna.strip().upper()
        if not dna_upper:
            error_message = "Error: Empty DNA string detected!"
            break
        if not is_valid_dna(dna_upper):
            error_message = f"Error: Invalid DNA string '{dna}' detected!"
            break
        if dna_upper in dna_set:
            error_message = "Error: Duplicate input!"
            break
        dna_set.add(dna_upper)
        dna_strings.append(dna_upper)

    if error_message:
        output = error_message
    else:
        output_dict = {}
        for dna in dna_strings:
            repeats = find_repeats(dna)
            output_dict[dna] = repeats
        # Convert the output dictionary to a JSON string with sorted keys
        output = json.dumps(output_dict, sort_keys=True)

    # Print expected and actual outputs
    print("Expected Output:")
    print(expected_output)
    print("\nActual Output:")
    print(output)

    # Compare the outputs
    if output == expected_output:
        print("\nTest Passed!")
    else:
        print("\nTest Failed!")

    print("\n" + "-" * 50 + "\n")

def process_fasta(file_path):
    """Processes a FASTA file and returns the results for all sequences."""
    sequences = read_fasta(file_path)
    results = {}
    dna_set = set()

    for seq in sequences:
        seq_upper = seq.strip().upper()
        if not seq_upper:
            results[seq] = "Error: Empty DNA string detected!"
        elif not is_valid_dna(seq_upper):
            results[seq] = "Error: Invalid DNA string detected!"
        elif seq_upper in dna_set:
            results[seq_upper] = "Error: Duplicate input!"
        else:
            dna_set.add(seq_upper)
            repeats = find_repeats(seq_upper)
            results[seq_upper] = repeats

    return results


def format_output(results):
    """Formats the results as a JSON string."""
    if len(results) == 1:
        key, value = next(iter(results.items()))
        if isinstance(value, str):  # Error message
            return json.dumps(value)
        else:
            return json.dumps({key: value})
    else:
        return json.dumps(results, indent=2)



def main():
    """Runs predefined test cases and processes FASTA file."""
    # Run test cases
    # Example #1
    input_strings_1 = ["ATCGGGGACGA"]
    expected_output_1 = '{"ATCGGGGACGA": [[3, 6]]}'
    check_example(1, input_strings_1, expected_output_1)

    # Example #2
    input_strings_2 = ["ATCGGGGACGA", "ATCGGGGACGA"]
    expected_output_2 = "Error: Duplicate input!"
    check_example(2, input_strings_2, expected_output_2)

    # Example #3
    input_strings_3 = [
        "ATCGGGGACGA",
        "ATTTTCGGGGACGA",
        "ATGCATCGATCG"
    ]
    expected_output_3 = '{"ATCGGGGACGA": [[3, 6]], "ATGCATCGATCG": null, "ATTTTCGGGGACGA": [[1, 4], [6, 9]]}'
    check_example(3, input_strings_3, expected_output_3)

    # Example #4: Invalid DNA String
    input_strings_4 = ["ATCGXGGGACGA"]
    expected_output_4 = "Error: Invalid DNA string 'ATCGXGGGACGA' detected!"
    check_example(4, input_strings_4, expected_output_4)

    # Example #5: Empty DNA String
    input_strings_5 = [""]
    expected_output_5 = "Error: Empty DNA string detected!"
    check_example(5, input_strings_5, expected_output_5)

    # Example #6: Short DNA Sequence (Less than 3 characters)
    input_strings_6 = ["AC"]
    expected_output_6 = '{"AC": null}'
    check_example(6, input_strings_6, expected_output_6)

    # Example #7: Single Character DNA Sequence
    input_strings_7 = ["AAAA"]
    expected_output_7 = '{"AAAA": [[0, 3]]}'
    check_example(7, input_strings_7, expected_output_7)

    # Example #8: No Repeats in the Sequence
    input_strings_10 = ["ACGTACGT"]
    expected_output_10 = '{"ACGTACGT": null}'
    check_example(10, input_strings_10, expected_output_10)

    # Example #9: Three DNA strings (two are the same)
    input_strings_13 = ["ATCGGGGACGA", "TTTAAACCCGGG", "ATCGGGGACGA"]
    expected_output_13 = "Error: Duplicate input!"
    check_example(13, input_strings_13, expected_output_13)

    # Example #10: Three DNA strings (all are the same)
    input_strings_14 = ["ATCGGGGACGA", "ATCGGGGACGA", "ATCGGGGACGA"]
    expected_output_14 = "Error: Duplicate input!"
    check_example(14, input_strings_14, expected_output_14)

    # Process FASTA file
    """Processes FASTA file and prints the results."""
    file_path = 'fasta_test_cases.fasta'
    fasta_results = process_fasta(file_path)
    print(format_output(fasta_results))


if __name__ == "__main__":
    main()









