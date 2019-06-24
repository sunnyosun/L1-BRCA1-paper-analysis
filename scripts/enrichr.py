import json
import requests
import sys
import pandas as pd

class Enrichr:
    """
    Running Enrichr.

    Functions
    ---------
    view_gene_list: return the input gene list
    get_enrichment_results: run the enrichment analysis
    download_enrichment_results: write the enrichment results to /mnt/data/cache/
    check_libraries: return the list of libraries

    """

    def __init__(self, genes, listdesrciption):
        """
        Params
        ------
        genes: a list of genes
        description: description of the input gene list

        """
        
        ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/addList'
        # gene list
        genes_str = '\n'.join(genes)

        # name of analysis or list
        description = str(listdesrciption)

        # payload
        payload = {
        'list': (None, genes_str),
        'description': (None, description)
        }

        # response
        print("Enrichr API : requests.post")
        response = requests.post(ENRICHR_URL, files=payload)

        if not response.ok:
            raise Exception('Error analyzing gene list')

        job_id = json.loads(response.text)
        self.user_list_id = job_id['userListId']

        print('Enrichr API : Job ID:', job_id)
        print('Enrichr API : Description:', listdesrciption)

    def view_gene_list(self):
        """
        Returns
        -------
        The input gene list.
        """

        ENRICHR_URL_A = 'http://amp.pharm.mssm.edu/Enrichr/view?userListId=%s'

        response_gene_list = requests.get(ENRICHR_URL_A % str(self.user_list_id))

        if not response_gene_list.ok:
            raise Exception('Error getting gene list')

        print('Enrichr API : View added gene list:', str(self.user_list_id))
        added_gene_list = json.loads(response_gene_list.text)
        print(added_gene_list)

    def get_enrichment_results(self, enrichr_library = 'KEGG_2019_Human'):
        """
        Params
        ------
        enrichr_library: Defaul='KEGG_2019_Human'
        Library used to run enrichment analysis

        Returns
        -------
        A dataframe that contains the enriched terms.
        """

        ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/enrich'
        query_string = '?userListId=%s&backgroundType=%s'

        ## Libraray
        gene_set_library = str(enrichr_library)
        print('Using Library :', gene_set_library)
        response = requests.get(
            ENRICHR_URL + query_string % (str(self.user_list_id), gene_set_library)
        )
        if not response.ok:
            raise Exception('Error fetching enrichment results')

        print('Enrichr API : Get enrichment results: Job Id:', self.user_list_id)
        data = json.loads(response.text)
        out = pd.DataFrame(list(data.values())[0])
        out.columns = ['Rank', 'Term name', 'P-value', 'Z-score', 'Combined score', 'Overlapping genes', 
        'Adjusted p-value', 'Old p-value', 'Old adjusted p-value']
        return out

    def download_enrichment_results(self, enrichr_library = 'KEGG_2019_Human'):
        """
        Params
        ------
        enrichr_library: Defaul='KEGG_2019_Human'
        Library used to run enrichment analysis

        Returns
        -------
        A file that contains the analysis results.
        """

        ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/export'
        query_string = '?userListId=%s&filename=%s&backgroundType=%s'
        filename = '/mnt/data/cache/' + str(self.user_list_id) + '_' + str(enrichr_library)
        
        ## Libraray
        gene_set_library = str(enrichr_library)
        print('Using Library :', gene_set_library)
        url = ENRICHR_URL + query_string % (self.user_list_id, filename, gene_set_library)
        response = requests.get(url, stream=True)
        print('Enrichr API : Downloading file of enrichment results: Job Id:', self.user_list_id)
        with open(filename + '.txt', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print('Enrichr API : Results written to:', filename + ".txt")

    def check_libraries(self):
        """
        Returns
        -------
        A list of all the available libraries to run enrichement analysis
        """

        print ("Check the list of libraries in here: \nhttp://amp.pharm.mssm.edu/Enrichr/#stats")

