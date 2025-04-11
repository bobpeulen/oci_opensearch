# Retrieval Augmented Generation with OCI OpenSearch and GenAI service

**The notebook will:**
- Create and store a custom embedding model in the OCI OpenSearch cluster
- Create a full RAG pipeline (OCI OpenSearch as Vector database and in-memory engine and the GenAI service (cohere) as LLM)

**Pre-requisites:**

- Create a VCN with a private subnet. Make sure there is NAT gateway attached.
- Add ingress rules to the security list: ports 9200 and 5601 ports on source 0.0.0.0/0, TCP
- Create the OpenSearch cluster in the public subnet
- Create the OCI Data Science notebook session in the private subnet
- Add the config file (API Key) and private key to this notebook in the .oci directory
- Install any of the latest pre-defined conda environments with latest version of OCI
- Create an object storage bucket

  
![image](images/img_1.jpg)
