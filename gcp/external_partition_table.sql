CREATE OR REPLACE EXTERNAL TABLE `tjr103.SalePartitionExternal`
(
  TransactionID STRING,
  ProductID STRING,
  Quantity INT64,
  SaleDate DATE,
)
WITH PARTITION COLUMNS
OPTIONS (
  format = 'CSV',
  uris = ['gs://tjr103-demo-allen/demo_partition/*'],
  hive_partition_uri_prefix = 'gs://tjr103-demo-allen/demo_partition',
  skip_leading_rows = 1,
  max_bad_records = 1
);