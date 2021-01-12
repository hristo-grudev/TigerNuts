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

	class Meta:
		verbose_name_plural = 'images'

	def __str__(self):
		return self.title

	def first_image(self):
		# code to determine which image to show. The First in this case.
		print(self.images)
		return self.images


class ItemImages(models.Model):
	title = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='images/')

	def __str__(self):
		return str(self.title)
