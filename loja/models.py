from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data_adicionado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome
    

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_adicionado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    sessao_id = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Carrinho {self.id}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())
    
    @property
    def quantidade_total(self):
        return sum(item.quantidade for item in self.itens.all())


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    adicionado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
    
    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade