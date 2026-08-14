# AGENTS.md

## Objetivo

Este repositório produz vistas multi-view geometricamente consistentes de um stand da Iven Stone e as utiliza no Hunyuan3D 2 dentro do ComfyUI. Agentes devem priorizar reprodutibilidade, consistência espacial e segurança para repositório público.

## Leia primeiro

1. `README.md`
2. `docs/AI_CONTEXT.md`
3. `ADDONS_E_WORKFLOW.md`
4. `create_stand_blockout.py`
5. `3d_hunyuan3d_multiview_to_model_v2.json`

## Fontes de verdade

- Geometria, objetos e câmeras: `create_stand_blockout.py` e o `.blend` gerado.
- Entradas do Hunyuan3D: quatro PNGs em `hunyuan_multiview_consistent/`.
- Workflow recomendado: `3d_hunyuan3d_multiview_to_model_v2.json`.
- Imagens originais: `ref1.png`, `ref2.png`, `stand_1.jpeg`, `stand_3.jpeg` e a referência superior.

## Regras obrigatórias

- Nunca gere as quatro vistas separadamente com IA; renderize-as da mesma cena Blender.
- Preserve as posições dos objetos entre `front`, `left`, `back` e `right`.
- Não substitua referências originais sem solicitação explícita.
- Não trate a malha Hunyuan como projeto executivo ou dimensionalmente preciso.
- Não versione checkpoints, modelos, caches, ambientes Python, preferências do Blender ou outputs temporários.
- Não versione add-ons ou ferramentas descompactados. Somente ZIPs dentro de `packages/addons/` e `packages/tools/`.
- Antes de commit, execute as validações descritas em `docs/AI_CONTEXT.md` e revise `git diff --cached`.
- O repositório é público: não grave tokens, credenciais, cookies, nomes de usuário locais ou caminhos absolutos pessoais.

## Alterações esperadas

- Ajustes geométricos devem ser feitos preferencialmente em `create_stand_blockout.py` e depois regenerados no `.blend`.
- Alterações no workflow devem preservar os quatro inputs ativos e produzir um novo prefixo de saída quando mudarem parâmetros relevantes.
- Documente versões de add-ons e hashes dos pacotes em `packages/SHA256SUMS.txt`.

## Validação mínima

- O JSON deve ser válido e conter `front`, `left`, `back` e `right`.
- O `.blend` deve abrir no Blender sem erro fatal.
- Devem existir exatamente quatro renders finais com nomes compatíveis com o workflow.
- Nenhum arquivo individual deve exceder o limite do GitHub.
- `git status --short` não deve mostrar conteúdo extraído de `addons/` ou `tools/`.
