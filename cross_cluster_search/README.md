# Cross-Cluster Search using OCI OpenSearch

- OpenSearch documentation: https://opensearch.org/docs/latest/search-plugins/cross-cluster-search/


- Create two clusters in two different regions
- Create two jumphosts/vms in the different regions, public subnet, same VCN as the clusters
- Open ports in VCN: 5601 (OpenSearch dashboard), 9200 (OpenSearch db), 22 (TCP/SSH)


## Test connection from jumphost to clusters

- For both jumphosts:- ssh into VMs.
- Change firewall setting
  ```
  sudo firewall-cmd --zone=public --add-port=5601/tcp --permanent
  ```

- Test the connection

  ```
  curl -XGET "[full_api_endpoint]/_cluster/health?pretty" -k -u [username]:[password]
  ```

## Access both dashboards

- Copy private key to jumphost
  
  ```
  scp -i ~/.ssh/private_key.pem "~/.ssh/private_key.pem" opc@[PUBLIC_ENDPOINT]:/home/opc
  ```

- Enable port forwarding for both instances
