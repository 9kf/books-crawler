import scrapy

class BooksCrawler(scrapy.Spider):
    name="books"
    
    start_urls = [
        'http://books.toscrape.com/'
    ]

    ratings = [
        {"key": "One", "value": 1},
        {"key": "Two", "value": 2},
        {"key": "Three", "value": 3},
        {"key": "Four", "value": 4},
        {"key": "Five", "value": 5},
    ]

    def parse(self, response):
        for product in response.css('.product_pod'):
            book_title = product.css('h3 a::attr(title)').get()
            book_price = product.css('div.product_price p.price_color::text').get()
            link_to_book = product.css('div.image_container a::attr(href)').get()
            stock = product.css('div.product_price p.instock').get().split('\n')[3].strip()
            stars = product.css('.star-rating').xpath('@class').get().replace('star-rating','').strip()
            star_number = next((item for item in self.ratings if item["key"] == stars), None)['value']

            yield {
                'title': book_title,
                'price': book_price,
                'link': response.urljoin(link_to_book),
                'hasStock': True if stock == "In stock" else False,
                'stars': star_number
            }

        next_page = response.css('li.next a::attr(href)').get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)