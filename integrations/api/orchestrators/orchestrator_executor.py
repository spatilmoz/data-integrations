import bonobo


class OrchestratorExecutor:
    @staticmethod
    def execute(nodes, services=[]):
        graph = bonobo.Graph()
        graph.add_chain(*nodes)
        bonobo.run(graph, services=services)
