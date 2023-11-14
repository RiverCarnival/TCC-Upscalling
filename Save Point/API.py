import requests
import csv

SCOPUS_API_URL = "https://api.elsevier.com/content/search/scopus"
# Substitua pela sua própria chave

def run_scopus_queries(api_key, queries, fields, items_per_page=30):
    for i, query in enumerate(queries):
        try:
            query = query.strip()
            if not query:
                continue

            query = query.replace('"', '')  # Remova as aspas duplas da consulta

            headers = {
                "Accept": "application/json",
                "X-ELS-APIKey": api_key,
            }

            params = {
                "query": query,
                "field": ",".join(fields),
                "date": "2018-2023",
                "count": items_per_page,  # Número de resultados por página
            }

            total_results = 0
            page_number = 1

            with open(f"query_{i}.csv", "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(fields)

                while True:
                    params["start"] = (page_number - 1) * items_per_page
                    response = requests.get(SCOPUS_API_URL, headers=headers, params=params)

                    if response.status_code == 200:
                        response_data = response.json()
                        total_results = int(response_data["search-results"]["opensearch:totalResults"])
                        results = response_data["search-results"]["entry"]

                        for result in results:
                            row = [result.get(field) for field in fields]
                            writer.writerow(row)

                        print(f"Query {i}, Page {page_number} completed. {len(results)} results added to 'query_{i}.csv'")

                        page_number += 1
                        if (page_number - 1) * items_per_page >= total_results:
                            break  # Sai do loop quando todos os resultados são obtidos
                    else:
                        print(f"Error for query {i}, Page {page_number}: {response.status_code} - {response.text}")
                        break

        except Exception as e:
            print(f"Error for query {i}: {str(e)}")

def requisicao(key_api, queries):

    api_key = key_api
    fields = ['dc:creator', 'author-profiles:author-profile:author-profile-id', 'dc:title', 'prism:coverDate',
              'prism:publicationName', 'prism:volume', 'prism:issue', 'prism:artNo', 'prism:pageRange',
              'prism:pageCount', 'citedby-count', 'prism:doi', 'prism:url', 'subtypeDescription',
              'publication-stage', 'openaccessFlag', 'prism:sourceTitle', 'eid']

    run_scopus_queries(api_key, queries, fields)
