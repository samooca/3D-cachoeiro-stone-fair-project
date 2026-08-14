# 3D Cachoeiro Stone Fair Project

Pipeline reproduzível para reconstrução e prototipagem 3D do stand da Iven Stone a partir de imagens de referência. O projeto combina um blockout determinístico no Blender, quatro câmeras ortográficas consistentes e um workflow multi-view do Hunyuan3D executado no ComfyUI.

> O arquivo Blender é a fonte geométrica principal. A malha gerada por IA deve ser tratada como proxy visual, não como projeto executivo ou base para fabricação.

## Conteúdo do repositório

| Caminho | Finalidade |
| --- | --- |
| `hunyuan_multiview_consistent/iven_stone_stand_multiview.blend` | Cena Blender com geometria e câmeras consistentes |
| `hunyuan_multiview_consistent/*_image.png` | Vistas front, left, back e right para o Hunyuan3D |
| `3d_hunyuan3d_multiview_to_model_v2.json` | Workflow ComfyUI recomendado |
| `create_stand_blockout.py` | Geração reproduzível do blockout e dos renders |
| `packages/addons/*.zip` | Add-ons do Blender, somente em formato ZIP |
| `packages/tools/*.zip` | Ferramentas auxiliares, somente em formato ZIP |
| `AGENTS.md` e `docs/AI_CONTEXT.md` | Contexto operacional para agentes e outros modelos de IA |

## Requisitos

- Blender 5.2 LTS ou compatível
- ComfyUI atualizado
- checkpoint `hunyuan3d-dit-v2-mv_fp16.safetensors`
- nodes ativos para Hunyuan3D 2 multi-view e exportação GLB
- GPU com VRAM suficiente para latent 3072 e octree 256

Consulte [ADDONS_E_WORKFLOW.md](ADDONS_E_WORKFLOW.md) para versões, instalação e integração.

## Uso rápido

1. Instale no Blender os ZIPs de `packages/addons/` em **Edit > Preferences > Add-ons > Install from Disk**.
2. Extraia `packages/tools/fSpy-1.0.3-win.zip` fora do repositório e execute o fSpy quando precisar calibrar perspectiva.
3. Abra `hunyuan_multiview_consistent/iven_stone_stand_multiview.blend`.
4. Se precisar reconstruir a cena, execute `create_stand_blockout.py` no Blender em modo background ou pelo editor de scripts.
5. Copie as quatro imagens `*_image.png` para a pasta `input` do ComfyUI.
6. Importe `3d_hunyuan3d_multiview_to_model_v2.json` e confirme os quatro inputs antes de executar.

Exemplo para recriar a cena no Windows:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' `
  --background `
  --python '.\create_stand_blockout.py'
```

## Convenção das vistas

- `front`: câmera em `-Y`
- `left`: câmera em `-X`
- `back`: câmera em `+Y`
- `right`: câmera em `+X`
- escala ortográfica: `6.4`
- resolução: `2048 × 1024`

As quatro imagens precisam vir da mesma cena e manter exatamente as mesmas transformações dos objetos. Não gere cada vista de forma independente com image-to-image.

## Limitação conhecida

O stand é uma cena arquitetônica aberta. Nas vistas laterais e traseira, as paredes ocultam fisicamente parte do mobiliário. Isso preserva coerência geométrica, mas não é o caso ideal para um gerador treinado principalmente com objetos isolados e fechados. Para melhores resultados, processe separadamente arquitetura, mobiliário e vegetação ou oculte paredes apenas para um conjunto auxiliar de condicionamento.

## Segurança e publicação

O repositório é público. Não inclua tokens, cookies, arquivos de preferências, caminhos pessoais, modelos/checkpoints, outputs temporários ou instalações descompactadas. Add-ons e ferramentas devem permanecer somente como ZIPs em `packages/`.

## Fontes dos componentes

- [fSpy](https://github.com/stuffmatic/fspy)
- [fSpy-Blender](https://github.com/stuffmatic/fSpy-Blender)
- [K-Meech Image Matcher](https://github.com/K-Meech/image-matcher)
- [ComfyUI-Blender](https://github.com/alexisrolland/ComfyUI-Blender)
- [Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)

Cada componente mantém sua própria licença. Verifique as licenças upstream antes de redistribuir ou usar comercialmente os pacotes incluídos.
