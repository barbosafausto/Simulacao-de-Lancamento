from manim import *
import numpy as np

class Lancamento(Scene):
    def construct(self):

        # Constantes e parâmetros iniciais
        g = 9.81
        k = 0.01 
        m = 1.0

        dt = 0.01

        v0 = 80.0
        angle_rad = np.deg2rad(45) 

        # Função que calcula os pontos da trajetória
        def get_trajectory_points(has_resistance):
            points = []
            vx, vy = v0 * np.cos(angle_rad), v0 * np.sin(angle_rad)
            x_pos, y_pos = 0, 0
            t = 0
            
            while True:
                #Vetor de coordenadas
                points.append(np.array([x_pos, y_pos, 0]))
                
                #Método de euler se tiver resistência
                if has_resistance:
                    v = np.sqrt(vx**2 + vy**2)

                    #Aceleração devido ao arrasto
                    ax = -(k/m) * v * vx 
                    ay = -(k/m) * v * vy - g

                    vx += ax * dt
                    vy += ay * dt

                    x_pos += vx * dt
                    y_pos += vy * dt

                #Movimento sem arrasto
                else:
                    x_pos = vx * t
                    y_pos = vy * t - 0.5 * g * t**2

                if y_pos < 0:
                    break

                t += dt

            return points

        # Cálculo das trajetórias (chamada da função)
        traj_no_res = get_trajectory_points(has_resistance=False)
        traj_with_res = get_trajectory_points(has_resistance=True)

        # Alcance e altura máximos
        max_x = max(point[0] for point in traj_no_res) 
        max_y = max(point[1] for point in traj_no_res)

        # Burocracia para fazer o gráfico da cena
        axes = Axes(
            x_range=[0, max_x * 1.1, 50],
            y_range=[0, max_y * 1.1, 50],
            axis_config={"color": WHITE}
        ).add_coordinates()
        
        #Gráfico do canto inferior esquerda 
        axes.to_corner(DL)
        
        #Legenda
        legend_no_res = Text("Sem Resistência", font_size=24).to_corner(UL).shift(DOWN * 0.5 + RIGHT).set_color(BLUE)
        legend_with_res = Text("Com Resistência", font_size=24).to_corner(UL).shift(DOWN * 0.8 + RIGHT).set_color(RED)
        
        #Adicionando tudo na tela
        self.add(axes, legend_no_res, legend_with_res)

        # Convertendo os pontos para coordenadas do Manim
        manim_points_no_res = [axes.coords_to_point(p[0], p[1]) for p in traj_no_res]
        manim_points_with_res = [axes.coords_to_point(p[0], p[1]) for p in traj_with_res]

        # Criação dos objetos que serão lançados
        dot_no_res = Dot(color=BLUE).move_to(manim_points_no_res[0])
        dot_with_res = Dot(color=RED).move_to(manim_points_with_res[0])
        
        # Convertendo as listas de pontos em objetos vetoriais
        path_no_res_obj = VMobject(stroke_color=BLUE).set_points_as_corners(manim_points_no_res)
        path_with_res_obj = VMobject(stroke_color=RED).set_points_as_corners(manim_points_with_res)

        #Adicionando tudo na tela
        self.add(dot_no_res, dot_with_res)

        # Pegando a distância com mais pontos
        time = len(traj_no_res) * dt;
        
        # Animando o lançamento
        self.play(
            MoveAlongPath(dot_no_res, path_no_res_obj),
            Create(path_no_res_obj),
            MoveAlongPath(dot_with_res, path_with_res_obj),
            Create(path_with_res_obj),
            run_time=time,
            rate_func=linear
        )
        
        self.wait(1)
