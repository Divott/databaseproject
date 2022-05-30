from django.db import models


# python manage.py makemigrations,生成数据库迁移文件
# python manage.py migrate,应用数据库迁移

# Create your models here.
class Center(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    profit = models.IntegerField(default=0)

    def update(self, profit):
        self.profit = profit
        self.save()

    def __str__(self):
        return self.name


class Enterprise(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True)
    supply_center = models.ForeignKey('Center', on_delete=models.CASCADE)
    industry = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Models(models.Model):
    number = models.CharField(max_length=10)
    model = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    unit_price = models.IntegerField()
    sales_volume = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(unit_price__gte=0), name='unit_price_gte_0')
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Models, self).save(*args, **kwargs)
        center = Center.objects.all()
        mc = Model_center.objects.filter(model=self)
        if not mc.exists():
            for cen in center:
                Model_center(model=self, center=cen).save()


class Staff(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    number = models.CharField(max_length=10, primary_key=True)
    supply_center = models.ForeignKey('Center', on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=0), name='age_gte_0')
        ]

    def __str__(self):
        return self.name


class Model_center(models.Model):
    model = models.ForeignKey(to=Models, on_delete=models.CASCADE)
    center = models.ForeignKey(to=Center, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'center'], name='unique_mc'),
            models.CheckConstraint(check=models.Q(quantity__gte=0), name='quantity_gte_0_model_center')
        ]

    def update(self, quantity):
        self.quantity = quantity
        self.save()

    def __str__(self):
        return self.center.name + "'s " + self.model.name


class Contract(models.Model):
    contract_num = models.CharField(max_length=15, primary_key=True)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE)
    contract_manager = models.ForeignKey('Staff', on_delete=models.CASCADE)
    contract_date = models.DateField()
    contract_type = models.CharField(max_length=10)

    def __str__(self):
        return self.contract_num


class Order(models.Model):
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)
    product_model = models.ForeignKey('Models', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    estimate_delivery_date = models.DateField()
    lodgement_delivery_date = models.DateField()
    salesman_num = models.ForeignKey('Staff', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=0), name='quantity_gte_0_order')
        ]
        ordering = ['salesman_num__number', 'estimate_delivery_date', 'product_model__model']

    def __str__(self):
        return self.salesman_num.name + "'s orders"
