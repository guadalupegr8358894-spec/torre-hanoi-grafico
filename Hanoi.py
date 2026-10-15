import tkinter as tk
from tkinter import messagebox, ttk


class HanoiManualApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Torre de Hanói - Versión Manual (Hasta 64 discos)")
    self.root.geometry("800x500")
    self.root.config(bg="#f0f0f0")

    self.num_discos = 4  # Valor inicial recomendado
    self.movimientos = 0
    self.origen_seleccionado = None

    self.setup_ui()
    self.reset_game()

  def setup_ui(self):
    control_frame = tk.Frame(self.root, bg="#f0f0f0")
    control_frame.pack(pady=15)

    tk.Label(
        control_frame,
        text="Discos (1-64):",
        bg="#f0f0f0",
        font=("Arial", 11),
    ).pack(side=tk.LEFT, padx=5)

    # Selector modificado para permitir de 1 hasta 64 discos
    self.spin_discos = ttk.Spinbox(
        control_frame, from_=1, to=64, width=5, font=("Arial", 11)
    )
    self.spin_discos.set(self.num_discos)
    self.spin_discos.pack(side=tk.LEFT, padx=5)

    btn_reiniciar = tk.Button(
        control_frame,
        text="Reiniciar / Aplicar",
        command=self.reset_game,
        bg="#f44336",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    btn_reiniciar.pack(side=tk.LEFT, padx=10)

    self.lbl_instruccion = tk.Label(
        self.root,
        text=(
            "Haz clic en la torre de origen y luego en la torre de destino para"
            " mover un disco."
        ),
        bg="#f0f0f0",
        font=("Arial", 10, "italic"),
        fg="#333",
    )
    self.lbl_instruccion.pack(pady=5)

    self.canvas = tk.Canvas(
        self.root, width=760, height=280, bg="white", highlightthickness=1
    )
    self.canvas.pack(pady=5)
    self.canvas.bind("<Button-1>", self.manejar_clic)

    self.lbl_movimientos = tk.Label(
        self.root,
        text="Movimientos: 0",
        bg="#f0f0f0",
        font=("Arial", 12, "bold"),
    )
    self.lbl_movimientos.pack(pady=5)

  def reset_game(self):
    try:
      self.num_discos = int(self.spin_discos.get())
      if self.num_discos < 1:
        self.num_discos = 1
      elif self.num_discos > 64:
        self.num_discos = 64
    except ValueError:
      self.num_discos = 4

    self.torres = {
        "A": list(range(self.num_discos, 0, -1)),
        "B": [],
        "C": [],
    }
    self.movimientos = 0
    self.origen_seleccionado = None
    self.lbl_movimientos.config(text="Movimientos: 0")
    self.dibujar_torres()

  def dibujar_torres(self):
    self.canvas.delete("all")
    x_coords = {"A": 150, "B": 400, "C": 650}
    base_y = 240
    rod_height = 180

    for nombre, x in x_coords.items():
      color_poste = "#FF9800" if self.origen_seleccionado == nombre else "#8B4513"

      self.canvas.create_rectangle(
          x - 5, base_y - rod_height, x + 5, base_y, fill=color_poste
      )
      self.canvas.create_rectangle(
          x - 75, base_y, x + 75, base_y + 10, fill="#8B4513"
      )
      self.canvas.create_text(
          x, base_y + 25, text=f"Torre {nombre}", font=("Arial", 11, "bold")
      )

      discos = self.torres[nombre]
      total_discos = len(discos)

      # Ajustar el alto de los discos dinámicamente si hay muchos,
      # para evitar que se salgan del área visible de la pantalla
      d_height = max(2, min(16, int(160 / max(1, self.num_discos))))

      for index, disco in enumerate(discos):
        d_width = max(
            10, int(140 * (disco / max(1, self.num_discos)))
        )  # Ancho proporcional
        d_y = base_y - 10 - (index * d_height)
        color = f"#{(disco*35)%256:02x}{(disco*60)%256:02x}{220:02x}"

        self.canvas.create_rectangle(
            x - d_width / 2,
            d_y - d_height,
            x + d_width / 2,
            d_y,
            fill=color,
            outline="black",
        )

        # Solo mostrar texto numérico si no son demasiados discos para evitar saturar
        if self.num_discos <= 10:
          self.canvas.create_text(
              x,
              d_y - d_height / 2,
              text=str(disco),
              fill="white",
              font=("Arial", 8, "bold"),
          )

  def manejar_clic(self, event):
    x = event.x
    if x < 280:
      torre_clic = "A"
    elif x < 530:
      torre_clic = "B"
    else:
      torre_clic = "C"

    if self.origen_seleccionado is None:
      if len(self.torres[torre_clic]) > 0:
        self.origen_seleccionado = torre_clic
        self.dibujar_torres()
      else:
        messagebox.showwarning(
            "Aviso", f"La Torre {torre_clic} está vacía. Elige otra."
        )
    else:
      origen = self.origen_seleccionado
      destino = torre_clic
      self.origen_seleccionado = None

      if origen == destino:
        self.dibujar_torres()
        return

      disco_a_mover = self.torres[origen][-1]
      if (
          len(self.torres[destino]) == 0
          or self.torres[destino][-1] > disco_a_mover
      ):
        disco = self.torres[origen].pop()
        self.torres[destino].append(disco)
        self.movimientos += 1
        self.lbl_movimientos.config(text=f"Movimientos: {self.movimientos}")
        self.dibujar_torres()

        if len(self.torres["C"]) == self.num_discos:
          messagebox.showinfo(
              "¡Felicidades!",
              (
                  "¡Has ganado el juego en"
                  f" {self.movimientos} movimientos!"
              ),
          )
          self.reset_game()
      else:
        messagebox.showerror(
            "Movimiento inválido",
            "No puedes colocar un disco grande sobre uno más pequeño.",
        )
        self.dibujar_torres()


if __name__ == "__main__":
  root = tk.Tk()
  app = HanoiManualApp(root)
  root.mainloop()