from jivago.wsgi.routing.routing_table import RoutingTable


class RoutingRule(object):

    def __init__(self, prefix_path: str, routing_table: RoutingTable):
        self.prefix_path = prefix_path
        self.routing_table = routing_table
