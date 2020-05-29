
import os
import csv
from xml.dom.minidom import parseString
import dicttoxml
import logging

logger = logging.getLogger()

class EntityExporter:

    def __init__(self, output_folder, entities, entities_name='entities', unique=True):
        '''
        New instance of exporter.

        Parameters:
            entities -- the entities to export.
            entities_name -- the term used to refer to the entities in logging. Defaults to 'entities'.
            unique -- export only unique reviews, i.e. no duplicates. Defaults to True.
        '''
        if not entities or len(entities) == 0:
            raise ValueError("'entities' cannot be None or an empty list")
        
        self.output_folder = output_folder
        self.entities = entities
        self.entities_name = entities_name
        self.unique = unique


    def to_csv(self, filename, delimiter=";"):
        '''
        Use a DictWriter and the entities' `to_dict()` to append the entities to the csv in path. 
        Write fieldnames as the first row / header. Note that the output of __str__ is used to obtain
        an identifying feature of the entity (i.e. for keeping track of uniqueness as well as logging).

        Also note that you can influence the order of the fields in the output by simply listing them in 
        the desired order in the ctor of the last child class (e.g. a child of 'BookReview`).

        Parameters
            filename -- the name (incl. extension) to export to.
            delimiter -- the delimiter to use in the csv. Defaults to a semicolon (';').
        '''
        if self.unique:
            exported_entities = []

        export_file = os.path.join(self.get_subfolder('CSV'), filename)

        with open(export_file, 'a', encoding='utf-8', newline='\n') as csv_file:
            fieldnames = list(self.entities[0].to_dict().keys())
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()

            for entity in self.entities:
                if not self.unique or (self.unique and not self.already_exported(exported_entities, entity)):
                    try:
                        writer.writerow(entity.to_dict())
                    except:
                        logger.info("Error encountered exporting review '{}'. Skipping.".format(entity.__str__()))
                        logger.debug(vars(entity.to_dict()))
                        exported_entities.pop()


        message = "{} {} exported to '{}'".format(len(self.entities), self.entities_name, export_file)
        if self.unique:
            message = "{} (unique) {} exported to '{}'".format(len(exported_entities), self.entities_name, export_file)
        
        logger.info(message)


    def to_xml(self, custom_root='root'):
        '''
        Export an xml file for each entity.
        Filename will be created by calling __str__ on the entity (and adding '.xml').

        Parameters:
            custom_root -- a custom tag for the root element. Defaults to 'root'
        '''
        if self.unique:
            exported_entities = []

        export_folder = self.get_subfolder('XML')

        for entity in self.entities:
            if not self.unique or (self.unique and not self.already_exported(exported_entities, entity)):
                filename = str(entity) + '.xml'
                xml = parseString(dicttoxml.dicttoxml(entity.to_dict(), custom_root=custom_root))
                
                with open(os.path.join(export_folder, filename), 'w') as out_file:
                    out_file.write(xml.toprettyxml())

        message = "{} {} exported to XML in '{}'".format(len(self.entities), self.entities_name, export_folder)
        if self.unique:
            message = "{} (unique) {} exported to XML in '{}'".format(len(exported_entities), self.entities_name, export_folder)
        
        logger.info(message)


    def to_txt(self, field='text'):
        '''
        Export an txt file for each entity, with `field` as the content of the txt.
        Filename will be created by calling __str__ on the entity (and adding '.txt').

        Parameters:
            field -- The field to print to the txt
        '''
        if self.unique:
            exported_entities = []

        export_folder = self.get_subfolder('TXT')

        for entity in self.entities:
            if not self.unique or (self.unique and not self.already_exported(exported_entities, entity)):
                filename = str(entity) + '.txt'
                content = getattr(entity, field)                
                with open(os.path.join(export_folder, filename), 'w') as out_file:
                    out_file.write(content)
        
        message = "{} {} exported to TXT in '{}'".format(len(self.entities), self.entities_name, export_folder)
        if self.unique:
            message = "{} (unique) {} exported to TXT in '{}'".format(len(exported_entities), self.entities_name, export_folder)
        
        logger.info(message)


    def already_exported(self, exported_entities, current_entity):
        '''
        Check if `current_entity` is in `exported_entities`.
        If it isn't, add it to the list
        '''
        identifier = current_entity.__str__()
        if identifier in exported_entities:
            return True
        else:
            exported_entities.append(identifier)
            return False


    def get_subfolder(self, subfoldername):
        '''
        Get full path to subfolder (of self.output_folder) with `subfoldername`.
        Subfolder will be created if it doesn't exist.
        '''
        subfolder = os.path.join(self.output_folder, subfoldername)
        if not (os.path.exists(subfolder)):
            os.mkdir(subfolder)
        return subfolder
