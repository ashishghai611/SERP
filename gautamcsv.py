from parsel import Selector
from urllib.parse import quote
import csv
import httpx
client = httpx.Client(
    headers={
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    },
)
def scrape_seo_ranks(keywords, domain, max_pages,search_engine):
    filecsv = open("seo_ranks.csv", "w", encoding="utf8")
    csv_columns = ["keyword", "domain", "url", "position"]
    writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
    writer.writeheader()
    for keyword in keywords:
        position = 0
        for page in range(1, max_pages + 1):
            print(f"Scraping keyword '{keyword}' at page number {page}")
            url = f"https://{search_engine}/search?hl=en&q={quote(keyword)}" + (
                f"&start={10 * (page - 1)}" if page > 1 else ""
            )
            request = client.get(url=url)
            selector = Selector(text=request.text)
            for result_box in selector.xpath(
                "//h1[contains(text(),'Search Results')]/following-sibling::div[1]/div"
            ):
                try:
                    title = result_box.xpath(".//h3/text()").get()
                    text = "".join(
                        result_box.xpath(".//div[@data-sncf]//text()").getall()
                    )
                    date = text.split("—")[0] if len(text.split("—")) > 1 else "None"
                    url = result_box.xpath(".//h3/../@href").get()
                    result_domain = url.split("/")[2].replace("www.", "")
                    position += 1
                    writer.writerow(
                        {
                            "keyword": keyword,
                            "domain": result_domain,
                            "url": url,
                            "position": position
                        }
                    )
                except:
                    pass
    filecsv.close()
if __name__ == "__main__":
    # Get user input for keywords, domain, and max_pages
    keywords_input = ["Health insurance",
"Auto insurance",
"Home insurance"]
   
    domain_input = "edifecs.com"
    max_pages_input = int(input("Enter maximum pages to scrape: "))
    search_engine="www.google.com"
    # Example use with user input
    scrape_seo_ranks(keywords_input, domain_input, max_pages_input,search_engine)