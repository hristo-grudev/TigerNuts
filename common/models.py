from django.db import models

CATEGORY_CHOICES = (
	('R', 'RAW'),
)


class Item(models.Model):
	title = models.CharField(max_length=100)
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	slug = models.SlugField()
	description = models.TextField()

	def __str__(self):
		return self.title


class ItemImages(models.Model):
	title = models.ForeignKey(Item, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/')

	def __str__(self):
		return str(self.title)
