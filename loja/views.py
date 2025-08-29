from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produto
from .cart import CarrinhoManager

# Create your views here.
def loja(request):
    lista_produtos = Produto.objects.all().order_by('data_adicionado')

    contexto = {
        'titulo': 'Lojinha',
        'usuario': 'Usuário',
        'produtos': lista_produtos
    }
    return render(request, 'loja.html', contexto)

def carrinho(request):
    # Inicializa o gerenciador de carrinho
    cart = CarrinhoManager(request)
    
    contexto = {
        'titulo': 'Carrinho de Compras',
        'itens': cart.get_itens(),
        'total': cart.get_total(),
        'quantidade_total': cart.get_quantidade_total()
    }
    return render(request, 'carrinho.html', contexto)

def adicionar_ao_carrinho(request, produto_id):
    # Inicializa o gerenciador de carrinho
    cart = CarrinhoManager(request)
    
    quantidade = 1
    if request.method == 'POST':
        if 'quantidade' in request.POST:
            try:
                quantidade = int(request.POST['quantidade'])
            except ValueError:
                quantidade = 1
    
    # Adiciona o produto ao carrinho
    cart.adicionar(produto_id, quantidade)
    messages.success(request, "Produto adicionado ao carrinho!")
    
    # Redireciona para a página anterior ou para a loja
    next_url = request.POST.get('next', '/')
    return redirect(next_url)

def remover_do_carrinho(request, produto_id):
    # Inicializa o gerenciador de carrinho
    cart = CarrinhoManager(request)
    
    # Remove o produto do carrinho
    cart.remover(produto_id)
    messages.success(request, "Produto removido do carrinho!")
    
    return redirect('carrinho')

def atualizar_quantidade(request, produto_id):
    # Inicializa o gerenciador de carrinho
    cart = CarrinhoManager(request)
    
    quantidade = 1
    if request.method == 'POST':
        if 'quantidade' in request.POST:
            try:
                quantidade = int(request.POST['quantidade'])
            except ValueError:
                quantidade = 1
    
    # Atualiza a quantidade do produto no carrinho
    cart.atualizar_quantidade(produto_id, quantidade)
    
    return redirect('carrinho')

def limpar_carrinho(request):
    # Inicializa o gerenciador de carrinho
    cart = CarrinhoManager(request)
    
    # Limpa o carrinho
    cart.limpar()
    messages.success(request, "Carrinho esvaziado!")
    
    return redirect('carrinho')

def finalizar_compra(request):
    # Inicializa o gerenciador de carrinho
    cart = CarrinhoManager(request)
    
    # Em um sistema real, aqui seria feito o processamento do pagamento,
    # salvamento dos dados do pedido, etc.
    
    # Verifica se há itens no carrinho
    if cart.get_quantidade_total() > 0:
        # Obter detalhes da compra para exibir no recibo
        itens = cart.get_itens()
        total = cart.get_total()
        
        # Limpa o carrinho após a compra
        cart.limpar()
        
        messages.success(request, "Compra realizada com sucesso! Obrigado por comprar conosco.")
        
        # Contexto para a página de confirmação
        contexto = {
            'titulo': 'Compra Finalizada',
            'itens': itens,
            'total': total,
            'compra_realizada': True
        }
        return render(request, 'compra_finalizada.html', contexto)
    else:
        messages.error(request, "Seu carrinho está vazio. Adicione produtos antes de finalizar a compra.")
        return redirect('carrinho')
