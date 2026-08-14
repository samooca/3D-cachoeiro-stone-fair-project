# Addons e workflow do stand

## Instalados no Blender 5.2

- fSpy-Blender 1.0.3 (`fspy_blender`)
- Image Matcher 1.0.3 (`image_matcher`)
- ComfyUI-Blender 4.5.1 (`comfyui_blender`)
- Hunyuan3D-2 Generator oficial da Tencent (`hunyuan3d_official`)
- OpenCV Contrib 5.0.0.93, necessário ao Image Matcher

O aplicativo fSpy portátil está em `tools/fSpy/fSpy.exe`.

## Integração com ComfyUI

Os custom nodes do ComfyUI-Blender foram copiados para:

`C:\Users\samoo\Documentos\ComfyUI_main\custom_nodes\ComfyUI-Blender`

É necessário reiniciar o ComfyUI para carregar os novos nós.

O ComfyUI-Blender está configurado inicialmente para `http://127.0.0.1:8188` e usa a pasta do projeto `comfyui_blender_data` para workflows, entradas, saídas e temporários.

O addon oficial Hunyuan3D usa outro servidor, padrão `http://localhost:8080`. Ele não substitui o workflow nativo do ComfyUI e só funciona se o `api_server.py` oficial da Tencent estiver rodando.

## Arquivos produzidos

- `hunyuan_multiview_consistent/iven_stone_stand_multiview.blend`
- quatro imagens ortográficas com câmeras separadas por 90 graus
- `3d_hunyuan3d_multiview_to_model_v2.json`

## Convenção de câmera

- Front: câmera em -Y
- Left: câmera em -X
- Back: câmera em +Y
- Right: câmera em +X

Todas usam escala ortográfica 6.4, altura 2.05 m, alvo em 2.05 m e resolução 2048 x 1024.

## Observação técnica

O stand é uma cena arquitetônica aberta. Nas vistas traseira e laterais, as paredes ocultam fisicamente o mobiliário. Isso é coerente com uma única cena 3D, mas limita o Hunyuan3D, que foi otimizado principalmente para objetos isolados e fechados. O `.blend` é a fonte geométrica consistente; o resultado generativo deve ser tratado como proxy, não como projeto executivo.
