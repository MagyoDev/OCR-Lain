# OCR-Lain

OCR-Lain é uma ferramenta de linha de comando para extrair texto de imagens e documentos utilizando OCR.

A ferramenta processa arquivos locais, aplica extração de texto nativa quando possível e utiliza OCR quando o conteúdo está em formato visual, como imagens, páginas escaneadas ou imagens incorporadas em documentos.

---

## Sumário

* [Formatos suportados](#formatos-suportados)
* [Requisitos](#requisitos)
* [Instalação do Tesseract OCR](#instalação-do-tesseract-ocr)
* [Instalação do projeto](#instalação-do-projeto)
* [Verificando a instalação](#verificando-a-instalação)
* [Uso básico](#uso-básico)
* [Exemplos de uso](#exemplos-de-uso)
* [Saída dos arquivos](#saída-dos-arquivos)
* [Opções disponíveis](#opções-disponíveis)
* [Modo explícito](#modo-explícito)
* [Exemplos avançados](#exemplos-avançados)
* [Estrutura de saída](#estrutura-de-saída)
* [Problemas comuns](#problemas-comuns)
* [Comandos principais](#comandos-principais)
* [Licença](#licença)

---

## Formatos suportados

| Formato                          | Suporte                                                         |
| -------------------------------- | --------------------------------------------------------------- |
| `.png`, `.jpg`, `.jpeg`          | OCR de imagem                                                   |
| `.webp`, `.bmp`, `.tiff`, `.tif` | OCR de imagem                                                   |
| `.pdf`                           | Extração de texto nativo e OCR em páginas escaneadas            |
| `.docx`                          | Extração de parágrafos, tabelas e OCR de imagens internas       |
| `.pptx`                          | Extração de texto dos slides, tabelas e OCR de imagens internas |

---

## Requisitos

Antes de instalar o projeto, certifique-se de possuir:

* Python 3.10 ou superior
* Tesseract OCR instalado no sistema
* Git, caso queira clonar o repositório

---

## Instalação do Tesseract OCR

O OCR-Lain utiliza o Tesseract como mecanismo de OCR. Por isso, além das dependências Python, é necessário instalar o Tesseract no sistema operacional.

### Windows

Após instalar o Tesseract, verifique se o comando está disponível no terminal:

```powershell
tesseract --version
```

Caso o comando não seja reconhecido, adicione o diretório de instalação do Tesseract ao PATH do Windows.

O caminho padrão costuma ser:

```text
C:\Program Files\Tesseract-OCR
```

Para verificar os idiomas disponíveis:

```powershell
tesseract --list-langs
```

Para utilizar OCR em português, o idioma `por` precisa aparecer na lista:

```text
eng
osd
por
```

---

## Instalação do projeto

Clone o repositório:

```bash
git clone https://github.com/MagyoDev/OCR-Lain.git
cd OCR-Lain
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação do ambiente virtual, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Depois tente ativar novamente:

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

---

## Verificando a instalação

Exibir a versão instalada:

```bash
ocr-lain version
```

Listar os formatos suportados:

```bash
ocr-lain formats
```

---

## Uso básico

Processar um arquivo:

```bash
ocr-lain caminho/do/arquivo
```

Exemplo no Windows:

```powershell
ocr-lain .\samples\documento.pdf
```

Por padrão, os resultados são salvos na pasta:

```text
outputs/
```

---

## Exemplos de uso

### Processar uma imagem

```powershell
ocr-lain .\samples\imagem.png
```

### Processar um PDF

```powershell
ocr-lain .\samples\documento.pdf
```

### Processar um documento Word

```powershell
ocr-lain .\samples\documento.docx
```

### Processar uma apresentação PowerPoint

```powershell
ocr-lain .\samples\apresentacao.pptx
```

### Processar uma pasta inteira

```powershell
ocr-lain .\samples
```

Ao receber uma pasta, o OCR-Lain procura automaticamente por arquivos suportados.

---

## Saída dos arquivos

Por padrão, o OCR-Lain gera uma saída em Markdown:

```text
outputs/documento.pdf.ocr.md
```

Também é possível gerar uma saída adicional em JSON:

```powershell
ocr-lain .\samples\documento.pdf --json
```

Nesse caso, serão gerados arquivos como:

```text
outputs/documento.pdf.ocr.md
outputs/documento.pdf.ocr.json
```

---

## Opções disponíveis

### Definir pasta de saída

Use `-o` ou `--output`:

```powershell
ocr-lain .\samples\documento.pdf -o resultados
```

Ou:

```powershell
ocr-lain .\samples\documento.pdf --output resultados
```

---

### Exportar em JSON

```powershell
ocr-lain .\samples\documento.pdf --json
```

---

### Alterar idioma do OCR

Português e inglês:

```powershell
ocr-lain .\samples\imagem.png --lang por+eng
```

Somente português:

```powershell
ocr-lain .\samples\imagem.png --lang por
```

Somente inglês:

```powershell
ocr-lain .\samples\imagem.png --lang eng
```

---

### Alterar DPI para PDFs

O parâmetro `--dpi` controla a qualidade usada ao transformar páginas de PDF em imagem para OCR.

```powershell
ocr-lain .\samples\documento.pdf --dpi 300
```

Valores maiores podem melhorar o OCR em PDFs escaneados, mas também aumentam o tempo de processamento.

---

### Desativar OCR em PDFs

Caso o PDF já possua texto selecionável, é possível evitar OCR nas páginas:

```powershell
ocr-lain .\samples\documento.pdf --no-pdf-ocr
```

---

### Desativar OCR em imagens internas

Para arquivos `.docx` e `.pptx`, é possível desativar o OCR em imagens internas:

```powershell
ocr-lain .\samples\documento.docx --no-embedded-images
```

```powershell
ocr-lain .\samples\apresentacao.pptx --no-embedded-images
```

---

## Modo explícito

Além do modo simples:

```powershell
ocr-lain .\samples\documento.pdf
```

Também é possível utilizar o comando explícito `run`:

```powershell
ocr-lain run .\samples\documento.pdf
```

Os dois comandos executam o mesmo processamento.

---

## Exemplos avançados

### PDF com saída em Markdown e JSON

```powershell
ocr-lain .\samples\apostila.pdf --json
```

### PDF escaneado com DPI maior

```powershell
ocr-lain .\samples\scan.pdf --dpi 300 --json
```

### PowerPoint sem OCR nas imagens internas

```powershell
ocr-lain .\samples\aula.pptx --no-embedded-images
```

### Pasta inteira com exportação em JSON

```powershell
ocr-lain .\samples --json
```

### Definir pasta de saída personalizada

```powershell
ocr-lain .\samples\documento.pdf -o resultados --json
```

---

## Estrutura de saída

Exemplo de arquivo Markdown gerado:

```text
outputs/documento.pdf.ocr.md
```

Exemplo de arquivo JSON gerado:

```text
outputs/documento.pdf.ocr.json
```

O Markdown é indicado para leitura humana.

O JSON é indicado para automações, integrações, APIs ou uso futuro em pipelines de IA.

---

## Problemas comuns

### `ModuleNotFoundError: No module named 'docx'`

Execute novamente a instalação das dependências:

```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
```

---

### `ModuleNotFoundError: No module named 'pptx'`

Execute novamente a instalação das dependências:

```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
```

---

### `tesseract is not installed or it's not in your PATH`

Verifique se o Tesseract está instalado:

```powershell
tesseract --version
```

Se o comando não funcionar, adicione o diretório do Tesseract ao PATH do sistema.

---

### O idioma português não aparece

Verifique os idiomas instalados:

```powershell
tesseract --list-langs
```

Caso `por` não apareça, instale o pacote de idioma português do Tesseract.

---

## Comandos principais

```bash
ocr-lain version
```

```bash
ocr-lain formats
```

```bash
ocr-lain arquivo.pdf
```

```bash
ocr-lain arquivo.pdf --json
```

```bash
ocr-lain pasta/ --json
```

```bash
ocr-lain arquivo.pdf -o resultados
```

---

## Licença

Este projeto está licenciado sob a licença MIT.
