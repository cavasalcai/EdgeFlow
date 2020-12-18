from ortools.sat.python import cp_model
import json
import math
from typing import List, Dict, Tuple, Any
import time

# typing aliases

IntVar = cp_model.CpModel.NewIntVar
CpModel = cp_model.CpModel
JSONdict = Dict[str, Any]  # Any here can be either str or List


def get_avail_resources(nodes: List[JSONdict]) -> Dict[int, Tuple[int, int, int]]:
    """
    Get the available resources of each individual node.
    :return: a dictionary having as key the node and as value a tuple (CPU, RAM, HDD)
    """
    avail_resources = dict()
    for n in nodes:
        avail_resources[int(n['id'])] = (int(n['CPU']), int(n['RAM']), int(n['HDD']))

    return avail_resources


def get_task_wcet(tasks: List[JSONdict]) -> Dict[str, Tuple[str, str]]:
    """
    Get the upper and lower bound of the WCET for each task.
    :param tasks: the list of tasks used in the application model
    :return: a dictionary where a key is the task and the value is (lower, upper)
    """
    wcet_dict = {}
    for t in tasks:
        wcet_low = t['WCET'][0]['l']
        wcet_up = t['WCET'][1]['u']
        wcet_dict[t['id']] = (wcet_low, wcet_up)

    return wcet_dict


def get_task_dependencies(flows: List[JSONdict]) -> Tuple[Dict[str, List[Tuple[str, str]]], Dict[str, int]]:
    """
    Get the two by two dependent tasks found in a flow.
    :param flows: a list of all flows for which we have to compute the e2e delay.
    :return: Two dictionaries:
            1. the key = the flow id and value = a list of tuples, where each tuple represents two
             dependent tasks.
            2. the key = the flow id and value = the maximum e2e delay allowed for the flow.
    """
    flows_dependent_tasks = {}
    flows_e2e = {}
    for f in flows:
        task_dependencies = []
        for t in f['path']:
            if t['dest'] != "":
                task_dependencies.append((t['src'], t['dest']))
        flows_dependent_tasks[f['id']] = task_dependencies
        flows_e2e[f['id']] = int(f['e2e'])
    return flows_dependent_tasks, flows_e2e


def initialize_dependent_vars_dict(flows_dependent_tasks: Dict[str, List[Tuple[str, str]]]) -> Dict[str, List[str]]:
    """
    Create a dictionary where all dependencies are initialized with empty strings.
    :param flows_dependent_tasks: the dependencies between tasks for each flow.
    :return: a dictionary where the key = the flow id and value = a list of empty strings.
    """

    task_variables_dict = {}

    for flow, dependent_tasks in flows_dependent_tasks.items():
        intern_list = []
        for pair in dependent_tasks:
            intern_lst = ['', '']
            intern_list.append(intern_lst)
        task_variables_dict[flow] = intern_list

    return task_variables_dict


def add_new_task_variable(flows_dependent_tasks: Dict[str, List[Tuple[str, str]]], task: str,
                          task_variable: IntVar, task_variables_dict: Dict[str, List[str]]) -> None:
    """
    Add new task variables to the task_variables_dict.
    :param flows_dependent_tasks: the dependencies between tasks for each flow.
    :param task: the task id taken from the application model
    :param task_variable: the IntVar model from the cp_model of the given task
    :param task_variables_dict: the target dict where we want to add the new task
    """
    for flow, dependent_tasks in flows_dependent_tasks.items():
        for i, pair in enumerate(dependent_tasks):
            if task in pair:
                idx = pair.index(task)
                task_variables_dict[flow][i][idx] = task_variable


def get_ports_for_tasks(flows: List[JSONdict]) -> Dict[str, Dict[str, List[str]]]:
    """
    Create a dictionary containing all ports used in a flow's execution path.
    :param flows: a list of flows and their paths.
    :return: a dictionary where key = flow id and value represents a dictionary with key = task and value = the input
     and output ports [in, out].
    """
    port_dict = {}
    for flow in flows:
        internal_port_dict = {}
        for t in flow['path']:
            if t['port'][1]['output'] != "":
                internal_port_dict[t['src']] = [t['port'][0]['input'], t['port'][1]['output']]
        port_dict[flow['id']] = internal_port_dict
    return port_dict


def get_task_latency(tasks: List[JSONdict], flows_dependent_tasks: Dict[str, List[Tuple[str, str]]],
                     nodes: List[JSONdict],
                     flow_ports: Dict[str, Dict[str, List[str]]]) -> Tuple[Dict[str, int], Dict[str, List[int]]]:
    """
    Get the data size sent by each task.
    :param tasks: the list of tasks.
    :param flows_dependent_tasks: a dictionary that has all pairs of dependent tasks for each flow.
    :param nodes: a list of nodes found in the network topology.
    :param flow_ports: a dictionary containing all ports used in a flow.
    :return: two dictionaries used to hold the latency in relation with the task mapping and their dependencies.
    """
    latency_dict = {}  # e.g., key = t1_t2_n1_n2 and value = 15, i.e., t1 is mapped on n1 and t2 on n2 latency = 15
    domain_latency = {}  # for each pair of dependent tasks we create a domain list of possible latencies

    for flow, dependencies in flows_dependent_tasks.items():
        for dependent_tasks in dependencies:
            for t in tasks:
                if t['id'] == dependent_tasks[0]:
                    for output_port in t['ports'][1]['output']:
                        if flow_ports[flow][t['id']][1] in output_port:
                            internal_task_data = int(output_port[flow_ports[flow][t['id']][1]]['data_size'])
                    break
            key_tasks = dependent_tasks[0] + '_' + dependent_tasks[1]
            domain = set()
            for n in nodes:
                key = dependent_tasks[0] + '_' + dependent_tasks[1] + '_' + n['id'] + '_' + n['id']
                latency_dict[key] = 0
                domain.add(0)
                for idx, node in enumerate(n['connections']):
                    key = dependent_tasks[0] + '_' + dependent_tasks[1] + '_' + n['id'] + '_' + node['id']
                    crt_dest_node = node['id']
                    latency = internal_task_data / int(n['bandwidth'][idx][crt_dest_node])
                    latency_dict[key] = math.ceil(latency)
                    domain.add(latency)
            domain_latency[key_tasks] = list(domain)
    return latency_dict, domain_latency


def create_cp_model(app_model_file: str, edge_file: str,
                    flow_constraints_file: str) -> Tuple[CpModel, List[IntVar], Dict[str, List[IntVar]]]:
    """
    Generate the cp_model from the three input files.
    :param app_model_file: The name of the application model input file.
    :param edge_file: The name of the edge computing platform input file.
    :param flow_constraints_file: The name of the flow constraints input file.
    :return: The CP model as well as a two data structures used for printing the solution:
                (i) a list containing the component variables
                (ii) a dict where key = flow id and value is a list containing both latency and WCET variables
    """
    tasks = []
    nodes = []
    flows = []
    tsk_vars = []
    nodes_used_resources = {}
    bool_helpers = {}
    flows_vars = {}
    bool_helpers_and = {}
    optimize_e2e = []

    with open('inputFiles/applications/' + app_model_file + '.json') as f:
        app_desc = json.load(f)

    with open('inputFiles/edgePlatforms/' + edge_file + '.json') as f:
        network = json.load(f)

    with open('inputFiles/flowsConstraints/' + flow_constraints_file + '.json') as f:
        flows_const = json.load(f)

    for t in app_desc['application']['components']:
        tasks.append(t)

    for n in network['network']['nodes']:
        nodes.append(n)

    for f in flows_const['constraints']['flows']:
        flows.append(f)

    flows_dependent_tasks, flows_e2e = get_task_dependencies(flows)

    # intialize the task_variables_dict with empty strings for every pair found in each flow
    task_variables_dict = initialize_dependent_vars_dict(flows_dependent_tasks)

    flow_ports = get_ports_for_tasks(flows)
    mapping_latency_dict, tasks_domain_latency = get_task_latency(tasks, flows_dependent_tasks, nodes, flow_ports)

    tasks_wcet = get_task_wcet(tasks)
    nodes_avail_resources = get_avail_resources(nodes)

    model = cp_model.CpModel()

    CONST_ZERO = model.NewConstant(0)

    # create the variables

    # create the variables required to compute the e2e delay for each flow
    for f in flows:
        e2e_delay = []
        bool_and = []

        # add the communication latency of each dependent pair of a flow
        for pair in flows_dependent_tasks[f['id']]:
            key_tasks = pair[0] + '_' + pair[1]
            communication_latency = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(tasks_domain_latency[key_tasks]),
                key_tasks + '_communication_latency')
            bool_helper_and = model.NewBoolVar(key_tasks + '_bool_and')
            bool_and.append(bool_helper_and)
            e2e_delay.append(communication_latency)

        # add a variable for the wcet of each task.
        for tsk in f['path']:
            task_wcet = model.NewIntVar(int(tasks_wcet[tsk['src']][0]), int(tasks_wcet[tsk['src']][1]), tsk['src'] +
                                        '_from_flow_' + f['id'])
            # search for wcet in decreasing value starting from the upper bound
            model.AddDecisionStrategy([task_wcet], cp_model.CHOOSE_FIRST, cp_model.SELECT_MAX_VALUE)
            e2e_delay.append(task_wcet)

        bool_helpers_and[f['id']] = bool_and
        flows_vars[f['id']] = e2e_delay

    # create the variables for each task and give the possible mappings nodes. for deployment
    nodes_len = len(nodes)
    for idx, t in enumerate(tasks):
        tsk_cpu = [0]
        tsk_ram = [0]
        tsk_hdd = [0]
        task = model.NewIntVar(0, nodes_len - 1, t['id'])
        tsk_vars.append(task)

        add_new_task_variable(flows_dependent_tasks, t['id'], task, task_variables_dict)

        tsk_cpu.append(int(t['CPU']))
        tsk_ram.append(int(t['RAM']))
        tsk_hdd.append(int(t['HDD']))

        # create a dict to track the used resources when a task is mapped on a node.
        for n in nodes:
            t_cpu = model.NewIntVarFromDomain(cp_model.Domain.FromValues(tsk_cpu), t['id'] + '_cpu_' + str(n['id']))
            t_ram = model.NewIntVarFromDomain(cp_model.Domain.FromValues(tsk_ram), t['id'] + '_ram_' + str(n['id']))
            t_hdd = model.NewIntVarFromDomain(cp_model.Domain.FromValues(tsk_hdd), t['id'] + '_hdd_' + str(n['id']))

            if int(n['id']) in nodes_used_resources:
                nodes_used_resources[int(n['id'])][0].append(t_cpu)
                nodes_used_resources[int(n['id'])][1].append(t_ram)
                nodes_used_resources[int(n['id'])][2].append(t_hdd)

            else:
                shared_CPU = []
                shared_RAM = []
                shared_HDD = []
                shared_CPU.append(t_cpu)
                shared_RAM.append(t_ram)
                shared_HDD.append(t_hdd)

                nodes_used_resources[int(n['id'])] = [shared_CPU, shared_RAM, shared_HDD]

        # constraints for deployment of tasks
        helpers_for_a_task = list()
        for i in range(nodes_len):
            bool_helper = model.NewBoolVar(t['id'] + '_bool_helper' + '_node_' + str(i))
            helpers_for_a_task.append(bool_helper)

            model.Add((task == i)).OnlyEnforceIf(bool_helper)
            model.Add((task != i)).OnlyEnforceIf(bool_helper.Not())
            model.Add((nodes_used_resources[i][0][idx] == int(t['CPU']))).OnlyEnforceIf(bool_helper)
            model.Add((nodes_used_resources[i][0][idx] == CONST_ZERO)).OnlyEnforceIf(bool_helper.Not())
            model.Add((nodes_used_resources[i][1][idx] == int(t['RAM']))).OnlyEnforceIf(bool_helper)
            model.Add((nodes_used_resources[i][1][idx] == CONST_ZERO)).OnlyEnforceIf(bool_helper.Not())
            model.Add((nodes_used_resources[i][2][idx] == int(t['HDD']))).OnlyEnforceIf(bool_helper)
            model.Add((nodes_used_resources[i][2][idx] == CONST_ZERO)).OnlyEnforceIf(bool_helper.Not())
        bool_helpers[task] = helpers_for_a_task

    # constraints for deployment of tasks
    for i in range(nodes_len):
        model.Add(sum(nodes_used_resources[i][0]) <= nodes_avail_resources[i][0])
        model.Add(sum(nodes_used_resources[i][1]) <= nodes_avail_resources[i][1])
        model.Add(sum(nodes_used_resources[i][2]) <= nodes_avail_resources[i][2])

    # constraints to consider e2e delay of flows
    for flow, dependent_tsk in task_variables_dict.items():
        for idx, pair_tsk in enumerate(dependent_tsk):
            first_task = flows_dependent_tasks[flow][idx][0]
            second_task = flows_dependent_tasks[flow][idx][1]
            for i in range(nodes_len):
                tmp_lst = list()
                tmp_lst.append(bool_helpers[pair_tsk[0]][i])
                for j in range(nodes_len):
                    tmp_lst.append(bool_helpers[pair_tsk[1]][j])
                    current_mapping = first_task + '_' + second_task + '_' + str(i) + '_' + str(j)
                    model.Add(flows_vars[flow][idx] == int(mapping_latency_dict[current_mapping])).OnlyEnforceIf(
                        tmp_lst)
                    del tmp_lst[-1]
        model.Add(sum(flows_vars[flow]) <= flows_e2e[flow])
        optimize_e2e.append(sum(flows_vars[flow]))

    # model.Minimize(sum(objectives))
    model.Minimize(sum(optimize_e2e))

    return model, tsk_vars, flows_vars


def print_solver_results(model: CpModel, tsk_vars: List[IntVar], flows_vars: Dict[str, List[IntVar]], file_name: str,
                         print_flag: bool, index: int, time_limit: int, find_optimal: bool, model_time: int) -> None:
    """
    Print the results either in a file or in the console.
    :param model: The CP model obtained from the three input files.
    :param tsk_vars: A list containing all components variables used in the CP model.
    :param flows_vars: A dictionary where the key = flow_id and the value is a list containing
            both latency and WCET variables.
    :param file_name: A list containing the component variables.
    :param print_flag: A flag to decide where to print the results.
    :param index: The test number.
    :param time_limit: The time limit for the solver to get a result in sec.
    :param find_optimal: A flag to decide if we want to find optimal solution.
    :param model_time: The total time required to build the CP model.
    """
    print('Find a deployment strategy...')

    solver = cp_model.CpSolver()

    if not find_optimal:
        # Sets a time limit for the solver to get a result, seconds.
        solver.parameters.max_time_in_seconds = time_limit

    status = solver.Solve(model)

    if print_flag:
        print('Status = {}'.format(solver.StatusName(status)))
        print('CP_model time = {} ms'.format(model_time))

        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            print('Total time was {} ms'.format(solver.WallTime() * 1000))
            for t in tsk_vars:
                print('comp {} = {}'.format(t, solver.Value(t)))
            print('=' * 40)
            for flow, vrs in flows_vars.items():
                print('Flow {} has the following:'.format(flow))
                for v in vrs:
                    print('{} = {}'.format(v, solver.Value(v)))
                print('=' * 40)
    else:
        print('Saving the results...')
        with open('results/' + file_name + '.txt', 'a+') as result_file:
            result_file.write('<' * 40 + '\r\n')
            result_file.write('Test = {} \r\n'.format(index))
            result_file.write('Network size = {} \r\n'.format(10 + index * 10))
            result_file.write('Status = {} \r\n'.format(solver.StatusName(status)))
            result_file.write('Model time = {} ms \r\n'.format(model_time))
            if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
                result_file.write('Total time was {} ms \r\n'.format(solver.WallTime() * 1000))
                for t in tsk_vars:
                    result_file.write('comp {} = {} \r\n'.format(t, solver.Value(t)))
                result_file.write('=' * 40 + '\r\n')
                for flow, vrs in flows_vars.items():
                    result_file.write('Flow {} has the following: \r\n'.format(flow))
                    for v in vrs:
                        result_file.write('{} = {} \r\n'.format(v, solver.Value(v)))
                    result_file.write('=' * 40 + '\r\n')
        print('Results for test {} are saved in the results folder!!'.format(index))


def millis():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    # for i in range(50):
    #     network_size = 10 + 10 * i
    #     print('Generating the CP model....')
    #     start_time = millis()
    #     model, tsk_vars, flows_vars = create_cp_model('application_model_30',
    #                                                   'network_topology_' + str(network_size),
    #                                                   'flow_constraints_app30_5')
    #     model_total_time = millis() - start_time
    #     print('Generating the CP model: Done!')
    #     print_solver_results(model, tsk_vars, flows_vars, 'results_app30_5_model_time', False, i, 5, True,
    #                          model_total_time)

    print('Generating the CP model....')
    start_time = millis()
    model, tsk_vars, flows_vars = create_cp_model('application_model_10',
                                                  'network_topology_10', 'flow_constraints_app10_1')
    model_total_time = millis() - start_time
    print('Generating the CP model: Done!')
    print_solver_results(model, tsk_vars, flows_vars, 'results_app30_1_feasible_120s', True, 9, 120, True,
                         model_total_time)