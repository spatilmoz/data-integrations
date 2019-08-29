import bonobo


class OrchestratorWorker:
    @staticmethod
    def work(nodes, services=[]):
        graph = bonobo.Graph()
        graph.add_chain(*nodes)
        bonobo.run(graph, services=services)
