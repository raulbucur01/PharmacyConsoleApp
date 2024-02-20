import jsonpickle
from typing import Dict, Union, Optional, List, Type

from Domain.Entity import Entity
from Repository.Exceptions import DuplicateIDError, NoSuchIDError
from Repository.Repository import Repository


class RepositoryJson(Repository):

    def __init__(self, filename):
        # super().__init__()
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Entity]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, entity: Entity) -> None:
        """
        Adauga o entitate in fisier
        :param entity: entitatea
        """

        entities = self.__read_file()
        if self.read(entity.id_entity) is not None:
            raise DuplicateIDError(f'Exista deja o entitate cu id-ul'
                                   f' {entity.id_entity}.')

        entities[entity.id_entity] = entity
        self.__write_file(entities)

    def read(self, id_entity: object = None) -> \
            Type[Union[Optional[Entity], List[Entity]]]:
        """
        Citeste ceva
        :param id_entity: id-ul votului
        :return:
            - entitatea cu id=id_entity sau None daca id_entity nu e None
            - lista cu toate entitatile daca id_entity e None
        """

        entities = self.__read_file()
        if id_entity:
            if id_entity in entities:
                return entities[id_entity]
            else:
                return None

        return list(entities.values())

    def update(self, entity: Entity) -> None:
        """
        Modifica o entitate existenta din fisier
        :param entity: entitatea
        """

        entities = self.__read_file()
        if self.read(entity.id_entity) is None:
            raise NoSuchIDError(f'Nu exista o entitate cu id-ul'
                                f' {entity.id_entity}'
                                f' pe care sa o modificam.')

        entities[entity.id_entity] = entity
        self.__write_file(entities)

    def delete(self, id_entity: str) -> None:
        """
        Sterge o entitate existenta din fisier
        :param id_entity:
        """
        entities = self.__read_file()
        if self.read(id_entity) is None:
            raise NoSuchIDError(
                f'Nu exista o entitate cu id-ul {id_entity} pe care sa'
                f' o stergem.')

        del entities[id_entity]
        self.__write_file(entities)
