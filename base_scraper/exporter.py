
import csv
import logging

logger = logging.getLogger()

class EntityExporter:

    def __init__(self, entities, entities_name='entities', unique=True):
        '''
        New instance of exporter.

        Parameters:
            entities -- the entities to export.
            entities_name -- the term used to refer to the entities in logging. Defaults to 'entities'.
            unique -- export only unique reviews, i.e. no duplicates. Defaults to True.
        '''
        if not entities or len(entities) == 0:
            raise ValueError("'entities' cannot be None or an empty list")
        
        self.entities = entities
        self.entities_name = entities_name
        self.unique = unique


    def to_csv(self, path, delimiter=";"):
        '''
        Use a DictWriter and the entities' `to_dict()` to append the entities to the csv in path. 
        Write fieldnames as the first row / header. Note that the output of __str__ is used to obtain
        an identifying feature of the entity (i.e. for keeping track of uniqueness as well as logging).

        Also note that you can influence the order of the fields in the output by simply listing them in 
        the desired order in the ctor of the last child class (e.g. a child of 'BookReview`).

        Parameters
            path -- the full path to the file to export to
            delimiter -- the delimiter to use in the csv. Defaults to a semicolon (';').
        '''
        if self.unique:
            exported_entities = []

        with open(path, 'a', encoding='utf-8', newline='\n') as csv_file:
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


        message = "{} {} exported to '{}'".format(len(self.entities), self.entities_name, path)
        if self.unique:
            message = "{} (unique) {} exported to '{}'".format(len(exported_entities), self.entities_name, path)
        
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
