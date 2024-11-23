
![Descripción de la imagen](Imagenes/7_Unlz_logo.jpg)


<h1 align="center">Análisis de fallas en placas electrónicas</h1>


# Detalle del trabajo realizado

El trabajo que realicé es un dispositivo mecatrónico que inspecciona placas electrónicas mediante una cámara y un robot, para luego informar las fallas detectadas. Está pensado para recibir placas electrónicas al final de una línea de producción y verificar que las mismas cuenten con las necesidades mínimas para ser aprobadas, controlando tanto los diferentes elementos electrónicos como los errores de soldadura mediante una cámara y realizando mediciones sobre la placa a través de un robot SCARA. El resultado de estos tres análisis es el que corroborará si placa está o no en condiciones para pasar dicho control de calidad. Todo esto será controlado a través de una interfaz gráfica desarrollada en Python, donde también se podrá observar en tiempo real las diferentes detecciones y mediciones realizadas sobre la placa. 

# Elementos Móviles
El prototipo está formado por tres elementos móviles, y si bien todos se controlan mediante placas electrónicas tipo Arduino estos elementos están integrados mediante un programa de Python para que coordinen sus movimientos y analicen las diferentes placas. Estos elementos son: un robot de tipo SCARA, la base porta placa y un elevador.
# Robot SCARA
El robot SCARA diseñado íntegramente en SOLIDWORKS e impreso con impresora 3D, es de tres grados de libertad (dos giros y un desplazamiento lineal). Este será el encardo de realizar los movimientos necesarios para posicionarse en los puntos de testeo de las placas, y gracias a su efector (puntas de medición) tomará las mediciones correspondientes. Medirá continuidad entre los puntos de testeo de la placa, y se tomarán como válidas las placas que presenten continuidad sobre esos puntos. 
Dicho robot está formado por tres mecanismos móviles (la base, el brazo, regulación de altura) y cada uno cuenta con un motor paso a paso nema 17 que es el encargado de darle el movimiento a cada mecanismo. La base es giratoria y está formada por dos rodamientos axiales de 60mm de diámetro exterior, los cuales acoplan mediante tornillos y tuercas a una polea dentada de 60 dientes, dicha polea acopla a otra polea de 20 dientes a 150mm de distancia ubicada en el eje del motor mediante una correa dentada gt2 de 400mm. De esta base salen tres varillas lisas de 6mm de diámetro y también una varilla roscada de 8mm de diámetro, es en estas varillas donde se acopla el mecanismo del brazo, el cual contiene al brazo 1, al brazo 2 y al efector, este último se encuentra al final del brazo 2. Dicho mecanismo está acoplado a las varillas lisas mediante rodamientos lineales de 6mm de diámetro y a la varilla roscada mediante una tuerca, por lo tanto, este mecanismo gira en concordancia con la base ya que está montado sobre ella. Y como también esta acoplado al mecanismo de regulación de altura cuando la varilla roscada gira, hace que este mecanismo se eleve o baje. El acople entre el motor nema 17 y el brazo 2 es exactamente igual al de la base. En el caso del mecanismo de regulación de altura, el eje del motor está directamente acoplado, mediante un acople flexible a dicha varilla roscada, esta es de 8 mm por vuelta, por lo tanto, cuando este motor gira una vuelta hace que el mecanismo del brazo se eleve o baje 8mm.
Para controlar el robot SCARA se diseñó una placa electrónica mediante el software PROTEUS, luego ese diseño fue impreso en una hoja transfer para transferir las pistas a la placa de cobre y posteriormente se utilizó cloruro férrico para eliminar el cobre y obtener el diseño útil sobre la placa. A dicha placa se le acoplo una esp32, 3 drivers A4988, y borneras para utilizar los pines como entradas o salidas de la esp32. 
La esp32 es la encargada de controlar el robot SCARA, esta contiene el código desarrollado en el Arduino IDE, y es capaz de realizar todos los cálculos de la cinemática inversa para que los motores giren la cantidad de grados necesarios y se posicionen en las ubicaciones correctas realizando todos los movimientos al mismo tiempo. Ejecuta la rutina de Home antes de cada movimiento de medición en la placa. Realiza las mediciones de continuidad en dicha placa, gracias al efector del robot. Y también sensa los finales de carrera presentes en el robot para evitar colisiones.



<table>
  <tr>
    <td style="text-align: center;">
      <img src="Imagenes/1_Scara_proyecto.jpg" alt="Descripción de la imagen 1" width="500">
      <p style="text-align: center;"><em>Robot SCARA</em></p>
    </td>
    <td style="text-align: center;">
      <img src="Imagenes/2_PCB_proyecto.png" alt="Descripción de la imagen 2" width="500">
      <p style="text-align: center;"><em>Controlador Robot SCARA</em></p>
    </td>
  </tr>
</table>

<table>
  <tr>
    <td style="text-align: center;">
      <div style="text-align: center;">
        <img src="Imagenes/1_Scara_proyecto.jpg" alt="Descripción de la imagen 1" width="200">
        <p><em>Robot SCARA</em></p>
      </div>
    </td>
    <td style="text-align: center;">
      <div style="text-align: center;">
        <img src="Imagenes/2_PCB_proyecto.png" alt="Descripción de la imagen 2" width="200">
        <p><em>Controlador Robot SCARA</em></p>
      </div>
    </td>
  </tr>
</table>

