from flask import Blueprint

from griphook.server.billing import views

billing_blueprint = Blueprint('billing', __name__, )

billing_blueprint.add_url_rule('/billing-table', 'billing-table-api',
                               view_func=views.get_billing_table_data,
                               methods=("POST",))
