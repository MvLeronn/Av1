from database import Database
from bson.objectid import ObjectId


class Cuidador:
    def __init__(self, id, nome, documento):
        self.id = id
        self.nome = nome
        self.documento = documento


class Habitat:
    def __init__(self, id, nome, tipoAmbiente, cuidador):
        self.id = id
        self.nome = nome
        self.tipoAmbiente = tipoAmbiente
        self.cuidador = cuidador


class Animal:
    def __init__(self, id, nome, especie, idade, habitat):
        self.id = id
        self.nome = nome
        self.especie = especie
        self.idade = idade
        self.habitat = habitat


class ZoologicoDAO:
    def __init__(self, database):
        self.db = database
        self.collection = database.collection

    def createAnimal(self, animal: Animal):
        try:
            result = self.collection.insert_one(
                {"id": animal.id, "nome": animal.nome, "especie": animal.especie, "idade": animal.idade,
                 "habitat.id": animal.habitat.id, "habitat.nome": animal.habitat.nome,
                 "habitat.tipoAmbiente": animal.habitat.tipoAmbiente, "cuidador.id": animal.habitat.cuidador.id,
                 "cuidador.nome": animal.habitat.cuidador.nome, "cuidador.documento": animal.habitat.cuidador.documento})
            animal_id = str(result.inserted_id)
            print(f"Animal{animal.nome} created with id: {animal.id}")
            return animal_id
        except Exception as error:
            print(f"An error occurred while creating animal: {error}")
            return None

    def readAnimal(self, id: str) -> dict:
        try:
            animal = self.collection.find_one({"_id": ObjectId(id)})
            if animal:
                print(f"Animal found: {animal}")
                return animal
            else:
                print(f"No animal found with id {id}")
                return None
        except Exception as error:
            print(f"An error occurred while reading animal: {error}")
            return None

    def updateAnimal(self, id: str, nome: str, especie: str, idade: int, habitat: Habitat) -> int:
        try:
            result = self.collection.update_one({"_id": ObjectId(id)}, {
                "$set": {"nome": nome, "especie": especie, "idade": idade, "habitat.id": habitat.id,"habitat.nome" : habitat.nome,"habitat.tipoambiente" : habitat.tipoAmbiente,"cuidador.id" : habitat.cuidador.id}, "cuidador.nome": habitat.cuidador.nome,"cuidador.documento":habitat.cuidador.documento})
            if result.modified_count:
                print(
                    f"Animal {id} updated with nome {nome} and especie {especie} and idade {idade} and habitat {habitat} ")
            else:
                print(f"No animal found with id {id}")
            return result.modified_count
        except Exception as error:
            print(f"An error occurred while updating animal: {error}")
            return None

    def deleteAnimal(self, id: str) -> int:
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count:
                print(f"Animal {id} deleted")
            else:
                print(f"No animal found with id {id}")
            return result.deleted_count
        except Exception as error:
            print(f"An error occurred while deleting animal: {error}")
            return None


class ZoologicoCLI:
    def __init__(self, database):
        self.zoo = ZoologicoDAO(database)

    def createAnimal(self,Animal):
        id = self.zoo.createAnimal(Animal)
        return id

    def readAnimal(self, id):
        self.zoo.readAnimal(id)

    def updateAnimal(self, id, nome, especie, idade, habitat):
        self.zoo.updateAnimal(id, nome, especie, idade, habitat)

    def deleteAnimal(self, id):
        self.zoo.deleteAnimal(id)


db = Database(database="av1", collection="Animais")

z1 = ZoologicoCLI(db)
habitats = []
c1 = Cuidador(1, "Nelson", "123456789")
c2 = Cuidador(2, "Rudeus", "987654321")
habitats0 = Habitat(1, "Floresta Clara", "Floresta", c1)
habitats1 = Habitat(2, "Deserto Cinza", "Deserto", c2)

habitats.append(habitats0)
habitats.append(habitats1)

a1 = Animal("1", "Pandinha", "Urso Panda", 13, habitats[0])

animal_id = z1.createAnimal(a1)
z1.readAnimal(animal_id)
z1.updateAnimal(animal_id, "Cobra Cinza", "Cobra", 50, habitats[1])
z1.deleteAnimal(animal_id)
