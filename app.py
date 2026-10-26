#!/usr/bin/env python3
"""
Shoplytics Application Entry Point
Smart Retail Management, Inventory Tracking, Expense Analytics,
and LSTM-Based Sales Forecasting System.
"""

import os
from flask import Flask, render_template, jsonify
from config import config_by_name, Config
from database.connection import close_db, DatabaseManager

# Import Blueprints
from routes.dashboard import dashboard_bp
from routes.products import products_bp
from routes.inventory import inventory_bp
from routes.sales import sales_bp
from routes.expenses import expenses_bp
from routes.analytics import analytics_bp
from routes.imports import imports_bp
from routes.forecasting import forecasting_bp
from routes.uploads import uploads_bp
from routes.help import help_bp


def create_app(config_name="default"):
    """Application factory for Shoplytics."""
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, Config))

    # Register Database Connection Teardown
    app.teardown_appcontext(close_db)

    # Register Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(forecasting_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(imports_bp)
    app.register_blueprint(help_bp)

    # Register Jinja globals and filters
    app.jinja_env.globals.update(zip=zip)

    @app.template_filter("inr")
    def inr_format(value):
        try:
            return f"₹{float(value):,.2f}"
        except (ValueError, TypeError):
            return "₹0.00"

    @app.template_filter("date_fmt")
    def date_format(value):
        if not value:
            return ""
        return str(value)[:10]

    # Health Check API
    @app.route("/health")
    def health_check():
        db_status = DatabaseManager.check_status()
        return jsonify({
            "status": "healthy",
            "app": "Shoplytics Retail Management & Forecasting System",
            "database": db_status
        })

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html", error=str(e)), 500

    return app


app = create_app(os.getenv("FLASK_ENV", "default"))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n=======================================================")
    print(f" Starting Shoplytics Server on http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host="127.0.0.1", port=port, debug=True)
