from flask import Blueprint

from griphook.server.billing import views

billing_blueprint = Blueprint('billing', __name__, )

billing_blueprint.add_url_rule('/get_table_data', 'get-billing-table-data',
                               view_func=views.get_filtered_billing_table_data,
                               methods=("POST",))
