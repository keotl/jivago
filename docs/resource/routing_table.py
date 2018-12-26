from jivago.wsgi.methods import GET, POST
from jivago.wsgi.routing.tree.tree_routing_table import TreeRoutingTable

my_routing_table = TreeRoutingTable()

my_routing_table.register_route(GET, "/hello", MyResourceClass, MyResourceClass.get_hello)
my_routing_table.register_route(POST, "/hello", MyResourceClass, MyResourceClass.get_hello)
