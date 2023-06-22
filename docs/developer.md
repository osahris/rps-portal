---
layout: docs
title: "Docs for Devs"
---
# Manual for developers

This section of the documentation is targeted at anyone doing further
development of the software stack.

_This page is currently under construction, sorry._

Auto-generated API documentation
--------------------------------

The API documentation, as far as it exists, can be found at
[API doc endpoint](../developer/API/).

Documentation workflow
-----------------------

The documentation your are reading is hosted in a project-wide or site-wide
`git` repository (probably the project's monorepos or primary repository)
as a bunch of (markdown) documents. This allows the documentation to follow
the code across git branches and merges, keeps it more up-to-date, and
allows an easy record of what the documentation looked like at the time of
release.

When adding new documentation, please try to follow the general structure
of enduser- / admin- / developer-specific sections.


## Traefik
**Reverse proxy service**  
A bit more detailed description and maybe reasoning to add it to RPS. This text in smaller size  
Comments on additional features and configurations that are added when this service is integrated to the RPS.  
More info: [official docs](https://doc.traefik.io/traefik/)


## OAuth2 proxy
**Short and very general description**  
A bit more detailed description and maybe reasoning to add it to RPS. This text in smaller size  
Comments on additional features and configurations that are added when this service is integrated to the RPS.  
More info: [official docs](https://oauth2-proxy.github.io/oauth2-proxy/docs/)


## Servicename
**Short and very general description**  
A bit more detailed description and maybe reasoning to add it to RPS. This text in smaller size

Comments on additional features and configurations that are added when this service is integrated to the RPS.  
More info: [official docs](https://URL)


```js
export default {
  data () {
    return {
      msg: 'this code line is focused!' // [!code  focus]
    }
  }
}
```

Additional resources
--------------------

 * [administrator documentation](../admin)
