import json
from serpapi_async.pagination import Pagination
from serpapi_async.serp_api_client_exception import SerpApiClientException
import aiohttp

GOOGLE_ENGINE = 'google'
BING_ENGINE = 'bing'
BAIDU_ENGINE = 'baidu'
GOOGLE_SCHOLAR_ENGINE = 'google_scholar'
YANDEX_ENGINE = 'yandex'
EBAY_ENGINE = 'ebay'
YAHOO_ENGINE = 'yahoo'
HOME_DEPOT_ENGINE = 'home_depot'
YOUTUBE_ENGINE = 'youtube'


class SerpApiClientAIOHTTP(object):
    """SerpApiClient enables to query any search engines supported by SerpApi and parse the results.
    ```python
    from serpapi import GoogleSearch
    search = SerpApiClient({
        "q": "Coffee", 
        "location": "Austin,Texas", 
        "engine": "google",
        "api_key": "<your private key>"
        })
	data = search.get_json()
    ```

    https://serpapi.com/search-api
    """

    BACKEND = "https://serpapi.com"
    SERP_API_KEY = None

    def __init__(self, params_dict, engine=None, timeout=60000):
        self.params_dict = params_dict
        self.engine = engine
        self.timeout = timeout

    def construct_url(self, path="/search"):
        self.params_dict['source'] = 'python'
        if self.SERP_API_KEY:
            self.params_dict['serp_api_key'] = self.SERP_API_KEY
        if self.engine:
            if not 'engine' in self.params_dict:
                self.params_dict['engine'] = self.engine
        if not 'engine' in self.params_dict:
            raise SerpApiClientException("engine must be defined in params_dict or engine")
        return self.BACKEND + path, self.params_dict

    async def get_response(self, path='/search'):
        """Returns:
            Response object provided by requests.get
        """
        url = None
        try:
            url, parameters = self.construct_url(path)
            print(url)
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, ) as response:
                    return await response.text()
        except Exception as e:
            print("fail: " + url)
            raise e

    async def get_results(self, path='/search'):
        """Returns:
            Response text field
        """
        return await self.get_response(path)

    async def get_html(self):
        """Returns:
            Raw HTML search result from Gooogle
        """
        return await self.get_results()

    async def get_json(self):
        """Returns:
            Formatted JSON search results using json package
        """
        self.params_dict["output"] = "json"
        return json.loads(await self.get_results())

    async def get_raw_json(self):
        """Returns:
            Formatted JSON search result as string
        """
        self.params_dict["output"] = "json"
        return await self.get_results()

    async def get_dictionary(self):
        """Returns:
            Dict with the formatted response content
        """
        return dict(await self.get_json())

    async def get_dict(self):
        """Returns:
            Dict with the formatted response content
            (alias for get_dictionary)
        """
        return await self.get_dictionary()

    async def get_object(self):
        """Returns: 
            Dynamically created python object wrapping the result data structure
        """
        # iterative over response hash
        node = self.get_dictionary()
        # create dynamic python object
        return await self.make_pyobj("response", node)

    async def make_pyobj(self, name, node):
        pytype = type(name, (object,), {})
        pyobj = pytype()

        if isinstance(node, list):
            setattr(pyobj, name, [])
            for el in node:
                getattr(pyobj, name).append(self.make_pyobj(name, el))
            return pyobj
        elif isinstance(node, dict):
            for name, child in node.items():
                if isinstance(child, list):
                    setattr(pyobj, name, [])
                    for el in child:
                        getattr(pyobj, name).append(self.make_pyobj(name, el))
                elif isinstance(child, dict):
                    setattr(pyobj, name, self.make_pyobj(name, child))
                else:
                    setattr(pyobj, name, child)
        else:
            setattr(pyobj, name, node)

        return pyobj

    async def get_search_archive(self, search_id, format='json'):
        """Retrieve search result from the Search Archive API
        Parameters:
            search_id (int): unique identifier for the search provided by metadata.id 
            format (string): search format: json or html [optional]
        Returns:
            dict|string: search result from the archive
        """
        result = await self.get_results("/searches/{0}.{1}".format(search_id, format))
        if format == 'json':
            result = json.loads(result)
        return result

    async def get_account(self):
        """Get account information using Account API
        Returns:
            dict: account information
        """
        return json.loads(await self.get_results("/account"))

    async def get_location(self, q, limit=5):
        """Get location using Location API
        Parameters:
            q (string): location (like: city name..)
            limit (int): number of matches returned
        Returns:
            dict: Location matching q
        """
        self.params_dict = {}
        self.params_dict["output"] = "json"
        self.params_dict["q"] = q
        self.params_dict["limit"] = limit
        buffer = await self.get_results('/locations.json')
        return json.loads(buffer)

    def pagination(self, start=0, end=1000000000, page_size=10):
        """Return:
            Generator to iterate the search results pagination
        """
        return Pagination(self, start, end, page_size)
