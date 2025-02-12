from flask import Flask, request, jsonify
app = Flask(__name__)

class AffiliateCalculator:
    # [Previous calculator class code here]

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    calc = AffiliateCalculator()
    
    try:
        calc.add_conversion_data(data['clicks'], data['conversions'])
        calc.add_financial_data(data['investment'], data['revenue'], data['expenses'])
        calc.add_customer_data(data['acquisition_cost'], data['ltv'])
        
        return jsonify({
            'report': calc.generate_report(),
            'kpis': calc.calculate_kpis()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()