from flask import Flask, render_template, request
from itertools import product

app = Flask(__name__)
GATES = ['AND', 'OR', 'NOT', 'XOR', 'NAND', 'IMPLIES', 'BICONDITIONAL']

def evaluate(gate, p, q):
    return {'AND': p and q, 'OR': p or q, 'NOT': not p,
            'XOR': p != q, 'NAND': not (p and q),
            'IMPLIES': (not p) or q, 'BICONDITIONAL': p == q}[gate]

@app.route('/', methods=['GET', 'POST'])
def home():
    data = request.form if request.method == 'POST' else request.args
    gate = data.get('gate', 'AND').upper()
    if gate not in GATES:
        gate = 'AND'
    p = data.get('p', '0') == '1'
    q = data.get('q', '0') == '1'
    output = evaluate(gate, p, q)
    rows = [{'p': a, 'q': b, 'result': evaluate(gate, a, b), 'active': a == p and b == q}
            for a, b in product((False, True), repeat=2)]
    outcomes = [row['result'] for row in rows]
    classification = 'Tautology' if all(outcomes) else 'Contradiction' if not any(outcomes) else 'Contingency'
    equivalence = all(not (a or b) == ((not a) and (not b)) for a, b in product((False, True), repeat=2))
    symbols = {'AND': 'P ∧ Q', 'OR': 'P ∨ Q', 'NOT': '¬P', 'XOR': 'P ⊕ Q', 'NAND': '¬(P ∧ Q)',
               'IMPLIES': 'P → Q', 'BICONDITIONAL': 'P ↔ Q'}
    return render_template('index.html', gates=GATES, gate=gate, p=p, q=q, output=output,
                           rows=rows, classification=classification, equivalence=equivalence, formula=symbols[gate])

if __name__ == '__main__':
    app.run(debug=True)
