#include <cmath>
char input;
int sum_angulos = 1;
float cont1 = 0.0;
float cont2 = 0.0;
float cont3 = 0.0;
float X;
float Y;
float Z;
float x;
float y;
float Zpaso;
int val_menu;
int m;
String mensaje1 = "Coordenada X: ";
String mensaje2 = "Coordenada Y: ";
String mensajez = "Coordenada Z: ";
String mensaje3 = "Coordenada X Ingresada: ";
String mensaje4 = "Coordenada Y Ingresada: ";
String mensajez_ing = "Coordenada Z Ingresada: ";
String mensaje5 = "Menu: ";
String mensaje6 = "1_Cinematica inversa: ";
String mensaje7 = "2_HOME: ";
const int led = 13;
const int L1 = 160;
const int L2 = 106;
float tita2R;
float tita2G;
float tita1R;
float tita1G;
float tita1G_a_pasos;
float tita2G_a_pasos;
float tita1G_actual;
float tita1pasos_anterior = 0;
float tita2G_actual;
float tita2pasos_anterior = 0;
float z_pasos_anterior = 0;
float z_actual;
int C = 0;
float temp = 2;
float temp_base;
float temp_brazo;
float temp_varilla;
float cont_base = 0.0;
float cont_brazo = 0.0;
float cont_varilla = 0.0;
float paso_max;
float rel_base;
float rel_brazo;
float rel_varilla;
float cont_prueba = 0.0;
long ti;
long par1T2;
long par2T2;
float par3T2;
float par4T2;
float par1T1;
float par2T1;
float par4T22;
float angeje1;
int movehome = 0;
int cine = 0;
//Finales de carrera
#define fcb1 34
volatile bool homeb1 = false;
#define fcb2 26
volatile bool homeb2 = false;
#define fc_brazo_1 27  //35
#define fc_brazo_2 32
volatile bool pararmotorbrazo35 = false;
volatile bool pararmotorbrazo32 = false;
#define fc_zsuperior 33
#define fc_zinferior 25
volatile bool pararmotorz_sup = false;
volatile bool pararmotorz_inf = false;
//Puntas
#define puntas 14
int estadopuntas = 0;

//Declaracion de motores
// Motor 1
#define step 2
#define dir 15
#define temp 2
#define EN 0
// Motor 2 Brazo 2
#define step_2 18
#define dir_2 5
#define EN_2 19
// Motor 3 Base
#define step_3 16
#define dir_3 4
#define EN_3 17
// Motor 4
#define step_4 22
#define dir_4 23
#define EN_4 21
void angulos(float x, float y, float Z) {
  do {
    if (isnan(tita1G) || isnan(tita2G)) {
      Serial.println("Posicion X o Y fuera del alcance");
      Serial.println("");
      Serial.println("Vuelva a ingreasar las coordenadas ");
    }
    //Serial.println(mensaje1);
    //while(Serial.available()==0){

    //}
    //x=Serial.parseInt();
    //limpiarBufferSerial();
    //Serial.print(mensaje3);
    //Serial.println(x);

    Serial.println(mensaje2);
    //while(Serial.available()==0){

    //}
    //y=Serial.parseInt();
    //limpiarBufferSerial();
    //Serial.print(mensaje4);
    //Serial.println(y);
    do {
      if (Z > 102) {
        Serial.println("Coordenada Z fuera de rango ");
        Serial.println(" ");
        Serial.println("Ingresela nuevamente");
      }
      if (Z < 0) {
        Serial.println("Ingrese un valor positivo de Z ");
        Serial.println(" ");
        Serial.println("Ingreselo nuevamente");
      }
      //Serial.println(mensajez);
      //while(Serial.available()==0){

      //}
      //Z=Serial.parseInt();
      //limpiarBufferSerial();
      //Serial.print(mensajez_ing);
      //Serial.println(Z);

      z_actual = Z * (1600 / 8);  //1600 porque esta configurado con micropasos 1/8, 8 porque son 8mm por vuelta de la varilla roscada
      Zpaso = z_actual - z_pasos_anterior;
      if (Zpaso < 0) {
        Zpaso = -1 * Zpaso;
        digitalWrite(dir_4, LOW);  //Low baja
      }
      //Serial.println("Cantidad de pasos Varilla: ");
      //Serial.println(Zpaso);
    } while (Z > 102);  // si Z es mayor a 150mm o negativo hay que ingresarlo nuevamente
    tita2R = acos((pow(x, 2) + pow(y, 2) - pow(L1, 2) - pow(L2, 2)) / ((long)2 * L1 * L2));
    tita2G = tita2R * (180 / 3.1416);  //paso de radianes a grados
    tita1R = atan(x / y) - (atan((L2 * sin(tita2R)) / (L1 + (L2 * cos(tita2R)))));
    tita1G = tita1R * (180 / 3.1416);

  } while (isnan(tita1G) || isnan(tita2G));
  movehome = 1;
  /*tita2R=acos((pow(x,2)+pow(y,2)-pow(L1,2)-pow(L2,2))/((long)2*L1*L2));
  tita2G=tita2R*(180/3.1416);
  tita1R=atan(x/y)-(atan((L2*sin(tita2R))/(L1+(L2*cos(tita2R)))));
  tita1G=tita1R*(180/3.1416);*/
  //return(tita2G,tita1G);
  //Primer cuadrante
  if (x >= 0 && y >= 0) {
    Serial.println("Ambos numeros son positivos, primer cuadrante");
    tita1G = 90 - tita1G;
    C = 1;
  }
  //Segundo cuadrante
  if (x < 0 && y >= 0) {
    Serial.println("X negativo, Y positivo, segundo cuadrante");
    tita1G = 90 - tita1G;
    C = 2;
  }
  //Tercer cuadrante
  if (x <= 0 && y < 0) {
    Serial.println("Ambos numeros son negativos, tercer cuadrante");
    tita1G = 270 - tita1G;
    C = 3;
  }
  //Cuarto cuadrante
  if (x > 0 && y < 0) {
    Serial.println("X positivo, Y negativo, Cuarto cuadrante");
    tita1G = -90 - tita1G;
    C = 4;
  }
  /* MODIFICACION POSICIONAMIENTO SOBRE EJES
  if (x >= 0 && y > 0) {
        Serial.println("Ambos numeros son positivos, primer cuadrante");
        tita1G=90-tita1G;
        C=1;
      }
  //Segundo cuadrante
  if (x < 0 && y > 0) {
        Serial.println("X negativo, Y positivo, segundo cuadrante");
        tita1G=90-tita1G;
        C=2;
      }
  //Tercer cuadrante
  if (x < 0 && y < 0) {
        Serial.println("Ambos numeros son negativos, tercer cuadrante");
        tita1G=270-tita1G;
        C=3;
      }
    //Cuarto cuadrante
  if (x > 0 && y < 0) {
        Serial.println("X positivo, Y negativo, Cuarto cuadrante");
        tita1G=-90-tita1G;
        C=4;
      }*/
}
void limpiarBufferSerial() {
  while (Serial.available() > 0) {
    char c = Serial.read();  // Lee y descarta los caracteres restantes.
  }
}
void girar(float paso_max, float tita1G_a_pasos, float tita2G_a_pasos, float Zpaso, float temp_base, float temp_brazo, float temp_varilla) {
  cont_base = 0.0;
  cont_brazo = 0.0;
  cont_varilla = 0.0;
  float ratio_base = (float)tita1G_a_pasos / paso_max;
  float ratio_brazo = (float)tita2G_a_pasos / paso_max;
  float ratio_varilla = (float)Zpaso / paso_max;
  cont_prueba = 0.0;
  int cont_prueba2 = 0;
  while (cont_base < tita1G_a_pasos || cont_brazo < tita2G_a_pasos || cont_varilla < Zpaso) {
    //if (pararmotorbase){
    //digitalWrite(EN_3, HIGH);
    //Serial.println("Final de carrera de la base activado");
    //digitalWrite(EN_3, LOW);
    //}
    if (pararmotorbrazo35 || pararmotorbrazo32) {
      digitalWrite(EN_2, HIGH);
    }
    if (pararmotorz_sup || pararmotorz_inf) {
      digitalWrite(EN_4, HIGH);
    }
    cont_prueba++;
    if (((cont_base < tita1G_a_pasos) && (cont_base / cont_prueba < ratio_base)) || paso_max / tita1G_a_pasos == 1.0) {  //((cont_base / (float) tita1G_a_pasos) < ratio_base * cont_varilla)) {
      digitalWrite(step_3, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_3, LOW);
      cont_base++;
    }

    if (((cont_brazo < tita2G_a_pasos) && (cont_brazo / cont_prueba < ratio_brazo)) || paso_max / tita2G_a_pasos == 1.0) {  //((cont_brazo / (float) tita2G_a_pasos) < ratio_brazo * cont_varilla)) {
      digitalWrite(step_2, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_2, LOW);
      cont_brazo++;
    }

    if (((cont_varilla < Zpaso) && (cont_varilla / cont_prueba < ratio_varilla)) || paso_max / Zpaso == 1.0) {
      digitalWrite(step_4, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_4, LOW);
      cont_varilla++;
    } /* Pruebo si el motor 2 termina al mismo momento que los demas motores, (-262,9,30)
    if(cont_brazo==560){
      cont_prueba2++;
      //Serial.println("Motor brazo termino 2222222: ");
      //cont_brazo=0.0;
    }
    if(cont_prueba2==1){
      cont_prueba2++;
      Serial.println("Motor brazo termino 2222222: ");
      //cont_brazo=0.0;
    }*/

    // Ajustar pausas para sincronizar
    delayMicroseconds(500);  // Puedes ajustar este valor para sincronizar más finamente
  }
}
/*void gira_base(float tita1G_a_pasos,float temp_base){////////////// funcion gira base
  for(float pasos_base_M3=0.0; pasos_base_M3<tita1G_a_pasos; pasos_base_M3++){
    cont_base++;
    cont_brazo++;
    cont_varilla++;
    //digitalWrite(step, HIGH);
    digitalWrite(step_3, HIGH);
    //digitalWrite(step_2, HIGH);
    //digitalWrite(step_4, HIGH);
    delay(temp_base);
    //digitalWrite(step,LOW);
    digitalWrite(step_3,LOW);
    //digitalWrite(step_2,LOW);
    //digitalWrite(step_4,LOW);
    delay(temp_base);
    return;
  }
}*/
void home_base() {
  delay(500);
  digitalWrite(dir_3, LOW);  // con LOW gira AntiHorario
  while (homeb1 == false && homeb2 == false) {
    digitalWrite(step_3, HIGH);
    delayMicroseconds(700);
    digitalWrite(step_3, LOW);
    delayMicroseconds(700);
  }
  delay(500);
  //Serial.println("Salio del While");
  if (homeb1) {
    digitalWrite(dir_3, HIGH);
    for (int i = 0; i < 2200; i++) {
      digitalWrite(step_3, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_3, LOW);
      delayMicroseconds(700);
    }
  }
  /*if(homeb2){
    digitalWrite(dir_3,HIGH);
    for(int i=0;i < 4000; i++){
      digitalWrite(step_3, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_3, LOW);
      delayMicroseconds(700);
    }
  }*/
  //homeb1=false;
  //homeb2=false;
}
void home_brazo() {
  delay(500);
  digitalWrite(dir_2, HIGH);  // con HIGH gira Horario
  while (pararmotorbrazo35 == false && pararmotorbrazo32 == false) {
    digitalWrite(step_2, HIGH);
    delayMicroseconds(700);
    digitalWrite(step_2, LOW);
    delayMicroseconds(700);
  }
  delay(500);
  //Serial.println("Salio del While");
  if (pararmotorbrazo35) {
    digitalWrite(dir_2, LOW);
    for (int i = 0; i < 3650; i++) {
      digitalWrite(step_2, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_2, LOW);
      delayMicroseconds(700);
    }
  }
  if (pararmotorbrazo32) {
    digitalWrite(dir_2, HIGH);
    for (int i = 0; i < 3650; i++) {
      digitalWrite(step_2, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_2, LOW);
      delayMicroseconds(700);
    }
  }
  //pararmotorbrazo35=false;
  //pararmotorbrazo32=false;
}
void home_z() {
  digitalWrite(dir_4, HIGH);  // con LOW baja
  while (pararmotorz_sup == false) {
    digitalWrite(step_4, HIGH);
    delayMicroseconds(700);
    digitalWrite(step_4, LOW);
    delayMicroseconds(700);
  }
  delay(500);
  //Serial.println("Salio del While");
  if (pararmotorz_sup) {
    digitalWrite(dir_4, LOW);
    for (int i = 0; i < 2000; i++) {  //21100
      digitalWrite(step_4, HIGH);
      delayMicroseconds(700);
      digitalWrite(step_4, LOW);
      delayMicroseconds(700);
    }
  }
  //pararmotorz_sup=false;
  //pararmotorz_inf=false;
}

void IRAM_ATTR f1() {
  homeb1 = true;
}
void IRAM_ATTR f2() {
  homeb2 = true;
}
void IRAM_ATTR finalpararbrazo35() {
  pararmotorbrazo35 = true;
}
void IRAM_ATTR finalpararbrazo32() {
  pararmotorbrazo32 = true;
}
void IRAM_ATTR finalpararz_sup() {
  pararmotorz_sup = true;
}
void IRAM_ATTR finalpararz_inf() {
  pararmotorz_inf = true;
}
void setup() {
  Serial.begin(9600);
  //Inicio Motores
  //Motor 1
  pinMode(step, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(EN, OUTPUT);
  //Motor 2
  pinMode(step_2, OUTPUT);
  pinMode(dir_2, OUTPUT);
  pinMode(EN_2, OUTPUT);
  //Motor 3
  pinMode(step_3, OUTPUT);
  pinMode(dir_3, OUTPUT);
  pinMode(EN_3, OUTPUT);
  //Motor 4
  pinMode(step_4, OUTPUT);
  pinMode(dir_4, OUTPUT);
  pinMode(EN_4, OUTPUT);
  //Fin motores
  //Finales carrera
  pinMode(fcb1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(fcb1), f1, FALLING);
  pinMode(fcb2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(fcb2), f2, FALLING);
  pinMode(fc_brazo_1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(fc_brazo_1), finalpararbrazo35, CHANGE);
  pinMode(fc_brazo_2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(fc_brazo_2), finalpararbrazo32, CHANGE);
  pinMode(fc_zsuperior, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(fc_zsuperior), finalpararz_sup, CHANGE);
  pinMode(fc_zinferior, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(fc_zinferior), finalpararz_inf, CHANGE);
  pinMode(puntas, INPUT_PULLUP);
}

void loop() {

  if (Serial.available()) {
    char input = Serial.read();
  
  //Serial.println(input);
  //val_menu=Serial.parseInt();
  //limpiarBufferSerial();
  if (input == 'm') {
    //Serial.println("Proceso de medicion");
    estadopuntas = digitalRead(puntas);

    // Envía el estado del pulsador por el puerto serial
    if (estadopuntas == LOW) {
      Serial.println("Continuidad");
    } else {
      Serial.println("No continuidad");
    }

    // Espera 500 ms antes de leer el estado del pulsador nuevamente
    delay(500);
  }
  if (input == 'h') {
    Serial.println("Rutina de Home");
    Serial.println("Homeb1:");
    Serial.println(homeb1);
    Serial.println("Homeb12:");
    Serial.println(homeb2);
    Serial.println("pararmotorbrazo35:");
    Serial.println(pararmotorbrazo35);
    Serial.println("pararmotorbrazo32:");
    Serial.println(pararmotorbrazo32);
    Serial.println("pararmotorz_sup:");
    Serial.println(pararmotorz_sup);
    Serial.println("pararmotorz_inf:");
    Serial.println(pararmotorz_inf);
    //cine=1;
    if (movehome == 1) {
      cine = 1;
      tita1G = 0.0;
      tita2G = 0.0;
      Zpaso = 0.0;
      goto pruebahome;
      //movehome=0;
    }
    vueltacine:
    delay(500);
    home_z();
    delay(500);
    pararmotorz_sup = false;
    homeb1 = false;
    delay(500);
    homeb2 = false;
    home_base();  // rutina de home de la base
    //Serial.println("homeb1: ");
    //Serial.println(homeb1);
    //Serial.println("homeb2: ");
    //Serial.println(homeb2);

    /*delay(500);
      homeb1=false;
      delay(500);
      homeb2=false;*/
    home_brazo();
    delay(500);
    pararmotorbrazo35 = false;
    delay(500);
    pararmotorbrazo32 = false;

    delay(500);
    pararmotorz_inf = false;
    Serial.println("Salida:");
    Serial.println("Homeb1:");
    Serial.println(homeb1);
    Serial.println("Homeb12:");
    Serial.println(homeb2);
    Serial.println("pararmotorbrazo35:");
    Serial.println(pararmotorbrazo35);
    Serial.println("pararmotorbrazo32:");
    Serial.println(pararmotorbrazo32);
    Serial.println("pararmotorz_sup:");
    Serial.println(pararmotorz_sup);
    Serial.println("pararmotorz_inf:");
    Serial.println(pararmotorz_inf);
    tita1pasos_anterior = 0;
    tita2pasos_anterior = 0;
    z_pasos_anterior = 0;
    tita1G = 0;
    tita2G = 0;
    Z = 0;
    /*if (homeb1==1){
        homeb1=false;
        homeb1=0;
        Serial.println("entro");
      }*/

    //Serial.println("homeb1 sal if: ");
    //Serial.println(homeb1);
    /*for(m=0; m<1000; m++){
        digitalWrite(step_3, HIGH);
        delayMicroseconds(700);
        digitalWrite(step_3, LOW);
        delayMicroseconds(700);
      }*/
    //val_menu=0;
  }
  //Serial.println("Salio del for");
  //Serial.println("Sum_angulos:");
  //Serial.println(sum_angulos);
 /* if (input == 'p' ) || sum_angulos > 1) {
    digitalWrite(dir_4, HIGH);
    if (sum_angulos == 1) {
      angulos(-80, 175, 0);
    }
    if (sum_angulos == 1) {
      angulos(-80, 175, -53);
      sum_angulos=0;
    }*/
  
   if ((input == 'p' ) || (input =='o')) {
    digitalWrite(dir_4, HIGH);
    if (input=='p') {
      angulos(-80, 175, 0);
    }
    if (input=='o') {
      angulos(-80, 175, -53);
      sum_angulos=0;
    }

    /*Serial.println(mensaje1);
    while(Serial.available()==0){

    }
    X=Serial.parseInt();
    limpiarBufferSerial();
    Serial.print(mensaje3);
    Serial.println(X);

    Serial.println(mensaje2);
    while(Serial.available()==0){

    }
    Y=Serial.parseInt();
    limpiarBufferSerial();
    Serial.print(mensaje4);
    Serial.println(Y);
    
    Serial.println(mensajez);
    while(Serial.available()==0){

    }
    Z=Serial.parseInt();
    limpiarBufferSerial();
    Serial.print(mensajez_ing);
    Serial.println(Z);


    
    angulos(X,Y);*/
    Serial.println("Valor de tita2G:");
    Serial.println(tita2G);
    Serial.println("Valor de tita1G:");
    Serial.println(tita1G);
    pruebahome:
    digitalWrite(EN, LOW);
    digitalWrite(dir, LOW);
    digitalWrite(EN_3, LOW);
    digitalWrite(dir_3, LOW);  //Motor base sentido antihorario ERA HIGH
    digitalWrite(EN_2, LOW);
    digitalWrite(dir_2, HIGH);  //Motor brazo 2 sentido horario ERA HIGH
    digitalWrite(EN_4, LOW);
    //digitalWrite(dir_4, HIGH); //Con HIGH Sube ERA HIGH
    //pruebahome:
    tita1G_actual = round(tita1G / 0.1125) * 3.16;  //0.1125 porque trabajo con micropasos, 3.16 por la relacion de transformacion entre las poleas
    tita1G_a_pasos = tita1G_actual - tita1pasos_anterior;
    Serial.println("Cantidad de pasos Base");
    Serial.println(tita1G_a_pasos);
    //Serial.println("Cantidad de pasos Base relativo");
    //Serial.println(tita1G_a_pasos);
    if (tita1G_a_pasos < 0) {
      tita1G_a_pasos = -1 * tita1G_a_pasos;
      digitalWrite(dir_3, HIGH);
    }
    /*for(float pasos_base_M3=0.0; pasos_base_M3<tita1G_a_pasos; pasos_base_M3++){////////////////////////// for base
      //digitalWrite(step, HIGH);
      digitalWrite(step_3, HIGH);
      //digitalWrite(step_2, HIGH);
      //digitalWrite(step_4, HIGH);
      delay(temp);
      //digitalWrite(step,LOW);
      digitalWrite(step_3,LOW);
     //digitalWrite(step_2,LOW);
      //digitalWrite(step_4,LOW);
      delay(temp);
    }*/
    tita2G_actual = round(tita2G / 0.1125) * 3.16;  //0.1125 porque trabajo con micropasos, 3.16 por la relacion de transformacion entre las poleas
    tita2G_a_pasos = tita2G_actual - tita2pasos_anterior;
    if (tita2G_a_pasos < 0) {
      tita2G_a_pasos = -1 * tita2G_a_pasos;
      digitalWrite(dir_2, LOW);
    }
    //tita2G_a_pasos=tita2G_a_pasos-tita2G_a_pasos;
    /*
     if (tita2G_a_pasos<0){
     tita2G_a_pasos=-1*tita2G_a_pasos;
     digitalWrite(dir_2, LOW);
    }*/
    Serial.println("Cantidad de pasos Brazo 2");
    Serial.println(tita2G_a_pasos);
    /*for(float pasos_brazo2_M2=0.0; pasos_brazo2_M2<tita2G_a_pasos; pasos_brazo2_M2++){//////////////////// for brazo
      //digitalWrite(step, HIGH);
      //digitalWrite(step_3, HIGH);
      digitalWrite(step_2, HIGH);
      //digitalWrite(step_4, HIGH);
      delay(temp);
      //digitalWrite(step,LOW);
      //digitalWrite(step_3,LOW);
      digitalWrite(step_2,LOW);
      //digitalWrite(step_4,LOW);
      delay(temp);
    }*/
    //MODIFICACION DE Zpaso ABAJO
    /*
    z_actual=Z*(1600/8);//1600 porque esta configurado con micropasos 1/8, 8 porque son 8mm por vuelta de la varilla roscada
    Zpaso=z_actual-z_pasos_anterior;
    if (Zpaso<0){
      Zpaso=-1*Zpaso;
      digitalWrite(dir_4, LOW);//Low baja
   }
   Serial.println("Cantidad de pasos Varilla: ");
    Serial.println(Zpaso);*/
    //MODIFICACION DE Zpaso ARRIBA
    Serial.println("Cantidad de pasos Varilla: ");
    Serial.println(Zpaso);
    /*for(float pasos_varilla=0.0;pasos_varilla<Zpaso;pasos_varilla++){//////////////////////// for varilla
     //digitalWrite(step, HIGH);
      //digitalWrite(step_3, HIGH);
      //digitalWrite(step_2, HIGH);
      digitalWrite(step_4, HIGH);
      delay(temp);
     //digitalWrite(step,LOW);
     //digitalWrite(step_3,LOW);
     //digitalWrite(step_2,LOW);
      digitalWrite(step_4,LOW);
      delay(temp);
    }*/
    ///////////////////////////////////////////////////////////////////////////////
    /*paso_max=tita1G_a_pasos;
    if(tita2G_a_pasos>paso_max){
      paso_max=tita2G_a_pasos;
    } else if(Zpaso>tita2G_a_pasos){
      paso_max=Zpaso;
    }*/
    if (tita1G_a_pasos >= tita2G_a_pasos && tita1G_a_pasos >= Zpaso) {
      paso_max = tita1G_a_pasos;
    } else if (tita2G_a_pasos >= tita1G_a_pasos && tita2G_a_pasos >= Zpaso) {
      paso_max = tita2G_a_pasos;
    } else {
      paso_max = Zpaso;
    }
    Serial.println("El mayor es: ");
    Serial.println(paso_max);

    /*
    Serial.println("Pasos de la base: ");
    Serial.println(tita1G_a_pasos);
    Serial.println("Pasos del brazo: ");
    Serial.println(tita2G_a_pasos);
    Serial.println("Paso de la varilla: ");
    Serial.println(Zpaso);
    Serial.println("El paso mayor es: ");
    Serial.println(paso_max);
    temp_base= ((paso_max*2*temp)/tita1G_a_pasos)/2;
   temp_brazo= ((paso_max*2*temp)/tita2G_a_pasos)/2;
    temp_varilla= ((paso_max*2*temp)/Zpaso)/2;
    Serial.println("Tiempo de la base: ");
    Serial.println(temp_base);
   Serial.println("Tiempo del brazo: ");
    Serial.println(temp_brazo);
    Serial.println("Tiempo de la varilla: ");
    Serial.println(temp_varilla);*/
    //Relaciones
    /*
    Serial.println("Relacion Base-Varilla: ");
    rel_base=Zpaso/tita1G_a_pasos;
    Serial.println(rel_base);
   Serial.println("Relacion Brazo-Varilla: ");
    rel_brazo=Zpaso/tita2G_a_pasos;
   Serial.println(rel_brazo);
   Serial.println("Relacion Varilla-Varilla: ");
    rel_varilla=Zpaso/Zpaso;
    Serial.println(rel_varilla);*/
    /*
    for(int j=0;j<10000;j++){
      cont1++;

     if(abs(fmod(cont1,1.1901928)-0.48)<0.52){
        cont2++;
      }/*
     if(cont3<tita2G_a_pasos){
      if(abs(fmod(cont1,4.1806020)-1.64)<0.52){
        cont3++;
      }
      }*/
    /*
      if(cont3<tita2G_a_pasos){
       if(abs(fmod(cont1,Zpaso/tita2G_a_pasos)-fmod(10,Zpaso/tita2G_a_pasos))<0.52){
       cont3++;
      }
      }

    }*/
    /*
    Serial.println("Contador base ultimo: ");
    Serial.println(cont2);
    Serial.println("Contador brazo ultimo: ");
    Serial.println(cont3);*/
    /*
    Serial.println("modulo: ");
    Serial.println((round(fmod(100,4.18)*1000))/1000);
    Serial.println("modulo: ");
    Serial.println(fmod(100,4.18));*/

    //gira_base(tita1G_a_pasos,temp_base);
    //Serial.println("el cont_base: ");
    //Serial.println(cont_base);
    /*
    for(float n=0.0;n<paso_max;n++){
      if(cont_base<tita1G_a_pasos){
        gira_base(tita1G_a_pasos,temp_base);
      }
      if(cont_base<tita2G_a_pasos){
       gira_base(tita2G_a_pasos,temp_brazo);
     }
     if(cont_base<Zpaso){
        gira_base(Zpaso,temp_varilla);
      }
    }*/
    /*
    Serial.println("el cont_base: ");
    Serial.println(cont_base);
    Serial.println("el cont_brazo: ");
    Serial.println(cont_brazo);
    */
    digitalWrite(step, LOW);
    digitalWrite(step_2, LOW);
    digitalWrite(step_3, LOW);
    digitalWrite(step_4, LOW);
    volatile bool homeb1 = false;
    volatile bool homeb2 = false;
    volatile bool pararmotorbrazo35 = false;
    volatile bool pararmotorbrazo32 = false;
    volatile bool pararmotorz_sup = false;
    volatile bool pararmotorz_inf = false;
    girar(paso_max, tita1G_a_pasos, tita2G_a_pasos, Zpaso, temp_base, temp_brazo, temp_varilla);
    delay(500);
    sum_angulos++;
    //pararmotorbase=false; //vuelvo a cambiar el estado del final de carrera para que luego se pueda actuar nuevamente
    digitalWrite(EN_3, LOW);    // habilito el motor en caso que se haya actuado el final de carrera
    pararmotorbrazo35 = false;  //vuelvo a cambiar el estado del final de carrera para que luego se pueda actuar nuevamente
    delay(500);
    pararmotorbrazo32 = false;
    digitalWrite(EN_2, LOW);  // habilito el motor en caso que se haya actuado el final de carrera
    delay(500);
    pararmotorz_sup = false;  //vuelvo a cambiar el estado del final de carrera para que luego se pueda actuar nuevamente
    delay(500);
    pararmotorz_inf = false;
    digitalWrite(EN_4, LOW);  // habilito el motor en caso que se haya actuado el final de carrera
    Serial.println("el cont_base: ");
    Serial.println(cont_base);
    Serial.println("el cont_brazo: ");
    Serial.println(cont_brazo);
    Serial.println("el cont_varilla: ");
    Serial.println(cont_varilla);
    //Serial.println("Estado EN_2: ");
    //Serial.println(digitalRead(EN_3));
    //Serial.println("pararmotorbrazo: ");
    //Serial.println(pararmotorbrazo);
    tita1pasos_anterior = tita1G_actual;
    tita2pasos_anterior = tita2G_actual;
    z_pasos_anterior = z_actual;
    //Serial.println("Zpaso: ");
    //Serial.println(Zpaso);
    cont_base = 0.0;
    cont_brazo = 0.0;
    cont_varilla = 0.0;
    cont1 = 0.0;
    if (cine == 1) {
      /*delay(500);
      homeb1=false;
      delay(500);
      homeb2=false;
      home_base();
      delay(500);
      home_brazo();
      delay(500);
      home_z();*/
      movehome = 0;
      cine = 0;
      goto vueltacine;
    }
  }  //fin del if cinematica inversa
 }
}