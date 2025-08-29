from .models import Carrinho, ItemCarrinho, Produto
from django.shortcuts import get_object_or_404

class CarrinhoManager:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        # Obter o ID do carrinho na sessão
        carrinho_id = self.session.get('carrinho_id')
        
        # Tenta obter o carrinho existente ou cria um novo
        if carrinho_id:
            try:
                self.carrinho = Carrinho.objects.get(id=carrinho_id)
            except Carrinho.DoesNotExist:
                self.carrinho = self._criar_carrinho()
        else:
            self.carrinho = self._criar_carrinho()
        
        # Salvar o ID do carrinho na sessão
        self.session['carrinho_id'] = self.carrinho.id
        self.session.save()
    
    def _criar_carrinho(self):
        # Cria um novo carrinho
        if self.request.user.is_authenticated:
            # Se o usuário estiver logado, associa o carrinho a ele
            carrinho = Carrinho.objects.create(usuario=self.request.user)
        else:
            # Se não, cria um carrinho anônimo com o ID da sessão
            carrinho = Carrinho.objects.create(sessao_id=self.session.session_key)
        return carrinho
    
    def adicionar(self, produto_id, quantidade=1):
        """Adiciona um produto ao carrinho ou atualiza sua quantidade"""
        produto = get_object_or_404(Produto, id=produto_id)
        
        # Verifica se o produto já está no carrinho
        try:
            item = self.carrinho.itens.get(produto=produto)
            item.quantidade += quantidade
            item.save()
        except ItemCarrinho.DoesNotExist:
            # Se não existe, cria um novo item
            ItemCarrinho.objects.create(
                carrinho=self.carrinho,
                produto=produto,
                quantidade=quantidade
            )
    
    def remover(self, produto_id):
        """Remove um produto do carrinho"""
        try:
            item = self.carrinho.itens.get(produto_id=produto_id)
            item.delete()
        except ItemCarrinho.DoesNotExist:
            pass
    
    def atualizar_quantidade(self, produto_id, quantidade):
        """Atualiza a quantidade de um produto no carrinho"""
        if quantidade <= 0:
            return self.remover(produto_id)
        
        try:
            item = self.carrinho.itens.get(produto_id=produto_id)
            item.quantidade = quantidade
            item.save()
        except ItemCarrinho.DoesNotExist:
            pass
    
    def limpar(self):
        """Remove todos os itens do carrinho"""
        self.carrinho.itens.all().delete()
    
    def get_total(self):
        """Retorna o valor total do carrinho"""
        return self.carrinho.total
    
    def get_itens(self):
        """Retorna todos os itens do carrinho"""
        return self.carrinho.itens.all()
    
    def get_quantidade_total(self):
        """Retorna a quantidade total de itens no carrinho"""
        return self.carrinho.quantidade_total
