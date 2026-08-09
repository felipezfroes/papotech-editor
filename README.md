# Papotech Editor

Ferramenta em Python criada para automatizar parte do processo de edição dos podcasts do projeto de extensão **Papotech**.

O sistema foi desenvolvido para trabalhar com gravações feitas por **dois microfones**, sincronizando os arquivos por meio de palmas realizadas no início da gravação.

## Funcionalidades

* Sincronização automática de dois arquivos de áudio
* Detecção das palmas utilizadas como referência
* Redução automática de pausas longas
* Aplicação dos mesmos cortes nos dois microfones
* Geração de um áudio de referência
* Transcrição automática com Whisper
* Identificação de possíveis repetições, gaguejos e marcadores como `"CORTA"`
* Geração de timestamps para facilitar a edição final no CapCut
* Exportação de relatórios em TXT e CSV

## Tecnologias

* Python
* FFmpeg
* Pydub
* NumPy
* SciPy
* OpenAI Whisper
* PyTorch

## Estrutura básica

```text
entrada/
├── mic1.wav
└── mic2.wav

assets/
├── abertura.mp3
└── encerramento.mp3

saida/
├── 01_MIC1_EDITADO.wav
├── 02_MIC2_EDITADO.wav
├── 03_MIX_REFERENCIA.mp3
├── transcricao.txt
└── marcacoes.txt
```

## Execução

Instale as dependências:

```bash
pip install -r requirements.txt
```

Depois coloque os arquivos dos dois microfones na pasta `entrada` e execute:

```bash
python main.py
```

O resultado será gerado automaticamente na pasta `saida`.

## Objetivo

O projeto busca reduzir o tempo gasto em tarefas repetitivas de edição de podcasts, principalmente sincronização, remoção de pausas e localização de erros de fala, deixando apenas o acabamento final para o editor de vídeo/áudio.
