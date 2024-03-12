from typing import Optional
from datetime import datetime
from urllib.parse import urlencode
from typing import List

from requests import Session

from .errors import YandexWebmasterError


class YandexWebmaster(object):
    API_URL = "https://api.webmaster.yandex.net/v4/"

    def __init__(self, access_token: str):
        self.set_access_token(access_token)
        self._session = self._init_session()
        self.user_id = self.get_user_id()

    def _send_api_request(
        self, http_method: str, endpoint: str, params: Optional[dict] = None
    ) -> dict:
        method = getattr(self._session, http_method)
        url = f"{self.API_URL}{endpoint}"
        if http_method == "post":
            response = method(url, json=params)
        else:
            if params:
                url = f"{url}?{urlencode(list(params.items()), doseq=True)}"
            response = method(url)
        if response.status_code == 204:
            return {}
        json_response = response.json()
        if response.status_code > 399:
            raise YandexWebmasterError(
                json_response["error_message"], json_response["error_code"]
            )
        return json_response

    def get_user_id(self) -> dict:
        response = self._send_api_request("get", "user")
        return response["user_id"]

    def get_hosts(self) -> list:
        """return user hosts
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts.html
        Returns:
            list: [{
            "host_id": "http:ya.ru:80",
            "ascii_host_url": "http://xn--d1acpjx3f.xn--p1ai/",
            "unicode_host_url": "http://яндекс.рф/",
            "verified": true,
            "main_mirror": {
                "host_id": "http:ya.ru:80",
                "verified": true,
                "ascii_host_url": "http://xn--d1acpjx3f.xn--p1ai/",
                "unicode_host_url": "http://яндекс.рф/"
            }
            }]
        """
        response = self._send_api_request("get", f"user/{self.user_id}/hosts")
        return response["hosts"]

    def get_popular_search_queries(
        self,
        host_id: str,
        date_from: datetime,
        date_to: datetime,
        query_indicator: List[str],
        order_by: str = "TOTAL_SHOWS",
        device_type_indicator: Optional[str] = "ALL",
        limit: int = 500,
        offset: int = 0,
    ) -> dict:
        """get popular queries
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-search-queries-popular.html
        Args:
            host_id (str): site id
            date_from (datetime): date from
            date_to (datetime): date to
            query_indicator (Optional[List[str]], optional): TOTAL_SHOWS or TOTAL_CLICK OR AVG_SHOW_POSITION or AVG_CLICK_POSITION. Defaults to None.
            order_by (str, optional): TOTAL_SHOWS or TOTAL_CLICK. Defaults to 'TOTAL_SHOWS'.
            device_type_indicator (Optional[str], optional): ALL or TABLET or MOBILE or DESKTOP or MOBILE_AND_TABLET. Defaults to ALL.
            limit (int, optional): [description]. Defaults to 500.
            offset (int, optional): [description]. Defaults to 0.

        Returns:
            dict: [description]
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/search-queries/popular"
        params = {
            "order_by": order_by,
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "limit": limit,
            "offset": offset,
            "device_type_indicator": device_type_indicator,
        }
        if query_indicator is not None:
            params["query_indicator"] = query_indicator
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_search_query_all_history(
        self,
        host_id: str,
        query_indicator: List[str],
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        device_type_indicator: Optional[str] = None,
    ) -> dict:
        """get all search query history
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-search-queries-history-all.html
        Args:
            host_id (str): site- id
            date_from (Optional[datetime], optional): datetime. Defaults to None.
            date_to (Optional[datetime], optional): datetime. Defaults to None.
            query_indicator (List[str]): TOTAL_SHOWS or TOTAL_CLICKS.
            device_type_indicator (Optional[str], optional): ALL or TABLET or MOBILE or DESKTOP or MOBILE_AND_TABLET. Defaults to None.

        Returns:
            dict: {
                "indicators": {
                    "TOTAL_SHOWS": [
                        {
                            "date": "2019-07-18T00:00:00.000+03:00",
                            "value": 100.0
                        },
                        ...
                        }
                    ]
                }
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/search-queries/all/history"
        params = {}
        if date_from is not None:
            params["date_from"] = date_from.strftime("%Y-%m-%d")
        if date_to is not None:
            params["date_to"] = date_to.strftime("%Y-%m-%d")
        if query_indicator is not None:
            params["query_indicator"] = query_indicator
        if device_type_indicator is not None:
            params["device_type_indicator"] = device_type_indicator
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_single_search_query_history(
        self,
        host_id: str,
        query_id: str,
        query_indicator: List[str],
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        device_type_indicator: Optional[str] = None,
    ) -> dict:
        """get single query history
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-search-queries-history.html
        Args:
            host_id (str): site_id
            query_id (str): query id
            date_from (Optional[datetime], optional): datetime. Defaults to None.
            date_to (Optional[datetime], optional): datetime. Defaults to None.
            query_indicator (str): TOTAL_SHOWS or TOTAL_CLICKS. Defaults to None.
            device_type_indicator (Optional[str], optional): ALL or TABLET or MOBILE or DESKTOP or MOBILE_AND_TABLET. Defaults to None.
        Returns:
            dict: {
                "queries": [
                    {
                    "query_id": "a08b",
                    "query_text": "some text",
                    "indicators": {
                        "TOTAL_SHOWS": [
                            {
                                "date": "2019-07-18T00:00:00.000+03:00",
                                "value": 2.0
                            },
                            ...
                        ]
                    }
                }
        """
        endpoint = (
            f"user/{self.user_id}/hosts/{host_id}/search-queries/{query_id}/history"
        )
        params = {}
        if date_from is not None:
            params["date_from"] = date_from.strftime("%Y-%m-%d")
        if date_to is not None:
            params["date_to"] = date_to.strftime("%Y-%m-%d")
        if query_indicator is not None:
            params["query_indicator"] = query_indicator
        if device_type_indicator is not None:
            params["device_type_indicator"] = device_type_indicator
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_list_query_analytics(
        self,
        host_id: str,
        device_type_indicator: str = "ALL",
        text_indicator: str = "URL",
        limit: int = 20,
        offset: int = 0,
        region_ids: Optional[list] = None,
        filters: Optional[dict] = None,
        sort_by_date: Optional[dict] = None,
    ) -> dict:
        """list query analytics
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-query-analytics.html

        Args:
            host_id (str): host id
            device_type_indicator (str, optional): device indictator. Defaults to "ALL".
            text_indicator (str, optional): text inditactor. Defaults to "URL".
            limit (int, optional): limit page. Defaults to 20.
            offset (int, optional): offset page. Defaults to 0.
            region_ids (Optional[list], optional): regions. Defaults to None.
            filters (Optional[dict], optional): filters. Defaults to None.
            sort_by_date (Optional[dict], optional): sort data. Defaults to None.

        Returns:
            dict: {
                "count": 5175,
                "text_indicator_to_statistics": [
                    {
                        "text_indicator": {
                            "type": "URL",
                            "value": "some text"
                        },
                        "statistics": [
                            {
                                "date": "2023-04-15",
                                "field": "CLICKS",
                                "value": 7.0
                            },
                            {
                                "date": "2023-04-15",
                                "field": "POSITION",
                                "value": 4.0
                            },
                            {
                                "date": "2023-04-15",
                                "field": "IMPRESSIONS",
                                "value": 8595.0
                            },
                            {
                                "date": "2023-04-15",
                                "field": "CTR",
                                "value": 0.0
                            },
                        ...
                        }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/query-analytics/list"
        data = {
            "limit": limit,
            "offset": offset,
            "device_type_indicator": device_type_indicator,
            "text_indicator": text_indicator,
        }
        if region_ids:
            data["region_ids"] = region_ids
        if filters:
            data["filters"] = filters
        if sort_by_date:
            data["sort_by_date"] = sort_by_date
        response = self._send_api_request("post", endpoint=endpoint, params=data)
        return response

    def get_host(self, host_id: str) -> dict:
        """get site info
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-id.html
        Args:
            host_id (str): site id

        Returns:
            dict: {
                "host_id": "https:ya.ru:443",
                "verified": true,
                "ascii_host_url": "https://ya.ru/",
                "unicode_host_url": "https://ya.ru/",
                "main_mirror": {
                    "host_id": "http:xn--d1acpjx3f.xn--p1ai:80",
                    "ascii_host_url": "http://xn--d1acpjx3f.xn--p1ai/",
                    "unicode_host_url": "http://яндекс.рф/",
                    "verified": false
                },
                "host_data_status": "NOT_INDEXED",
                "host_display_name": "Ya.ru"
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}"
        response = self._send_api_request("get", endpoint)
        return response

    def get_sqi_history(
        self,
        host_id: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> dict:
        """get sqi history
        DOC - https://yandex.ru/dev/webmaster/doc/dg/reference/sqi-history.html
        Args:
            host_id (str): site id
            date_from (Optional[datetime], optional): datetime. Defaults to None.
            date_to (Optional[datetime], optional): datetime. Defaults to None.

        Returns:
            dict: {
            "points": [
                    {
                        "date": "2016-01-01T00:00:00,000+0300",
                        "value": 1
                    }
                ]
            }
        """
        params = {}
        if date_from is not None:
            params["date_from"] = date_from.strftime("%Y-%m-%d")
        if date_to is not None:
            params["date_to"] = date_to.strftime("%Y-%m-%d")
        endpoint = f"user/{self.user_id}/hosts/{host_id}/sqi-history"
        response = self._send_api_request("get", endpoint, params)
        return response

    def add_host(self, host_url: str) -> dict:
        """add site to webmaster
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-add-site.html
        Args:
            host_url (str): site url

        Returns:
            dict: {
                "host_url": "http://example.com"
            }
        """
        params = {"host_url": host_url}
        endpoint = f"user/{self.user_id}/hosts"
        response = self._send_api_request("post", endpoint, params)
        return response

    def delete_host(self, host_id: str) -> dict:
        """delete site from webmaster
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-delete.html
        Args:
            host_id (str): site id

        Returns:
            dict: {}
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}"
        response = self._send_api_request("delete", endpoint)
        return response

    def get_sitemaps(
        self,
        host_id: str,
        parent_id: Optional[str] = None,
        limit: int = 10,
        from_site_id: Optional[str] = None,
    ) -> dict:
        """get alls sitemsaps
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-sitemaps-get.html
        Args:
            host_id (str): id of host
            parent_id (Optional[str], optional): parent sitemap_id. Defaults to None.
            limit (int, optional): limit rows. Defaults to 10.
            from_site_id (Optional[str], optional): last sitemap_id. Defaults to None.

        Returns:
            dict: {
                "sitemaps": [
                {
                    "sitemap_id": "c7-fe:80-c0",
                    "sitemap_url": "some url",
                    "last_access_date": "2016-01-01T00:00:00,000+0300",
                    "errors_count": 1,
                    "urls_count": 1,
                    "children_count": 1,
                    "sources": [
                    "ROBOTS_TXT"
                    ], ...
                    "sitemap_type": "SITEMAP"
                }, ...
            ]
        }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/sitemaps"
        params = {"limit": limit}
        if parent_id:
            params["parent_id"] = parent_id  # type: ignore
        if from_site_id:
            params["from"] = from_site_id  # type: ignore
        response = self._send_api_request("get", endpoint, params=params)
        return response

    def get_sitemap(self, host_id: str, sitemap_id: str) -> dict:
        """get single sitemap
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-sitemaps-sitemap-id-get.html
        Args:
            host_id (str): id of host
            sitemap_id (str): id of sitemap

        Returns:
            dict: {
                "sitemap_id": "c7-fe:80-c0",
                "sitemap_url": "some url",
                "last_access_date": "2016-01-01T00:00:00,000+0300",
                "errors_count": 1,
                "urls_count": 1,
                "children_count": 1,
                "sources": [
                    "ROBOTS_TXT", ...
                ],
                "sitemap_type": "SITEMAP"
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/sitemaps"
        params = {"sitemap_id": sitemap_id}
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_user_added_sitemaps(
        self, host_id: str, limit: int = 100, offset: Optional[str] = None
    ) -> dict:
        """get user added sitemaps
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-user-added-sitemaps-get.html
        Args:
            host_id (str): id of host
            limit (int, optional): limit rows. Defaults to 100.
            offset (Optional[str], optional): pagination offset. Defaults to None.

        Returns:
            dict: {
                "sitemaps": [
                    {
                    "sitemap_id": "c7-fe:80-c0",
                    "sitemap_url": "some url",
                    "added_date": "2016-01-01T00:00:00,000+0300"
                    }, ...
                ],
                "count": 1
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/user-added-sitemaps"
        params = {"limit": limit}
        if offset:
            params["offset"] = offset  # type: ignore
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_user_added_sitemap(self, host_id: str, sitemap_id: str) -> dict:
        """get user added sitemap
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-user-added-sitemaps-sitemap-id-get.html
        Args:
            host_id (str): id of host
            sitemap_id (str): id of sitemap

        Returns:
            dict: {
                "sitemap_id": "c7-fe:80-c0",
                "sitemap_url": "some url",
                "added_date": "2016-01-01T00:00:00,000+0300"
            }
        """
        endpoint = (
            f"user/{self.user_id}/hosts/{host_id}/user-added-sitemaps/{sitemap_id}"
        )
        response = self._send_api_request("get", endpoint)
        return response

    def add_sitemap(self, host_id: str, url: str) -> dict:
        """add sitemap
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-user-added-sitemaps-post.html
        Args:
            host_id (str): id of host
            url (str): url

        Returns:
            dict: {
                "sitemap_id": "c7-fe:80-c0"
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/user-added-sitemaps"
        params = {"url": url}
        response = self._send_api_request("post", endpoint, params)
        return response

    def delete_sitemap(self, host_id: str, sitemap_id: str) -> dict:
        """delete sitemap
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-user-added-sitemaps-sitemap-id-delete.html
        Args:
            host_id (str): id of host
            sitemap_id (str): id of sitemap

        Returns:
            dict:
        """
        endpoint = (
            f"user/{self.user_id}/hosts/{host_id}/user-added-sitemaps/{sitemap_id}"
        )
        response = self._send_api_request("delete", endpoint)
        return response

    def get_indexing_stats(self, host_id: str) -> dict:
        """get indexing statistic
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-id-summary.html
        Args:
            host_id (str): id of host

        Returns:
            dict: {
                "sqi": 1,
                "excluded_pages_count": 1,
                "searchable_pages_count": 1,
                "site_problems": {
                    "FATAL": 1
                }
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/summary"
        response = self._send_api_request("get", endpoint)
        return response

    def get_indexing_history(
        self, host_id: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """get indexing history
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-indexing-history.html
        Args:
            host_id (str): id of host
            date_from (datetime): date from
            date_to (datetime): date to

        Returns:
            dict: {
                "indicators": {
                    "HTTP_2XX": [
                    {
                        "date": "2016-01-01T00:00:00,000+0300",
                        "value": 1
                    }
                    ]
                }
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/indexing/history"
        params = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_indexing_samples(
        self, host_id: str, limit: int = 100, offset: int = 0
    ) -> dict:
        """get indexing samples
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-indexing-samples.html
        Args:
            host_id (str): id of host
            limit (int, optional): row limit. Defaults to 100.
            offset (int, optional): offset limit. Defaults to 0.

        Returns:
            dict: {
                "count": 1,
                "samples": [
                    {
                    "status": "HTTP_2XX",
                    "http_code": 200,
                    "url": "http://example.com/some/path?a=b",
                    "access_date": "2016-01-01T00:00:00,000+0300"
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/indexing/samples"
        params = {
            "limit": limit,
            "offset": offset,
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_monitoring_important_urls(self, host_id: str) -> dict:
        """get monitoring important urls
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-id-important-urls.html
        Args:
            host_id (str): id of host

        Returns:
            dict: {
                "urls": [
                    {
                        "url": "https://example.com/",
                        "update_date": "2019-09-05T00:00:00.000+03:00",
                        "change_indicators": [],
                        "indexing_status": {
                            "status": "HTTP_2XX",
                            "http_code": 200,
                            "access_date": "2019-09-04T00:00:00.000+03:00"
                        },
                        "search_status": {
                            "title": "some string",
                            "description": "some string",
                            "last_access": "2019-09-02T00:00:00.000+03:00",
                            "excluded_url_status": NOTHING_FOUND,
                            "bad_http_status": 500,
                            "searchable": true,
                            "target_url": "https://example.com/some/path?a=b"
                        }
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/important-urls"
        response = self._send_api_request("get", endpoint)
        return response

    def get_important_url_history(self, host_id: str, url: str) -> dict:
        """get important url history
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-id-important-urls-history.html
        Args:
            host_id (str): id of host
            url (str): encoded url  RFC 3986

        Returns:
            dict: {
                "history": [
                    {
                        "url": "https://example.com/",
                        "update_date": "2019-09-05T00:00:00.000+03:00",
                        "change_indicators": [],
                        "indexing_status": {
                            "status": "HTTP_2XX",
                            "http_code": 200,
                            "access_date": "2019-09-04T00:00:00.000+03:00"
                        },
                        "search_status": {
                            "title": "some string",
                            "description": "some string",
                            "last_access": "2019-09-02T00:00:00.000+03:00",
                            "excluded_url_status": NOTHING_FOUND,
                            "bad_http_status": 500,
                            "searchable": true,
                            "target_url": "https://example.com/some/path?a=b"
                        }
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/important-urls"
        params = {"url": url}
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_insearch_url_history(
        self, host_id: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """get insearch url history
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-indexing-insearch-history.html
        Args:
            host_id (str): id of host
            date_from (datetime): date from
            date_to (datetime): date to

        Returns:
            dict: {
                "history": [
                    {
                        "date": "2016-01-01T00:00:00,000+0300",
                        "value": 1
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/search-urls/in-search/history"
        params = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_insearch_url_samples(
        self, host_id: str, limit: int = 100, offset: int = 0
    ) -> dict:
        """get insearch url samples
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-indexing-insearch-samples.html
        Args:
            host_id (str): id of host
            limit (int, optional): limit rows. Defaults to 100.
            offset (int, optional): offset rows. Defaults to 0.

        Returns:
            dict: {
                "count": 1,
                "samples": [
                    {
                        "url": "http://example.com/some/path?a=b",
                        "last_access": "2016-01-01T00:00:00,000+0300",
                        "title": "some string"
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/search-urls/in-search/samples"
        params = {
            "limit": limit,
            "offset": offset,
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_insearch_url_events_history(
        self, host_id: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """get insearch url events history
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-search-events-history.html
        Args:
            host_id (str): id of host
            date_from (datetime): date from
            date_to (datetime): date to

        Returns:
            dict: {
                "count": 1,
                "samples": [
                    {
                        "url": "http://example.com/some/path?a=b",
                        "last_access": "2016-01-01T00:00:00,000+0300",
                        "title": "some string"
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/search-urls/events/history"
        params = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_insearch_url_events_samples(
        self, host_id: str, limit: int = 100, offset: int = 0
    ) -> dict:
        """get insearch url samples
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-search-events-samples.html
        Args:
            host_id (str): id of host
            limit (int, optional): limit rows. Defaults to 100.
            offset (int, optional): offset rows. Defaults to 0.

        Returns:
            dict: {
                "count": 1,
                "samples": [
                    {
                        "url": "http://example.com/some/path?a=b",
                        "last_access": "2016-01-01T00:00:00,000+0300",
                        "title": "some string"
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/search-urls/events/samples"
        params = {
            "limit": limit,
            "offset": offset,
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def recrawl_url(self, host_id: str, url: str) -> dict:
        """recrawl url
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-post.html
        Args:
            host_id (str): id of host
            url (str): url

        Returns:
            dict: {
                "task_id": "c7fe80c0-36e3-11e6-8b2d-df96aa592c0a",
                "quota_remainder": 1
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/recrawl/queue"
        params = {
            "url": url,
        }
        response = self._send_api_request("post", endpoint, params)
        return response

    def get_recrawl_task(self, host_id: str, task_id: str) -> dict:
        """get recrawl task info
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-task-get.html
        Args:
            host_id (str): id of host
            task_id (str): crawl task id

        Returns:
            dict: {
                "task_id": "c7fe80c0-36e3-11e6-8b2d-df96aa592c0a",
                "url": "http://example.com/some/path?a=b",
                "added_time": "2016-01-01T00:00:00,000+0300",
                "state": "IN_PROGRESS"
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/recrawl/queue/{task_id}"
        response = self._send_api_request("get", endpoint)
        return response

    def get_recrawl_tasks(
        self,
        host_id: str,
        date_from: datetime,
        date_to: datetime,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """get recrawl tasks
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-get.html
        Args:
            host_id (str): id of host
            date_from (datetime): date from
            date_to (datetime): date to
            limit (int, optional): limit rows. Defaults to 100.
            offset (int, optional): offset rows. Defaults to 0.

        Returns:
            dict: {
                "tasks": [
                    {
                        "task_id": "c7fe80c0-36e3-11e6-8b2d-df96aa592c0a",
                        "url": "http://example.com/some/path?a=b",
                        "added_time": "2016-01-01T00:00:00,000+0300",
                        "state": "IN_PROGRESS"
                    }
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/recrawl/queue"
        params = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "limit": limit,
            "offset": offset,
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_recrawl_quota(self, host_id: str) -> dict:
        """get recrawl quota
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-quota-get.html
        Args:
            host_id (str): id of host

        Returns:
            dict: {
                "daily_quota": 1,
                "quota_remainder": 1
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/recrawl/quota"
        response = self._send_api_request("get", endpoint)
        return response

    def diagnostic_site(self, host_id: str) -> dict:
        """diagnostic site
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-diagnostics-get.html
        Args:
            host_id (str): id of host

        Returns:
            dict: {
                "problems": {
                    "NO_SITEMAPS": {
                        "severity": "FATAL",
                        "state": "PRESENT",
                        "last_state_update": "2016-01-01T00:00:00,000+0300"
                    }
                }
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/diagnostics"
        response = self._send_api_request("get", endpoint)
        return response

    def get_broken_internal_links_samples(
        self, host_id: str, indicator: str, limit: int = 100, offset: int = 0
    ) -> dict:
        """get broken internal links samples
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-links-internal-samples.html
        Args:
            host_id (str): id of host
            indicator (str): must be ON OF (SITE_ERROR, DISALLOWED_BY_USER, UNSUPPORTED_BY_ROBOT)
            limit (int, optional): limit rows. Defaults to 100.
            offset (int, optional): offset rows. Defaults to 0.

        Returns:
            dict: {
                "count": 1,
                "links": [
                    {
                        "source_url": "http://example.com/page1/",
                        "destination_url": "https://example.com/page2/",
                        "discovery_date": "2019-01-01",
                        "source_last_access_date": "2019-01-01",
                    }, ...
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/links/internal/broken/samples"
        params = {"limit": limit, "offset": offset, "indicator": indicator}
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_broken_internal_links_history(
        self, host_id: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """get broken internal links samples
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-links-internal-history.html
        Args:
            host_id (str): id of host
            date_from (datetime): date from
            date_to (datetime): date to

        Returns:
            dict: {
                "indicators": {
                    "DISALLOWED_BY_USER": [
                        {
                            "date": "2019-04-15T00:00:00.000+03:00",
                            "value": 116
                        }
                    ]
                }
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/links/internal/broken/history"
        params = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_external_links_samples(
        self, host_id: str, limit: int = 100, offset: int = 0
    ) -> dict:
        """get external links samples
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-links-external-samples.html
        Args:
            host_id (str): id of host
            limit (int, optional): limit rows. Defaults to 100.
            offset (int, optional): offset rows. Defaults to 0.

        Returns:
            dict: {
                "count": 1,
                "links": [
                    {
                        "source_url": "https://other-example.com/page/",
                        "destination_url": "https://example.com/page1/",
                        "discovery_date": "2019-01-01",
                        "source_last_access_date": "2019-01-01",
                    }, ...
                ]
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/links/external/samples"
        params = {
            "limit": limit,
            "offset": offset,
        }
        response = self._send_api_request("get", endpoint, params)
        return response

    def get_external_links_history(self, host_id: str) -> dict:
        """get extrenal links history
        DOC: https://yandex.ru/dev/webmaster/doc/dg/reference/host-links-external-history.html
        Args:
            host_id (str): id of host

        Returns:
            dict: {
                "indicators": {
                    "LINKS_TOTAL_COUNT": [
                        {
                            "date": "2019-01-01T00:00:00,000+0300",
                            "value": 1
                        }
                    ]
                }
            }
        """
        endpoint = f"user/{self.user_id}/hosts/{host_id}/links/external/history"
        response = self._send_api_request("get", endpoint)
        return response

    def _init_session(self) -> Session:
        session = Session()
        session.headers.update({"Authorization": f"OAuth {self.access_token}"})
        return session

    @property
    def access_token(self) -> str:
        return self._access_token

    def set_access_token(self, access_token: str) -> None:
        self._access_token = access_token
