# Dans ton template principal, ajoute ce filtre pour events_by_day|get_item:day
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])
