from apps.users.models import Area

TAGS = (
    'boşanma',
    'ceza',
    'borç-alacak',
    'tazminat',
    'miras',
    'işçi-işveren',
    'sigorta',
    'bilişim',
    'şirket ve ticaret',
    'arabulucu',
    'uzlaştırıcı',
    'doktor ve hekim',
    'emlak ve emlakçı',
    'icra takip',
    'kamu-idari',
    'iflas',
    'patent marka',
    'trafik ve kaza',
    'uluslarası hukuk',
    'vergi',
    'temyiz',
    'tüketici',
    'istisnaf',
)

def create():
    tags = list()
    for area in TAGS:
        object = Area(
            name = area.title()
        )
        object.save()
        tags.append(object)
    return tags