from django.db import models


class FAQ(models.Model):
    title = models.CharField('başlık', max_length=30)
    content = models.TextField(verbose_name='içerik')

    class Meta:
        verbose_name = 'sıkça sorulan soru'
        verbose_name_plural = 'sıkça sorulan sorular'


class Media(models.Model):
    title = models.CharField(verbose_name='medya adı',max_length=255)
    link = models.TextField(verbose_name='medya linki')
    icon_class = models.CharField(verbose_name='font-awesome class',max_length=255)

    class Meta:
        verbose_name = 'medya hesabı'
        verbose_name_plural = 'medya hesapları'