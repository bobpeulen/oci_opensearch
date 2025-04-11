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

- From local machine, copy private key to Instance. Change the public IP.
  ```
  scp -i ~/.ssh/private_key.pem "C:/Users/Bob/.ssh/private_key.pem" opc@129.213.47.148:/home/opc
  scp -i ~/.ssh/private_key.pem "~/.ssh/private_key.pem" opc@129.213.47.148:/home/opc/.ssh
  
  ```

- Enable port forwarding. Change the private IP of the OCI OpenSearch cluster and the public IP of the instance
  ```
  ssh -C -v -t -L 127.0.0.1:5601:10.0.1.214:5601 opc@129.213.47.148 -i ~/.ssh/private_key.pem
  ssh -C -v -t -L 127.0.0.1:5601:10.0.1.214:5601 opc@129.213.47.148 -i C:/Users/Bob/.ssh/private_key.pem

  129.213.47.148

  ssh -C -v -t -L 127.0.0.1:5601:10.0.1.214:5601 -L 127.0.0.1:9200:10.0.1.20:9200 opc@129.213.47.148 -i C:/Users/Bob/.ssh/private_key.pem
  ```

  Port good example
  ```
   ssh -C -v -t -L 127.0.0.1:5601:10.0.0.96:5601 opc@129.213.47.148 -i C:/Users/Bob/.ssh/private_key.pem 
  ```

- Access at
  ```
  https://localhost:5601
  ```

