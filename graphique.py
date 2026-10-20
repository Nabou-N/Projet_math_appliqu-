import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fonctions import calculer, evaluer_expression_libre

class Graphique:
    def __init__(self, parent):
        self.figure, self.ax = plt.subplots(figsize=(8, 5), dpi=100)
        self.figure.patch.set_facecolor("white")
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.vide()

    def vide(self):
        self.ax.clear()
        self.ax.set_title("La courbe apparaîtra après le calcul",
                          fontsize=11, color="#737373", pad=10)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.grid(True, alpha=.18)
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.canvas.draw()

    def tracer(self, nom, params, xmin, xmax):
        xmin, xmax = float(xmin), float(xmax)
        if xmin >= xmax:
            raise ValueError("Intervalle graphique invalide.")

        if nom == "Logarithme":
            xmin = max(xmin, 0.01)
        elif nom == "Puissance" and isinstance(params, list) and len(params) > 1 and params[1] != int(params[1]):
            xmin = max(xmin, 0.01)

        x = np.linspace(xmin, xmax, 1200)

        if nom in ["Exponentielle", "Logarithme"]:
            try:
                a, u_expr, b = params
                u_val = evaluer_expression_libre(u_expr, x)
                
                if nom == "Exponentielle":
                    y = a * np.exp(u_val) + b
                else:  
                    y = a * np.log(np.where(u_val > 0, u_val, np.nan)) + b
                    
                y = np.where(np.isfinite(y) & (np.abs(y) < 1e12), y, np.nan)
            except Exception as e:
                raise ValueError(f"Erreur dans l'expression u(x) : {e}")
        else:
            y = np.empty_like(x)
            for i, xv in enumerate(x):
                try:
                    value = calculer(nom, params, float(xv))
                    y[i] = value if np.isfinite(value) and abs(value) < 1e12 else np.nan
                except Exception:
                    y[i] = np.nan

        self.ax.clear()
        self.ax.plot(x, y, color="#C62828", linewidth=2.4)
        self.ax.axhline(0, color="#777777", linewidth=.9)
        self.ax.axvline(0, color="#777777", linewidth=.9)
        self.ax.grid(True, alpha=.22)
        self.ax.set_title(nom, fontsize=12, color="#262626", pad=10)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.figure.tight_layout()
        self.canvas.draw()
