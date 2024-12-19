# Cross-Cluster Search using OCI OpenSearch

- OpenSearch documentation: https://opensearch.org/docs/latest/search-plugins/cross-cluster-search/


- Create two clusters in two different regions
- Create two jumphosts/vms in the different regions, public subnet, same VCN as the clusters
- Open ports in VCN: 5601 (OpenSearch dashboard), 9200 (OpenSearch db), 22 (TCP/SSH)

For both jumphosts:
- ssh into VMs.
- 
