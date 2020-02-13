from jsonpickle.pickler import Pickler
from jsonpickle.unpickler import Unpickler
from typing import Dict, List
from botbuilder.core import Storage
import motor.motor_asyncio


class MongodbStorage(Storage):
    """The class for MongoDB middleware for the Azure Bot Framework."""

    ID_TAG = 'real_id'
    DOCUMENT_TAG = 'document'

    def __init__(self, connection_string, db, collection, **kwargs):
        """Create the storage object.

        :param connection_string: mongoDB connection URI
        :param db: db name
        :param collection: collection name
        :param kwargs: parameters to pass to MongoClient as keyword arguments
        """
        super(MongodbStorage, self).__init__()

        self.connection_string = connection_string
        self.db_name = db
        self.collection_name = collection

        self.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string, **kwargs)
        self.db = self.mongodb_client[self.db_name]

    async def write(self, changes: Dict[str, object]):
        """Save storeitems to storage.

        :param changes:
        :return:
        """
        if changes is None:
            raise Exception("Changes are required when writing")
        if not changes:
            return
        try:
            # get the collection to save changes in
            collection = self.__collection

            for (key, change) in changes.items():
                # create a dictionary from the change object
                doc = self.__create_dict(change)

                # save each change in db collection
                await collection.update_one({MongodbStorage.ID_TAG: key},
                                            {'$set': {MongodbStorage.DOCUMENT_TAG: doc}},
                                            upsert=True)
        except Exception as error:
            raise error

    async def read(self, keys: List[str]):
        """Read storeitems from storage.

        :param keys:
        :return dict:
        """
        data = {}
        if not keys:
            return data
        try:
            # get the collection to read storeitems from
            collection = self.__collection

            # get the data for given keys from db collection
            data_from_db = collection.find({MongodbStorage.ID_TAG: {'$in': keys}})

            async for item in data_from_db:
                # create a storeitem from each db and save it in the result dictionary
                data[item[MongodbStorage.ID_TAG]] = self.__create_object(item)
        except TypeError as error:
            raise error

        return data

    async def delete(self, keys: List[str]):
        """Remove storeitems from storage.

        :param keys:
        :return:
        """
        try:
            # get the collection to delete storeitems from
            collection = self.__collection

            # delete all storeitems for given keys
            await collection.delete_many({MongodbStorage.ID_TAG: {'$in': keys}})
        except TypeError as error:
            raise error

    @property
    def __collection(self) -> motor.motor_asyncio.AsyncIOMotorCollection:
        """Return db collection where storeitems are stored.

        :param:
        :return motor.motor_asyncio.AsyncIOMotorCollection:
        """
        return self.db[self.collection_name]

    @staticmethod
    def __create_object(result) -> object:
        """Create an object from a result out of MongoDb.

        :param result:
        :return object:
        """
        # get the document item from the result and turn into a dict
        doc = result.get(MongodbStorage.DOCUMENT_TAG)

        # create and return the object
        result_obj = Unpickler().restore(doc)

        return result_obj

    @staticmethod
    def __create_dict(store_item: object) -> Dict:
        """Return the dict of an object.
        This eliminates non_magic attributes and the e_tag.

        :param store_item:
        :return dict:
        """
        # read the content
        json_dict = Pickler().flatten(store_item)
        if "e_tag" in json_dict:
            del json_dict["e_tag"]

        return json_dict
