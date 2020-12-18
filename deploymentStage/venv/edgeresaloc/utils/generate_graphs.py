import matplotlib.pyplot as plt
from typing import List


def get_time(file_name: str) -> List[float]:
    times = []
    model_times = []
    with open('../results/' + file_name + '.txt', 'r') as f:
        for line in f.readlines():
            if line.startswith('Status'):
                status, status_type = line.split(' = ')
                if status_type.rstrip() == 'INFEASIBLE':
                    times.append(0)
            if line.startswith('Total time'):
                time = line.split()[3]
                times.append(int(float(time))/1000)
            if line.startswith('Model'):
                model_time = line.split()[3]
                model_times.append(int(float(model_time))/1000)
    return times, model_times


def generate_graph(time: List[List], topology_size: int, file_name: str) -> None:
    plt.plot(list(range(10, topology_size + 1, 10)), time[0], 'D-', markersize=5, label='app_10')
    plt.plot(list(range(10, topology_size + 1, 10)), time[1], 'o-', markersize=5, label='app_20')
    plt.plot(list(range(10, topology_size + 1, 10)), time[2], 'ks-', markersize=5, label='app_30')

    plt.xlabel('# of nodes')
    plt.ylabel('time [s]')
    plt.legend()
    plt.savefig('../results/figures/' + file_name + '.pdf')
    plt.show()


def generate_graph_flows(time: List[List], topology_size: int, app_size: int, file_name: str) -> None:
    plt.plot(list(range(10, topology_size + 1, 10)), time[0], 'D-', markersize=5, label='flow_1')
    plt.plot(list(range(10, topology_size + 1, 10)), time[1], 'o-', markersize=5, label='flow_3')
    plt.plot(list(range(10, topology_size + 1, 10)), time[2], 'ks-', markersize=5, label='flow_5')

    plt.xlabel('# of nodes')
    plt.ylabel('time [s]')
    plt.legend()
    plt.savefig('../results/figures/' + file_name + str(app_size) + '.pdf')
    plt.show()


if __name__ == '__main__':
    times_10_1, model_times_10_1 = get_time('results_app10_1_model_time')
    # print(len(times_10_1))
    print(times_10_1)
    print(model_times_10_1)
    times_20_1, model_times_20_1 = get_time('results_app20_1_model_time')
    # print(len(times_20_1))
    # print(times_20_1)
    times_30_1, model_times_30_1 = get_time('results_app30_1_model_time')
    # print(len(times_30_1))
    # print(times_30_1)

    times_10_1_total = [sum(grp) for grp in zip(times_10_1, model_times_10_1)]
    times_20_1_total = [sum(grp) for grp in zip(times_20_1, model_times_20_1)]
    times_30_1_total = [sum(grp) for grp in zip(times_30_1, model_times_30_1)]

    generate_graph([times_10_1_total, times_20_1_total, times_30_1_total], 500, 'deployment_1_flow_graph_total')
    # generate_graph([times_10_1, times_20_1, times_30_1], 500, 'deployment_1_flow_graph')
    # generate_graph([model_times_10_1, model_times_20_1, model_times_30_1], 500, 'deployment_1_flow_graph_module_time')

    # times_10_3, model_times_10_3 = get_time('results_app10_3_model_time')
    # print(len(times_10_3))
    # # print(times_10_1)
    # times_20_3, model_times_20_3 = get_time('results_app20_3_model_time')
    # print(len(times_20_3))
    # # print(times_20_1)
    # times_30_3, model_times_30_3 = get_time('results_app30_3_model_time')
    # print(len(times_30_3))
    #
    # times_10_5, model_times_10_5 = get_time('results_app10_5_model_time')
    # print(len(times_10_5))
    # # print(times_10_1)
    # times_20_5, model_times_20_5 = get_time('results_app20_5_model_time')
    # print(len(times_20_5))
    # # print(times_20_1)
    # times_30_5, model_times_30_5 = get_time('results_app30_5_model_time')
    # print(len(times_30_5))

    # generate_graph_flows([times_10_1, times_10_3, times_10_5], 500, 10, 'deployed_graph_app_')
    # generate_graph_flows([times_20_1, times_20_3, times_20_5], 500, 20, 'deployed_graph_app_')
    # generate_graph_flows([times_30_1, times_30_3, times_30_5], 500, 30, 'deployed_graph_app_')

    # generate_graph_flows([model_times_10_1, model_times_10_3, model_times_10_5], 500, 10, 'deployed_graph_app_model_')
    # generate_graph_flows([model_times_20_1, model_times_20_3, model_times_20_5], 500, 20, 'deployed_graph_app_model_')
    # generate_graph_flows([model_times_30_1, model_times_30_3, model_times_30_5], 500, 30, 'deployed_graph_app_model_')