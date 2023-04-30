import os
import requests
from models import *
from dotenv import load_dotenv

load_dotenv()


api_key = os.environ.get("API_KEY")


def _request(query, category, sort=None):
    """
    Makes request to Best Buy API

    Args:
        category (str): Refers to different APIs (products, categories, stores, openBox)
        query (str): Query for the specific APIs (https://bestbuyapis.github.io/bby-query-builder/#/productSearch)
        sort (str): None

    Returns:
        str: JSON response of request

    """
    return requests.get(
        'https://api.bestbuy.com/v1/{category}{query}?apiKey={key}{sort}&format=json'.format(
            category=category, query=query, key=api_key, sort=(
                sort if sort else ""))).json()


class BestBuy:
    """
    A class for storing different Best Buy API requests.
    """

    """
    1. Change _query to _request
    2. Change key to api_key
    """

    def __init__(self):
        """
        Initializes an instance depending on the API.
        """

        global api_key
        self.ProductAPI = ProductAPI()
        self.StoreAPI = StoreAPI()
        self.RecommendationAPI = RecommendationAPI()
        self.CategoryAPI = CategoryAPI()
        self.OpenBoxAPI = OpenBoxAPI()
        self.StoreAPI = StoreAPI()


class ProductAPI:

    def _query(self, query, sort=None):
        """
        Private function to call API

        Args:
            query (str): Query for API

        Returns:
            list: Either a single or list of Product object(s)
        """
        product_list = _request(
            query,
            'products',
            '&sort={0}.asc'.format(sort) if sort else None).get(
            'products',
            [])
        return [Product(product) for product in product_list]

    def search(self, keyword=None, **kwargs):
        """
        Search Best Buy Product catalog based on search Keyword(s) and product attributes

        Args:
            keyword (str): search element
            **kwargs (str): key, value pair (product attribute, search (any))

        Options:
            bestSellingRank: str,
            categoryPath.id: str,
            categoryPath.name: str,
            color: str,
            condition: str (new, reburished),
            customerReviewAverage: float,
            customerReviewCount: float,
            description: str,
            dollarSavings: float,
            freeShipping: boolean,
            inStoreAvailability: boolean,
            manufacturer: str,
            modelNumber: str,
            name: str,
            onlineAvailability: boolean,
            onSale: boolean,
            percentSavings: float,
            preowned: boolean,
            regularPrice: float,
            salePrice: float,
            shippingCost: float,
            sku: str,
            type: str,
            upc: str

        Returns:
            list: List of all products based on criteria
        """

        if not keyword:
            keyword = ""
        else:
            keyword = '(search={})'.format(keyword)
        if kwargs:
            keyword += '&'
            for key, value in kwargs.items():
                keyword = '{s}{k}={v}&'.format(s=keyword, k=key, v=value)
            keyword = '({})'.format(keyword[:-1])
        return self._query(keyword)

    def search_sku(self, sku, sort=None):
        """
        Search Best Buy Product catalog based on sku

        Args:
            sku (str): search element

        Returns:
            object: Singular Product object
        """

        try:
            return self._query('(sku={0})'.format(str(sku)), sort)[0]
        except IndexError:
            return None

    def search_upc(self, upc, sort=None):
        """
        Search Best Buy Product catalog based on upc

        Args:
            upc (str): search element

        Returns:
            object: Singular Product object
        """

        try:
            return self._query('(upc={0})'.format(str(upc)), sort)[0]
        except IndexError:
            return None

    def search_description(self, description, sort=None):
        """
        Search Best Buy Product catalog based on description

        Args:
            description (str): search element

        Returns:
            object: Singular Product object
        """
        return self._query('(description={0})'.format(description), sort=None)


class StoreAPI:

    def _query(self, query):
        store_list = _request(
            'v1',
            '({0})'.format(query),
            'stores',
            None).get(
            'stores',
            [])
        return [Store(store) for store in store_list]

    def search_postal_code(
            self,
            postal_code,
            distance=None,
            store_services=[],
            store_type=[]):
        """
        Searches for stores within a given postal code and optional distance,
        filtering by store services and type.

        Args:
            postal_code (str): The postal code to search for stores around.
            distance (int): The maximum distance in kilometers to search for stores.
                            If not specified, all stores in the postal code are returned.
            store_services (list[str]): A list of services to filter the stores by.
                                        Only stores that provide all of the specified services will be returned.
            store_type (list[str]): A list of store types to filter the stores by.
                                    Only stores that are of any of the specified types will be returned.

        Returns:
            list[object]: A list of Store objects matching the specified criteria.
        """
        query = ""
        if store_type:
            query = query + '&('
            for storeType in store_type:
                query = query + "(storeType={0})|".format(storeType)
            query = query[:-1] + ")"
        if store_services:
            query = query + '&('
            for service in store_services:
                query = query + "(services.service=\"{0}\")&".format(service)
            query = query[:-1] + ")"
        if distance:
            return self._query(
                '(area({0},{1}))'.format(
                    str(postal_code),
                    str(distance)))
        return self._query(
            '(postalCode={0}){1}'.format(str(postal_code, query)))

    def search_city(self, city, store_services=[], store_type=[]):
        """
        Searches for stores within a given city, filtering by store services and type.

        Args:
            city (str): The name of the city to search for stores in.
            store_services (list[str]): A list of services to filter the stores by.
                                        Only stores that provide all of the specified services will be returned.
            store_type (list[str]): A list of store types to filter the stores by.
                                    Only stores that are of any of the specified types will be returned.

        Returns:
            list[object]: A list of Store objects matching the specified criteria.
        """
        query = ""
        if store_type:
            query = query + '&('
            for storeType in store_type:
                query = query + "(storeType={0})|".format(storeType)
            query = query[:-1] + ")"
        if store_services:
            query = query + '&('
            for service in store_services:
                query = query + "(services.service=\"{0}\")&".format(service)
            query = query[:-1] + ")"
        return self._query('(city={0}){1}'.format(city, query))

    def search_lat_long(
            self,
            latitude,
            longitude,
            distance,
            store_services=[],
            store_type=[]):
        """
        Searches for stores within a given distance from a specified latitude and longitude,
        filtering by store services and type.

        Args:
            latitude (float): The latitude of the location to search around.
            longitude (float): The longitude of the location to search around.
            distance (int): The maximum distance in kilometers to search for stores.
            store_services (list[str]): A list of services to filter the stores by.
                                        Only stores that provide all of the specified services will be returned.
            store_type (list[str]): A list of store types to filter the stores by.
                                    Only stores that are of any of the specified types will be returned.

        Returns:
            list[object]: A list of Store objects matching the specified criteria.
        """
        query = ""
        if store_type:
            query = query + '&('
            for storeType in store_type:
                query = query + "(storeType={0})|".format(storeType)
            query = query[:-1] + ")"
        if store_services:
            query = query + '&('
            for service in store_services:
                query = query + "(services.service=\"{0}\")&".format(service)
            query = query[:-1] + ")"
        return self._query(
            '(area({0},{1},{2}){3}'.format(
                str(latitude),
                str(longitude),
                str(distance),
                query))

    def search_store_id(self, store_id, store_services=[], store_type=[]):
        """
        Searches for a store by its ID, filtering by store services and type.

        Args:
            store_id (str): The ID of the store to search for.
            store_services (list[str]): A list of services to filter the stores by.
                                        Only stores that provide all of the specified services will be returned.
            store_type (list[str]): A list of store types to filter the stores by.
                                    Only stores that are of any of the specified types will be returned.

        Returns:
            object or None: A Store object matching the specified criteria if found, else None.
        """
        query = ""
        if store_type:
            query = query + '&('
            for storeType in store_type:
                query = query + "(storeType={0})|".format(storeType)
            query = query[:-1] + ")"
        if store_services:
            query = query + '&('
            for service in store_services:
                query = query + "(services.service=\"{0}\")&".format(service)
            query = query[:-1] + ")"
        try:
            return self._query(
                '(storeId={0}){1}'.format(
                    str(store_id), query))[0]
        except IndexError:
            return None

    def search_region_state(
            self,
            region_state,
            store_services=[],
            store_type=[]):
        """
        Search Best Buy stores by region/state name and optional filter parameters.

        Args:
            region_state (str): Name of the region/state to search stores in.
            store_services (list, optional): List of service names to filter stores by. Defaults to [].
            store_type (list, optional): List of store type names to filter stores by. Defaults to [].

        Returns:
            list: List of Store objects that match the search criteria.
        """
        query = ""
        if store_type:
            query = query + '&('
            for storeType in store_type:
                query = query + "(storeType={0})|".format(storeType)
            query = query[:-1] + ")"
        if store_services:
            query = query + '&('
            for service in store_services:
                query = query + "(services.service=\"{0}\")&".format(service)
            query = query[:-1] + ")"
        return self._query('(region={0}){1}'.format(region_state), query)


class CategoryAPI:

    def _query(self, query):
        category_list = _request(
            'v1',
            '{0}'.format(query),
            'categories',
            None).get(
            'categories',
            [])
        """
        Send request with the specified query to the Best Buy API and parse the returned data to a list of Category objects.

        Args:
            query (str): The query to send to the Best Buy API.

        Returns:
            list: List of Category objects that match the search criteria.
        """
        return [Category(category) for category in category_list]

    def search_all_categories(self):
        """
        Returns a list of all Category objects available from Best Buy.

        Returns:
            list: List of all Category objects available from Best Buy.
        """
        return self._query('')

    def search_top_level_categories(self):
        """
        Returns a list of all top level Category objects available from Best Buy.

        Returns:
            list: List of all top level Category objects available from Best Buy.
        """
        return self._query('(id=abcat*)')

    def search_category_name(self, name):
        """
        Returns a list of all Category objects whose names match the provided search element.

        Args:
            name (str): The name of the category to search for.

        Returns:
            list: List of all Category objects whose names match the provided search element.
        """
        return self._query('(name={0}*)'.format(str(name)))

    def search_category_id(self, id):
        """
        Returns a list of all Category objects whose IDs match the provided search element.

        Args:
            id (str): The ID of the category to search for.

        Returns:
            list: List of all Category objects whose IDs match the provided search element.
        """
        return self._query('(id={0})'.format(str(id)))


class OpenBoxAPI:

    def _query(self, query):
        openBox_list = _request(
            'beta/products',
            query,
            'openBox',
            None).get(
            'results',
            [])
        return [OpenBox(openBox) for openBox in openBox_list]

    def all_open_box_offers(self):
        """
        Returns all OpenBox offers.

        Returns:
            list: List of all OpenBox objects.
        """

        return self._query('')

    def open_box_offers_skus(self, skus):
        query = ""
        for sku in skus:
            query = str(sku) + ", "
        query = query[:-2]
        """
        Returns OpenBox offers by a list of SKUs.

        Args:
            skus (list): List of SKU strings.

        Returns:
            list: List of OpenBox objects that match the search criteria.
        """

        return self._query('(sku%20%in({0}))'.format(query))

    def open_box_offers_category_id(self, category_id):
        """
        Returns OpenBox offers by a category ID.

        Args:
            category_id (str): Category ID string.

        Returns:
            list: List of OpenBox objects that match the search criteria.
        """
        return self._query('(categoryId={0})'.format(str(category_id)))


class RecommendationAPI:

    def _query(self, query, endpoint):
        recommendation_list = _request(
            'beta/products',
            '{0}'.format(query),
            endpoint,
            None).get(
            'results',
            [])
        return [Recommendation(recommendation)
                for recommendation in recommendation_list]

    def most_popular_category_id(self, category_id):
        """
        Returns a list of Recommendation objects for the most popular products in a category.

        Args:
            category_id (str): The ID of the category to search for.

        Returns:
            list: A list of Recommendation objects.
        """

        return self._query(
            '(categoryId={0})'.format(
                str(category_id)),
            'mostViewed')

    def trending_category_id(self, category_id):
        """
        Returns a list of Recommendation objects for the trending products in a category.

        Args:
            category_id (str): The ID of the category to search for.

        Returns:
            list: A list of Recommendation objects.
        """

        return self._query(
            '(categoryId={0})'.format(
                str(category_id)),
            'trendingViewed')


class SmartListAPI:
    def connected_home_smart_list():
        return _request('beta/products', '', 'connectedHome')


    def active_adventurer_smart_list():
        return _request('beta/products', '', 'activeAdventurer')
