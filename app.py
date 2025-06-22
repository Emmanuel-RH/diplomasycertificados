from flask import Flask, render_template, request, redirect, url_for, flash
from certificados_blockchain import CertificateBlockchain
import os

app = Flask(__name__)
app.secret_key = "blockchain_secret_key"  # Necesario para mensajes flash

blockchain = CertificateBlockchain()

# Importa la cadena desde archivo al iniciar
if os.path.exists("blockchain_certificados.json"):
    blockchain.import_from_file("blockchain_certificados.json")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/certificados')
def certificados():
    return render_template("certificados.html", chain=blockchain.chain[1:])  # Omitimos el bloque génesis

@app.route('/verificar', methods=["GET", "POST"])
def verificar():
    resultado = None
    if request.method == "POST":
        id_cert = request.form.get("id_certificado")
        block = blockchain.find_certificate(id_cert)
        if block:
            if block.certificate_data.get("anulado", False):
                resultado = ("anulado", block.certificate_data)
            else:
                resultado = ("válido", block.certificate_data)
        else:
            resultado = ("no_encontrado", None)
    return render_template("verificar.html", resultado=resultado)

@app.route('/nuevo', methods=["GET", "POST"])
def nuevo_certificado():
    if request.method == "POST":
        datos = {
            "nombre_estudiante": request.form.get("nombre_estudiante"),
            "curso": request.form.get("curso"),
            "fecha_emision": request.form.get("fecha_emision"),
            "institucion": request.form.get("institucion"),
            "id_certificado": request.form.get("id_certificado"),
            "calificacion": request.form.get("calificacion"),
            "duracion": request.form.get("duracion"),
            "email": request.form.get("email"),
        }
        # Validación simple
        if not all(datos.values()):
            flash("Por favor, completa todos los campos.", "error")
            return render_template("nuevo_certificado.html")
        # Evitar duplicados
        if blockchain.find_certificate(datos["id_certificado"]):
            flash("El ID de certificado ya existe.", "error")
            return render_template("nuevo_certificado.html")

        blockchain.add_certificate(datos)
        blockchain.export_to_file("blockchain_certificados.json")
        flash("Certificado añadido correctamente.", "success")
        return redirect(url_for("certificados"))

    return render_template("nuevo_certificado.html")

@app.route('/anular/<id_certificado>', methods=["POST"])
def anular_certificado(id_certificado):
    if blockchain.anular_certificado(id_certificado):
        blockchain.export_to_file("blockchain_certificados.json")
        flash("Certificado anulado correctamente.", "success")
    else:
        flash("No se pudo anular: certificado no encontrado o ya estaba anulado.", "error")
    return redirect(url_for("certificados"))

if __name__ == '__main__':
    app.run(debug=True)