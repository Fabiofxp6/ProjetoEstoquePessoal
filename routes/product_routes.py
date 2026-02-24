from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from bson.objectid import ObjectId
import re

# Cria o Blueprint para as rotas de produtos
product_bp = Blueprint('product', __name__)

@product_bp.route('/estoque')
def index():
    db = current_app.db
    search_query = request.args.get('search', '').strip()
    
    query = {}
    if search_query:
        safe_search = re.escape(search_query)
        query = {"$or": [
            {"modelo": {"$regex": safe_search, "$options": "i"}},
            {"marca": {"$regex": safe_search, "$options": "i"}}
        ]}
    
    produtos = list(db.produtos.find(query))
    
    # Dashboard Stats
    stats = {
        "total_itens": sum(p['quantidade'] for p in produtos),
        "baixo_estoque": len([p for p in produtos if 0 < p['quantidade'] <= 2]),
        "esgotados": len([p for p in produtos if p['quantidade'] == 0]),
        "valor_estoque": sum(p['preco_custo'] * p['quantidade'] for p in produtos)
    }
    
    return render_template('index.html', produtos=produtos, stats=stats, search_query=search_query)

@product_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    """Adiciona um novo produto ao estoque."""
    if request.method == 'POST':
        try:
            # Captura e validação básica dos dados do formulário
            quantidade = int(request.form['quantidade'])
            if quantidade < 0:
                flash('A quantidade não pode ser negativa.', 'danger')
                return redirect(url_for('product.add_product'))

            preco_custo = float(request.form['preco_custo'])
            preco_venda = float(request.form['preco_venda'])
            lucro = preco_venda - preco_custo # Regra de Negócio: Cálculo automático de lucro
            
            produto = {
                "modelo": request.form['modelo'].strip(),
                "cor": request.form['cor'].strip(),
                "tamanho": request.form['tamanho'].strip(),
                "descricao": request.form['descricao'].strip(),
                "quantidade": quantidade,
                "preco_custo": preco_custo,
                "preco_venda": preco_venda,
                "lucro": lucro,
                "marca": request.form.get('marca', '').strip(),
                "observacao": request.form.get('observacao', '').strip()
            }
            
            current_app.db.produtos.insert_one(produto)
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('product.index'))
            
        except ValueError:
            flash('Erro de validação: Verifique os números digitados.', 'danger')
            return redirect(url_for('product.add_product'))

    return render_template('form.html', acao="Adicionar", produto={})

@product_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_product(id):
    """Edita um produto existente."""
    db = current_app.db
    # Proteção básica contra IDs inválidos do MongoDB
    if not ObjectId.is_valid(id):
        flash('ID de produto inválido.', 'danger')
        return redirect(url_for('product.index'))
        
    produto = db.produtos.find_one({"_id": ObjectId(id)})
    
    if request.method == 'POST':
        try:
            quantidade = int(request.form['quantidade'])
            if quantidade < 0:
                flash('A quantidade não pode ser negativa.', 'danger')
                return redirect(request.url)

            preco_custo = float(request.form['preco_custo'])
            preco_venda = float(request.form['preco_venda'])
            lucro = preco_venda - preco_custo
            
            updated_data = {
                "modelo": request.form['modelo'].strip(),
                "cor": request.form['cor'].strip(),
                "tamanho": request.form['tamanho'].strip(),
                "descricao": request.form['descricao'].strip(),
                "quantidade": quantidade,
                "preco_custo": preco_custo,
                "preco_venda": preco_venda,
                "lucro": lucro,
                "marca": request.form.get('marca', '').strip(),
                "observacao": request.form.get('observacao', '').strip()
            }
            
            db.produtos.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('product.index'))
            
        except ValueError:
            flash('Erro de validação nos campos numéricos.', 'danger')
            
    return render_template('form.html', acao="Editar", produto=produto)

@product_bp.route('/delete/<id>', methods=['POST'])
def delete_product(id):
    """Exclui um produto."""
    if ObjectId.is_valid(id):
        current_app.db.produtos.delete_one({"_id": ObjectId(id)})
        flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('product.index'))