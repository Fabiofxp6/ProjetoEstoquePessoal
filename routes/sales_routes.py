from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from bson.objectid import ObjectId

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/')
def checkout():
    """Página principal de vendas."""
    db = current_app.db
    # Pegamos apenas produtos que possuem estoque
    produtos = list(db.produtos.find({"quantidade": {"$gt": 0}}))
    return render_template('vendas.html', produtos=produtos)

@sales_bp.route('/realizar_venda', methods=['POST'])
def process_sale():
    db = current_app.db
    # O formulário enviará listas de IDs e Quantidades
    product_ids = request.form.getlist('product_id[]')
    quantities = request.form.getlist('quantity[]')
    payment_method = request.form.get('payment_method')
    
    itens_venda = []
    total_venda = 0

    for p_id, qty in zip(product_ids, quantities):
        qty = int(qty)
        produto = db.produtos.find_one({"_id": ObjectId(p_id)})
        
        if produto and produto['quantidade'] >= qty:
            subtotal = produto['preco_venda'] * qty
            total_venda += subtotal
            
            # 1. Diminuir o estoque
            db.produtos.update_one(
                {"_id": ObjectId(p_id)},
                {"$inc": {"quantidade": -qty}}
            )
            
            itens_venda.append({
                "produto_id": p_id,
                "modelo": produto['modelo'],
                "quantidade": qty,
                "preco_unitario": produto['preco_venda'],
                "subtotal": subtotal
            })
        else:
            flash(f"Erro: Estoque insuficiente para {produto['modelo']}", "danger")
            return redirect(url_for('sales.checkout'))

    # 2. Registrar a venda no histórico
    venda_doc = {
        "data": datetime.now(),
        "itens": itens_venda,
        "total": total_venda,
        "pagamento": payment_method
    }
    db.vendas.insert_one(venda_doc)
    
    flash(f"Venda realizada com sucesso! Total: R$ {total_venda:.2f}", "success")
    return redirect(url_for('sales.checkout'))

@sales_bp.route('/relatorios')
def reports():
    db = current_app.db
    vendas = list(db.vendas.find().sort("data", -1)) # Vendas mais recentes primeiro
    
    total_faturado = sum(v['total'] for v in vendas)
    total_vendas_contagem = len(vendas)
    
    # Cálculo de Lucro Real (Venda - Custo de cada item)
    lucro_total = 0
    for v in vendas:
        for item in v['itens']:
            # Buscamos o produto para saber o custo (ou usamos o salvo na venda se preferir)
            p = db.produtos.find_one({"_id": ObjectId(item['produto_id'])})
            if p:
                custo_total_item = p['preco_custo'] * item['quantidade']
                lucro_total += (item['subtotal'] - custo_total_item)

    ticket_medio = total_faturado / total_vendas_contagem if total_vendas_contagem > 0 else 0

    metrics = {
        "faturamento": total_faturado,
        "lucro": lucro_total,
        "contagem": total_vendas_contagem,
        "ticket": ticket_medio
    }

    return render_template('relatorios.html', vendas=vendas, metrics=metrics)