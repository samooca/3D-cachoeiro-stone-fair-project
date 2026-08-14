# Contexto técnico para agentes de IA

## Problema que o projeto resolve

As referências do stand foram produzidas em ângulos diferentes e nem todas contêm o mesmo enquadramento. Geradores de imagem independentes deslocam móveis, plantas e paredes entre vistas, fazendo o Hunyuan3D reconstruir volumes incompatíveis. A solução adotada é criar uma única cena Blender e renderizar quatro câmeras ortográficas separadas por 90 graus.

## Estado atual da cena

A cena representa um stand retangular aberto, com piso e paredes em pedra clara, painel verde no fundo, mesa com seis cadeiras, balcão com oito amostras, floreira central, pendentes em V, iluminação arquitetônica e estrutura superior. O blockout é determinístico, mas não é uma reconstrução métrica certificada.

## Contrato das câmeras

| Vista | Posição relativa | Eixo observado |
| --- | --- | --- |
| Front | `-Y` | interior pela abertura frontal |
| Left | `-X` | lateral esquerda |
| Back | `+Y` | face traseira |
| Right | `+X` | lateral direita |

Todas usam projeção ortográfica, escala `6.4`, altura e alvo em `2.05 m`, resolução `2048 × 1024`. Alterar uma propriedade exige atualizar todas em conjunto e regenerar os quatro renders.

## Contrato do workflow ComfyUI

Arquivo preferencial: `3d_hunyuan3d_multiview_to_model_v2.json`.

- checkpoint: `hunyuan3d-dit-v2-mv_fp16.safetensors`
- quatro condicionamentos CLIP Vision ativos
- steps `30`, CFG `6.5`, sampler `euler`, scheduler `normal`
- latent resolution `3072`, octree resolution `256`
- voxel `surface net`, threshold `0.6`
- saída `mesh/iven_stone_stand_v2`

Ao editar o JSON, valide as referências entre nodes. Os IDs podem mudar; os contratos semânticos acima não podem desaparecer.

## Estratégia recomendada

1. Corrigir proporções e posição no script Blender.
2. Regenerar o `.blend` e as quatro vistas.
3. Comparar silhueta e oclusão com as referências.
4. Rodar o Hunyuan como proxy.
5. Importar o GLB no Blender e comparar com o blockout.
6. Para maior qualidade, reconstruir separadamente estrutura, mesa/cadeiras, balcão e vegetação.

## Limitação de oclusão

As paredes escondem o interior nas vistas traseira e laterais. Não corrija isso movendo objetos entre vistas. Se o modelo precisar enxergar o interior, crie um segundo conjunto chamado `conditioning_open_shell`, no qual apenas a visibilidade das paredes muda; mantenha as transformações intactas.

## Validação

```powershell
Get-Content -Raw '.\3d_hunyuan3d_multiview_to_model_v2.json' | ConvertFrom-Json | Out-Null

& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' `
  --background `
  '.\hunyuan_multiview_consistent\iven_stone_stand_multiview.blend' `
  --python-expr "import bpy; print(sorted(o.name for o in bpy.data.objects if o.type == 'CAMERA'))"

Get-FileHash '.\packages\addons\*.zip', '.\packages\tools\*.zip' -Algorithm SHA256
```

Critérios: quatro câmeras e PNGs, seis cadeiras, oito amostras, quatro inputs multi-view conectados, nenhuma instalação extraída rastreada e nenhum caminho pessoal na documentação.
