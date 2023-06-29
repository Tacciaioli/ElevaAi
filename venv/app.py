import nltk
import os
import PyPDF2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Definindo um dicionário de abreviações
abreviacoes = {
    'ans': 'Anti abuso de chamas de cabine',
    # adicione mais abreviações aqui
}

def importar_arquivo_pdf(pasta):
    pdf_files = [f for f in os.listdir(pasta) if f.endswith('.pdf')]

    if len(pdf_files) == 1:
        arquivo_pdf = os.path.join(pasta, pdf_files[0])
        # Aqui você pode chamar a função para importar o arquivo PDF
        atualizar_abreviacoes(arquivo_pdf)
    else:
        print("Nenhum arquivo PDF encontrado ou mais de um arquivo encontrado na pasta.")

def atualizar_abreviacoes(arquivo_pdf):
    with open(arquivo_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            lines = text.split('\n')

            for line in lines:
                line = line.strip()
                if line:
                    words = line.split()
                    if len(words) >= 2:
                        key = words[0]
                        value = ' '.join(words[1:])
                        abreviacoes[key] = value

@app.route('/expand-abbreviation', methods=['GET'])
def expand_abbreviation():
    abbreviation = request.args.get('abbreviation', '')
    abbreviation = abbreviation.lower()

    if abbreviation in abreviacoes:
        return jsonify({'abbreviation': abbreviation, 'expansion': abreviacoes[abbreviation]})
    else:
        return jsonify({'abbreviation': abbreviation, 'expansion': 'Desculpe, não reconheço essa abreviação.'})

if __name__ == '__main__':
    nltk.download('punkt')

    # Ler um arquivo PDF
    pasta_dos_pdfs = r'C:\Caminho\Para\A\Pasta\Do\PDF'
    importar_arquivo_pdf(pasta_dos_pdfs)

    app.run()
