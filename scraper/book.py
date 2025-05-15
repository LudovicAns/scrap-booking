class Book:

    def __init__(self, title: str, price: float, price_type: str, availability: bool, rating: int):
        self.title = title
        self.price = price
        self.price_type = price_type
        self.availability = availability
        self.rating = rating

    def __str__(self):
        return f"{self.title} - {self.price} {self.price_type} - {"En stock" if self.availability else "Épuisé"} - {self.rating}/5"

    def to_dict(self):
        """
        Converts the attributes of an object to a dictionary representation.

        This method gathers specific attributes of the class instance and returns
        them in a structured dictionary format. This output can be used for
        data serialization, logging, or further processing.

        :return: A dictionary containing the attribute names as keys and their values
            corresponding to the object's current state.
        :rtype: Dict
        """
        return {
            'title': self.title,
            'price': self.price,
            'price_type': self.price_type,
            'availability': self.availability,
            'rating': self.rating
        }