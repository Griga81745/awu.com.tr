from django.db import models

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

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

class SiteSettings(SingletonModel):
    support_email = models.EmailField(default='support@example.com')