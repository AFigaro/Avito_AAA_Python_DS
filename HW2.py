import json
import keyword


lesson_str = """{
        "title": "iPhone X",
        "price": 100,
        "class": "smartphone",
        "location": {
        "address": "город Самара, улица Мориса Тореза, 50",
        "metro_stations": ["Спортивная", "Гагаринская"]
        }
        }
        """


class Advert:

    def __init__(self, adv):

        """
        Пока не получилось написать корректное чтение(
        """

        for key, value in adv.items():
            if not keyword.iskeyword(key):
                setattr(self, key, value)
            else:
                setattr(self, key + '_', value)

        if hasattr(self, 'location'):
            for key, value in self.location.items():
                if not keyword.iskeyword(key):
                    setattr(self, 'location.' + key, value)
                else:
                    setattr(self, 'location.' + key + '_', value)
    
        if hasattr(self, 'price'):
            if self.price < 0:
                raise ValueError("price must be >= 0")
        else:
            self.price = 0

    def __repr__(self, repr_color_code=32):
        return f"\033[1;{repr_color_code};40m' {self.title} | {self.price}"


if __name__ == '__main__':
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad)
