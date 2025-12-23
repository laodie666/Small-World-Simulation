import random
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
# Build simulation first visualization later


# implementing newman_watts_strogatz_graph
if __name__ == "__main__":
    n = 20
    p = 0.1

    iteration = 0
    infected = [{0} for _ in range(3)]


    complete_graph = nx.complete_graph(n)
    regular_graph = nx.cycle_graph(n)
    small_world = nx.cycle_graph(n)

    for i in range(0,n):
        for j in range(0,n):
            if random.random() < p and i != j:
                small_world.add_edge(i,j)
                small_world.add_edge(j,i)

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    infected_history = [[], [], []] 

    def update(frame):
        graphs = [complete_graph, small_world, regular_graph]
        graph_name = ["complete_graph", "small_world", "regular_graph"]
        layouts = [nx.circular_layout(g) for g in graphs]
        for i in range(3):
            graph = graphs[i]
            global iteration 
            iteration += 1
            spreader = random.sample(list(infected[i]), 1)
            target = random.sample(list(graph[spreader[0]]), 1)
            if target[0] not in infected[i]:
                infected[i].add(target[0])

            infected_history[i].append(len(infected[i]))

            color_map = []
            for node in graph.nodes():
                if node in infected[i]:
                    color_map.append('red')
                else:
                    color_map.append('blue')
            
            ax[0, i].clear()
            nx.draw(graph, layouts[i], ax=ax[0, i], node_color=color_map)
            ax[0, i].set_title(f"Graph: {graph_name[i]} | Infected: {len(infected[i])}/{n}")
        
            ax[1, i].clear()
            
            ax[1, i].plot(infected_history[i], color='red')
            ax[1, i].set_ylim(0, n + 5)

        fig.suptitle(f"Iteration {iteration}")
        if all(len(s) == n for s in infected):
            global ani
            ani.event_source.stop()


    ani = animation.FuncAnimation(fig, update, interval=80)
    done = False

    plt.show()




        

        

        