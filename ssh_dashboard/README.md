# Open Dashboard through SSH port forwarding


- Create instance in public subnet, same VCN as OCI OpenSearch

- SSH into instance. Add port to firewall
  ```
  sudo firewall-cmd --zone=public --add-port=5601/tcp --permanent
  sudo firewall-cmd --zone=public --add-port=443/tcp --permanent
  sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
  sudo firewall-cmd --zone=public --add-port=9200/tcp --permanent
  sudo firewall-cmd --reload  
  ```

- Test connection from Instance to OCI OpenSearch
  ```
  curl -u '[username]:[password]' [full API endpoint, including https:// and port]
  ```


  Port example. Change in the below:
  - Private IP of Dashboard
  - Public URL jump host
  ```
   ssh -C -v -t -L 127.0.0.1:5601:10.0.0.96:5601 opc@129.213.47.148 -i C:/Users/Bob/.ssh/private_key.pem 
  ```

- Access at
  ```
  https://localhost:5601
  ```

