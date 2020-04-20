#!/usr/bin/env python3
import sys


def get_info(reports):

    # Initialize unique sample set
    samples = set()

    # Initialize the relatedness and sites count tables
    rel_table = {}
    sites_count = {}

    for report in reports:

        # Obtain sample_ids
        _, sample_id1, sample_id2, _ = report.rsplit(".", 3)

        # Add samples to set
        samples.add(sample_id1)
        samples.add(sample_id2)

        # Extract the relatednes
        with open(report) as report_fp:
            for line in report_fp:

                # Identify the line with the total sites compared
                if "total sites compared" in line.lower():

                    # Obtain the sites count
                    sites_count[(sample_id1, sample_id2)] = line.split(":", 1)[1].strip()

                # Identify the line with the fraction of common
                elif "fraction of common" in line.lower():

                    # Obtain the fraction of common
                    rel_table[(sample_id1, sample_id2)] = line.split(":", 1)[1].strip().split()[0]

    # Convert samples to list and sort
    samples = list(samples)
    samples.sort()

    return samples, rel_table, sites_count


def generate_table(samples, table, output_file):

    with open(output_file, "w") as out:

        # Output the header
        out.write(",".join([""] + samples))
        out.write("\n")

        # Obtain values according to sample order
        for sample1 in samples:

            # Initialize list of values for sample1
            values = [sample1]

            for sample2 in samples:

                # Skip certain pairs to ensure the output is an upper triangular matrix
                if sample1 > sample2:
                    values.append(".")
                    continue

                # Try to find the pair in the table dictionary
                if (sample1, sample2) in table:
                    values.append(table[(sample1, sample2)])
                elif (sample2, sample1) in table:
                    values.append(table[(sample2, sample1)])
                else:
                    values.append(".")

            # Output the values for sample1
            out.write(",".join(values))
            out.write("\n")


def main():

    # Check if command was run correctly
    if len(sys.argv) <= 2:
        sys.stderr.write("usage: ./{0} <output_prefix> 1.report 2.report 3.report ...\n".format(sys.argv[0]))
        exit(1)

    # Obtain the data from arguments
    output_prefix = sys.argv[1]
    reports = sys.argv[2:]

    # Obtain the relatedness and sites count info
    samples, rel_table, sites_count = get_info(reports)

    # Write relatedness table to file
    out_file = "{0}.relatedness.csv".format(output_prefix)
    generate_table(samples, rel_table, out_file)

    # Write sites count table to file
    out_file = "{0}.sites_count.csv".format(output_prefix)
    generate_table(samples, sites_count, out_file)


if __name__ == "__main__":
    main()
