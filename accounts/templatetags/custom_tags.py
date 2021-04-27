from django import template

register = template.Library()

def get_lst_lgn(obj):
    return obj.last_login.strftime("%H:%M:%S %D")

register.filter('get_lst_lgn', get_lst_lgn)