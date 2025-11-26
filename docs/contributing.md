# Contributing

some rough guidelines for developing this collection.

## dependency architecture

no lower level should ever depend on a higher level. That means we should never need kubernetes to bootstrap a virtual machine, nor any deployment inside kuberentes.

also the system level services should not depend on kubernetes, only the other way around.

for that we need to find custom solutions, like what i did with extending pves replicated filesystem with my own secrets, using ansible to generate and slurp them each time.

everything that can be generalized should be put into this collection or reusable terraform modules. following common infrastructure as code practices of creating one repository per environment/cluster, these repositories than act as boilerplate and minimal customization / variable holder layers, importing the core modules and collection at a certain tagged version.

this makes the process of updating of different environments easier.

## authentication

ssh is the single means for authentication. we use it in .envrc files, for ansible inventories aswell as terraform with the external provider. With just ssh we can setup the 
cloud initially and reach a fully functional state where we can deploy services that can serve valid https requests.

from there we go to more advanced services like awx for executing cron playbooks.