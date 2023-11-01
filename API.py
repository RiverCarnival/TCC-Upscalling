import requests
import csv

SCOPUS_API_URL = "https://api.elsevier.com/content/search/scopus"
# Substitua pela sua própria chave

def run_scopus_queries(api_key, queries, fields):
    for i, query in enumerate(queries):
        try:
            query = query.strip()
            if not query:
                continue

            headers = {
                "Accept": "application/json",
                "X-ELS-APIKey": api_key,
            }

            params = {
                "query": query,
                "field": ",".join(fields),
                "date": "2018-2023",
            }

            response = requests.get(SCOPUS_API_URL, headers=headers, params=params)

            if response.status_code == 200:
                response_data = response.json()
                total_results = int(response_data["search-results"]["opensearch:totalResults"])
                if total_results > 0:
                    results = response_data["search-results"]["entry"]

                    with open(f"query_{i+1}.csv", "w", newline="") as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(fields)
                        for result in results:
                            row = [result.get(field) for field in fields]
                            writer.writerow(row)
                    print(f"Query {i+1} Completa. Numero de resultados encontrados: {total_results} 'query_{i+1}.csv'")
                else:
                    print(f"Sem resultados para a query {i+1}")
            else:
                print(f"Error for query {i+1}: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error for query {i}: {str(e)}")

def requisicao(key_api, queries):

    api_key = key_api
    fields = ['dc:creator', 'author-profiles:author-profile:author-profile-id', 'dc:title', 'prism:coverDate',
              'prism:publicationName', 'prism:volume', 'prism:issue', 'prism:artNo', 'prism:pageRange',
              'prism:pageCount', 'citedby-count', 'prism:doi', 'prism:url', 'subtypeDescription',
              'publication-stage', 'openaccessFlag', 'prism:sourceTitle', 'eid']

    run_scopus_queries(api_key, queries, fields)
