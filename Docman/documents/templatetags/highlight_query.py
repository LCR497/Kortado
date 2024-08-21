from django import template

register = template.Library()

@register.filter
def highlight_query(text, query):
    # Приводим текст и запрос к нижнему регистру
    text_lower = text.lower()
    query_lower = query.lower()
    highlighted = text_lower.replace(query_lower, f'<mark style="background-color: #ffa500">{query}</mark>')
    return highlighted