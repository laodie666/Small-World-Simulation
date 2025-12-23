import random
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
# Build simulation first visualization later


# implementing newman_watts_strogatz_graph
if __name__ == "__main__":
    n = 30
    p = 0.05

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

    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 3)
    infected_history = [[], [], []] 

    ax_top = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])]
    ax_bottom = fig.add_subplot(gs[1, :]) 

    def update(frame):
        graphs = [complete_graph, small_world, regular_graph]
        graph_name = ["complete_graph", "small_world", "regular_graph"]
        line_colors = ['red', 'orange', 'green']
        layouts = [nx.circular_layout(g) for g in graphs]
        ax_bottom.clear()
        for i in range(3):
            graph = graphs[i]
            global iteration 
            
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
            
            ax_top[i].clear()
            nx.draw(graph, layouts[i], ax=ax_top[i], node_color=color_map, width = 0.3)
            ax_top[i].set_title(f"Graph: {graph_name[i]} | Infected: {len(infected[i])}/{n}")
        
            ax_bottom.plot(infected_history[i], color=line_colors[i], label = graph_name[i])
        
        iteration += 1
        ax_bottom.set_ylim(0, n + 5)
        ax_bottom.set_ylabel("Total Infected")
        ax_bottom.set_xlabel("Iteration")
        ax_bottom.legend(loc="upper left")

        fig.suptitle(f"Iteration {iteration}, p value of {p}")
        if all(len(s) == n for s in infected):
            global ani
            ani.event_source.stop()


    ani = animation.FuncAnimation(fig, update, interval=10)
    done = False

    plt.show()

