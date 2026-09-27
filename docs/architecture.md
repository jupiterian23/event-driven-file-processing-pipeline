# Event-Driven File-Processing Pipeline Architecture

```mermaid
flowchart LR
    A[User / Application] -->|Upload File| B[S3 Input Bucket]

    B -->|ObjectCreated Event| C[AWS Lambda]

    C -->|GetObject| B
    C -->|Process File| D[File Processing Logic]
    D -->|PutObject| E[S3 Output Bucket]

    C -->|Execution Logs| F[CloudWatch Logs]

    G[IAM Role] -->|Least-Privilege Permissions| C
