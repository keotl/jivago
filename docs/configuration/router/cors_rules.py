from jivago.config.router.cors_rule import CorsRule

# Applies to all requests
CorsRule("/", {"Access-Control-Allow-Origin": '*'})

# Applies to all requests on a path which starts with '/users'
CorsRule("/users", {"Access-Control-Allow-Origin": 'api.example.com'})
