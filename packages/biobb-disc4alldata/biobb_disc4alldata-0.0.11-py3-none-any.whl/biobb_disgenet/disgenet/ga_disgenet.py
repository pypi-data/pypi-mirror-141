#!/usr/bin/env python3

"""Module containing the BioBBs DisGeNET class and the command line interface."""
import argparse
import shutil
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_disgenet.disgenet.common import *


# 1. Rename class as required
class GA_disgenet(BiobbObject):
    """
    | biobb_disgenet Gene Attribute Disgenet
    | This class is for downloading a Gene Attribute request from DisGeNET database.
    | Wrapper for the DisGeNET database `https://www.disgenet.org` and the  DisGeNET REST API ´https://www.disgenet.org/api/´ for downloading available collections of genes and variants associated data to human diseases.

    Args:

        retrieve_by (str): Configuration params to pass for the retrieval of the association on the REST API (gene, uniprot_entry, disease, source, evidences_gene, evidences_disease)  
        output_file_path (str): Path to the output file, that can be in format TSV, JSON or XML. 
        properties (dict - Python dict containing the properties for the API interrogation, considering also the credentials of the user to the database):
            * **gene_id** (*str*) - Number identification for a gene or a list of genes separated by commas recognized by the database.
            * **uniprot_id** (*str*) - Uniprot id or a list of uniprot ids separated by commas.
            * **source** (*str*) - Source of the associations (CURATED, INFERRED, ANIMAL_MODELS, ALL, BEFREE, CGI, CLINGEN, CLINVAR, CTD_human, CTD_mouse, CTD_rat, GENOMICS_ENGLAND, GWASCAT, GWASDB, HPO, LHGDN, MGD, ORPHANET, PSYGENET, RGD, UNIPROT).
            * **max_dsi** (*str*) - Max value of DSI range for the gene.
            * **min_dsi** (*str*)  - Min value of DSI range for the gene.
            * **min_dpi** (*str*) - Min value of DPI range for the gene.
            * **max_dpi** (*str*) - Max value of DPI range for the gene.
            * **max_pli** (*str*) -  Max value of pLI range for the gene.
            * **min_pli** (*str*) -  Min value of pLI range for the gene.
            * **format** (*str*) - Format output file.
            * **limit** (*str*) - Number of disease to retrieve.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python:

            from biobb_disgenet.disgenet.ga_disgenet import ga_disgenet

            prop = {
                'gene_id': '351',
                'source': 'source', 
                'min_dsi': 'min_dsi',
                'max_dsi': 'max_dsi',
                'min_dpi': 'min_dpi',
                'max_dpi': 'max_dpi',
                'min_pli': 'min_pli',
                'max_pli':'max_pli', 
                'format': 'format',
                'limit': 'limit'
            }
            ga_disgenet(
                    retrieve_by='gene'
                    output_file_path='/path/to/associationsFile',
                    properties=prop)

    Info:
        retrieve_by can be: 
            gene, uniprot, source

    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, output_file_path, retrieve_by = None,
            properties = None, **kwargs) -> None:
        properties = properties or {}

        # 2.0 Call parent class constructor
        super().__init__(properties)

        # 2.1 Modify to match constructor parameters
        # Input/Output files
        self.io_dict = { 
                'in': {'retrieve_by': retrieve_by}, 
            'out': { 'output_file_path': output_file_path } 
        }

        # 3. Include all relevant properties here as 
        # self.property_name = properties.get('property_name', property_default_value)

        # Properties specific for BB
        bb_properties = {}

        self.email = properties.get('email', None)
        self.password = properties.get('password', None)

        #print (properties)
        #print (self.email, self.password)

        bb_properties["gene_id"] = properties.get('gene_id', None)
        bb_properties["uniprot_id"] = properties.get('uniprot_id', None)
        bb_properties["source"] = properties.get('source', "ALL")
        bb_properties["min_dsi"] = properties.get('min_dsi', None)
        bb_properties["max_dsi"] = properties.get('max_dsi', None)
        bb_properties["max_dpi"] = properties.get('max_dpi', None)
        bb_properties["min_dpi"] = properties.get('min_dpi', None)
        bb_properties["max_pli"] = properties.get('max_pli', None)
        bb_properties["min_pli"] = properties.get('min_pli', None)
        bb_properties["format"] = properties.get('format', "json")
        bb_properties["limit"] = properties.get('limit', None)
        bb_filtered = {k: v for k, v in bb_properties.items() if v is not None}
        bb_properties.clear()
        bb_properties.update(bb_filtered)
        self.properties = bb_properties


        # Check the properties

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`GDA_disgenet <disgenet.GDA_disgenet.GDA_disgenet>` object."""
        
        # 4. Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()
        
        #check mandatory params that is gene_id
        output_path = check_output_path(self.io_dict["out"]["output_file_path"], False, "output", self.properties["format"], self.out_log, self.__class__.__name__)
        
        response = ga_va_session("gene", self.io_dict["in"]["retrieve_by"], self.properties, self.out_log, self.global_log)
        new_keys, request = extension_request(response, self.io_dict["in"]["retrieve_by"], self.properties)
        
        auth_session(request, new_keys, output_path, self.out_log, self.global_log)

        return self.return_code

def ga_disgenet(output_file_path: str, retrieve_by: str = None , properties: dict = None, **kwargs) -> int:
    """Create :class:`Template <template.template.Template>` class and
    execute the :meth:`launch() <template.template.Template.launch>` method."""

    return GA_disgenet(
                    output_file_path=output_file_path,
                    retrieve_by=retrieve_by,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='This class is a wrapper for an associations call of teh DisGeNET database REST API.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    parser.add_argument('--retrieve_by', required=False, help='Retrieval factor necessary to define the search of the associations; gene, uniprot entry, disease, source, evidence by disease, evidence by gene available choices.')
    required_args.add_argument('--output_file_path', required=True, help='Description for the output file path. Accepted formats: json, csv or html.')
    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # 11. Adapt to match Class constructor (step 2)
    # Specific call of each building block
    ga_disgenet(
             output_file_path=output_file_path,
             retrieve_by=retrieve_by,
             properties=properties)

if __name__ == '__main__':
    main()

# 12. Complete documentation strings
