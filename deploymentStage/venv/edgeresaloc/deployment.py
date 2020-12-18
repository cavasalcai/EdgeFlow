import argparse
from resourceAllocation.resourceAllocation import create_cp_model, print_solver_results, millis


def parse_args():
    """
    Create the options and parse the arguments given as input by the user.
    :return: an argparse object.
    """

    parser = argparse.ArgumentParser(description="Find an optimal or feasible deployment strategy such that all "
                                                 "application's requirements are satisfied.")
    parser.add_argument('-f', '--flows_file', type=str, help='Give the name of the flow constraints file.',
                        required=True)
    parser.add_argument('-a', '--application_file', type=str, help='Give the name of the application model file.',
                        required=True)
    parser.add_argument('-e', '--edge_platform', type=str, help='Give the name of the edge computing platform file.',
                        required=True)
    parser.add_argument('-r', '--results_file', type=str, help='Give the name of the file where results are saved. '
                                                               'The default is: results_file.',
                        default='results_file')
    parser.add_argument('-i', '--test_index', type=int, help='Give the current test number.', default=1)
    parser.add_argument('-s', '--stdout', action='store_true', help='Print the results on the python console.'
                                                                    'The default value is False.')
    parser.add_argument('-t', '--time_limit', type=int, help='Set the maximum search time for the CP solver.')
    parser.add_argument('-o', '--optimal_strategy', help='Find the optimal deployment strategy. '
                                                         'The default value is False.'
                        , action='store_true')

    args = parser.parse_args()

    return args


def main(parsed_args):
    app_file = parsed_args.application_file
    edge_file = parsed_args.edge_platform
    flows_file = parsed_args.flows_file
    res_file = parsed_args.results_file
    test_index = parsed_args.test_index
    print_flag = parsed_args.stdout
    time_limit = parsed_args.time_limit
    optimal_flag = parsed_args.optimal_strategy

    print(f'print_flag {print_flag}')
    print(f'optimal {optimal_flag}')

    if not app_file or not edge_file or not flows_file:
        print(f'Please provide a filename for all options!')
        return 0

    if not optimal_flag and time_limit is None:
        print(f'When -o/--optimal_strategy not provided, the option -t/--time_limit is required.'
              f' Please set -t to a value using the short option -t or --time_limit.')
        return 0

    print('Generating the CP model....')
    start_time = millis()
    model, tsk_vars, flows_vars = create_cp_model(app_file, edge_file, flows_file)

    model_total_time = millis() - start_time
    print('Generating the CP model: Done!')

    print_solver_results(model, tsk_vars, flows_vars, res_file, print_flag, test_index, time_limit, optimal_flag,
                         model_total_time)


if __name__ == '__main__':
    given_args = parse_args()
    main(given_args)