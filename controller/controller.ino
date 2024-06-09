/*
KEY_UP_ARROWc
KEY_DOWN_ARROW
KEY_LEFT_ARROW
KEY_RIGHT_ARROW
*/
#include "HID-Project.h"
const char CONFIRM = 'y';
const char ENTER = 10;

const char GUIDE = 'u';
const long GUIDE_FIRST_X = -30000;
const long GUIDE_FIRST_Y = -2000;
const long GUIDE_DISTANCE_X = 1650;
const long MOVE_BOUnD_MAX = 32767;
const long MOVE_BOUND_MIN = -32767;

const unsigned long WHEEL_CD = 930;
const char JUMP = 'f';
const char WIND_MOVE = 'w';
const char ELF_SHIELD = 'd';
const char SONG_SKY = 'a';
const char ROPE = '9';
const char FRENZY = '8';
const unsigned long FRENZY_CD = 300;

const char FOUNTAIN = 'z';
const unsigned long FOUNTAIN_CD = 58; 
const char TORNADO = 'b';
const unsigned long TORNADO_CD = 20;
const char MONSOON = 'q';
const unsigned long MONSOON_CD = 24;
const char SWIRL = 'e';
const unsigned long SWIRL_CD = 25;
const char FANTASY = ' ';
const unsigned long FANTASY_CD = 8;
const char BIRD = 'v';
const unsigned long BIRD_CD = 25;
const char C2F = 'g';
const unsigned long MONEY_CD = 90; 

const int BUFF_COUNTS = 5;
const char BUFF[5] = {'2', '3', C2F, 'c', 'x'};
const String BUFF_NAME[5] = {"Storm", "Glory", "Shilff", "Grandpa", "Critical"};
unsigned long BUFF_CD[5] = {120, 120, 90, 150, 120};

int hunting_graph = 3; // 3: alley2, 4: spring1

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Keyboard.begin();
  randomSeed(analogRead(0));
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "hunting") {
      // Get hunting seconds
      Serial.println("next: seconds");
      WaitInput();
      int seconds = Serial.readStringUntil('\n').toInt();

      Battle(seconds, 0, true, true);
      Serial.println("hunting ack");

    } else if (command == "songsky") {
      // Get wait seconds
      Serial.println("next: seconds");
      WaitInput();
      int seconds = Serial.readStringUntil('\n').toInt();

      SongSkyStandby(seconds);
      Serial.println("songsky ack");

    } else if (command == "standby") {
      // Get standby seconds
      Serial.println("next: seconds");
      WaitInput();
      int seconds = Serial.readStringUntil('\n').toInt();

      Battle(seconds, 0, false, false);
      Serial.println("standby ack");

    } else if (command == "fountain") {
      // Get standby seconds
      Serial.println("next: seconds");
      WaitInput();
      int seconds = Serial.readStringUntil('\n').toInt();

      Battle(seconds, 0, true, false);
      Serial.println("fountain ack");

    } else if (command == "frenzy") {
      Serial.print("next: minutes");
      WaitInput();
      int minutes = Serial.readStringUntil('\n').toInt();

      PlayFrenzy(minutes);
      Serial.println("frenzy ack");

    } else if (command == "move") {
        // Get moving duration (sec)
        Serial.println("next: duration");
        WaitInput();
        float duration = Serial.readStringUntil('\n').toFloat();

        duration *= 1000;
        if (duration < 0) {
            duration *= -1;
            Keyboard.press(KEY_LEFT_ARROW);
        } else {
            Keyboard.press(KEY_RIGHT_ARROW);
        }

        delay(duration);
        Keyboard.releaseAll();
        Serial.println("move ack");

    } else if (command == "updown") {
        // Get up down directoin
        Serial.println("next: direction");
        WaitInput();
        String direction = Serial.readStringUntil('\n');

        if (direction == "up") {
          SimpleSkill(true, ROPE);
          delay(3500);
          Serial.println("up ack");
        } else if (direction == "down"){
          DownJump();
          delay(2500);
          Serial.println("down ack");
        } else {
          Serial.println("Unknown updown direction");
        }
        
    } else if (command == "mine") {
      SimpleSkill(true, CONFIRM);
      delay(500);
      Serial.println("mine ack");

    } else if (command == "rune") {
      // Get rune answer
      Serial.println("next: answer");
      WaitInput();
      String answer = Serial.readStringUntil('\n');
      for (int i = 0; i < answer.length(); i++) {
        char c = answer.charAt(i);
        switch (c) {
          case 'w':
            Keyboard.write(KEY_UP_ARROW);
            delay(200);
            break;
          case 'a':
            Keyboard.write(KEY_LEFT_ARROW);
            delay(200);
            break;
          case 's':
            Keyboard.write(KEY_DOWN_ARROW);
            delay(200);
            break;
          case 'd':
            Keyboard.write(KEY_RIGHT_ARROW);
            delay(200);
            break;
        }
      }
      Serial.println("rune ack");

    } else {
        // Unknown command
        Serial.println("Unknown command");
    }
  }
}

void PlayFrenzy(int minutes) {
  unsigned long start = millis();
  unsigned long FrenzyStart = start;
  unsigned long BurnStart = start;
  unsigned long time = millis();
  int second = (time-start)/1000;
  bool startUp = true;
  char notRobot[] = {'z', 'x'};
  unsigned long minDelay[] = {300, 300};
  unsigned long maxDelay[] = {350, 350};

  while (second < minutes * 60) {
    // Frenzys
    if (startUp || (time - FrenzyStart)/1000 > FRENZY_CD) {
      FrenzyStart = millis();
      Move(notRobot, 2, minDelay, maxDelay);
      SimpleSkill(true, FRENZY);

      // frenzy delay
      delay(3000);
    }

    // time set
    time = millis();
    second = (time-start)/1000;
    startUp = false;
  }
}

void Battle(unsigned long period, int preMove, bool useFountain, bool collectMoney) {
  if (preMove == 1) {
    char toCenterCommand[] = {'d', 'd', 'd'};
    unsigned long minDelay[] = {600, 600, 600};
    unsigned long maxDelay[] = {650, 650, 650};
    Move(toCenterCommand, 3, minDelay, maxDelay);

  } else if (preMove == 2) {
    char toCenterCommand[] = {'d', 'd', 'd', 'd'};
    unsigned long minDelay[] = {600, 600, 600, 600};
    unsigned long maxDelay[] = {650, 650, 650, 650};
    Move(toCenterCommand, 4, minDelay, maxDelay);

  } else if (preMove == 3) {
    char toCenterCommand[] = {'e', 'd', 'd'};
    unsigned long minDelay[] = {1500, 600, 600};
    unsigned long maxDelay[] = {1600, 650, 650};
    Move(toCenterCommand, 3, minDelay, maxDelay);

  } else if (preMove == 4) {
    char toCenterCommand[] = {'s', 's', 's'};
    unsigned long minDelay[] = {600, 600, 600};
    unsigned long maxDelay[] = {650, 650, 650};
    Move(toCenterCommand, 3, minDelay, maxDelay);

  } else if (preMove == 5) {
    char toCenterCommand[] = {'q', 'q', 'q', 'x', 'x', 'x', 'w', 's'};
    unsigned long minDelay[] = {1300, 1100, 1100, 300, 300, 300, 1200, 600};
    unsigned long maxDelay[] = {1400, 1200, 1200, 350, 350, 350, 1250, 650};
    Move(toCenterCommand, 8, minDelay, maxDelay);

  } else if (preMove == 6) {
    char toCenterCommand[] = {'d', 'w', 's', 'z', 'z'};
    unsigned long minDelay[] = {600, 1000, 600, 300, 300};
    unsigned long maxDelay[] = {650, 1200, 650, 350, 350};
    Move(toCenterCommand, 5, minDelay, maxDelay);

  } else if (preMove == 7) {

  } else if (preMove == 8) {
    char toCenterCommand[] = {'q', 's', 's'};
    unsigned long minDelay[] = {1200, 600, 600};
    unsigned long maxDelay[] = {1300, 650, 650};
    Move(toCenterCommand, 3, minDelay, maxDelay);

  } else if (preMove == 9) {
    char toCenterCommand[] = {'z', 'z', 'z', 'w', 's'};
    unsigned long minDelay[] = {300, 300, 300, 1500, 800};
    unsigned long maxDelay[] = {350, 350, 350, 1600, 850};
    Move(toCenterCommand, 5, minDelay, maxDelay);
    collectMoney = true;
  }
  delay(800);

  bool direction = false;
  unsigned long start = millis();
  unsigned long FrenzyStart = start;
  unsigned long TornadoStart = start;
  unsigned long SwirlStart = start;
  unsigned long MonsoonStart = start;
  unsigned long FantasyStart = start;
  unsigned long FountainStart = start;
  unsigned long BirdStart = start;
  unsigned long MoneyStart = start;

  unsigned long buffStart[5] = {start, start, start, start, start};

  unsigned long time = millis();
  int second = (time-start)/1000;
  bool startUp = true;
  while (second < period) {
    bool underAttack = false;
    SongOfTheSky(direction, 10, 20, 500, 1000);
    direction = !direction;

    // Frenzy
    time = millis();
    second = (time-start)/1000;
    if (startUp || (time-FrenzyStart)/1000 > FRENZY_CD) {
      SimpleSkill(direction, FRENZY);      
      FrenzyStart = millis();
      delay(random(700, 1000));
    }

    // Fantasy
    if (startUp || (time-FantasyStart)/1000 > FANTASY_CD) {
      SimpleSkill(direction, FANTASY);
      FantasyStart = millis();
      delay(600);
    }
        
    // Tornado
    time = millis();
    second = (time-start)/1000;
    if (startUp || (time-TornadoStart)/1000 > TORNADO_CD) {
      Tornado(direction);
      TornadoStart = millis();
      delay(random(700, 1000));
      underAttack = true;
    }

    // Swirl
    time = millis();
    second = (time-start)/1000;
    if (startUp || (time-SwirlStart)/1000 > SWIRL_CD) {
      Swirl(direction);
      SwirlStart = millis();
      delay(random(800, 1000));
    }

    // Bird
    time = millis();
    second = (time-start)/1000;
    if (startUp || (time-BirdStart)/1000 > BIRD_CD) {
      SimpleSkill(direction, BIRD);
      BirdStart = millis();
      delay(random(800, 1000));
    }

    // Monsoon
    time = millis();
    second = (time-start)/1000;
    if (startUp || (time-MonsoonStart)/1000 > MONSOON_CD) {
      SimpleSkill(direction, MONSOON);
      MonsoonStart = millis();
      delay(random(1500, 1700));
    }

    // Buffs
    for (int i = 0; i < BUFF_COUNTS; i++) {
      time = millis();
      second = (time-start)/1000;
      if (startUp || (time-buffStart[i])/1000 > BUFF_CD[i]) {
        SimpleSkill(direction, BUFF[i]);
        buffStart[i] = millis();
        delay(random(800, 1000));
      }
    }

    // Fountain
    time = millis();
    second = (time-start)/1000;
    if (useFountain && (startUp || (time-FountainStart)/1000 > FOUNTAIN_CD)) {
      // Move to the specific position
      MoveToFountain();
      
      // Fountain
      Fountain(false);
      FountainStart = millis();
      delay(random(800, 1000));
         
      // Move back to origin position
      BackFromFountain();
    }

    // Money
    time = millis();
    second = (time-start)/1000;
    if (startUp || (underAttack && (time-MoneyStart)/1000 > MONEY_CD)) {
      CollectMoney(collectMoney, 5);
      MoneyStart = millis();
    }
    delay(random(50, 100));
    startUp = false;
  }
}

void ArrowMove(char direction[], int counts, unsigned long wait[]) {
  for (int i = 0; i < counts; i++) {
    switch (direction[i]) {
    case 'w':
      Keyboard.write(KEY_UP_ARROW);
      delay(wait[i]);
      break;
    case 's':
      Keyboard.write(KEY_DOWN_ARROW);
      delay(wait[i]);
      break;
    case 'a':
      Keyboard.write(KEY_LEFT_ARROW);
      delay(wait[i]);
      break;
    case 'd':
      Keyboard.write(KEY_RIGHT_ARROW);
      delay(wait[i]);
      break;
    case 'y':
      Keyboard.write(CONFIRM);
      delay(wait[i]);
      break;
    case 'e':
      Keyboard.write(ENTER);
      delay(wait[i]);
      break;
    
    default:
      break;
    }
  }
}

void WalkingSongSky(int times) {
  for (int i = 0; i < times; i++) {
    SongOfTheSky(true, 100, 105, 50, 55);
  }
}

void SongSkyStandby(unsigned long period) {
  bool direction = false;
  unsigned long start = millis();
  unsigned long time = millis();
  int second = (time-start)/1000;
  while (second < period) {
    SongOfTheSky(direction, 120, 150, 500, 1000);
    direction = !direction;
    time = millis();
    second = (time-start)/1000;
  }
}

// Daily task
void GuideMoving(int index) {
  // Open UI
  Keyboard.write(GUIDE);
  delay(1000);
  // Move mouse to the first location
  AbsoluteMouse.moveTo(GUIDE_FIRST_X, GUIDE_FIRST_Y);
  delay(1000);
  
  // Move right according to the index value
  for (int i = 0; i < index; i++) {
    AbsoluteMouse.move(GUIDE_DISTANCE_X, 0);
    delay(200);
  }

  // Move and wait
  AbsoluteMouse.click(MOUSE_LEFT);
  delay(2000);
}

void DoubleJumpAttackA(bool direction, char jump, char attack) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  for (int i = 0; i < 3; i++) {
    DoubleJump(jump);
    delay(100);
    Keyboard.write(attack);
    delay(600); // 600 ~ 
  }
  Keyboard.releaseAll();
}

void DoubleJump(char jump) {
  Keyboard.write(jump);
  delay(100);
  Keyboard.write(jump);
  Keyboard.write(jump);
}

void WalkLatency(bool direction, unsigned long minLatency, unsigned long maxLatency) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  delay(random(minLatency, maxLatency));
  Keyboard.releaseAll();
}

void Turn(bool direction) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  delay(30);
  Keyboard.releaseAll();
  delay(100);
}

// minUp maxUp will affect the height of UpJump
void UpJump(unsigned long minUp, unsigned long maxUp) {
  Keyboard.write(JUMP);  
  Keyboard.press(KEY_UP_ARROW);
  delay(random(minUp, maxUp));

  Keyboard.write(JUMP);
  Keyboard.write(JUMP);
  delay(random(80, 100));
  Keyboard.releaseAll();
}

void DownJump() {
  Keyboard.press(KEY_DOWN_ARROW);
  Keyboard.write(JUMP);
  delay(random(80, 100));
  Keyboard.releaseAll();
}

// minDJ: 90, maxDJ: 120 (Round_min: 700, Round_max: 900)
void DoubleJumpLatency(bool direction, unsigned long minDJ, unsigned long maxDJ) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  Keyboard.write(JUMP);
  delay(random(minDJ, maxDJ));
  Keyboard.write(JUMP);
  Keyboard.write(JUMP);
  Keyboard.releaseAll();
}

// minDJ: 80, maxDJ: 120 (Round_min + minAttack: >800, Attack: 0 ~ 300)
void DoubleJumpAttackLatency(bool direction, unsigned long minDJ, unsigned long maxDJ, unsigned long minAttack, unsigned long maxAttack) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  Keyboard.write(JUMP);
  delay(random(minDJ, maxDJ));
  Keyboard.write(JUMP);
  Keyboard.write(JUMP);
  delay(random(minAttack, maxAttack));
  Keyboard.write(ELF_SHIELD);
  Keyboard.releaseAll();
}

// minWalk: 80, maxWalk: 120 (Round_min: 550, Round_max: 800)
void WindMove(bool direction, unsigned long minWalk, unsigned long maxWalk) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  delay(random(minWalk, maxWalk));
  Keyboard.write(WIND_MOVE);
  Keyboard.releaseAll();
}

// minDJ: 80, maxDJ: 120 (Round_min: 900, Margin: 100 ~ 500)
// margin: 100 moves the shortest
// margin: 500 moves the longest
void DoubleJumpWindMove(bool direction, unsigned long minDJ, unsigned long maxDJ, unsigned long minMargin, unsigned long maxMargin, unsigned long minWalk, unsigned long maxWalk) {
  DoubleJumpLatency(direction, minDJ, maxDJ);
  delay(random(minMargin, maxMargin)); 
  WindMove(direction, minWalk, maxWalk);
}

// minWalk: 80, maxWalk: 120 (Round_min: 50, Duration: >100)
unsigned long SongOfTheSky(bool direction, unsigned long minWalk, unsigned long maxWalk, unsigned long minDuration, unsigned long maxDuration) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  unsigned long distance = random(minWalk, maxWalk);
  delay(distance);
  Keyboard.press(SONG_SKY);
  delay(random(minDuration, maxDuration));
  Keyboard.releaseAll();
  return distance;
}

void Fountain(bool direction) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  delay(random(50, 100));
  Keyboard.releaseAll();

  Keyboard.press(KEY_DOWN_ARROW);
  Keyboard.write(FOUNTAIN);
  delay(random(70, 100));
  Keyboard.releaseAll();
}

void Tornado(bool direction) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  delay(random(50, 100));
  Keyboard.write(TORNADO);
  Keyboard.releaseAll();
}

void Swirl(bool direction) {
  if (direction == true) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.press(KEY_LEFT_ARROW);
  }
  delay(random(50, 100));
  Keyboard.write(SWIRL);
  Keyboard.releaseAll();
}

void SimpleSkill(bool direction, char Command) {
  //if (direction == true) {
  //  Keyboard.press(KEY_RIGHT_ARROW);
  //} else {
  //  Keyboard.press(KEY_LEFT_ARROW);
  //}
  //delay(random(50, 70));
  Keyboard.write(Command);
  //Keyboard.releaseAll();
}

void Move(char direction[], int counts, unsigned long minDelay[], unsigned long maxDelay[]){
  for (int i = 0; i < counts; i++) {
    if (direction[i] == 'w') {
      UpJump(300, 350);
    } else if (direction[i] == 'a') {
      WindMove(false, 80, 100);
    } else if (direction[i] == 's') {
      DownJump();
    } else if (direction[i] == 'd') {
      WindMove(true, 80, 100);
    } else if (direction[i] == 'q') {
      DoubleJumpLatency(false, 110, 120);
    } else if (direction[i] == 'e') {
      DoubleJumpLatency(true, 110, 120);
    } else if (direction[i] == 'l') {
      Turn(false);
    } else if (direction[i] == 'r') {
      Turn(true);
    } else if (direction[i] == 'j') {
      DoubleJumpAttackLatency(false, 80, 100, 100, 200);
    } else if (direction[i] == 'k') {
      DoubleJumpAttackLatency(true, 80, 100, 100, 200);
    } else if (direction[i] == 'z') {
      WalkLatency(false, 200, 250);
    } else if (direction[i] == 'x') {
      WalkLatency(true, 200, 250);
    } else if (direction[i] == 'p') {
      SimpleSkill(true, ROPE);
    } else if (direction[i] == 'b') {
      Tornado(true);
    }
    delay(random(minDelay[i], maxDelay[i]));
  }
}

/************** Fountain ***************/
void MoveToFountain_eastside() {
  char commands[] = {'q', 'a', 'a', 'd', 'd', 'd', 'd', 'd', 'd', 'a', 'p'};
  unsigned long minDelay[] = {400, 600, 600, 600, 600, 600, 600, 600, 600, 600, 2000};
  unsigned long maxDelay[] = {410, 650, 650, 650, 650, 650, 650, 650, 650, 650, 2050};
  Move(commands, 11, minDelay, maxDelay);
}

void BackFromFountain_eastside() {
  char commands[] = {'q', 'q', 'q', 's', 'x'};
  unsigned long minDelay[] = {800, 800, 800, 800, 800};
  unsigned long maxDelay[] = {810, 810, 810, 810, 810,};
  Move(commands, 5, minDelay, maxDelay);
}

void MoveToFountain_fall1() {
  char commands[] = {'e', 'd'};
  unsigned long minDelay[] = {400, 750};
  unsigned long maxDelay[] = {410, 850};
  Move(commands, 2, minDelay, maxDelay);
}

void BackFromFountain_fall1() {
  char commands[] = {'q', 'a'};
  unsigned long minDelay[] = {400, 900};
  unsigned long maxDelay[] = {410, 1000};
  Move(commands, 2, minDelay, maxDelay);
}

void MoveToFountain_library4() {
  char commands[] = {'e', 'd'};
  unsigned long minDelay[] = {400, 750};
  unsigned long maxDelay[] = {410, 850};
  Move(commands, 2, minDelay, maxDelay);
}

void BackFromFountain_library4() {
  char commands[] = {'q', 'a'};
  unsigned long minDelay[] = {400, 900};
  unsigned long maxDelay[] = {410, 1000};
  Move(commands, 2, minDelay, maxDelay);
}

void CollectMoney_alley2() {
  char premove[] = {'e', 'd'};
  unsigned long minDelay[] = {400, 750};
  unsigned long maxDelay[] = {410, 850};
  Move(premove, 2, minDelay, maxDelay);
  delay(800);

  char commands[] = {'s', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'w', 'd', 'd', 'e', 'e'};
  unsigned long minDelay2[] = {900, 580, 580, 580, 580, 580, 580, 580, 700, 700, 1000, 650, 650};
  unsigned long maxDelay2[] = {1000, 600, 600, 600, 600, 600, 600, 600, 800, 800, 1100, 700, 700};
  Move(commands, 13, minDelay2, maxDelay2);
}

void CollectMoney_library4() {
  char premove[] = {'e', 'd'};
  unsigned long minDelay[] = {400, 750};
  unsigned long maxDelay[] = {410, 850};
  Move(premove, 2, minDelay, maxDelay);
  delay(800);

  char commands[] = {'s', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'w', 'd', 'd', 'e', 'd'};
  unsigned long minDelay2[] = {900, 580, 580, 580, 580, 580, 580, 580, 700, 700, 1000, 400, 900};
  unsigned long maxDelay2[] = {1000, 600, 600, 600, 600, 600, 600, 600, 800, 800, 1100, 450, 1000};
  Move(commands, 13, minDelay2, maxDelay2);
}

/************** 2-6 ***************/
void MoveToFountain_2_6() {
  unsigned long rand = random(4);
  if (rand == 0) {
    MoveToFountainA_2_6();
  } else if (rand == 1) {
    MoveToFountainB_2_6();
  } else if (rand == 2) {
    MoveToFountainC_2_6();
  } else if (rand == 3) {
    MoveToFountainD_2_6();
  }
}

void BackFromFountain_2_6() {
  unsigned long rand = random(2);
  if (rand == 0) {
    BackFromFountainA_2_6();
  } else if (rand == 1) {
    BackFromFountainB_2_6();
  } 
}

void MoveToFountainA_2_6() {
  char commands[] = {'a', 'a', 'w', 'r'};
  unsigned long minDelay[] = {550, 650, 900, 50};
  unsigned long maxDelay[] = {650, 750, 1000, 80};
  Move(commands, 4, minDelay, maxDelay);
}

void MoveToFountainB_2_6() {
  char commands[] = {'w', 'a', 'a', 'r'};
  unsigned long minDelay[] = {700, 550, 550, 250};
  unsigned long maxDelay[] = {750, 600, 600, 280};
  Move(commands, 4, minDelay, maxDelay);
}

void MoveToFountainC_2_6() {
  char commands[] = {'a', 'w', 'a', 'r'};
  unsigned long minDelay[] = {550, 700, 550, 250};
  unsigned long maxDelay[] = {600, 750, 600, 280};
  Move(commands, 4, minDelay, maxDelay);
}

void MoveToFountainD_2_6() {
  char commands[] = {'q', 'w', 'r'};
  unsigned long minDelay[] = {700, 400, 1000};
  unsigned long maxDelay[] = {750, 500, 1200};
  Move(commands, 3, minDelay, maxDelay);
}

void BackFromFountainA_2_6() {
  char commands[] = {'e', 'd'};
  unsigned long minDelay[] = {350, 1000};
  unsigned long maxDelay[] = {450, 1200};
  Move(commands, 2, minDelay, maxDelay);
}

void BackFromFountainB_2_6() {
  char commands[] = {'s', 'd', 'd'};
  unsigned long minDelay[] = {1100, 550, 700};
  unsigned long maxDelay[] = {1200, 600, 800};
  Move(commands, 3, minDelay, maxDelay);
}

void CollectMoney_2_6() {
  unsigned long rand = random(1);
  if (rand == 0) {
    CollectMoneyA_2_6();
  } else if (rand == 1) {

  }
}

void CollectMoneyA_2_6() {
  char commands[] = {'d', 'd', 'w', 'l', 'q', 'a'};
  unsigned long minDelay[] = {550, 550, 900, 200, 350, 1000};
  unsigned long maxDelay[] = {650, 650, 1000, 250, 450, 1200};
  Move(commands, 6, minDelay, maxDelay);
}

void CollectMoney_spring1() {
  MoveToFountain_library4();
  delay(800);
  char commands[] = {'s', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'w', 'd', 'd', 'e', 'x'};
  unsigned long minDelay[] = {900, 580, 580, 580, 580, 580, 580, 580, 700, 700, 1000, 650, 300};
  unsigned long maxDelay[] = {1000, 600, 600, 600, 600, 600, 600, 600, 800, 800, 1100, 700, 320};
  Move(commands, 13, minDelay, maxDelay);
}

void CollectMoney_fall1() {
  MoveToFountain_fall1();
  delay(800);
  char commands[] = {'e', 'e', 'a', 'a', 's', 'b', 's', 'e', 'd'};
  unsigned long minDelay[] = {580, 1300, 580, 580, 650, 700, 800, 400, 580};
  unsigned long maxDelay[] = {600, 1350, 600, 600, 660, 750, 810, 430, 600};
  Move(commands, 9, minDelay, maxDelay);
}

/* ============ Move to Fountain ============ */
void MoveToFountain() {
  // MoveToFountain_2_6();
  // MoveToFountain_library4();
  MoveToFountain_fall1();
  // MoveToFountain_eastside();
}

/* ============ Back from Fountain ============ */
void BackFromFountain() {
  // BackFromFountain_2_6();
  // BackFromFountain_library4();
  BackFromFountain_fall1();
  // BackFromFountain_eastside();
}

/* ============ Collect Money ============ */
void CollectMoney(bool collect, int graph) {
  if (collect == true) {
    // Collect money
    if (graph == 3) {
      CollectMoney_alley2();
    } else if (graph == 4) {
      CollectMoney_spring1();
    } else if (graph == 5) {
      CollectMoney_fall1();
    }
  }
}

/* ========================================== */
void WaitInput() {
  for (;Serial.available() <= 0;) {
    // Waiting input
  }
}
void ConsumeInput() {
  while (Serial.available()  > 0) {
    char c = Serial.read();
  }
}