from django.db import models

# Create your models here.


class CsvFile(models.Model):
    csv_file = models.FileField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return self.csv_file.name
    


class CandleData(models.Model):
    open = models.DecimalField(max_digits=10,decimal_places=5, null=True, blank=True)
    close = models.DecimalField(max_digits=10,decimal_places=5, null=True, blank=True)
    high = models.DecimalField(max_digits=10,decimal_places=5, null=True, blank=True)
    low = models.DecimalField(max_digits=10,decimal_places=5, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.open} | {self.close} | {self.low} | {self.high}'
    
class Candle:
    def __init__(self, id, _open, high, low, close, date):
        self.id = id
        self._open = _open
        self.high = high
        self.low = low
        self.close = close
        self.date = date