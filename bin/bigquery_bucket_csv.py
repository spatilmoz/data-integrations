from __future__ import division
import sys,os, argparse
import logging

from integrations.connectors import BigQuery, Util

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get BigQuery Dataset")
    parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
    parser.add_argument('-l', '--log-level', action='store',
                        help='log level (debug, info, warning, error, or critical)', type=str, default='info')
    args = parser.parse_args()

    Util.set_up_logging(args.log_level)

    logger = logging.getLogger(__name__)

    logger.info("Starting...")

    dataset = BigQuery.get_dataset(project_id='imposing-union-227917',dataset_name='cdp_to_salesforce')
    
    tables = BigQuery.get_dataset_tables(dataset)

    if tables:
        for table in tables:
            logger.info("Found table: '{}".format(table.table_id))
            logger.info("Exporting '{}' to bucket".format(table.table_id))
            BigQuery.export_tables(bucket_name='test-bq-sfmc-bucket',project='imposing-union-227917',dataset_id='cdp_to_salesforce',table_id=table.table_id)
    else:
        logger.info("This dataset does not contain any tables.")  #fix the error message
