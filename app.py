# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Base de datos simulada para servicios
services_db = {
    "sonido": [
        {"id": 1, "name": "DJ Profesional", "rating": 4.5, "price": "Desde $2000",
         "description": "Servicio de DJ para todo tipo de eventos con equipo profesional incluido."},
        {"id": 2, "name": "Renta de Equipo de Sonido", "rating": 4.8, "price": "Desde $1500",
         "description": "Alquiler de equipos de sonido para eventos, incluye instalación."}
    ],
    "bebidas": [
        {"id": 3, "name": "Barman Profesional", "rating": 4.6, "price": "Desde $1800",
         "description": "Servicio de barman con preparación de cócteles personalizados."},
        {"id": 4, "name": "Paquete de Bebidas Premium", "rating": 4.9, "price": "Desde $3000",
         "description": "Variedad de bebidas alcohólicas y no alcohólicas para tu evento."}
    ],
    "magia": [
        {"id": 5, "name": "Mago para Eventos", "rating": 4.7, "price": "Desde $1700",
         "description": "Espectáculo de magia e ilusionismo para sorprender a tus invitados."},
        {"id": 6, "name": "Show de Mentalismo", "rating": 4.5, "price": "Desde $2200",
         "description": "Presentación de mentalismo y trucos psicológicos."}
    ],
    "comida": [
        {"id": 7, "name": "Catering Gourmet", "rating": 4.8, "price": "Desde $250/persona",
         "description": "Servicio de catering con menú personalizado y chef profesional."},
        {"id": 8, "name": "Taquiza para Eventos", "rating": 4.9, "price": "Desde $150/persona",
         "description": "Auténtica taquiza mexicana con variedad de guisos y complementos."}
    ],
    "fotografias": [
        {"id": 9, "name": "Fotógrafo Profesional", "rating": 4.7, "price": "Desde $3500",
         "description": "Servicio completo de fotografía para eventos con edición incluida."},
        {"id": 10, "name": "Cabina de Fotos", "rating": 4.6, "price": "Desde $2800",
         "description": "Cabina fotográfica divertida con props y recuerdos impresos."}
    ],
    "decoracion": [
        {"id": 11, "name": "Decoración Temática", "rating": 4.8, "price": "Desde $5000",
         "description": "Decoración completa para eventos con tema personalizado."},
        {"id": 12, "name": "Arreglos Florales", "rating": 4.7, "price": "Desde $1500",
         "description": "Diseño y montaje de arreglos florales para eventos."}
    ],
    "postres": [
        {"id": 13, "name": "Mesa de Postres", "rating": 4.9, "price": "Desde $180/persona",
         "description": "Variedad de postres gourmet para complementar tu evento."},
        {"id": 14, "name": "Pastel Personalizado", "rating": 4.8, "price": "Desde $800",
         "description": "Pasteles artesanales con diseño y sabor personalizado."}
    ],
    "infantil": [
        {"id": 15, "name": "Animador Infantil", "rating": 4.7, "price": "Desde $1600",
         "description": "Servicios de animación con juegos, música y actividades para niños."},
        {"id": 16, "name": "Inflables y Juegos", "rating": 4.6, "price": "Desde $2000",
         "description": "Renta de inflables, juegos y actividades recreativas para niños."}
    ]
}

# Carrito de compras simulado
cart = []


@app.route('/')
def home():
    # Lista de categorías para los botones
    categories = [
        {"id": "sonido", "name": "Sonido", "icon": "music", "color": "#4A90E2"},
        {"id": "bebidas", "name": "Bebidas", "icon": "glass-cheers", "color": "#50E3C2"},
        {"id": "magia", "name": "Magia", "icon": "hat-wizard", "color": "#9013FE"},
        {"id": "comida", "name": "Comida", "icon": "utensils", "color": "#F5A623"},
        {"id": "fotografias", "name": "Fotografías", "icon": "camera", "color": "#D0021B"},
        {"id": "decoracion", "name": "Decoración", "icon": "paint-brush", "color": "#7ED321"},
        {"id": "postres", "name": "Postres", "icon": "ice-cream", "color": "#E91E63"},
        {"id": "infantil", "name": "Infantil", "icon": "child", "color": "#00BCD4"}
    ]
    return render_template('index.html', categories=categories, cart_count=len(cart))


@app.route('/<category>')
def category(category):
    if category in services_db:
        return render_template('category.html', category=category, services=services_db[category], cart_count=len(cart))
    return redirect(url_for('home'))


@app.route('/service/<int:service_id>')
def service_detail(service_id):
    # Buscar el servicio en la base de datos
    found_service = None
    category_name = ""

    for category, services in services_db.items():
        for service in services:
            if service["id"] == service_id:
                found_service = service
                category_name = category
                break
        if found_service:
            break

    if found_service:
        return render_template('service_detail.html', service=found_service, category=category_name,
                               cart_count=len(cart))
    return redirect(url_for('home'))


@app.route('/add_to_cart/<int:service_id>', methods=['POST'])
def add_to_cart(service_id):
    # Buscar el servicio y agregarlo al carrito
    for category, services in services_db.items():
        for service in services:
            if service["id"] == service_id:
                cart.append(service)
                return jsonify({"success": True, "cart_count": len(cart)})

    return jsonify({"success": False, "message": "Servicio no encontrado"})


@app.route('/cart')
def view_cart():
    total = sum(float(item["price"].replace("Desde $", "").replace("/persona", "")) for item in cart)
    return render_template('cart.html', cart_items=cart, total=total, cart_count=len(cart))


@app.route('/checkout', methods=['POST'])
def checkout():
    # Simular proceso de pago
    cart.clear()
    return render_template('success.html', cart_count=0)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []

    if query:
        for category, services in services_db.items():
            for service in services:
                if query.lower() in service["name"].lower() or query.lower() in service.get("description", "").lower():
                    service_copy = service.copy()
                    service_copy["category"] = category
                    results.append(service_copy)

    return render_template('search_results.html', results=results, query=query, cart_count=len(cart))


if __name__ == '__main__':
    app.run(debug=True)