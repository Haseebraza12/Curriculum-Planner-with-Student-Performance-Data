from flask import Flask, jsonify, send_from_directory
from rdflib import Graph
import os

app = Flask(__name__)

# Load the RDF data
g = Graph()
g.parse('student_performance.rdf', format='turtle')

@app.route('/students', methods=['GET'])
def get_students():
    query = """
    PREFIX cp: <http://www.mruniversity.edu/ontologies/curriculum-planner#>
    SELECT ?student ?id ?gpa
    WHERE {
        ?student a cp:Student .
        ?student cp:studentID ?id .
        ?student cp:gpa ?gpa .
    }
    """
    results = g.query(query)
    students = []
    for row in results:
        students.append({
            'student_uri': str(row.student),
            'student_id': str(row.id),
            'gpa': str(row.gpa)
        })
    return jsonify(students)

@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
