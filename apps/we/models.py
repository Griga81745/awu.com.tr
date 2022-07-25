from django.db import models


class FAQ(models.Model):
    title = models.CharField('Başlık', max_length=30)
    content = models.TextField(verbose_name='İçerik')

    class Meta:
        verbose_name = 'Sıkça Sorulan Soru'
        verbose_name_plural = 'Sıkça Sorulan Sorular'


class Media(models.Model):
    title = models.CharField(verbose_name='Medya Adı',max_length=255)
    link = models.TextField(verbose_name='Medya Linki')
    icon_class = models.CharField(verbose_name='Font-Awesome Class',max_length=255)

    class Meta:
        verbose_name = 'Medya Hesabı'
        verbose_name_plural = 'Medya Hesapları'