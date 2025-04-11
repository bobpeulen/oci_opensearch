
# Ingest OCI PostgreSQL logs into OCI OpenSearch for database monitoring

## 1. Enable logging
Enable export of logging from OCI PostgreSQL in Object Storage. See [documentation](https://docs.oracle.com/en-us/iaas/Content/postgresql/export-logs-to-object-storage.htm).

## 2. Create OCI ostgreSQL database and OCI OpenSearch cluster
- Set up default VCN with private and public subnet, add ports for OCI OpenSearch and OCI PostgreSQL
- Create OCI OpenSearch cluster in public subnet
- Create OCI PostgreSQL database, add a custom configuration with (See [documentation](https://docs.oracle.com/en-us/iaas/Content/postgresql/export-logs-to-object-storage.htm)).
  - oci.log_destination: oci_object_storage
  - oci.log_destination_os_namespace: The Object Storage namespace for the tenancy
  - oci.log_destination_os_bucket_name: The Object Storage bucket name to which the logs are exported

  When the OCI PostgreSQL instance is active, you should see already logs added to your bucket for your specific OCI PostgreSQL instance OCID.
  ![image](images/img_1.png)

## 3. Test the logging output
- Log in to your OCI PostgreSQL instance
- Execute an example statement.

  ```
  CREATE TABLE products ( 

    product_no integer, 

    name text, 

    price numeric 

  ); 
  ```
  ```
  INSERT INTO products (product_no, name, price) VALUES 

  (1, 'Cheese', 9.99), 
  
  (2, 'Bread', 1.99), 
  
  (3, 'Meat', 1.55), 
  
  (4, 'Milk', 2.99), 
  
  (5, 'Bread', 1.99), 
  
  (6, 'Meat', 1.01), 
  
  (8, 'Meat', 3.99), 
  
  (9, 'Meat', 4.69), 
  
  (10, 'Meat', 1.99), 
  
  (11, 'Meat', 1.99), 
  
  (12, 'Milk', 2.99);
  ```
- Export the latest updated log file from the bucket, unzip, and review the csv file.



