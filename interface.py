import tkinter as tk
from tkinter import ttk, messagebox
from fonctions import FUNCTIONS, calculer, expression
from graphique import Graphique

BG = "#F4F5F7"
WHITE = "#FFFFFF"
BLACK = "#111111"
DARK = "#1B1B1B"
RED = "#C62828"
RED_HOVER = "#A61F1F"
RED_LIGHT = "#FDECEC"
TEXT = "#262626"
MUTED = "#737373"
BORDER = "#D9D9D9"
GREEN = "#16803A"
GREEN_LIGHT = "#E7F6EC"
YELLOW = "#E5A500"
YELLOW_LIGHT = "#FFF5D6"

class MathLab:
    def __init__(self, root):
        self.root = root
        self.root.title("MathLab - Calculatrice scientifique & fonctions")
        self.root.geometry("1240x760")
        self.root.minsize(980, 620)
        self.root.configure(bg=BG)

        self.param_vars = []
        self.type_var = tk.StringVar(value="Affine")
        self.graph_visible = False

        self.setup_style()
        self.build()
        self.change_function()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Clean.TCombobox",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=7
        )
        style.map("Clean.TCombobox",
                  fieldbackground=[("readonly", WHITE)],
                  selectbackground=[("readonly", RED_LIGHT)],
                  selectforeground=[("readonly", TEXT)])

    def build(self):
        self.build_header()

        self.body = tk.Frame(self.root, bg=BG)
        self.body.pack(fill="both", expand=True, padx=16, pady=14)

        # panel gauche 
        self.left_outer = tk.Frame(self.body, bg=WHITE,
                                   highlightbackground=BORDER,
                                   highlightthickness=1)
        self.left_outer.pack(side="left", fill="both", expand=True)

        self.left_canvas = tk.Canvas(
            self.left_outer, bg=WHITE, highlightthickness=0, bd=0
        )
        self.left_scrollbar = ttk.Scrollbar(
            self.left_outer, orient="vertical",
            command=self.left_canvas.yview
        )
        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

        self.left_scrollbar.pack(side="right", fill="y")
        self.left_canvas.pack(side="left", fill="both", expand=True)

        self.left = tk.Frame(self.left_canvas, bg=WHITE)
        self.left_window = self.left_canvas.create_window(
            (0, 0), window=self.left, anchor="nw"
        )

        self.left.bind(
            "<Configure>",
            lambda e: self.left_canvas.configure(
                scrollregion=self.left_canvas.bbox("all")
            )
        )
        self.left_canvas.bind(
            "<Configure>",
            lambda e: self.left_canvas.itemconfigure(
                self.left_window, width=e.width
            )
        )

        self.left_canvas.bind_all("<MouseWheel>", self.mousewheel)
        self.left_canvas.bind_all("<Button-4>", self.mousewheel_linux)
        self.left_canvas.bind_all("<Button-5>", self.mousewheel_linux)

        self.build_left()

        # mpamorina le graph fa mbola afenina
        # miala loza ty rhf vokitika le bouton calcul
        self.right = tk.Frame(self.body, bg=BG)
        self.build_right()

    def mousewheel(self, event):
        if self.graph_visible and self.left_canvas.winfo_containing(
            event.x_root, event.y_root
        ):
            self.left_canvas.yview_scroll(int(-event.delta / 120), "units")

    def mousewheel_linux(self, event):
        if self.graph_visible and self.left_canvas.winfo_containing(
            event.x_root, event.y_root
        ):
            self.left_canvas.yview_scroll(
                -1 if event.num == 4 else 1, "units"
            )

    def build_header(self):
        header = tk.Frame(self.root, bg=BLACK, height=68)
        header.pack(fill="x")
        header.pack_propagate(False)

       
        tk.Frame(header, bg=RED, width=7).pack(side="left", fill="y")

        logo = tk.Frame(header, bg=RED, width=43, height=43)
        logo.pack(side="left", padx=(18, 11), pady=12)
        logo.pack_propagate(False)

        tk.Label(
            logo, text="ƒ", bg=RED, fg=WHITE,
            font=("Segoe UI", 21, "bold")
        ).pack(expand=True)

        title_box = tk.Frame(header, bg=BLACK)
        title_box.pack(side="left", pady=10)

        tk.Label(
            title_box, text="MathLab",
            bg=BLACK, fg=WHITE,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_box, text="Calculatrice scientifique & fonctions",
            bg=BLACK, fg="#BDBDBD",
            font=("Segoe UI", 8)
        ).pack(anchor="w")

    def build_left(self):
        top = tk.Frame(self.left, bg=WHITE)
        top.pack(fill="x", padx=22, pady=(20, 8))

        tk.Label(
            top, text="Configuration",
            bg=WHITE, fg=TEXT,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            top, text="Choisissez une fonction et ses paramètres.",
            bg=WHITE, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))

        card = tk.Frame(
            self.left, bg="#FAFAFA",
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="x", padx=22, pady=8)

        tk.Label(
            card, text="TYPE DE FONCTION",
            bg="#FAFAFA", fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=14, pady=(12, 4))

        combo = ttk.Combobox(
            card, textvariable=self.type_var,
            values=list(FUNCTIONS.keys()),
            state="readonly",
            style="Clean.TCombobox"
        )
        combo.pack(fill="x", padx=14)
        combo.bind("<<ComboboxSelected>>",
                   lambda e: self.change_function())

        self.formula = tk.Label(
            card, text="f(x) = ax + b",
            bg=RED_LIGHT, fg=RED,
            font=("Segoe UI", 10, "bold"),
            padx=10, pady=7
        )
        self.formula.pack(fill="x", padx=14, pady=10)

        self.section_title("PARAMÈTRES", 13)
        self.params_frame = tk.Frame(self.left, bg=WHITE)
        self.params_frame.pack(fill="x", padx=22)

        # Only results, no x value and no graph domain.
        self.section_title("RÉSULTAT", 18)

        result_frame = tk.Frame(
            self.left, bg="#FAFAFA",
            highlightbackground=BORDER,
            highlightthickness=1
        )
        result_frame.pack(fill="x", padx=22)

        self.result = tk.Text(
            result_frame, bg="#FAFAFA", fg=TEXT,
            font=("Consolas", 10), relief="flat", bd=0,
            wrap="word", height=7
        )
        self.result.pack(fill="x", padx=10, pady=10)
        self.result.config(state="disabled")

        self.section_title("ACTIONS", 18)

        self.calculate_btn = self.button(
            self.left,
            "▶  AFFICHER LES RÉSULTATS & LA COURBE",
            self.calculate, RED, RED_HOVER, WHITE
        )
        self.calculate_btn.pack(fill="x", padx=22, pady=(0, 7))

        self.reset_btn = self.button(
            self.left,
            "↺  RÉINITIALISER",
            self.reset, "#E9E9E9", "#DCDCDC", TEXT
        )
        self.reset_btn.pack(fill="x", padx=22, pady=(0, 20))

    def build_right(self):
        result_card = tk.Frame(
            self.right, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        result_card.pack(fill="x", pady=(0, 10))

        self.right_expression = tk.Label(
            result_card, text="f(x) = ...",
            bg=WHITE, fg=TEXT,
            font=("Segoe UI", 16, "bold")
        )
        self.right_expression.pack(anchor="w", padx=18, pady=(13, 2))

        self.right_value = tk.Label(
            result_card, text="Résultat : —",
            bg=WHITE, fg=GREEN,
            font=("Segoe UI", 11, "bold")
        )
        self.right_value.pack(anchor="w", padx=18, pady=(0, 13))

        graph_card = tk.Frame(
            self.right, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        graph_card.pack(fill="both", expand=True)

        tk.Label(
            graph_card, text="COURBE",
            bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=15, pady=8)

        area = tk.Frame(graph_card, bg=WHITE)
        area.pack(fill="both", expand=True)

        self.graph = Graphique(area)

    def section_title(self, text, pady):
        tk.Label(
            self.left, text=text,
            bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=22, pady=(pady, 4))

    def field(self, label, variable):
        row = tk.Frame(self.params_frame, bg=WHITE)
        row.pack(fill="x", pady=4)

        tk.Label(
            row, text=label,
            bg=WHITE, fg=TEXT,
            font=("Segoe UI", 9)
        ).pack(side="left")

        tk.Entry(
            row, textvariable=variable, width=13,
            bg="#FAFAFA", fg=TEXT,
            relief="solid", bd=1,
            font=("Segoe UI", 9)
        ).pack(side="right", ipady=4)

    def button(self, parent, text, command, bg, hover, fg):
        return tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=hover,
            activeforeground=WHITE if fg == WHITE else TEXT,
            relief="flat", bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2", pady=10
        )

    def change_function(self):
        for w in self.params_frame.winfo_children():
            w.destroy()

        self.param_vars.clear()
        name = self.type_var.get()
        data = FUNCTIONS[name]
        self.formula.config(text=data["formula"])

        for _, label, default in data["params"]:
            var = tk.StringVar(value=default)
            self.param_vars.append(var)
            self.field(label, var)

        self.set_result("Choisissez les paramètres puis cliquez sur le bouton rouge.")

    def set_result(self, text):
        self.result.config(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("end", text)
        self.result.config(state="disabled")

    def calculate(self):
        try:
            name = self.type_var.get()
            
           
            if name in ["Exponentielle", "Logarithme"]:
                params = [
                    float(self.param_vars[0].get().replace(",", ".")), 
                    self.param_vars[1].get(),                          
                    float(self.param_vars[2].get().replace(",", "."))   
                ]
            else:
                params = [
                    float(v.get().replace(",", "."))
                    for v in self.param_vars
                ]

            x = 1.0
            xmin, xmax = -10, 10
            
            if name == "Logarithme":
                xmin, xmax = 0.05, 10
                try:
                    y = calculer(name, params, x)
                except Exception:
                    x = 3.0
                    y = calculer(name, params, x)
            else:
                y = calculer(name, params, x)
                
            expr = expression(name, params)

            self.graph.tracer(name, params, xmin, xmax)
            self.show_graph_panel()

            self.right_expression.config(text=expr)
            self.right_value.config(text=f"Résultat : f({x:g}) = {y:.8g}")

            self.set_result(
                f"Fonction : {name}\n\n"
                f"{expr}\n\n"
                f"Valeur de référence : f({x:g}) = {y:.8g}"
            )

        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Vérifiez la saisie de vos paramètres.\n\n⚠️ Rappel : Écrivez les multiplications avec une étoile (ex: 3*x+3 au lieu de 3x+3).\n\nDétail technique : {e}")

    def show_graph_panel(self):
        if self.graph_visible:
            return

        self.left_outer.pack_forget()
        self.left_outer.pack(
            side="left", fill="y",
            expand=False
        )
        self.left_outer.configure(width=365)
        self.left_outer.pack_propagate(False)

        self.right.pack(
            side="left", fill="both",
            expand=True, padx=(12, 0)
        )

        self.graph_visible = True
        self.left_canvas.update_idletasks()
        self.left_canvas.configure(
            scrollregion=self.left_canvas.bbox("all")
        )

    def reset(self):
        self.type_var.set("Affine")
        self.change_function()
        self.graph.vide()

        self.right_expression.config(text="f(x) = ...")
        self.right_value.config(text="Résultat : —")

        if self.graph_visible:
            self.right.pack_forget()
            self.left_outer.pack_forget()
            self.left_outer.pack(
                side="left", fill="both", expand=True
            )
            self.graph_visible = False

        self.left_canvas.yview_moveto(0)

    def update_clock(self):
        
        self.root.after(60000, self.update_clock)
