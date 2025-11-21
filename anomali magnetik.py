import tkinter as tk 
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import RBFInterpolator, interp1d
import os
import matplotlib
import matplotlib.patheffects as path_effects
matplotlib.use("TkAgg") 


class AnomaliMagnetikApp:
    """
    Aplikasi GUI untuk Pemetaan dan Visualisasi Anomali Magnetik Total.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ANOMALI MAGNETIK TOTAL - MUNTILAN")
        
        self.root.geometry("1500x600")
        self.root.configure(bg='#ffffff')  # LIGHT MODE
        self.df = None
        self.data_file = ""
        self.contour_fig = None
        self.profile_fig = None
        
        self._setup_styles()
        self.create_widgets()


    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure('TFrame', background='#ffffff')
        style.configure('TButton', background='#e6e6e6', foreground='black',
                        font=('Arial', 10, 'bold'))
        style.map('TButton', background=[('active', '#d0d0d0')])

        style.configure('TLabel', background='#ffffff', foreground='black',
                        font=('Arial', 10))

        style.configure('TNotebook', background='#ffffff', borderwidth=0)
        style.configure('TNotebook.Tab', background='#eeeeee', foreground='black',
                        padding=[10,5], font=('Arial',10,'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#ffffff')])


    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10", style='TFrame')
        main_frame.pack(fill='both', expand=True)

        title_label = ttk.Label(main_frame, 
                                text="PEMETAAN ANOMALI MAGNETIK TOTAL",
                                font=('Arial',16,'bold'), foreground='black')
        title_label.pack(pady=10)
        
        self.notebook = ttk.Notebook(main_frame, style='TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=10)

        self.contour_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.contour_frame, text='PETA KONTUR')
        self.create_contour_plot_area(self.contour_frame)

        self.profile_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.profile_frame, text='GRAFIK PROFIL')
        self.create_profile_plot_area(self.profile_frame)

        bottom_frame = ttk.Frame(main_frame, style='TFrame')
        bottom_frame.pack(fill='x', pady=10)
        
        self.status_label = ttk.Label(bottom_frame, text="SIAP", foreground='black')
        self.status_label.pack(side='left', padx=10, pady=5)
        
        ttk.Button(bottom_frame, text="RELOAD FILE",
                   command=self.reload_file).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="REFRESH SEMUA",
                   command=self.process_data).pack(side='left', padx=5)
        
        ttk.Button(bottom_frame, text="SIMPAN SEMUA",
                   command=lambda: self.save_all(save_data=True)).pack(side='right', padx=5)
        ttk.Button(bottom_frame, text="SIMPAN GRAFIK",
                   command=lambda: self.save_plot(self.profile_fig, "Profil_Anomali_Magnetik")).pack(side='right', padx=5)
        ttk.Button(bottom_frame, text="SIMPAN PETA",
                   command=lambda: self.save_plot(self.contour_fig, "Peta_Anomali_Magnetik")).pack(side='right', padx=5)


    #   AREA PETA
    def create_contour_plot_area(self, parent):
        plot_container = ttk.Frame(parent, style='TFrame')
        plot_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.contour_title = ttk.Label(plot_container,
            text="PETA ANOMALI MAGNETIK TOTAL DAERAH MUNTILAN",
            font=('Arial',12,'bold'), foreground='black')
        self.contour_title.pack(pady=10)
        
        self.contour_fig, self.contour_ax = plt.subplots(figsize=(10,7),
                                                          facecolor='white')
        self.contour_ax.set_facecolor('white')
        self.contour_fig.tight_layout()
        
        self.contour_canvas = FigureCanvasTkAgg(self.contour_fig, master=plot_container)
        self.contour_canvas_widget = self.contour_canvas.get_tk_widget()
        self.contour_canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        zoom_sidebar = ttk.Frame(plot_container, style='TFrame', width=50)
        zoom_sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        ttk.Label(zoom_sidebar, text="KETERANGAN", foreground='black').pack()

        self.contour_ax.clear()
        self.contour_ax.set_title("Silakan Muat Data", color='black')
        self.contour_canvas.draw()

    #   AREA PROFIL
    def create_profile_plot_area(self, parent):
        self.profile_fig, self.profile_ax = plt.subplots(figsize=(10,7),
                                                         facecolor='white')
        self.profile_ax.set_facecolor('white')
        self.profile_fig.tight_layout()
        
        self.profile_canvas = FigureCanvasTkAgg(self.profile_fig, master=parent)
        self.profile_canvas_widget = self.profile_canvas.get_tk_widget()
        self.profile_canvas_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.profile_ax.clear()
        self.profile_ax.set_title("Profil Anomali Magnetik • Lintasan Barat - Timur",
                                  color='black')
        self.profile_ax.set_xlabel("Titik Pengukuran", color='black')
        self.profile_ax.set_ylabel("Anomali (nT)", color='black')
        self.profile_ax.grid(color='#cccccc')
        self.profile_ax.axhline(0, color='black', linestyle='--')
        self.profile_canvas.draw()


    def reload_file(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files","*.xlsx")]
        )
        if filepath:
            self.data_file = filepath
            self.load_data(filepath)


    #   LOAD DATA
    def load_data(self, filepath):

        try:
            required_cols = ['x', 'y', 'Anomali Magnetik']

            self.df = pd.read_excel(
                filepath,
                sheet_name=0,
                header=0,
                usecols="A:D",
                decimal=','
            )

            for col in required_cols:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

            self.df.dropna(subset=required_cols, inplace=True)

            if self.df.empty:
                messagebox.showwarning("Peringatan", "Data kosong setelah pembersihan.")
                return
            
            self.update_status(f"BERHASIL LOAD {len(self.df)} TITIK • {os.path.basename(filepath)}")
            self.process_data()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat file:\n{e}")
            self.df = None


    def process_data(self):
        if self.df is None or self.df.empty:
            return
        self.plot_contour()
        self.plot_profile()


    #   PETA KONTUR
    def plot_contour(self):
        self.contour_ax.clear()
        self.contour_ax.set_facecolor('white')

        X = self.df[['x','y']].values
        Z = self.df['Anomali Magnetik'].values
        
        min_x, max_x = X[:,0].min(), X[:,0].max()
        min_y, max_y = X[:,1].min(), X[:,1].max()
        nx, ny = 600, 600
        xi = np.linspace(min_x, max_x, nx)
        yi = np.linspace(min_y, max_y, ny)
        Xi, Yi = np.meshgrid(xi, yi)
        
        try:
            rbfi = RBFInterpolator(X, Z, kernel='thin_plate_spline')
            Zi = rbfi(np.array([Xi.flatten(), Yi.flatten()]).T).reshape(Xi.shape)
        except Exception as e:
            messagebox.showerror("Error", f"Interpolasi gagal:\n{e}")
            return
        
        contour_plot = self.contour_ax.contourf(
            Xi, Yi, Zi, levels=60, cmap='cividis'
        )
        
        self.contour_ax.set_title("PETA ANOMALI MAGNETIK TOTAL DAERAH MUNTILAN",
                                  color='black')
        self.contour_ax.set_xlabel("X", color='black')
        self.contour_ax.set_ylabel("Y", color='black')
        self.contour_ax.tick_params(colors='black')

        # Label titik
        for i in range(len(self.df)):
            x_i = self.df["x"].iloc[i]
            y_i = self.df["y"].iloc[i]
            label = str(self.df.iloc[i, 0])

            self.contour_ax.text(
                x_i, y_i, label,
                fontsize=8, color='black',
                path_effects=[path_effects.withStroke(linewidth=2,
                                                      foreground='white')]
            )

        cbar = self.contour_fig.colorbar(contour_plot, ax=self.contour_ax)
        plt.setp(cbar.ax.get_yticklabels(), color='black')
        
        self.contour_canvas.draw()


    #   PROFIL
    def plot_profile(self):
        self.profile_ax.clear()
        self.profile_ax.set_facecolor('white')

        df_sorted = self.df.sort_values(by='x').reset_index(drop=True)
        Z = df_sorted['Anomali Magnetik'].values
        X_index = np.arange(len(df_sorted))
        
        if len(X_index) > 3:
            X_smooth = np.linspace(X_index.min(), X_index.max(), 500)
            f_interp = interp1d(X_index, Z, kind='cubic')
            Z_smooth = f_interp(X_smooth)
        else:
            X_smooth = X_index
            Z_smooth = Z
        
        self.profile_ax.plot(X_smooth, Z_smooth, color='#0066cc', linewidth=2.5)
        self.profile_ax.scatter(X_index, Z, color='#cc0000')
        
        for i in range(len(df_sorted)):
            label = str(df_sorted.iloc[i, 0])

            self.profile_ax.text(
                i, Z[i], label,
                fontsize=8, color='black',
                path_effects=[path_effects.withStroke(linewidth=2,
                                                      foreground='white')]
            )
        
        self.profile_ax.set_title("Profil Anomali Magnetik • Lintasan Barat - Timur",
                                  color='black')
        self.profile_ax.set_xlabel("Nomor Titik", color='black')
        self.profile_ax.set_ylabel("Anomali (nT)", color='black')
        self.profile_ax.grid(color='#cccccc')
        self.profile_ax.axhline(0, color='black', linestyle='--')
        self.profile_canvas.draw()

    def save_plot(self, figure, filename_prefix):
        if figure is None:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{filename_prefix}_{timestamp}.png"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files","*.png")],
            initialfile=default_filename
        )
        if filepath:
            figure.savefig(filepath, facecolor=figure.get_facecolor())

    def save_all(self, save_data=False):
        if self.df is None:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_dir = filedialog.askdirectory()
        
        if save_dir:
            out = os.path.join(save_dir, f"Anomali_Magnetik_{timestamp}")
            os.makedirs(out, exist_ok=True)
            
            self.contour_fig.savefig(os.path.join(out, "Peta_Kontur.png"),
                                     facecolor=self.contour_fig.get_facecolor())
            self.profile_fig.savefig(os.path.join(out, "Grafik_Profil.png"),
                                     facecolor=self.profile_fig.get_facecolor())
            
            if save_data:
                self.df.to_csv(os.path.join(out, "Data_Anomali.csv"), index=False)
                
            messagebox.showinfo("Sukses", f"Data tersimpan di:\n{out}")

    def update_status(self, message):
        self.status_label.config(text=message)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AnomaliMagnetikApp()
    app.run()
