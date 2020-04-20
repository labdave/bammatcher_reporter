#!/usr/bin/env python3
import sys


def get_relatedness_info(reports):

    # Initialize unique sample set
    samples = set()

    # Initialize the relatedness table
    rel_table = {}

    for report in reports:

        # Obtain sample_ids
        _, sample_id1, sample_id2, _ = report.rsplit(".", 3)

        # Add samples to set
        samples.add(sample_id1)
        samples.add(sample_id2)

        # Extract the relatednes
        with open(report) as report_fp:
            for line in report_fp:

                # Identify the line with the fraction of common
                if "fraction of common" in line.lower():

                    # Obtain the fraction of common
                    rel_table[(sample_id1, sample_id2)] = line.split(":", 1)[1].strip().split()[0]

    # Convert samples to list and sort
    samples = list(samples)
    samples.sort()

    return samples, rel_table


def generate_relatedness_table(samples, rel_table):

    # Output the header
    print(",".join([""] + samples))

    # Obtain relatedness value according to sample order
    for sample1 in samples:

        # Initialize list of values for sample1
        values = [sample1]

        for sample2 in samples:

            # Skip certain pairs to ensure the output is an upper triangular matrix
            if sample1 > sample2:
                values.append(".")
                continue

            # Try to find the pair in the rel_table dictionary
            if (sample1, sample2) in rel_table:
                values.append(rel_table[(sample1, sample2)])
            elif (sample2, sample1) in rel_table:
                values.append(rel_table[(sample2, sample1)])
            else:
                values.append(".")

        # Output the values for sample1
        print(",".join(values))


def main():

    # Obtain the list of reports from arguments
    reports = sys.argv[1:]
    if not reports:
        sys.stderr.write("usage: ./{0} 1.report 2.report 3.report ...".format(sys.argv[0]))
        exit(1)

    # Obtain the relatedness info
    samples, rel_table = get_relatedness_info(reports)

    # Write table to file
    generate_relatedness_table(samples, rel_table)


if __name__ == "__main__":
    main()
