from django.db import models

CATEGORY_CHOICES = (
    ('property', 'املاک'),
    ('vehicle', 'وسایل نقلیه'),
    ('electronics', 'وسایل الکترونیکی'),
    ('decoration', 'مربوط به خانه'),
    ('services', 'خدمات'),
    ('private', 'وسایل شخصی'),
    ('entertainment', 'سرگرمی و فراغت'),
    ('social', 'اجتماعی'),
    ('employ', 'استخدام و کاریابی'),
    ('business', 'برای کسب و کار'),
)


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Cluster(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
