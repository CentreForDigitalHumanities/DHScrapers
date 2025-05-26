## Maintenance
In the Github workflow, there is a `KUBECTL_VERSION` variable defined, this needs to be on a par with the current Openshift version.
Albeit it's overprovisioned, the free space on PVC needs to be monitored. Maybe some `previous_runs` need to be removed or to increase the PVC disk space.
Secret management is manual see commands like:
`kubectl create secret generic elasticsearch-apikey --from-file=elastic-apikey=/path/to/elastic-apikey`