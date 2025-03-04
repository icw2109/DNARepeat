# DNA Repeat Finder using Suffix Trees
# Input file format: Each DNA string is on a separate line.
# Indexing: Zero-based indexing.

class DNARepeatFinder:
    class SuffixTreeNode:
        def __init__(self, start, end):
            self.children = {}
            self.start = start
            self.end = end
            self.suffix_link = None

    class SuffixTree:
        def __init__(self, text):
            self.text = text + '$'  # Add a unique end character to mark the end of the string
            self.root = DNARepeatFinder.SuffixTreeNode(-1, -1)  # The root node
            self.build_suffix_tree()  # Build the tree upon initialization

        def build_suffix_tree(self):
            n = len(self.text)
            # Active variables used in Ukkonen's algorithm
            active_node = self.root
            active_edge = -1
            active_length = 0
            remainder = 0  # Number of suffixes to be added
            last_new_node = None

            for i in range(n):
                # Extending the suffix tree for the new character text[i]
                remainder += 1
                last_new_node = None

                while remainder > 0:
                    if active_length == 0:
                        active_edge = i

                    if self.text[active_edge] not in active_node.children:
                        # Create a new leaf node
                        active_node.children[self.text[active_edge]] = DNARepeatFinder.SuffixTreeNode(i, n)
                        if last_new_node:
                            last_new_node.suffix_link = active_node
                            last_new_node = None
                    else:
                        # There is an existing edge, so we need to walk down the tree
                        next_node = active_node.children[self.text[active_edge]]
                        edge_length = next_node.end - next_node.start

                        if active_length >= edge_length:
                            active_edge += edge_length
                            active_length -= edge_length
                            active_node = next_node
                            continue

                        if self.text[next_node.start + active_length] == self.text[i]:
                            # There is already a match, increment active_length
                            active_length += 1
                            if last_new_node:
                                last_new_node.suffix_link = active_node
                                last_new_node = None
                            break

                        # Split the edge and create a new internal node
                        split_node = DNARepeatFinder.SuffixTreeNode(next_node.start, next_node.start + active_length)
                        active_node.children[self.text[active_edge]] = split_node
                        split_node.children[self.text[i]] = DNARepeatFinder.SuffixTreeNode(i, n)
                        next_node.start += active_length
                        split_node.children[self.text[next_node.start]] = next_node

                        if last_new_node:
                            last_new_node.suffix_link = split_node

                        last_new_node = split_node

                    remainder -= 1

                    if active_node == self.root and active_length > 0:
                        active_length -= 1
                        active_edge = i - remainder + 1
                    else:
                        active_node = active_node.suffix_link if active_node.suffix_link else self.root

        def find_repeats(self):
            """Find all repeated substrings in the suffix tree."""
            repeats = []

            def dfs(node, current_string):
                # A node with more than one child indicates a repeated substring
                if len(node.children) > 1 and node != self.root:
                    # The substring represented by this node is repeated
                    for child in node.children.values():
                        if child.end - child.start > 0:
                            start_pos = child.start - len(current_string)
                            end_pos = child.start + child.end - child.start - 1
                            if end_pos > start_pos:
                                repeats.append((start_pos, end_pos))
                for char, child in node.children.items():
                    edge_length = child.end - child.start
                    dfs(child, current_string + self.text[child.start:child.start + edge_length])

            dfs(self.root, "")
            # Remove duplicates and sort the repeats
            repeats = list(set(repeats))
            repeats.sort()
            return repeats if repeats else None

    def __init__(self, file_path):
        self.file_path = file_path
        self.dna_strings = []
        self.results = {}
        self.error = None

    def read_dna_file(self):
        """Read DNA strings from a file, one per line."""
        try:
            with open(self.file_path, 'r') as file:
                self.dna_strings = [line.strip().upper() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            self.error = f"Error: File {self.file_path} not found."

    def check_duplicates(self):
        """Check for duplicates in the list of DNA strings."""
        seen = set()
        for dna in self.dna_strings:
            if dna in seen:
                self.error = "Error: Duplicate input!"
                return
            seen.add(dna)

    def validate_dna_strings(self):
        """Validate DNA strings to contain only A, C, G, T."""
        import re
        for dna in self.dna_strings:
            if not re.fullmatch(r'[ACGT]+', dna):
                self.error = f"Error: Invalid DNA string '{dna}' detected!"
                return

    def process_dna_strings(self):
        """Process the list of DNA strings and detect repeats."""
        if self.error:
            return

        self.check_duplicates()
        if self.error:
            return

        self.validate_dna_strings()
        if self.error:
            return

        for dna in self.dna_strings:
            suffix_tree = self.SuffixTree(dna)
            repeats = suffix_tree.find_repeats()
            self.results[dna] = repeats

    def output_results(self):
        """Output the results or error message."""
        if self.error:
            print(self.error)
        else:
            for dna, repeats in self.results.items():
                if repeats:
                    print(f"DNA: {dna}, Repeats: {repeats}")
                else:
                    print(f"DNA: {dna}, No Repeats")

    def run(self):
        """Run the DNA Repeat Finder."""
        self.read_dna_file()
        if self.error:
            print(self.error)
            return
        self.process_dna_strings()
        self.output_results()

# Usage
if __name__ == "__main__":
    # Input file path
    file_path = "dna_strings.txt"
    dna_repeat_finder = DNARepeatFinder(file_path)
    dna_repeat_finder.run()
