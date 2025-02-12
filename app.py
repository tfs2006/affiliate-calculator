from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class AffiliateCalculator:
    def __init__(self):
        self.metrics = {
            'conversion_data': {},
            'financial_data': {},
            'customer_data': {}
        }

    def _validate_input(self, value, name, min_val=0):
        try:
            value = float(value)
            if value < min_val:
                raise ValueError(f"{name} cannot be negative")
            return value
        except (TypeError, ValueError):
            raise ValueError(f"Invalid value for {name}")

    def add_conversion_data(self, clicks, conversions):
        self.metrics['conversion_data'] = {
            'clicks': self._validate_input(clicks, 'Clicks'),
            'conversions': self._validate_input(conversions, 'Conversions')
        }

    def add_financial_data(self, investment, revenue, expenses):
        self.metrics['financial_data'] = {
            'investment': self._validate_input(investment, 'Investment'),
            'revenue': self._validate_input(revenue, 'Revenue'),
            'expenses': self._validate_input(expenses, 'Expenses')
        }

    def add_customer_data(self, acquisition_cost, ltv):
        self.metrics['customer_data'] = {
            'acquisition_cost': self._validate_input(acquisition_cost, 'CAC'),
            'ltv': self._validate_input(ltv, 'LTV')
        }

    def calculate_kpis(self):
        results = {}
        cd = self.metrics['conversion_data']
        fd = self.metrics['financial_data']
        cad = self.metrics['customer_data']

        # Conversion Metrics
        if cd.get('clicks') and cd.get('conversions'):
            results['conversion_rate'] = (cd['conversions'] / cd['clicks']) * 100
            results['cost_per_conversion'] = fd.get('investment', 0) / cd['conversions'] if cd['conversions'] > 0 else 0

        # Financial Metrics
        if fd.get('revenue') and fd.get('expenses'):
            net_profit = fd['revenue'] - fd['expenses']
            results['roi'] = ((net_profit - fd['investment']) / fd['investment']) * 100 if fd['investment'] != 0 else 0
            results['profit_margin'] = (net_profit / fd['revenue']) * 100 if fd['revenue'] != 0 else 0

        # Customer Metrics
        if cad.get('acquisition_cost') and cad.get('ltv'):
            results['ltv_cac_ratio'] = cad['ltv'] / cad['acquisition_cost'] if cad['acquisition_cost'] != 0 else 0

        return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        calc = AffiliateCalculator()
        
        calc.add_conversion_data(
            clicks=data.get('clicks', 0),
            conversions=data.get('conversions', 0)
        )
        
        calc.add_financial_data(
            investment=data.get('investment', 0),
            revenue=data.get('revenue', 0),
            expenses=data.get('expenses', 0)
        )
        
        calc.add_customer_data(
            acquisition_cost=data.get('acquisition_cost', 0),
            ltv=data.get('ltv', 0)
        )

        results = calc.calculate_kpis()
        return jsonify({
            "status": "success",
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)