from flask import Flask, render_template, request, make_response
from weasyprint import HTML
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Fecha automática si no se ingresa
        if not data.get('fecha_ingreso'):
            data['fecha_ingreso'] = datetime.date.today().strftime("%d/%m/%Y")
            
        # Generar PDF
        html_string = render_template('ficha_pdf.html', d=data)
        pdf = HTML(string=html_string).write_pdf()

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        filename = f"Ficha_{data.get('orden', 'General')}.pdf"
        response.headers['Content-Disposition'] = f'inline; filename={filename}'
        return response

    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')