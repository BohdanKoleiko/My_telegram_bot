import string, random
from models.cat_and_products import Category, Product, Text
from mongoengine import connect

random_bool = (True, False)

#Рандомно присваивает имена подкатегориям:
def name_for_cat(*args, str_len=3):
    names_list = ['Одежда', 'Обувь', 'Мебель']
    for n in range(str_len):
        random_list = names_list[int(*args)]
    return random_list

def name_for_product(item):
    if item == 'Одежда':
        Clothes = ['Куртка зимняя(men)', 'Чулки', 'Джинсы(women)']
        return Clothes[random.choice(range(3))]
    elif item == 'Обувь':
        Footwear = ['Ботинки(men)', 'Туфли', 'Красовки(women)', 'Слипоны']
        return Footwear[random.choice(range(4))]
    else:
        Furniture = ['Стулья', 'Письменный стол', 'Диван']
        return Furniture[random.choice(range(3))]


#Работет с классом Category и присваивает имена:
def seed_and_get(num):
    category_list = []
    for i in range(num):
        cat = Category(title=name_for_cat(i)).save()
        category_list.append(cat)
    return category_list


#Записывает значения в класс Product:
def seed_products(num, list_of_cats):
    for i in range(num):
        product = dict(
            title=name_for_product(name_for_cat()),
            description='test',
            price=random.randint(1000, 100 * 1000),
            quantity=random.randint(0, 100),
            is_available=random.choice(random_bool),
            is_discount=random.choice(random_bool),
            category=random.choice(list_of_cats),
            weight=random.uniform(0, 100)
        )
        Product(**product).save()

def seed_products_with_image():
    products = Product.objects.all()

    for i in products:
        with open(r'D:\ITEA\Lesson_14_2019_09_10\bot\images\test.png', 'rb') as image:
            i.image.put(image)
            i.save()

if __name__ == '__main__':
    con = connect('bot_shop', host='<host name or IP', port=<port ID>)
    cats = seed_and_get(3)
    seed_products(10, cats)
    Text(title="Greeting", text='Я бот интернет магазина '
                                '"Все про все и еще немного"').save()
