from controller import SDNController
from graph import Graph

if __name__ == '__main__':

    graphIt = Graph()
    
    for u, v, w in [('S1', 'S2', 1), ('S1', 'S3', 1), ('S2', 'S4', 1), ('S3', 'S4', 1), ('S1', 'S4', 5)]:
        graphIt.add_link(u, v, w)
        
    graphIt.add_node('H1')
    graphIt.add_node('H2')
    graphIt.add_link('H1', 'S1', 1)
    graphIt.add_link('H2', 'S2', 1)

    ctrl = SDNController(graphIt)

    instructions = 'Commands:\n\tadd_node <node>\n\tremove_node <node>\n\tadd_link <u> <v> <weight>\n\tremove_link <u> <v>\n\tinject_flow <src> <dst>\n\tsimulate_failure <u> <v>\n\tshow_flows\n\tquery <src> <dst>\n\tvisualize\n\thelp\n\texit'
    print(instructions)
    while True:
        cmd = input('sdn> ').split()
        if not cmd:
            continue
        op = cmd[0]
        if op == 'add_node' and len(cmd) == 2:
            graphIt.add_node(cmd[1]); ctrl.install_flows(); print('Node added')
        elif op == 'remove_node' and len(cmd) == 2:
            graphIt.remove_node(cmd[1]); ctrl.install_flows(); print('Node removed')
        elif op == 'add_link' and len(cmd) == 4:
            graphIt.add_link(cmd[1], cmd[2], int(cmd[3])); ctrl.install_flows(); print('Link added')
        elif op == 'remove_link' and len(cmd) == 3:
            ctrl.remove_link_and_reconfigure(cmd[1], cmd[2])
        elif op == 'inject_flow' and len(cmd) == 3:
            ctrl.active_flows.append((cmd[1], cmd[2])); ctrl.install_flows(); print('Flow injected')
        elif op == 'simulate_failure' and len(cmd) == 3:
            ctrl.remove_link_and_reconfigure(cmd[1], cmd[2])
        elif op == 'show_flows':
            ctrl.show_tables()
        elif op == 'query' and len(cmd) == 3:
            path = ctrl.compute_path(cmd[1], cmd[2])
            print('Path:', path if path else 'unreachable')
        elif op == 'visualize':
            ctrl.visualize()
        elif op == 'help':
            print(instructions)
        elif op in ('exit', 'quit'):
            break
        else:
            print('Unknown command, type help')
