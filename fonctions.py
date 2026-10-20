import math
import numpy as np

FUNCTIONS = {
    "Affine": {
        "formula": "f(x) = ax + b",
        "params": [
            ("a", "Coefficient directeur", "1"),
            ("b", "Ordonnée à l'origine", "0")
        ]
    },
    "Linéaire": {
        "formula": "f(x) = ax",
        "params": [
            ("a", "Coefficient", "1")
        ]
    },
    "Puissance": {
        "formula": "f(x) = axⁿ",
        "params": [
            ("a", "Coefficient", "1"),
            ("n", "Exposant", "2")
        ]
    },
    "Exponentielle": {
        "formula": "f(x) = aeᵘ⁽ˣ⁾ + b",
        "params": [
            ("a", "Coefficient a", "1"),
            ("u", "Exposant u(x)", "x"),
            ("b", "Constante b", "0")
        ]
    },
    "Logarithme": {
        "formula": "f(x) = a ln(u(x)) + b",
        "params": [
            ("a", "Coefficient a", "1"),
            ("u", "Argument u(x)", "x"),
            ("b", "Constante b", "0")
        ]
    },
    "Polynôme 2nd degré": {
        "formula": "f(x) = ax² + bx + c",
        "params": [
            ("a", "Coefficient de x²", "1"),
            ("b", "Coefficient de x", "0"),
            ("c", "Constante", "0")
        ]
    }
}

def rendre_exposant_joli(texte):
    """Convertit une chaîne normale en vrais caractères exposants pour l'affichage visuel."""
    normal = "0123456789xX+-*()"
    expo   = "⁰¹²³⁴⁵⁶⁷⁸⁹ˣˣ⁺⁻*⁽⁾"
    table = str.maketrans(normal, expo)
    
    res = texte.translate(table)
    res = res.replace('*', '')  
    return res

def evaluer_expression_libre(expression_str, x):
    """Évalue dynamiquement l'exposant ou l'argument textuel saisi par l'utilisateur."""
    expr = expression_str.lower()
    
    expr = expr.replace('²', '**2')
    expr = expr.replace('³', '**3')
    expr = expr.replace('^', '**')
    expr = expr.replace('e**', 'np.exp')
    expr = expr.replace('ln', 'np.log')
    expr = expr.replace('exp', 'np.exp')
    
    contexte = {
        'x': x,
        'np': np,
        'pi': np.pi,
        'cos': np.cos,
        'sin': np.sin,
        'tan': np.tan,
        'sqrt': np.sqrt
    }
    return eval(expr, {"__builtins__": None}, contexte)

def calculer(nom, params, x):
    if nom == "Affine":
        a, b = params
        return a * x + b
    if nom == "Linéaire":
        return params * x
    if nom == "Puissance":
        a, n = params
        return a * (x ** n)
    if nom == "Exponentielle":
        a, u_expr, b = params
        u_val = evaluer_expression_libre(u_expr, x)
        return a * math.exp(float(u_val)) + b
    if nom == "Logarithme":
        a, u_expr, b = params
        u_val = evaluer_expression_libre(u_expr, x)
        if u_val <= 0:
            raise ValueError("L'argument du ln doit être strictement supérieur à 0.")
        return a * math.log(float(u_val)) + b
    if nom == "Polynôme 2nd degré":
        a, b, c = params
        return a*x*x + b*x + c
    raise ValueError("Fonction inconnue.")

def expression(nom, params):
    if nom == "Affine":
        a, b = params
        return f"f(x) = {a:g}x + {b:g}"
    if nom == "Linéaire":
        return f"f(x) = {params:g}x"
    if nom == "Puissance":
        a, n = params
        return f"f(x) = {a:g}x^{n:g}"
    if nom == "Exponentielle":
        a, u_expr, b = params
        signe = "+" if b >= 0 else "-"
        u_joli = rendre_exposant_joli(u_expr)
        return f"f(x) = {a:g}e{u_joli} {signe} {abs(b):g}"
    if nom == "Logarithme":
        a, u_expr, b = params
        signe = "+" if b >= 0 else "-"
        u_joli = u_expr.replace('*', '')
        return f"f(x) = {a:g}ln({u_joli}) {signe} {abs(b):g}"
    if nom == "Polynôme 2nd degré":
        a, b, c = params
        return f"f(x) = {a:g}x² + {b:g}x + {c:g}"
