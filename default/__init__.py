from .tag import create as create_tags
from .faq import create as create_faq

def create():
    
    objects = (
        create_tags(),
        create_faq(),
    )

    return objects
