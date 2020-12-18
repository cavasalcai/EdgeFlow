import json
import random
from typing import List


def generate_topology(file_name: str, size: int, resources_range: List, bandwidth_range: List) -> None:
    """
    Generate a random network topology in JSON format.
    :param file_name: The name of the current topology file.
    :param size: The total number of nodes.
    :param resources_range: The range [low, up] from which the node's available resources are chosen.
    :param bandwidth_range: The range [low, up] from which the connection's bandwidth is chosen.
    """

    network = {}
    nodes = []

    for i in range(size):

        node = dict()
        connections = []
        bandwidth = []

        # add id and available resources of node i
        node['id'] = str(i)
        node['CPU'] = str(random.randint(resources_range[0], resources_range[1]))
        node['RAM'] = str(random.randint(resources_range[0], resources_range[1]))
        node['HDD'] = str(random.randint(resources_range[0], resources_range[1]))

        # add connections between node i and all other nodes
        for j in range(size):
            if j != i:
                intern_dict_connection = dict()
                intern_dict_band = dict()

                intern_dict_connection['id'] = str(j)
                connections.append(intern_dict_connection)

                # add the bandwidth associated to each connection
                intern_dict_band[str(j)] = str(random.randint(bandwidth_range[0], bandwidth_range[1]))
                bandwidth.append(intern_dict_band)

        node['connections'] = connections
        node['bandwidth'] = bandwidth
        nodes.append(node)

    network['network'] = {'nodes' : nodes}

    with open('../inputFiles/edgePlatforms/' + file_name + '.json', 'w') as f:
        json.dump(network, f)


def generate_application(file_name: str, size: int, wcet_low_range: List, wcet_up_range: List,
                         resources_range: List, input_ports: int, output_ports: int,
                         period_range: List, data_size: List) -> None:
    """
    Generate random application model file in JSON format.
    :param file_name: The name of the current application file.
    :param size: The total number of components.
    :param wcet_low_range: The range [low, up] for the components's WCET lowerbound.
    :param wcet_up_range: The range [low, up] for the components's WCET upperbound.
    :param resources_range: The range [low, up] from which the component's resource requirements are chosen.
    :param input_ports: The number of input ports a component has.
    :param output_ports: The number of output ports a component has.
    :param period_range: The range [low, up] from which the component's period is chosen.
    :param data_size: The range [low, up] from which the port's data size is chosen.
    """
    
    application = {}
    components = []
    for i in range(size):
        component_descr = dict()
        ports = []
        input_ports_list = []
        output_ports_list = []
        
        component_descr['id'] = 'c' + str(i)
        component_descr['CPU'] = str(random.randint(resources_range[0], resources_range[1]))
        component_descr['RAM'] = str(random.randint(resources_range[0], resources_range[1]))
        component_descr['HDD'] = str(random.randint(resources_range[0], resources_range[1]))
        wcet_low = str(random.randint(wcet_low_range[0], wcet_low_range[1]))
        wcet_up = str(random.randint(wcet_up_range[0], wcet_up_range[1]))
        component_descr['WCET'] = [{'l': wcet_low}, {'u': wcet_up}]

        for p in range(input_ports):
            intern_dict = {}

            comp_period = str(random.randint(period_range[0], period_range[1]))
            ip_data_size = str(random.randint(data_size[0], data_size[1]))
            intern_dict['IN' + str(p)] = {'period': comp_period, 'data_size': ip_data_size}
            input_ports_list.append(intern_dict)
        ports.append({'input': input_ports_list})

        for p in range(output_ports):
            intern_dict = {}

            comp_period = str(random.randint(period_range[0], period_range[1]))
            ip_data_size = str(random.randint(data_size[0], data_size[1]))
            intern_dict['OUT' + str(p)] = {'period': comp_period, 'data_size': ip_data_size}
            output_ports_list.append(intern_dict)
        ports.append({'output': output_ports_list})

        component_descr['ports'] = ports

        components.append(component_descr)

    application['application'] = {'components': components}

    with open('../inputFiles/applications/' + file_name + '.json', 'w') as f:
        json.dump(application, f)


def generate_flow_constraints(file_name: str, no_flows: int, app_model: str, e2e: int) -> None:
    """
    Generate the flow constraints input file in JSON format.
    :param file_name: The name of the flow constraint file.
    :param no_flows: The total number of flows.
    :param app_model: The file name of the application model file.
    :param e2e: The e2e delay for all flows.
    """

    constraints = {}
    flows = []
    flow = {}
    components = []

    with open('../inputFiles/applications/' + app_model + '.json', 'r') as f:
        app = json.load(f)

    for c in app['application']['components']:
        components.append(c)

    flow['id'] = 'f1'
    flow['e2e'] = str(e2e)

    path = []

    for i in range(1, len(components)):
        internal_dict = dict()

        internal_dict['src'] = components[i - 1]['id']
        internal_dict['dest'] = components[i]['id']
        input_port = [key for key in random.choice(components[i - 1]['ports'][0]['input'])][0]
        output_port = [key for key in random.choice(components[i - 1]['ports'][1]['output'])][0]
        internal_dict['port'] = [{'input': input_port}, {'output': output_port}]
        path.append(internal_dict)
    else:
        internal_dict = dict()
        internal_dict['src'] = components[i]['id']
        internal_dict['dest'] = ''
        input_port = [key for key in random.choice(components[i]['ports'][0]['input'])][0]
        output_port = ''
        internal_dict['port'] = [{'input': input_port}, {'output': output_port}]
        path.append(internal_dict)

    flow['path'] = path

    flows.append(flow)

    if no_flows > 1:
        for f in range(no_flows - 1):
            flow = dict()
            path = []

            flow['id'] = 'f' + str(f + 2)
            flow['e2e'] = str(e2e)
            # choose randomly the total number of components used in the creation of a path.
            path_length = random.choice(range(2, len(components) - 1))
            participating_comps = sorted(random.sample(components, k=path_length), key=lambda k: k['id'])

            for i in range(1, len(participating_comps)):
                internal_dict = dict()

                internal_dict['src'] = participating_comps[i - 1]['id']
                internal_dict['dest'] = participating_comps[i]['id']
                input_port = [key for key in random.choice(participating_comps[i - 1]['ports'][0]['input'])][0]
                output_port = [key for key in random.choice(participating_comps[i - 1]['ports'][1]['output'])][0]
                internal_dict['port'] = [{'input': input_port}, {'output': output_port}]
                path.append(internal_dict)
            else:
                internal_dict = dict()
                internal_dict['src'] = participating_comps[i]['id']
                internal_dict['dest'] = ''
                input_port = [key for key in random.choice(participating_comps[i]['ports'][0]['input'])][0]
                output_port = ''
                internal_dict['port'] = [{'input': input_port}, {'output': output_port}]
                path.append(internal_dict)

            flow['path'] = path

            flows.append(flow)

    constraints['constraints'] = {'flows': flows}

    with open('../inputFiles/flowsConstraints/' + file_name + '.json', 'w') as f:
        json.dump(constraints, f)


if __name__ == '__main__':

    # for i in range(50):
    #     size = 10 + i * 10
    #     print('size = ', size)
    #     generate_topology('edge_platform_' + str(size), size, [15, 30], [30, 90])
    generate_topology('edge_platform_' + str(1400), 1400, [15, 30], [30, 90])
    # generate_application('application_model_10', 10,  [4, 10], [10, 12], [5, 15], 2, 2, [10, 30], [30, 120])
    # generate_flow_constraints('flow_constraints_app30_3', 3, 'application_model_30', 500)



