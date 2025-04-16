
# Ingest OCI PostgreSQL logs into OCI OpenSearch for database monitoring

# Example 1.

## Use OCI Logging and OCI Streaming to stream any logs into OCI OpenSearch, using pipelines.

The below steps follow the following flow: OCI PostgreSQL logs > OCI Logging > Connector Hub > OCI Streaming > OCI OpenSearch Pipelines > OCI OpenSearch

## 1. Create an OCI postgreSQL database and OCI OpenSearch cluster
- Set up default VCN with private and public subnet, add ports for OCI OpenSearch and OCI PostgreSQL
- Create OCI OpenSearch cluster in public subnet

## 2. Create logging for OCI PostgreSQL
- Create an OCI Log Group
- Follow the steps here to enable OCI Logging for OCI PostgreSQL. [link to documentation](https://docs.oracle.com/en-us/iaas/Content/postgresql/logging-service-logs.htm#logging)
- Use the below as example for CLI to enable logging.

  ```
  oci logging log create --display-name "postgres_logging" --log-group-id [YOUR_LOG_GROUP_OCID] --log-type SERVICE --is-enabled true --configuration '{"compartmentId":"[YOUR_COMPARTMENT_OCID]","source":{"resource":"[YOUR_OCI_POSTGRESQL_INSTANCE_OCID","service":"postgresql","sourceType":"OCISERVICE","category":"postgresql_database_logs"}}'
  ```

## 3. Create an OCI Stream and Connector Hub
- Go to OCI Streaming and create a Stream
- Go to Connector Hub and select OCI Logging as source, with your Log group and specific Log name to which the OCI PostgreSQL logs are pushed
- Select your just created Stream as target. After creating the connector, go to your Stream. When logs are sent in the last minute, you can see a message like the below.

  ```
  {'data': {'application_name': 'postgresql',
    'backend_type': 'postmaster',
    'command_tag': '',
    'conString': '',
    'connection_from': '',
    'database_name': '',
    'detail': '',
    'hint': '',
    'internal_query': '',
    'internal_query_pos': '',
    'leader_pid': '',
    'level': 'LOG',
    'location': '',
    'msg': 'received fast shutdown request',
    'process_id': '18',
    'query': '',
    'query_id': '0',
    'query_pos': '',
    'session_id': '67fe430e.12',
    'session_line_num': '11',
    'session_start_time': '2025-04-15 11:29:18 UTC',
    'sql_state_code': '00000',
    'transaction_id': '0',
    'user_name': '',
    'virtual_transaction_id': ''},
   'id': 'e7f25bcf-5fa9-4c73-9a71-',
   'oracle': {'compartmentid': 'ocid1.compartment.oc1..',
    'ingestedtime': '2025-04-15T11:58:29.386Z',
    'loggroupid': 'ocid1.loggroup.oc1.eu-frankfurt-1.',
    'logid': 'ocid1.log.oc1.eu-frankfurt-1.',
    'tenantid': 'ocid1.tenancy.oc1..'},
   'source': 'ocid1.postgresqldbsystem.oc1.eu-frankfurt-1.',
   'specversion': '1.0',
   'subject': '146ec356-89ed-4084-baba-',
   'time': '2025-04-15T11:58:25.354Z',
   'type': 'com.oraclecloud.postgresql.postgresqlDbSystem.postgresql_database_logs'}
   ```

## 4. In OCI OpenSearch, create a Pipeline
- First, in OCI Vault, create a secret for your OCI OpenSearch username and password
- Go to OCI OpenSearch, click on Pipeline. Use the below YAML and change:
  - Your Secret OCIDS for username and password
  - Your OCI Streaming bootstrap server
  - Your topic name and group_id
  - Your stream pool id (OCID)
  - Your OCI OpenSearch cluster OCID


    ```
    version: 2
    pipeline_configurations:
      oci:
        secrets:
          opensearch-username:
            secret_id: "ocid1.vaultsecret.oc1.iad.amaaaaaaeicj2tiakvgrvpgni25otepemketb5whptuiigh65d6ehc5rnzda" 
          opensearch-password:
            secret_id: "ocid1.vaultsecret.oc1.iad.amaaaaaaeicj2tiawkcd46idkvgpemzes5p4rmiuivlx53xlcn4y4p6fapfq"
    kafka-pipeline:
      source:
        kafka:
          bootstrap_servers:
            - "https://cell-1.streaming.eu-frankfurt-1.oci.oraclecloud.com:9092"
          topics:
            - name: "postgres_logs"
              group_id: "DefaultPool"
          acknowledgments: true
          encryption:
            type: ssl
            insecure: false
          authentication:
            sasl:
              oci:
                stream_pool_id: "ocid1.streampool.oc1.eu-frankfurt-1.amaaaaaaeicj2tiarw4bnzt7he7ask4ioqfc74cbxwrsaxgpj2mxpri5chyq"
    
      sink:
        - opensearch:
            hosts: ["ocid1.opensearchcluster.oc1.eu-frankfurt-1.amaaaaaaeicj2tiaarjsvsbdddguxnnplg2qimrwb3ms4v6iki63dxthe5fq"]
            username: ${{oci_secrets:opensearch-username}}
            password: ${{oci_secrets:opensearch-password}}
            insecure: false
            index: "pipeline_logs_streaming_index"
    
    ```




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

## 4. Set up Ingestion Pipeline

- Open your OCI OpenSearch cluster and create a new pipeline. Give it a name. Add the below YAML. Change the:
  - Region
  - Bucket names
  - Namespace
  - Your OCI PostgreSQL OCID and ID (under the prefix, in the filter)
  - Your Vault OCIDs for your username and password for OCI OpenSearch

 - **Source Coordination YAML**
```
source_coordination:
  store:
    oci-object-bucket:
      name: "oci_opensearch_pipeline_source_coordination"
      namespace: "fro8fl9kuqli"
```

- **Pipeline YAML**
```
version: 2
pipeline_configurations:
  oci:
    secrets:
      opensearch-username:
        secret_id: "ocid1.vaultsecret.oc1.iad."
      opensearch-password:
        secret_id: "ocid1.vaultsecret.oc1.iad."


postgresql-logs-pipeline:
  source:
    oci-object:
      acknowledgments: true
      codec:
        csv: null
      compression: gzip
      scan:
        scheduling:
          interval: PT60S
        buckets:
          - bucket:
              namespace: "fro8fl9kuqli"
              name: "oci_postgresql_logs_bp"
              region: "us-ashburn-1"
              filter:
                 include_prefix: ["ocid1.postgresqldbsystem.oc1.iad.amaaaaaaeicj2tiaxceslki45vuy2edmkq3iz7lghph22cbnxmay7xgrxy5q/2855037a-01ee-4003-b493-adc0a0ef526f"]

  sink:
    - opensearch:
        hosts: ["ocid1.opensearchcluster.oc1.iad.amaaaaaaeicj2tiaxwl72s22qzk7jm7ro6fpz2qmrc7xis2v6knzhejjmewa"]
        username: ${{oci_secrets:opensearch-username}}
        password: ${{oci_secrets:opensearch-password}}
        insecure: false
        index: "postgresql_logs_v1"
 
```
- When done, click on "Dry run" to test the YAML files.
  ![image](images/img_2.png)


test with unzipped csv.
```
version: 2
pipeline_configurations:
  oci:
    secrets:
      opensearch-username:
        secret_id: "ocid1.vaultsecret.oc1.iad."
      opensearch-password:
        secret_id: "ocid1.vaultsecret.oc1.iad."


postgresql-logs-pipeline:
  source:
    oci-object:
      acknowledgments: true
      codec:
        csv: null
      compression: "none"
      scan:
        scheduling:
          interval: PT60S
        buckets:
          - bucket:
              namespace: "fro8fl9kuqli"
              name: "oci_postgresql_logs_bp"
              region: "us-ashburn-1"

  sink:
    - opensearch:
        hosts: ["ocid1.opensearchcluster.oc1.iad.amaaaaaaeicj2tiaxwl72s22qzk7jm7ro6fpz2qmrc7xis2v6knzhejjmewa"]
        username: ${{oci_secrets:opensearch-username}}
        password: ${{oci_secrets:opensearch-password}}
        insecure: false
        index: "postgresql_logs_v1" 
```


