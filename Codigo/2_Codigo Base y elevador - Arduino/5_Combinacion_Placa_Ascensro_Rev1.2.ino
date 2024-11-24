//Motor Placa
#define STEP_PIN A6
#define DIR_PIN A7
#define ENABLE_PIN A2
#define ENDSTOP_PIN 3 
//Motor ascensor
#define STEP_PIN_1 26
#define DIR_PIN_1 28
#define ENABLE_PIN_1 24
#define ENDSTOP_PIN_1 2
//Variables motor placa
char input;
const int stepsPerRevolution = 400;
const int stepsBack = 98; // Pasos a girar en sentido antihorario cuando se activa el final de carrera
const int stepsForward = 300;
int stepaux;
volatile bool endstopTriggered = false; // Bandera para indicar si el final de carrera ha sido activado
volatile bool motorRunning = false;
//Variables motor ascensor
const int stepsPerRevolution_2 = 200; // Ajusta esto según tu motor
volatile bool endstopTriggered_2 = false; // Bandera para el final de carrera
volatile bool motorRunning_2 = false;

void setup() {
  // Configurar los pines
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(ENDSTOP_PIN, INPUT_PULLUP); // Final de carrera como entrada con pull-up interno

  pinMode(STEP_PIN_1, OUTPUT);
  pinMode(DIR_PIN_1, OUTPUT);
  pinMode(ENABLE_PIN_1, OUTPUT);
  pinMode(ENDSTOP_PIN_1, INPUT_PULLUP); // Final de carrera como entrada con resistencia pull-up

  // Iniciar la comunicación serial
  Serial.begin(9600);
  digitalWrite(ENABLE_PIN_1, LOW); // LOW habilita el motor
  
  
  Serial.println("Presiona 'w' para girar 200 pasos en sentido horario.");
  Serial.println("Presiona 'l' para girar 200 pasos en sentido antihorario.");
  // Habilitar el driver
  digitalWrite(ENABLE_PIN, LOW);

  Serial.println("Escribe 'g' para empezar a girar en sentido horario hasta que se active el final de carrera.");

  // Configurar la interrupción para el final de carrera
  attachInterrupt(digitalPinToInterrupt(ENDSTOP_PIN), endstopInterrupt, FALLING);
  //pinMode(ENDSTOP_PIN_1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENDSTOP_PIN_1), endstopInterrupt_1, FALLING);
}
void loop() {
  // Comprobar la entrada serial
  if (Serial.available()) {
    char input = Serial.read();

    // Girar en sentido horario al presionar 'g'
    if (input == 'g') {
      Serial.println("Girando en sentido horario...");
      motorRunning = true;
      stepaux=stepsBack;
      rotateUntilEndstop(true, 'g');  // Inicia el giro en sentido horario
    }
    else if (input == 's') {
      Serial.println("Girando 200 pasos en sentido horario...");
      motorRunning = true;
      stepaux=stepsForward;
      rotateUntilEndstop(true, 's');
      //rotateSteps(true, stepsForward); // Girar 200 pasos en sentido horario
      //motorRunning = false;            // Detener el motor
    }
    //else if (endstopTriggered_2) {
      //Serial.println("Final de carrera ya no está activo. Habilitando motor.");
      //endstopTriggered_2 = false;  // Reiniciamos la bandera
      //digitalWrite(ENABLE_PIN_1, LOW); // Rehabilitamos el motor
    //}

    // Girar en sentido horario (200 pasos) al presionar 'w'
    else if (input == 'w') {
      Serial.println("Girando 200 pasos en sentido horario...");
      endstopTriggered_2 = false;
      rotateSteps_2(650, true); // 200 pasos en sentido horario
    }

    // Girar en sentido antihorario (200 pasos) al presionar 's'
    else if (input == 'l') {
      Serial.println("endstopTriggered_2");
      Serial.println(endstopTriggered_2);
      /*if (endstopTriggered_2){
        //endstopTriggered_2 = false;
        rotateSteps_2(5, true);
      }else {
        motorRunning_2 = true;
        endstopTriggered_2 = false;
        //endstopTriggered_2 = false;
        rotateUntilEndstop(true, 'l');
      }*/
      motorRunning_2 = true;
      endstopTriggered_2 = false;
      //endstopTriggered_2 = false;
      rotateUntilEndstop(true, 'l');
      endstopTriggered_2 = false;
      //rotateSteps_2(5, true);
      //Serial.println("ingresaste l");
      //motorRunning_2 = true;//
      //endstopTriggered_2 = false;//
      //endstopTriggered_2 = false;
      //rotateUntilEndstop(true, 'l');//
      //Serial.println("Pasa");
      //delay(5);
      //endstopTriggered_2 = false;  
      
    }
  }

if (endstopTriggered) {
  //Serial.println("Final de carrera activado. Girando 120 pasos en sentido antihorario...");
  rotateSteps(false, stepaux);
        
      //rotateSteps(false, stepsBack); //letra g
      //rotateSteps(false, stepsForward); // letra s
                // Girar 120 pasos en sentido antihorario
  endstopTriggered = false;       // Resetear la bandera
  motorRunning = false;           // Detener el motor
  }
}



// Función para girar el motor hasta que se active el final de carrera
void rotateUntilEndstop(bool clockwise, char n) {
  if (n == 'g' || n == 's'){
    if (clockwise) {
      digitalWrite(DIR_PIN, HIGH); // Sentido horario
    } else {
      digitalWrite(DIR_PIN, LOW);  // Sentido antihorario
    }
    while (!endstopTriggered && motorRunning) {
      stepMotor();   // Gira el motor continuamente
      delay(1);
    }
  }
  else if (n == 'l'){
    digitalWrite(DIR_PIN_1, LOW);//gira antihorario
    //Serial.println(endstopTriggered_2);
    //Serial.println(motorRunning_2);
    while (!endstopTriggered_2 && motorRunning_2) {
      stepMotor_1();   // Gira el motor continuamente
      delay(1);
    }
    motorRunning_2 = false;
  }

}

// Función para girar el motor un número específico de pasos
void rotateSteps(bool clockwise, int steps) {
  if (clockwise) {
    digitalWrite(DIR_PIN, HIGH); // Sentido horario
  } else {
    digitalWrite(DIR_PIN, LOW);  // Sentido antihorario
  }

  for (int i = 0; i < steps; i++) {
    stepMotor();
    delay(1);
  }
}

// Función para un solo paso del motor
void stepMotor() {
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(3000);
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(3000);
}

// Función de interrupción del final de carrera
void endstopInterrupt() {
  endstopTriggered = true;  // Activar la bandera cuando el final de carrera se activa
}



// Función para girar un número específico de pasos
void rotateSteps_2(int steps, bool clockwise) {
  Serial.println("ingreso a rotateSteps_2");
  // Configurar la dirección
  digitalWrite(DIR_PIN_1, clockwise ? HIGH : LOW);
  endstopTriggered_2 = false;
  for (int i = 0; i < steps; i++) {
    /*if (endstopTriggered_2) {
      Serial.println(endstopTriggered_2);
      Serial.println("Final de carrera activado. Motor detenido.");
      return; // Detener el motor si el final de carrera está activado
    }*/
    stepMotor_1();
    delay(1); // Ajustar la velocidad del motor
  }
}

void stepMotor_1() {
  digitalWrite(STEP_PIN_1, HIGH);
  delayMicroseconds(3000); // Ajusta este valor para controlar la velocidad
  digitalWrite(STEP_PIN_1, LOW);
  delayMicroseconds(3000); // Ajusta este valor para controlar la velocidad
}

// Función de interrupción del final de carrera
void endstopInterrupt_1() {
  endstopTriggered_2 = true;
  //digitalWrite(ENABLE_PIN_1, HIGH); // Deshabilitar el motor cuando se activa el final de carrera
}





