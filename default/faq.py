from apps.we.models import FAQ

FAQs = (
    {
        'title': 'Avukat Ne Demek?',
        'content': 'Avukat, mahkeme sürecinde gerçek ya da tüzel kişilerin haklarını yargı önünde savunan, hukuki ve yasa işlerinde yol gösterici olan kişilere denilmektedir. Latince kökenli olan avukat kelimesi, mahkemeye tanık olarak çağrılan kimse, savunucu anlamlarına gelir. Avukatlık mesleği; hukuk fakültelerinde öğrenim görmüş, avukatlık stajını başarıyla bitirmiş ve yasaların gerektirdiği nitelikleri taşıyan kişiler tarafından yapılır.',
    },
    {
        'title': 'Avukat Ne İş Yapar? Görev ve Sorumlulukları Nelerdir?',
        'content': 'Avukatlık mesleği, 1136 nolu kanunda, ‘kamu hizmeti ve serbest meslek’ olarak tanımlanmıştır. Avukatlar Mahkeme sürecinde gerçek veya tüzel kişilerin haklarını dava etmek veya savunmak, Hukuki destek verdiği kişi/kurumun menfaatlerini koruyucu, anlaşmazlıkları önleyici hukuki tedbirleri alıp, anlaşma ve sözleşmeleri bu doğrultuda hazırlamak, Sözleşme ve şartname taslakları, kurum ile üçüncü kişiler arasındaki uyuşmazlıklarla ilgili hukuki mütalaa bildirmek, Davaları takip edip (karar tashihi, itiraz, temyiz vb.) sonuçlandırmak, Hukuki ve yasal konularda yorum yapmak gibi görevleri üstlenmektedir.'
    },
    {
        'title': 'Avukat Olma Şartları Nelerdir?',
        'content': 'Türkiye’de avukatlık yapabilmek için Türkiye Cumhuriyeti (TC) vatandaşı olmak, hukuk fakültesi mezunu olmak, avukatlık stajını tamamlamış olmak ve staj bitim belgesini almış olmak gerekir.'
    },
    {
        'title': 'Kimler Avukatlık Yapamaz?',
        'content': 'Kasten işlenen bir suç nedeniyle 2 yıldan fazla hapis cezası almış olmak, Devletin güvenliğine karşı suç işlemiş olmak ve Anayasal düzene ve bu düzenin işleyişine karşı suç işlemiş olmak (İrtikap, zimmet, hırsızlık, rüşvet,sahtecilik, dolandırıcılık, hileli iflas, ihaleye fesat karıştırma, güveni kötüye kullanma, suçtankaynaklanan malvarlığı değerlerini aklama veya kaçakçılık, edimin ifasına fesat karıştırma gibisuçlarından mahkûm olmak.'
    },
    {
        'title': 'Avukatlık Stajı Nasıl Yapılır?',
        'content': 'Avukatlık stajı 1 yıllık bir süreyi kapsar. Hukuk fakültesini bitirdikten sonra avukatlık stajının ilk 6 ayı mahkemelerde, diğer 6 ayı da baro levhasına kayıtlı, meslekte en az 5 yıl kıdemli bir avukat yanında yapılır.'
    },
    {
        'title': 'Avukatta Olması Gereken Özellikler Nelerdir?',
        'content': 'Avukat Sistematik düşünme yeteneğine sahip olmalı, Analiz gücü yüksek olmalı, Problemleri hızlı bir şekilde kavrayıp, çözümünde başrol oynayabilmeli ve Üstlendiği konuları etkili konuşma kabiliyetiyle savunabilmelidir.'
    },
    {
        'title': 'Avukatta Olması Gereken Özellikler Nelerdir?',
        'content': 'Avukat Sistematik düşünme yeteneğine sahip olmalı, Analiz gücü yüksek olmalı, Problemleri hızlı bir şekilde kavrayıp, çözümünde başrol oynayabilmeli, Üstlendiği konuları etkili konuşma kabiliyetiyle savunabilmelidir.'
    },
    {
        'title': 'Avukat Branşları & Çeşitleri Nelerdir?',
        'content': 'Avukatlar, hukuk önünde birey-kurumsal şirketleri argümanlarını toplayıp savunan, davalarını takip edip olumlu sonuçlar almayı sağlayan kişilerdir. Avukat olmak için uzun ve zorlu geçen bir eğitim sürecini başarıyla bitirmek gerekiyor. Lise sonrası milyonlarca öğrenci arasından sıyrılarak hukuk fakültesini kazanmalı, burayı bitirdikten sonra baro stajı ve tecrübeli avukat yanında 1 yıllık stajı da başarıyla bitirmek gerekiyor. Hukukun da çok sayıda alt dalı bulunuyor. Ticaret Hukuku, İş Hukuku, İdare Hukuku, Gayrimenkul Hukuku, Miras Hukuku, Aile Hukuku, İcra ve İflas Hukuku, Vergi Hukuku, Sözleşmeler ve Borçlar Hukuku, Tüketici Hukuku, Bilişim Hukuku, Ceza Hukuku, Kooperatifler Hukuku, Gayrimenkul ve Portföy Hukuku, Gayrimenkul Yönetim Danışmanlığı, Gayrimenkul Yönetim Hukuku gibi onlarca hukuk çeşidi bulunuyor. Dolayısıyla bu hukuk dallarına yönelik avukatların branşlaşma çalışmaları oluyor.'
    }
)

def create():
    objects = list()
    for faq in FAQs:
        object = FAQ(
            title = faq['title'],
            content = faq['content']
        )
        object.save()
        objects.append(object)
    return objects