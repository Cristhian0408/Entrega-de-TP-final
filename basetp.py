from PyQt5.QtWidgets import QLineEdit, QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import sqlite3


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar interfaz de usuario
        uic.loadUi("basetp.ui", self)

        # Conectar a la base de datos
        self.conexion = sqlite3.connect('basetp.db')
        self.cursor = self.conexion.cursor()
        

        #Se crea una lista vacia    
        self.array_contactos = []
       
        #Se Ocultan los botones de del apartado de edicion
        self.edit_buttons.hide()

        #Se deshabilitan los line-edit
        self.datos_usuarios(False)
        
        #Se Deshabilitan los botones  exepto Nuevo  
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        
        #mostrar texto en line edit
        self.lista.itemClicked.connect(self.visualizar)
        
        #Funciones de botones
        self.nuevo.clicked.connect(self.pushnuevo)
        self.aceptar.clicked.connect(self.pushaceptar)
        self.cancelar.clicked.connect(self.pushcancelar)
        self.editar.clicked.connect(self.pusheditar)
        self.eliminar.clicked.connect(self.pusheliminar)
        
        self.edit1.clicked.connect(self.on_aceptar_en_editar) 
        self.edit2.clicked.connect(self.on_cancelar_en_editar)        
        
        #Deshabilito los botones      
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        #llamo a la funcion on_cargar para caragr mi base de datos
        self.on_cargar()
            
    def on_cargar(self):
        self.cursor.execute('select * from usuarios')
        usuarios = self.cursor.fetchall()
        
        for usuario in usuarios:
            #Muestro mi base de datos, en listawidget 
            self.lista.addItem(f'{usuario[0]} {usuario[1]}  {usuario[2]}')
            usuario = {'id':usuario[0],'nombre':usuario[1],'apellido':usuario[2],'email':usuario[3],'telefono':usuario[4],'direccion':usuario[5],'nacimiento':usuario[6],'altura':str(usuario[7]),'peso':str(usuario[8])}
            self.array_contactos.append(usuario)
            
    def datos_usuarios(self,bool):
        self.nombre.setEnabled(bool)
        self.apellido.setEnabled(bool)
        self.email.setEnabled(bool)
        self.telefono.setEnabled(bool)
        self.direccion.setEnabled(bool)
        self.fecha.setEnabled(bool)
        self.altura.setEnabled(bool)
        self.peso.setEnabled(bool)

    def clean_ledit(self):
        self.nombre.setText('')
        self.apellido.setText('')
        self.email.setText('')
        self.telefono.setText('')
        self.direccion.setText('')
        self.fecha.setText('')
        self.altura.setText('')
        self.peso.setText('')
        
    
    def pushnuevo(self):
        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.nuevo.setEnabled(False)
        self.clean_ledit()
        self.datos_usuarios(True)
        self.lista.setEnabled(False)
           
    
    def pushaceptar(self):
  
        #Agregar usuario a la base de datos
        
        if len(self.nombre.text() and self.apellido.text()) == 0:
            mensaje = QMessageBox()
            mensaje.setWindowTitle('Problem')
            mensaje.setText(f'No ingreso Nombre y Apellido')
    
            #icono
            mensaje.setIcon(QMessageBox.Warning)
            
            #Botones
            #mensaje.setStandardButtons(QMessageBox.No | QMessageBox.Yes )
            
            resultado = mensaje.exec_()
        
            if resultado == QMessageBox.Yes:
                pass
        else:
            self.cursor.execute(f"INSERT INTO USUARIOS(nombres,apellidos,email,telefono,direccion,fecha_nac,altura,peso) VALUES ('{self.nombre.text()}','{self.apellido.text()}','{self.email.text()}','{self.telefono.text()}','{self.direccion.text()}','{self.fecha.text()}','{self.altura.text()}','{self.peso.text()}')")
            self.conexion.commit()

            self.lista.addItem(f'{self.cursor.lastrowid}  {self.nombre.text()}  {self.apellido.text()} ')
            usuario = {'id':self.cursor.lastrowid,'nombre':self.nombre.text(),'apellido':self.apellido.text(),'email':self.email.text(),'telefono':self.telefono.text(), 'direccion':self.direccion.text(),'nacimiento':self.fecha.text(),'altura':self.altura.text(),'peso':self.peso.text()}
            
            self.array_contactos.append(usuario)
            
            self.nuevo.setEnabled(True)
            self.aceptar.setEnabled(False)
            self.cancelar.setEnabled(False)
            self.datos_usuarios(False)
            self.clean_ledit()
            self.lista.setEnabled(True)
        
    def pushcancelar(self):
        self.nuevo.setEnabled(True)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.datos_usuarios(False)
        self.clean_ledit()
        self.lista.setEnabled(True)
        
    def visualizar(self):

        numero = self.lista.currentRow()
        usuario = self.array_contactos[numero]
        
        self.usuarioid = self.array_contactos[numero]
        
        self.nombre.setText(usuario['nombre'])
        self.apellido.setText(usuario['apellido'])
        self.email.setText(usuario['email'])
        self.telefono.setText(usuario['telefono'])
        self.direccion.setText(usuario['direccion'])
        self.fecha.setText(usuario['nacimiento'])
        self.altura.setText(str(usuario['altura']))
        self.peso.setText(str(usuario['peso']))
        
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        
        
    def pusheditar(self):
        #Habilito los line edit
        self.datos_usuarios(True)
        self.edit_buttons.show()
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.nuevo.setEnabled(False)
        
    def on_aceptar_en_editar(self):
        
        usuario_edit = {'id':self.usuarioid['id'],'nombre':self.nombre.text(),'apellido':self.apellido.text(),'email':self.email.text(),'telefono':self.telefono.text(),
                   'direccion':self.direccion.text(),'nacimiento':self.fecha.text(),'altura':self.altura.text(),'peso':self.peso.text()}
        
        #Se reemplaza usuario en array_contacto
        numero = self.lista.currentRow()
        self.array_contactos[numero] = usuario_edit
        
        #actualizacion de  la base de datos
        usuario_id = self.usuarioid['id']
        self.cursor.execute(f"UPDATE usuarios SET nombres='{self.nombre.text()}',apellidos='{self.apellido.text()}',email='{self.email.text()}',telefono='{self.telefono.text()}',direccion='{self.direccion.text()}',fecha_nac='{self.fecha.text()}',altura='{self.altura.text()}',peso='{self.peso.text()}' WHERE id='{usuario_id}'")
        self.conexion.commit()
        
        #actualizocion de list widget
        self.lista.currentItem().setText(f'{usuario_id}  {self.nombre.text()}  {self.apellido.text()} ')
        
        self.edit_buttons.hide()
        self.datos_usuarios(False)
        self.nuevo.setEnabled(True)
        
    def on_cancelar_en_editar(self):
        self.edit_buttons.hide()
        self.datos_usuarios(False)
        self.nuevo.setEnabled(True)
        
    def pusheliminar(self):
        
        mensaje = QMessageBox()
        mensaje.setWindowTitle('Quitar Lista')
        mensaje.setText(f'Desea eliminar el contacto seleccionado?')
    
        #icono
        mensaje.setIcon(QMessageBox.Warning)
            
        #Botones
        mensaje.setStandardButtons(QMessageBox.No | QMessageBox.Yes )
            
        resultado = mensaje.exec_()
        
        if resultado == QMessageBox.Yes:
            
            self.lista.takeItem(self.lista.currentRow()) 
            self.array_contactos.remove(self.usuarioid) 
            
            #Borro de la base de datos
            usuario_id = self.usuarioid['id']
            self.cursor.execute(f"DELETE FROM usuarios WHERE id='{usuario_id}'")
            self.conexion.commit()  
             
    #def closeEvent(self, event):
        #self.conexion.close()


app = QApplication([])

win = MiVentana()
win.show()

app.exec_()