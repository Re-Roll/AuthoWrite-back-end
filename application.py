from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields, abort
from config import DevConfig
from compare_texts import compare_mix_texts
from docu_functions import simplify_response

# Create the Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(DevConfig)
api = Api(app,doc='/docs')  # Setup API documentation

# Create the API models
compare_model = api.parser()
compare_model.add_argument('known_texts', type=str, action='append', required=False, help='List of known texts to compare against')
compare_model.add_argument('unknown_text', type=str, required=False, help='Unknown text to compare against')
compare_model.add_argument('known_files', type='file', action='append', required=False, help='List of known files to compare against')
compare_model.add_argument('unknown_file', type='file', required=False, help='Unknown file to compare against')

score_model = api.model('Score', {
    'w_sim': fields.List(fields.Float(required=True, description='Word similarity between known and unknown texts')),
    'punct_p': fields.List(fields.Float(required=True), description='Proportion of punctuation used'),
    'avg_sent_l': fields.List(fields.Float(required=True), description='Average sentence length'),
    'rare_word_p': fields.List(fields.Float(required=True), description='Proportion of rare words used'),
    'long_word_p': fields.List(fields.Float(required=True), description='Proportion of long words used'),
    'ttr': fields.List(fields.Float(required=True), description='Proportion of unique words used compared to total words used'),
    'word_count': fields.List(fields.Float(required=True), description='Total number of words used'),
    'score': fields.Integer(required=True, description='Overall authorship score out of 100')
})  

@api.route('/compare', methods=['POST'])
class Compare(Resource):
    @api.expect(compare_model)
    @api.marshal_with(score_model)
    def post(self):
        '''Compares a list of known texts to an unknown text and returns a score'''
        
        # Get the request data
        known_files = request.files.getlist('known_files')
        known_texts = request.form.getlist('known_texts')
        unknown_file = request.files.get('unknown_file')
        unknown_text = request.form.get('unknown_text')
        
        # Calculate the score
        score, response = compare_mix_texts(known_files, known_texts, unknown_file, unknown_text)

        # Check for errors
        if score == 2:
            abort(400, 'No known texts provided')
        elif score == 3:
            abort(401, 'No unknown text provided')
        
        # finalise response
        response = simplify_response(response)
        try:
            response['score'] = int(round(score*100))
        except:
            abort(500, 'Error calculating score')
        
        return response, 200
    
@api.route('/test_again')
class TestAgain(Resource):
    def get(self):
        '''Test the API'''
        return 'Hello World', 200
    
@api.route('/test')
class TestAgain(Resource):
    def get(self):
        '''Test the API'''
        return 'Hello World', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')