import sys
from anubis.results_utils.results_utils_arguments import parse_arguments
from anubis import results


if __name__ == '__main__':
    args = parse_arguments()
    results.create_aggregate(args.files, args.output_file)
    sys.exit(0)
