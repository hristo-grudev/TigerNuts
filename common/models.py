from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from phone_field import PhoneField

CATEGORY_CHOICES = (
    ('R', 'RAW'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

COUNTRY_CHOICES = (
    ('BG', 'България'),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField()
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'images'

    def __str__(self):
        return str(self.title)

    def first_image(self):
        image = ItemImages.objects.filter(title=self.pk).first()
        return image

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

    def add_to_favorites_url(self):
        return reverse("add-to-favorites", kwargs={
            'slug': self.slug
        })


class ItemImages(models.Model):
    title = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.title)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        if self.item.discount_price:
            total = self.quantity * self.item.discount_price
        else:
            total = self.quantity * self.item.price

        return total

    def get_item_price(self):
        if self.item.discount_price:
            price = self.item.discount_price
        else:
            price = self.item.price

        return price

    def get_absolute_url(self):
        return reverse('view item', kwargs={'slug': self.slug})


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    town = models.CharField(max_length=100, default='')
    street_address = models.CharField(max_length=100, default='')
    apartment_address = models.CharField(max_length=100, default='', null=True, blank=True)
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=100, default='')
    zip = models.CharField(max_length=100, default='')
    phone = PhoneField(default='')
    email = models.EmailField(max_length=254, default='')
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return str(self.code)


class WishList(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.item)

    def add_to_favorites_url(self):
        return reverse("add-to-favorites", kwargs={
            'slug': self.slug
        })
