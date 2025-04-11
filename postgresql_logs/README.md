
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







