import random

def generate_fasta_test_cases():
    test_cases = []
    
    # Example #1: Simple string with repeat
    test_cases.append((">Example1\nATCGGGGACGA"))

    # Example #2: Duplicate input
    test_cases.append((">Example2_1\nATCGGGGACGA\n>Example2_2\nATCGGGGACGA"))

    # Example #3: Multiple strings
    test_cases.append((">Example3_1\nATCGGGGACGA\n>Example3_2\nATTTTCGGGGACGA\n>Example3_3\nATGCATCGATCG"))

    # Additional edge cases
    test_cases.append((">EdgeCase1\n" + "A" * 10000))
    test_cases.append((">EdgeCase2\n" + "AT" * 5000))
    test_cases.append((">EdgeCase3\n" + "ACGT" * 2500))
    test_cases.append((">EdgeCase4\n" + "G" * 10000))
    random_seq = ''.join(random.choices("ACGT", k=10000))
    test_cases.append((">EdgeCase5\n" + random_seq))
    test_cases.append((">EdgeCase6_1\nA\n>EdgeCase6_2\nC\n>EdgeCase6_3\nG\n>EdgeCase6_4\nT"))
    test_cases.append((">EdgeCase7\nAAAAACGTCGTCGTCGTCGT"))
    test_cases.append((">EdgeCase8\nATCGATCGTTTTAAAA"))
    test_cases.append((">EdgeCase9\nATATCGCGCGCGAT"))
    test_cases.append((">EdgeCase10_1\n" + "A" * 100 + "\n>EdgeCase10_2\n" + "C" * 1000 + "\n>EdgeCase10_3\n" + "G" * 10000))

    # Save the test cases into a file in correct FASTA format
    with open("fasta_test_cases.fasta", "w") as file:
        for fasta_content in test_cases:
            file.write(f"{fasta_content}\n\n")

    print("FASTA test cases have been generated and saved to 'fasta_test_cases.fasta'.")

# Generate and save the FASTA test cases
generate_fasta_test_cases()
