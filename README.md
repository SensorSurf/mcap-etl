# mcap_etl

`.mcap` (MCAP) and `.bag` (ROS Bag) files pose challenges for data engineers due to their large size, complex structure, and lack of standardization. Managing and transferring these massive files requires substantial storage capacity and bandwidth, leading to slow processing times. Extracting and interpreting the desired information becomes time-consuming and error-prone due to the mix of timestamped messages and the need for custom parsing and processing pipelines.

mcap_etl is alleviating these pain points by offering a comprehensive suite of options to transform the contents of MCAP files into a structured database or alternative file formats, streamlining the data engineering process and enabling easier analysis and visualization of the captured data.

Presently, mcap_etl supports the following conversions:
* From `.mcap` to `.bag`
* From `.mcap` to TimescaleDB

We are actively seeking to extend this list and invite community contributions. Specifically, we aim to include transformations to InfluxDB, Timestream, and Parquet.

## Installation and Usage

### Installation

mcap_etl can be installed easily via pip:
```shell
pip install mcap-etl
```

### Usage

mcap_etl requires a running Timescale database. Once set up, you can execute jobs against any file. Note that the database connection parameters are optional, enhancing flexibility.
```shell
mcap_etl timescale \
    --host localhost \
    --port 5432 \
    --user postgres \
    --password password \
    --name postgres \
    /path/to/file.mcap
```

You can now perform queries against your database.

## Future Development: Hosted Solution

We are in the process of developing a hosted solution, offering:

* Managed services for data ingestion, database, and infrastructure for integrations, including S3 and Grafana.
* A tool to convert data back from Timescale to `.mcap` and `.bag` formats.
* Vector search capabilities for unstructured data types, such as imagery and audio.
* A web interface to monitor and share data with your team.

## Key Design Considerations

mcap_etl has been designed with the following key principles:

* __Timescale Hypertables__: Due to the large number of messages, we use Timescale's hypertables and take advantage of their compression features.
* __No ROS Dependency__: mcap_etl operates without any ROS dependencies, avoiding the complexity of ROS installations for simple data extraction from `.bag` or `.mcap` files. Instead, we utilize the `rosbags` project, which allows for dynamic loading of message schemas at runtime.
* __MCAP to ROS bag Transformation__: mcap_etl first converts MCAP files into ROS bags before performing data transformations. This approach avoids the need to rewrite the ingestion flow.