from sqlite3 import Cursor
from PyQt5 import uic, QtWidgets
import mysql.connector

from reportlab.pdfgen import canvas


banco = mysql.connector.connect(
    host ="localhost",
    user ="root",
    password ="",
    database = "agenda"
)


app=QtWidgets.QApplication([])
agenda=uic.loadUi("agenda.ui")
listaContatos = uic.loadUi("listaContatos.ui")

#---------------------------------------------------Cadastrar----------------------------------------------------------------

def cadastrarContato():
    campoNome = agenda.leNome.text()
    campoEmail = agenda.leEmail.text()
    campoTelefone = agenda.leTelefone.text()

    if agenda.rbResidencial.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.rbCelular.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Nâo informado"

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO contato (nome , email , telefone , tipoTelefone) VALUES (%s,%s,%s,%s)"
    dados = (str(campoNome),str(campoEmail),str(campoTelefone),tipoTelefone)
    cursor.execute(comando_SQL,dados)
    banco.commit()

agenda.btnCadastro.clicked.connect(cadastrarContato)

#---------------------------------------------------CONSULTAR----------------------------------------------------------------

def consultarContatos():
    listaContatos.show()

    cursor = banco.cursor()
    comando_SQL2 = "SELECT * FROM contato"
    cursor.execute(comando_SQL2)
    contatosLidos = cursor.fetchall()

    listaContatos.tabelaContatos.setRowCount(len(contatosLidos))
    listaContatos.tabelaContatos.setColumnCount(5)

    for i in range (0,len(contatosLidos)):
        for f in range(0,5):
            listaContatos.tabelaContatos.setItem(i,f,QtWidgets.QTableWidgetItem(str(contatosLidos[i][f])))

agenda.btnConsulta.clicked.connect(consultarContatos)

#---------------------------------------------------Excluir-----------------------------------------------------------------------

def excluirContato():
    linhaContatos = listaContatos.tabelaContatos.currentRow()
    listaContatos.tabelaContatos.removeRow(linhaContatos)

    cursor = banco.cursor()
    comando_SQL3 = "SELECT id FROM contato"
    cursor.execute(comando_SQL3)
    contatos_lidos = cursor.fetchall()
    valorId = contatos_lidos[linhaContatos][0]
    cursor.execute("DELETE FROM contato WHERE id=" + str(valorId))
    banco.commit()

listaContatos.btnExcluir.clicked.connect(excluirContato)

#----------------------------------------------------Atualizar---------------------------------------------------------------------

def atualizarContato():
    cursor = banco.cursor()

    for i in range(listaContatos.tabelaContato.rowCount()):
        id = listaContatos.tabelaContato.item(i,0).text()
        campoNome = listaContatos.tabelaContato.item(i,1).text()
        campoEmail = listaContatos.tabelaContato.item(i,2).text()
        campoTelefone = listaContatos.tabelaContato.item(i,3).text()
        tipoTelefone = listaContatos.tabelaContato.item(i,4).text()

    comando_SQL4 = "UPDATE contato SET nome = %s, email = %s, telefone = %s, tipoTelefone = %s WHERE id = " + str(id)
    dados = (str(campoNome),str(campoEmail),str(campoTelefone),str(tipoTelefone))
    cursor.execute(comando_SQL4,dados)
    banco.commit()


listaContatos.btnAtualizar.clicked.connect(atualizarContato)

#----------------------------------------------------Gerar PDF---------------------------------------------------------------------

def gerarPDF():
    cursor = banco.cursor()
    comando_SQL6 = "SELECT * FROM contato"
    cursor.execute(comando_SQL6)
    contatos_lidos = cursor.fetchall()

    y=0
    pdf = canvas.Canvas("lista_contatos.pdf")
    pdf.setFont("Times-Bold",25)
    pdf.drawString(200,800,"Lista de contatos")

    pdf.setFont("Times-Bold",18)
    pdf.drawString(10,750,"ID")
    pdf.drawString(110,750,"NOME")
    pdf.drawString(210,750,"EMAIL")
    pdf.drawString(410,750,"TELEFONE")
    pdf.drawString(510,750,"TIPO DE CONTATO")

    for i in range(0, len(contatos_lidos)):
        y = y + 50

        pdf.drawString(10, 750 - y, str(contatos_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(contatos_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(contatos_lidos[i][2]))
        pdf.drawString(410, 750 - y, str(contatos_lidos[i][3]))
        pdf.drawString(510, 750 - y, str(contatos_lidos[i][4]))

    pdf.save()
    print("pdf gerado com sucesso!")


listaContatos.btnPdf.clicked.connect(gerarPDF)


agenda.show()
app.exec()
