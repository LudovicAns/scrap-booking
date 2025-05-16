class Webcam:

    def __init__(self, name: str, url: str, price: float, price_type: str, rating: float, rating_count: int, vendor: str):
        self.name = name
        self.url = url
        self.price = price
        self.price_type = price_type
        self.rating = rating
        self.rating_count = rating_count
        self.vendor = vendor

    def __str__(self):
        return f"{self.name} | {self.url} | {self.price} | {self.price_type} | {self.rating} | {self.rating_count} | {self.vendor}"

    def to_dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'price': self.price,
            'price_type': self.price_type,
            'rating': self.rating,
            'rating_count': self.rating_count,
            'vendor': self.vendor
        }