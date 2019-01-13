from jivago.config.router.filtering.filtering_rule import FilteringRule

# Applies to all subpaths of "/users/". DOES NOT apply to "/users" itself.
FilteringRule("/users/*", [MyFilter])

# Only applies to "/users", and nothing else.
FilteringRule("/users", [MyFilter])

# Applies to "/users" and subpaths of "/users/...".
FilteringRule("/users*", [MyFilter])

# Applies to all requests matching regexp.
# First parameter is not used when regex_pattern is supplied.
FilteringRule(None, [MySpecialFilter], regex_pattern=r"^/users.*$")
