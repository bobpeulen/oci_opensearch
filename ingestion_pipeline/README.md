
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

## Example using compressed csv

```
log-pipeline:
  source:
    oci-object:
      acknowledgments: true
      codec:
        csv:
      compression: gzip
      scan:
        start_time: 2023-01-01T00:00:00Z
        end_time: 2024-01-01T00:00:00Z
        buckets:
          - bucket:
              namespace: "idee4xpu3dvm"
              name: "data-prepper-test-dnd"
              region: "us-ashburn-1"
          - bucket:
              namespace: "idee4xpu3dvm"
              name: "data-prepper-test-dnd"
              region: "us-phoenix-1"
    - grok:
        match:
          log: [ "%{COMMONAPACHELOG}" ]
  sink:
    - opensearch:
        hosts: [ "ocid1.opensearchcluster.oc1.iad.amaaaaaa2da6iyaacehx5go7jepe6ivq623p3dtnsvlywctrjzd3dbug4dra" ]
        insecure: false
        username: ${{oci_secrets:opensearch-username}}
        password: ${{oci_secrets:opensearch-password}}
        index: apache_logs
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


# Example JSON message for OCI Streaming

- See https://github.com/graytaylor0/Fake-Apache-Log-Generator

{"timestamp": "2024-12-03T09:45:00.000Z", "name":"John", "age":30, "car":"Volvo"}
{"timestamp": "2024-12-03T09:46:00.000Z","name":"Bob", "age":31, "car":"Ford"}


{"idx": 235, "carbrand": "Volvo", "message_timestamp": Dec 3, 2024 @ 15:13:58.515, "error_code": 99}

idx 582 carbrand Ford message_timestamp Dec 3, 2024 @ 15:14:58.515 error_code 99
idx 36 carbrand Volvo message_timestamp Dec 3, 2024 @ 15:15:58.515 error_code 99
idx 87 carbrand Mercedes message_timestamp Dec 3, 2024 @ 15:16:58.515 error_code 22
idx 965 carbrand Ford message_timestamp Dec 3, 2024 @ 15:17:58.515 error_code 2
idx 36 carbrand Volvo message_timestamp Dec 3, 2024 @ 15:18:58.515 error_code 99
idx 87 carbrand Mercedes message_timestamp Dec 3, 2024 @ 15:19:58.515 error_code 22
idx 965 carbrand Ford message_timestamp Dec 3, 2024 @ 15:20:58.515 error_code 99












