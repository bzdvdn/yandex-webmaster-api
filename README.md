# wrapper for yandex webmaster api

## Install

Install using `pip`...

    pip install yandex-webmaster-api

## Usage

=======

```python
from yandex_webmaster import YandexWebmaster
client = YandexWebmaster('<access_token>')
```

### get hosts

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts.html

```python
hosts = client.get_hosts()
```

### get popular search queries

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-search-queries-popular.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | datetime | required |
  | date_to | datetime | required |
  | query_indicator | List[str] | required |
  | order_by | Optional[str] | TOTAL_SHOWS |
  | device_type_indicator | Optional[str] | None |
  | limit | int | 500 |
  | offset | int | 0 |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_popular_search_queries('<host_id>', date_from, date_to, query_indicator=['TOTAL_SHOWS'])
```

### get search query all history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-search-queries-history-all.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | datetime | required |
  | date_to | datetime | required |
  | query_indicator | List[str] | required |
  | order_by | Optional[str] | TOTAL_SHOWS |
  | device_type_indicator | Optional[str] | None |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_search_query_all_history('<host_id>', date_from, date_to, query_indicator=['TOTAL_SHOWS'], device_type_indicator='DESKTOP')
```

### get single search query history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-search-queries-history.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | query_id | str | required |
  | date_from | datetime | required |
  | date_to | datetime | required |
  | query_indicator | List[str] | required |
  | device_type_indicator | Optional[str] | None |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_single_search_query_history('<host_id>', '<query_id>', date_from, date_to, query_indicator=['TOTAL_SHOWS'], device_type_indicator='DESKTOP')
```

### get list query analytics

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-query-analytics.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | device_type_indicator | str | "ALL" |
  | text_indicator | str | "URL" |
  | limit | int | 20 |
  | offset | int | 0 |
  | region_ids | Optional[list] | None |
  | filters | Optional[dict] | None |
  | sort_by_date | Optional[dict] | None |

```python
result = client.get_list_query_analytics('<host_id>', "ALL", limit=500, offset=500)
```

### get host info

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-id.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.get_host('<host_id>')
```

### get sqi history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/sqi-history.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | datetime | required |
  | date_to | datetime | required |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_sqi_history('<host_id>', '<query_id>', date_from, date_to)
```

### add host

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-add-site.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_url | str | required |

```python
result = client.add_host(host_url='<host_url>')
```

### delete host

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-delete.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.delete_host(host_id='<host_id>')
```

### get sitemaps

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-sitemaps-get.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.get_sitemaps(host_id='<host_id>')
```

### get_sitemap

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-sitemaps-get.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | sitemap_id | str | required |

```python
result = client.get_sitemap(host_id='<host_id>', sitemap_id='<sitemap_id>')
```

### add sitemap

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-user-added-sitemaps-post.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | host_url | str | required |

```python
result = client.add_sitemap(host_id='<host_id>', host_url='<host_url>')
```

### delete sitemap

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-user-added-sitemaps-post.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | sitemap_id | str | required |

```python
result = client.delete_sitemap(host_id='<host_id>', sitemap_id='<sitemap_id>')
```

### get indexing stats

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-id-summary.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.get_indexing_stats(host_id='<host_id>')
```

### get indexing history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-id-summary.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | str | required |
  | date_to | str | required |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_indexing_history(host_id='<host_id>', date_from=date_from, date_to=date_to)
```

### get indexing samples

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-indexing-samples.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | limit | int | 100 |
  | offest | int | 0 |

```python
result = client.get_indexing_samples(host_id='<host_id>')
```

### get monitoring important urls

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-id-important-urls.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.get_monitoring_important_urls(host_id='<host_id>')
```

### get important url history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-id-important-urls.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | url | str | required |

```python
result = client.get_important_url_history(host_id='<host_id>', url='<url>')
```

### get insearch url history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-indexing-insearch-history.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | str | required |
  | date_to | str | required |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_important_url_history(host_id='<host_id>', date_from=date_from, date_to=date_to)
```

### get insearch url samples

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-indexing-insearch-history.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | limit | int | 100 |
  | offest | int | 0 |

```python
result = client.get_insearch_url_samples(host_id='<host_id>', limit=limit, offset=offset)
```

### get insearch url events history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-search-events-history.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | str | required |
  | date_to | str | required |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_insearch_url_events_history(host_id='<host_id>', date_from=date_from, date_to=date_to)
```

### get insearch url events samples

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/hosts-search-events-samples.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | limit | int | 100 |
  | offest | int | 0 |

```python
result = client.get_insearch_url_events_samples(host_id='<host_id>', limit=limit, offset=offset)
```

### recrawl url

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-post.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | url | str | required |

```python
result = client.recrawl_url(host_id='<host_id>', url='<recrawl_url>')
```

### get recrawl task

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-task-get.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | task_id | str | required |

```python
result = client.get_recrawl_task(host_id='<host_id>', task_id='<task_id>')
```

### get recrawl tasks

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-get.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | datetime | required |
  | date_to | datetime | required |
  | limit | int | 100 |
  | offset | int | 0 |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_recrawl_tasks(
    host_id='<host_id>',
    date_from=date_from,
    date_to=date_to,
    limit=10,
    offset=10
)
```

### get recrawl quota

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-recrawl-quota-get.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.get_recrawl_quota(host_id='<host_id>')
```

### diagnostic site

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-diagnostics-get.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.diagnostic_site(host_id='<host_id>')
```

### get broken internal links samples

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-diagnostics-get.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | indicator | str | required |
  | limit | int | 100 |
  | offset | int | 0 |

```python
result = client.get_broken_internal_links_samples(host_id='<host_id>', indicator='SITE_ERROR')
```

### get broken internal links history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-links-internal-history.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | date_from | datetime | required |
  | date_to | datetime | required |

```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=4)
date_to = datetime.now()
result = client.get_broken_internal_links_samples(host_id='<host_id>', date_from=date_from, date_to=date_to)
```

### get external links samples

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-links-external-samples.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |
  | limit | int | 100 |
  | offset | int | 0 |

```python
result = client.get_external_links_samples(host_id='<host_id>')
```

### get external links history

- doc - https://yandex.ru/dev/webmaster/doc/dg/reference/host-links-external-history.html
- params
  | name | type | default value |
  | :--------------------: | :--: | :-----------: |
  | host_id | str | required |

```python
result = client.get_external_links_history(host_id='<host_id>')
```

## CHANGELOG

0.0.3 - change query_indicator params to list[str]
0.0.2 - add get_list_query_analytics method
