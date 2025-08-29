from django.contrib import admin
from .models import Produto, Categoria, Carrinho, ItemCarrinho

admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
