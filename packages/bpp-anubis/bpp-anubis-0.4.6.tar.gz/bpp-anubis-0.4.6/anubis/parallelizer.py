from subprocess import call
from .arg_parser import parse_arguments
import os


def command_generator(account_feature_groups: list) -> str:
    """
    Use args, accounts, and features to construct behave command
    :param account_feature_groups:
    :return:
    """

    # get arguments
    _known, _unknown = parse_arguments()

    # get data for constructing behave command
    process_name = account_feature_groups[0][0]
    acc = account_feature_groups[0][1].split()
    feature_set = account_feature_groups[1]

    # construct the behave command
    results_json_file = None
    commands = []

    op_retry = f'-D retry="{_known.retry}" ' if _known.retry > 1 else ' '
    op_browser = f'-D browser="{_known.browser}" -D headless="{_known.headless}" ' if _known.browser else ' '
    op_userdata = f'-D user="{acc[0]}" -D pass="{acc[1]}" ' if _known.account_file and _known.account_section else ' '
    tags = ' '.join('--tags="@{}" '.format(t) for t in _known.itags) + ' '.join('--tags="~@{}" '.format(t) for t in _known.etags)
    unknown_args = (' '.join([f"-D {arg}" for arg in _unknown]) if _unknown else ' ') + ' '
    results_json_file = os.path.join(_known.output_dir, f'{process_name}.json')
    features_string = ' '.join("\"{}\"".format(feature_path) for feature_path in feature_set)

    cmd = (f'behave -D parallel="True" -D env="{_known.env}" ' + op_retry + op_browser + op_userdata +
           tags + ' ' + unknown_args + f'-f json.pretty -o {results_json_file} ' + f'-D output="{_known.output_dir}" ' +
           features_string)
    commands.append(cmd)

    # run the command(s)
    for command in commands:
        print(command, end='\n\n')

    for command in commands:
        r = call(command, shell=True)

    return results_json_file
