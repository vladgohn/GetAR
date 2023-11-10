import gradio as gr
import modules.scripts as scripts
from modules import script_callbacks

class GetAR(scripts.Script):
    txt2img_w_slider = None
    txt2img_h_slider = None

    def __init__(self):
        pass

    def on_image_clear(self):
        return None, None, ""
    
    def title(self):
        return "Adjust Width"

    def show(self, is_img2img):
        return scripts.AlwaysVisible 
    def ui(self, is_img2img):
        with gr.Accordion(label="GetAR", open=True):
            with gr.Row(elem_id="txt2img_get_ar"):
                with gr.Column():
                    image_drop = gr.Image(label="Drop", width=200, height=200, elem_id="getar_image_drop")
                with gr.Column():
                    with gr.Row():
                        input_real_w = gr.Number(label="Real Width", value=None, elem_id="ar_input_real_w",  style={'width': 'auto'})
                        input_real_h = gr.Number(label="Real Height", value=None, elem_id="ar_input_real_h", style={'width': 'auto'})
                    with gr.Row():
                        calc_aspect = gr.Text(label="Aspect Ratio", value="", elem_id="ar_calc_aspect",  style={'width': 'auto'})
                    with gr.Row():
                        input_calc_w = gr.Number(label="Calc Width", value=None, elem_id="input_calc_w", style={'width': 'auto'})
                        input_calc_h = gr.Number(label="Calc Height", value=None, elem_id="input_calc_h", style={'width': 'auto'})
                    with gr.Row():
                        but_set_size = gr.Button("Set Size", css_class="my-button", elem_id="but_set_size")
                        but_set_calc = gr.Button("Set Сalc", css_class="my-button", elem_id="but_set_calc")

        but_set_size.click(
            self.ar_set_size,
            inputs=[input_real_w, input_real_h],  # Теперь мы передаем два значения
            outputs=[self.txt2img_w_slider, self.txt2img_h_slider]  # И обновляем два слайдера
        )
        
        but_set_calc.click(
            self.ar_set_size,  # Используем ту же функцию ar_set_size
            inputs=[input_calc_w, input_calc_h],  # Передаем значения из input_calc_w и input_calc_h
            outputs=[self.txt2img_w_slider, self.txt2img_h_slider]
        )

        image_drop.clear(self.on_image_clear, inputs=[], outputs=[input_real_w, input_real_h, calc_aspect])

        image_drop.change(self.image_dropped, inputs=[image_drop], outputs=[input_real_w, input_real_h, calc_aspect])
        return [image_drop, input_real_w, input_real_h, calc_aspect, input_calc_w, input_calc_h, but_set_size]

    def ar_set_size(self, real_width, real_height):
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
            return None, None, None

    @staticmethod
    def on_after_component(component, **_kwargs):
        elem_id = getattr(component, "elem_id", None)
        if elem_id == "txt2img_width":
            GetAR.txt2img_w_slider = component
        elif elem_id == "txt2img_height":
            GetAR.txt2img_h_slider = component
script_callbacks.on_after_component(GetAR.on_after_component)
