import sys
from collections import defaultdict

class BedSorter:
    def __init__(self, selection_file):
        self.selection_file = selection_file
        self.chrom_order = []      # List to store the order (e.g., chr1, chr2...)
        self.chrom_set = set()     # Set for fast lookup/filtering
        self.buckets = defaultdict(list) # The "filing cabinet"

    def load_rules(self):
        """Reads the rulebook file to establish order and filter list."""
        try:
            with open(self.selection_file, "r") as f:
                for line in f:
                    chrom = line.strip()
                    if chrom:
                        self.chrom_order.append(chrom)
                        self.chrom_set.add(chrom)
        except FileNotFoundError:
            sys.stderr.write(f"Error: Rulebook '{self.selection_file}' not found.\n")
            sys.exit(1)

    def process_input(self, input_stream):
        """Reads lines from stdin and buckets them if they match the rules."""
        for raw_line in input_stream:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split('\t')
            
            # Basic BED validation (needs at least 3 columns: chr, start, end)
            if len(parts) < 3:
                continue

            chrom = parts[0]
            
            # Filter: Only keep if it's in our rulebook
            if chrom in self.chrom_set:
                try:
                    start = int(parts[1])
                    end = int(parts[2])
                    
                    # Store as a tuple: (start, end, original_text)
                    # Storing 'end' allows for a cleaner secondary sort later
                    self.buckets[chrom].append((start, end, raw_line))
                except ValueError:
                    continue # Skip lines with non-integer coordinates

    def write_output(self, output_stream):
        """Sorts each bucket and writes to the output stream."""
        # Iterate through the CHROMOSOME ORDER list (not the dictionary keys)
        # This ensures the output order matches the rulebook exactly.
        for chrom in self.chrom_order:
            
            # Get the list of lines for this chromosome
            entries = self.buckets.get(chrom, [])
            
            # Sort the list. 
            # Python sorts tuples element-by-element:
            # 1. First by 'start'
            # 2. If starts are equal, then by 'end'
            entries.sort() 

            # Write the lines
            for _, _, original_line in entries:
                output_stream.write(original_line)

def main():
    # 1. Initialize the Sorter
    sorter = BedSorter("standard_selection.tsv")
    
    # 2. Load Rules
    sorter.load_rules()
    
    # 3. Process Data (Pipe in from stdin)
    sorter.process_input(sys.stdin)
    
    # 4. Write Data (Pipe out to stdout)
    sorter.write_output(sys.stdout)

if __name__ == "__main__":
    main()