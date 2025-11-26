# Contributing

Some rough guidelines for developing this collection. Check out our [tdd e2e section](tdd.md), for setting up your development environment.

## Dependency architecture

No lower level should ever depend on a higher level. That means we should never need kubernetes to bootstrap a virtual machine, nor any deployment inside kuberentes.

Also the system level services should not depend on kubernetes, only the other way around.

For that we need to find custom solutions, like what i did with extending pves replicated filesystem with my own secrets, using ansible to generate and slurp them each time.

Everything that can be generalized should be put into this collection or reusable terraform modules. Following common infrastructure as code practices of creating one repository per environment/cluster, these repositories than act as boilerplate and minimal customization / variable holder layers, importing the core modules and collection at a certain tagged version.

This makes the process of updating of different environments easier.

## Authentication

SSH is our core layer for authentication. Most of the collection is using it in one way or another, even the terraform modules are using it to fetch secrets and authenticate with k8s.