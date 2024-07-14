from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        # Print statements for debugging
        print("Request form data:", request.form)
        print("Request args data:", request.args)

        # Check if the data is in the form (POST) or args (GET)
        total_sqft = float(request.form.get('total_sqft') or request.args.get('total_sqft'))
        location = request.form.get('location') or request.args.get('location')
        bhk = int(request.form.get('bhk') or request.args.get('bhk'))
        bath = int(request.form.get('bath') or request.args.get('bath'))

        # Ensure all parameters are present
        if not all([total_sqft, location, bhk, bath]):
            raise KeyError("All parameters are required")

        response = jsonify({
            'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter type: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)
