import logging

from google.cloud import bigquery
from integrations.connectors.BigQuery.secrets_bigquery import config as bigquery_config

logger = logging.getLogger(__name__)

class LocalConfig(object):

    def __init__(self):
        self.debug = 3
        self._config = LocalConfig()
        #self.client = bigquery.Client()

    def __getattr__(self, attr):
        return bigquery_config[attr]

client = bigquery.Client()

def get_dataset(project_id,dataset_name):

    # Returns the dataset that stores marketing tables
    logger.info("Getting dataset from project: %s" % project_id)

    #Set dataset_id to the ID of the dataset to fetch
    dataset_id = project_id+'.'+dataset_name
    dataset = client.get_dataset(dataset_id)

    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    
    if(full_dataset_id):
        logger.info("Got dataset '{}' with friendly_name ".format(full_dataset_id))
    else:
        error = 'Dataset not found'
        logger.critical(error)
        raise Exception(error)
        
    return dataset

def get_dataset_tables(dataset):

    logger.info("Getting tables from dataset")
    tables = list(client.list_tables(dataset))
    
    return tables

def export_tables(bucket_name,project,dataset_id,table_id):

    filename = table_id+'.'+'csv'
    destination_uri = "gs://{}/{}".format(bucket_name, filename)
    dataset_ref = client.dataset(dataset_id, project=project)
    table_ref = dataset_ref.table(table_id)

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        # Location must match that of the source table.
        location="US",
    )  # API request
    extract_job.result()  # Waits for job to complete.

    logger.info("Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri))

    


