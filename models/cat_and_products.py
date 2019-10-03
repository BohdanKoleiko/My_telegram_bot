from mongoengine import *
from models.user_model import User

connect('bot_shop', host='192.168.0.9', port=27017)

#Записывает в базу названия подкатегорий
class Category(Document):
    title = StringField(max_length=4096)
    sub_categories = ListField(ReferenceField('self'))

    @property
    def is_parent(self):
        if self.sub_categories:
            return True

class Text(Document):
    title = StringField()
    text = StringField(max_length=4096)

    @classmethod
    def get_text(cls, title):
        return cls.objects.filter(title=title).first().text

class Product(Document):
    title = StringField(max_length=64)
    image = FileField(required=True)
    description = StringField(max_length=4096)
    price = IntField(min_value=0)
    quantity = IntField(min_value=0)
    is_available = BooleanField()
    is_discount = BooleanField(default=False)
    category = ReferenceField(Category)
    weight =FloatField(min_value=0, null=True)

    def __str__(self):
        return f'name - {self.title}, category - {self.category},' \
               f'price - {self.price/100}'

class Cart(Document):
    user = ReferenceField(User)
    products = ListField(ReferenceField(Product))
    is_archived = BooleanField(default=False)

    def get_sum(self):
        cart_sum = 0
        for p in self.products:
            cart_sum += p
        return cart_sum/100

    @classmethod
    def create_or_append_to_cart(cls, product_id, user_id):
        user = User.objects.get(user_id=user_id)
        user_cart = cls.objects.filter(user=user).first()
        product = Product.objects.get(id=product_id)

        if user_cart and not user_cart.is_archived:
            user_cart.products.append(product)
            user_cart.save()
        else:
            cls(user=user, products=[product]).save()

    def clean_cart(self):
        self.products=[]
        self.save()

class OrdersHistory(Document):
    user = ReferenceField(User)
    orders = ListField(ReferenceField(Cart))

    @classmethod
    def get_or_create(cls, user):
        history = cls.objects.filter(user=user).first()
        if history:
            return history
        else:
            return cls(user)


# if __name__ == '__main__':
# #     text = dict(title="Greetings",
# #                 text='I`m bot Alex')
# #     Text(**text).save()