This roles configures redirects with the traefik redirectRegex middleware.

You can define redirects in the `redirects` variable. The variable is a list of objects with the following keys:
- `host`: The host to redirect from
- `path`: The path to redirect from
- `target`: The target to redirect to