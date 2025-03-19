from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Бренд")

    def __str__(self):
        return self.name

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100, verbose_name="Модель автомобиля")

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Телефон")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Car(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="cars")
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="cars")
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    vin = models.CharField(max_length=17, unique=True, verbose_name="VIN номер")

    def __str__(self):
        return f"{self.model} ({self.year}) - {self.vin}"

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Поставщик")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        return self.name

class Part(models.Model):
    name = models.CharField(max_length=100, verbose_name="Деталь")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="parts")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.name

class Inventory(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    location = models.CharField(max_length=100, verbose_name="Место на складе")

    def __str__(self):
        return f"{self.part.name} - {self.quantity} шт."

class RepairOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="repair_orders")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="repair_orders")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=50, choices=[("open", "Открыт"), ("closed", "Закрыт")], default="open")
    workers = models.ManyToManyField(User, related_name="repair_orders", verbose_name="Работники")

    def __str__(self):
        return f"Заказ {self.id} - {self.car}"

class RepairOrderPhoto(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="repair_photos/", verbose_name="Фото")
    before_repair = models.BooleanField(default=True, verbose_name="До ремонта")

    def __str__(self):
        return f"Фото {self.id} для заказа {self.repair_order.id}"

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Услуга")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        return self.name

class RepairOrderService(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.service.name} ({self.quantity})"

class RepairOrderPart(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="parts")
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.part.name} ({self.quantity})"

class Invoice(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="invoices")
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выставления")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")

    def __str__(self):
        return f"Инвойс {self.id} - {self.total_amount} руб."

# Регистрация моделей в админке
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "brand")
    search_fields = ("name", "brand__name")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone")
    search_fields = ("first_name", "last_name", "phone")

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "vin", "client")
    search_fields = ("vin", "client__first_name", "client__last_name", "model__name")

@admin.register(RepairOrderPhoto)
class RepairOrderPhotoAdmin(admin.ModelAdmin):
    list_display = ("repair_order", "before_repair")

@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ("client", "car", "status", "created_at")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("repair_order", "issued_at", "total_amount")
