import gradio as gr
import modules.scripts as scripts
from modules import script_callbacks

class SetWidthScript(scripts.Script):
    # Статический атрибут для слайдера ширины
    txt2img_w_slider = None
    txt2img_h_slider = None

    def __init__(self):
        pass  # Инициализация не требуется

    def title(self):
        return "Adjust Width"

    def show(self, is_img2img):
        return scripts.AlwaysVisible  # Показывать всегда
    
    def ui(self, is_img2img):
        # Ваш интерфейс для загрузки изображений и настройки размеров
        with gr.Box():
            with gr.Row(elem_id="txt2img_get_ar"):
                with gr.Column():
                    image_drop = gr.Image(label="Upload your image", width=150, height=150, elem_id="getar_image_drop")
                with gr.Column():
                    with gr.Row():
                        input_real_w = gr.Number(label="Real Width", value=None, elem_id="ar_input_real_w", style={'width': '4em'})
                        input_real_h = gr.Number(label="Real Height", value=None, elem_id="ar_input_real_h", style={'width': '4em'})
                        calc_aspect = gr.Text(label="Aspect Ratio", value="", elem_id="ar_calc_aspect", style={'width': '4em'})
                    with gr.Row():
                        input_calc_w = gr.Number(label="Calc Width", value=None, elem_id="input_calc_w", style={'width': '4em'})
                        input_calc_h = gr.Number(label="Calc Height", value=None, elem_id="input_calc_h", style={'width': '4em'})
                    with gr.Row():
                        but_set_size = gr.Button("Set Size", css_class="my-button", elem_id="but_set_size")
                        but_set_calc = gr.Button("Set calc", css_class="my-button", elem_id="but_set_calc")

        # Настройка обработчика клика для кнопки 'but_set_size'
        but_set_size.click(
            self.ar_set_size,
            inputs=[input_real_w, input_real_h],  # Теперь мы передаем два значения
            outputs=[self.txt2img_w_slider, self.txt2img_h_slider]  # И обновляем два слайдера
        )
        
        but_set_calc.click(
            self.ar_set_size,  # Используем ту же функцию ar_set_size
            inputs=[input_calc_w, input_calc_h],  # Передаем значения из input_calc_w и input_calc_h
            outputs=[self.txt2img_w_slider, self.txt2img_h_slider]  # Обновляем два слайдера
        )

        image_drop.change(self.image_dropped, inputs=[image_drop], outputs=[input_real_w, input_real_h, calc_aspect])
        return [image_drop, input_real_w, input_real_h, calc_aspect, input_calc_w, input_calc_h, but_set_size]

    def ar_set_size(self, real_width, real_height):
        # Теперь функция устанавливает размеры как для ширины, так и для высоты
        if real_width is not None and real_width > 0:
            print(f"Setting width to {real_width}")
        else:
            real_width = self.txt2img_w_slider.value  # Берем текущее значение слайдера, если новое невалидно
            print("No valid width provided, not setting size")
        
        if real_height is not None and real_height > 0:
            print(f"Setting height to {real_height}")
        else:
            real_height = self.txt2img_h_slider.value  # Берем текущее значение слайдера, если новое невалидно
            print("No valid height provided, not setting size")
            
        return real_width, real_height

    def gcd(self, x, y):
        while(y):
            x, y = y, x % y
        return x

    def image_dropped(self, image):
        if image is not None:
            width, height = image.shape[1], image.shape[0]
            aspect_gcd = self.gcd(width, height)
            aspect_ratio = f"{width // aspect_gcd}:{height // aspect_gcd}"
            print(f"Image dropped with width: {width}, height: {height}, aspect ratio: {aspect_ratio}")  # Вывод в консоль
            return width, height, aspect_ratio
        else:
            return "", "", ""

    @staticmethod
    def on_after_component(component, **_kwargs):
        # Теперь мы сохраняем ссылки на оба слайдера: ширины и высоты
        elem_id = getattr(component, "elem_id", None)
        if elem_id == "txt2img_width":
            SetWidthScript.txt2img_w_slider = component
        elif elem_id == "txt2img_height":
            SetWidthScript.txt2img_h_slider = component

# Регистрация методов on_after_component
script_callbacks.on_after_component(SetWidthScript.on_after_component)












# VERSION 2
# import gradio as gr
# import modules.scripts as scripts
# from modules import script_callbacks

# class SetWidthScript(scripts.Script):
#     # Статический атрибут для слайдера ширины
#     txt2img_w_slider = None

#     # Инициализация скрипта
#     def __init__(self):
#         pass 

#     def title(self):
#         return "Set Width to 888"

#     def show(self, is_img2img):
#         return scripts.AlwaysVisible  # Показывать всегда
    
#     def ui(self, is_img2img):
#         ar_set_size_button = gr.Button("Set width to 888")
#         ar_set_size_button.click(
#             self.ar_set_size,
#             inputs=[],
#             outputs=[self.txt2img_w_slider]
#         )
#         return [ar_set_size_button]

#     def ar_set_size(self):
#         print("Set size") 
#         # Возвращаем значение, которое должно быть установлено в слайдере
#         return 888

#     @staticmethod
#     def on_after_component(component, **_kwargs):
#         # Связывание слайдера ширины с атрибутом скрипта
#         elem_id = getattr(component, "elem_id", None)
#         if elem_id == "txt2img_width":
#             SetWidthScript.txt2img_w_slider = component

# # Регистрация методов on_after_component
# script_callbacks.on_after_component(SetWidthScript.on_after_component)


# VERSION 1
# import gradio as gr
# import modules.scripts as scripts
# from modules import images, script_callbacks
# from modules.processing import process_images, Processed
# from modules.shared import opts, cmd_opts, state

# class GetARScript(scripts.Script):
#     def title(self):
#         return "Extension GetAR"

#     def show(self, is_img2img):
#         return scripts.AlwaysVisible
    
#     def __init__(self):
#         self.t2i_w = 512  # временное значение
#         self.t2i_h = 512  # временное значение

#     def ui(self, is_img2img):
#         with gr.Box():
#             with gr.Row(elem_id="txt2img_get_ar"):
#                 with gr.Column():
#                     image_drop = gr.Image(label="Upload your image", width=150, height=150, elem_id="getar_image_drop")
#                 with gr.Column():
#                     with gr.Row():
#                         input_real_w = gr.Number(label="Real Width", value=None, elem_id="ar_input_real_w", style={'width': '4em'})
#                         input_real_h = gr.Number(label="Real Height", value=None, elem_id="ar_input_real_h", style={'width': '4em'})
#                         calc_aspect = gr.Text(label="Aspect Ratio", value="", elem_id="ar_calc_aspect", style={'width': '4em'})
#                     with gr.Row():
#                         input_calc_w = gr.Number(label="Calc Width", value=None, elem_id="input_calc_w", style={'width': '4em'})
#                         input_calc_h = gr.Number(label="Calc Height", value=None, elem_id="input_calc_h", style={'width': '4em'})
#                     with gr.Row():
#                         but_set_size = gr.Button("Set size", css_class="my-button", elem_id="but_set_size")
#                         but_set_calc = gr.Button("Set calc", css_class="my-button", elem_id="but_set_calc")

#         but_set_size.click(
#             self.ar_set_size,
#             inputs=[input_real_w, input_real_h],
#             outputs=[self.t2i_w, self.t2i_h]  # Убедитесь, что self.t2i_w и self.t2i_h — это объекты Gradio
#         )


#         image_drop.change(self.image_dropped, inputs=[image_drop], outputs=[input_real_w, input_real_h, calc_aspect])
#         return [image_drop, input_real_w, input_real_h, calc_aspect, input_calc_w, input_calc_h, but_set_size, but_set_calc]

    
#     def ar_set_size(self, input_real_w, input_real_h):
#         print("Set size") 
#         # Возвращаем значение, которое должно быть установлено в слайдере
#         return 888, 888  # Например, если вы хотите установить оба слайдера на 888

#     def gcd(self, x, y):
#         while(y):
#             x, y = y, x % y
#         return x

#     def image_dropped(self, image):
#         if image is not None:
#             width, height = image.shape[1], image.shape[0]
#             aspect_gcd = self.gcd(width, height)
#             aspect_ratio = f"{width // aspect_gcd}:{height // aspect_gcd}"
#             print(f"Image dropped with width: {width}, height: {height}, aspect ratio: {aspect_ratio}")  # Вывод в консоль
#             return width, height, aspect_ratio
#         else:
#             return "", "", ""
        
#     def after_component(self, component, **kwargs):
#         if kwargs.get("elem_id") == "txt2img_width":
#             self.t2i_w = component
#         elif kwargs.get("elem_id") == "txt2img_height":
#             self.t2i_h = component

