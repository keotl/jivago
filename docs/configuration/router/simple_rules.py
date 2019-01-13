from jivago.wsgi.methods import GET
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable
from jivago.wsgi.routing.table.tree_routing_table import TreeRoutingTable

my_routing_table = TreeRoutingTable()
my_routing_table.register_route(GET, "/hello", HelloClass, HelloClass.get_hello)

root_rule = RoutingRule("/", my_routing_table)
my_rule = RoutingRule("/static", StaticFileRoutingTable("/var/www"), rewrite_path=True)
