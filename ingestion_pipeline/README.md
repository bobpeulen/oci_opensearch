
# **OCI OpenSearch YAML for OCI Streaming and Object Storage**


## **Example Object Storage YAML**

```
version: 2
pipeline_configurations:
  oci:
    secrets:
      opensearch-username:
        secret_id: "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaaeicj2tia3i4o2bn2s6anp3og4wceyyoo7bllvjjrhh2fro5xkdva"
      opensearch-password:
        secret_id: "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaaeicj2tiaji77odioulqprczn52jvq445765ljdwp7egwl5zns43q"
my-first-pipeline:
  source:
    oci-object:
      codec:
        newline:
      compression: none
      scan:
        start_time: 2024-12-03T08:43:25.675Z
        buckets:
          - bucket:
              namespace: "fro8fl9kuqli"
              name: "test"
  sink:
    - opensearch:
        hosts: ["ocid1.opensearchcluster.oc1.eu-frankfurt-1.amaaaaaaeicj2tiabwfk6ro2avxjxjhji5ud4x7snjm4t7jouxu6jzul6rcq"]
        username: ${{oci_secrets:opensearch-username}}
        password: ${{oci_secrets:opensearch-password}}
        insecure: false
        index: "index_pipeline_v1"

```


## **OCI Streaming**

```
version: 2
pipeline_configurations:
  oci:
    secrets:
      opensearch-username:
        secret_id: "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaaeicj2tia3i4o2bn2s6anp3og4wceyyoo7bllvjjrhh2fro5xkdva"
      opensearch-password:
        secret_id: "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaaeicj2tiaji77odioulqprczn52jvq445765ljdwp7egwl5zns43q"
kafka-pipeline:
  source:
    kafka:
      bootstrap_servers:
        - "https://cell-1.streaming.eu-frankfurt-1.oci.oraclecloud.com:9092"
      topics:
        - name: "OpenSourceData_stream_1"
          group_id: "OpenSourceData_stream_pool_1"
      acknowledgments: true
      encryption:
        type: ssl
        insecure: false
      authentication:
        sasl:
          oci:
            stream_pool_id: "ocid1.streampool.oc1.eu-frankfurt-1.amaaaaaaeicj2tiacazj6xzvn7rkfdyci6w2io6erapt7ctpxtqxauvocmea"

  sink:
    - opensearch:
        hosts: ["ocid1.opensearchcluster.oc1.eu-frankfurt-1.amaaaaaaeicj2tiabwfk6ro2avxjxjhji5ud4x7snjm4t7jouxu6jzul6rcq"]
        username: ${{oci_secrets:opensearch-username}}
        password: ${{oci_secrets:opensearch-password}}
        insecure: false
        index: "pipeline_streaming_index"
```
















