#include <Servo.h>  
Servo myservoA;  
Servo myservoB;
Servo myservoC;
Servo myservoD;
Servo myservoE;
Servo myservoF;
int i,pos,myspeed,myshow;
int sea,seb,sec,sed,see,sef;
static int v=0;

String mycommand="";    /// Serial capture   #auto: automatic operation  #com: computer serial port control  #stop: standstill
static int mycomflag=2; // #auto：2 automatic operation  , #com： 1  computer serial port control    #stop：0  standstill 


void myservosetup()  //initialization
{
   sea=myservoA.read();
   seb=myservoB.read();
   sec=myservoC.read();
   sed=myservoD.read();
   see=myservoE.read();
   sef=myservoF.read();
   
   myspeed=500;
   for(pos=0;pos<=myspeed;pos+=1)
   {
    myservoA.write(int(map(pos,1,myspeed,sea,66)));
    myservoB.write(int(map(pos,1,myspeed,seb,60)));
    myservoC.write(int(map(pos,1,myspeed,sec,20)));
    myservoD.write(int(map(pos,1,myspeed,sed,60)));
    myservoE.write(int(map(pos,1,myspeed,see,90)));
    myservoF.write(int(map(pos,1,myspeed,sef,90)));    
    delay(1);
   }
}

void setup() 
{ 
  pinMode(13,INPUT);
  pinMode(12,INPUT);  
  Serial.begin(9600);
  myshow=0;
  mycomflag=2;         // the  ARM default  state: 2 automatic operation
  myservoA.attach(3);  //  Control waist (A) port number is   3    
  myservoB.attach(5);  //  Control lorearm（B）port number is 5    
  myservoC.attach(6);  //  Control  Forearm（C）port number is 6
  myservoD.attach(9);  // Control Forearm rotation (D) port number is 9
  myservoE.attach(10); // Control wrist（E）port number is 10 wrist
  myservoF.attach(11); // Control wrist rotation (F) port number is 9
  
  myservoA.write(66);
  myservoB.write(60);
  myservoC.write(20);
  myservoD.write(60);
  myservoE.write(90);
  myservoF.write(90);    

}

void loop() 
{ 
  while (Serial.available() > 0)  
    {
        mycommand += char(Serial.read());
        delay(2);
    }
    if (mycommand.length() > 0)
    {
        if(mycommand=="#auto")
        {
          mycomflag=2;
          Serial.println("auto station");
          mycommand="";
        }
        if(mycommand=="#com")
        {
          mycomflag=1;
          Serial.println("computer control station");
          mycommand="";
          myservosetup();
        }
        if(mycommand=="#stop")
        {
          mycomflag=0;
          Serial.println("stop station");
          mycommand="";
        }
        
    }
  
  
  if(mycomflag==1)  //if  read myconflag==1 means computer serial port control
  {      
 
   for(int m=0;m<mycommand.length();m++) // 
  {
    char ch = mycommand[m];   //Read serial data
    switch(ch)
    {
      case '0'...'9':
      v = v*10 + ch - '0';   //Character conversion to decimal
      break;
      
      
      
      case 'a':             //If you post data with a, it means that the first servo data, such as serial port 85a
      if(v >= 5 || v <= 175 ) myservoA.write(v); 
      v = 0;
      break;

      case 'b':   //If you post data with b, it means that the second servo data, such as serial port 85b

      myservoB.write(v);   //For setting the steering angle of rotation of the statement can be set angle range is 0 ° to 180 °, 
                           // "V" get the value of the input and change the angle, such as 90b is 90°
      v = 0;
      break;
      case 'c':   
      if(v >= 20 ) myservoC.write(v);   
      v = 0;
      break;
      case 'd':  
      myservoD.write(v);   
      v = 0;
      break;
      case 'e':  
      myservoE.write(v);   
      v = 0;
      break;
      case 'f':  
      myservoF.write(v);   
      v = 0;
      break;
    }
   
    }  
   mycommand="";
  }  // end if(mycomflag=2)
  
  if(mycomflag==2)  //if mycomflag==2  means automatic operation
  {    
   delay(3000); 
   //Serial.println("auto station"); 
   myservosetup();
   myspeed=600;
    for(pos = 0; pos <=myspeed; pos += 1)  
  {                                
    myservoA.write(int(map(pos,1,myspeed,66,10))); //Let A rotation from 66 degrees to 90 degrees (angle can be modified)1
    myservoB.write(int(map(pos,1,myspeed,60,100))); //Let B rotation from 60 degrees to 100 degrees (angle can be modified)
    delay(1);                       
  }
   delay(1000);
   myspeed=500;
  for(pos = 0; pos <=myspeed; pos += 1)  
  {                                
    myservoC.write(int(map(pos,1,myspeed,20,40))); // 30-65
    myservoD.write(int(map(pos,1,myspeed,60,100))); //  4
    myservoE.write(int(map(pos,1,myspeed,90,40))); //
    delay(1);                       
   }
   delay(1000);
  myspeed=1000;
  for(pos = 0; pos <=myspeed; pos += 1)  
  {                                
    myservoB.write(int(map(pos,1,myspeed,100,120))); // 
//    myservoC.write(int(map(pos,1,myspeed,40,50))); //
    delay(1);                       
   }
     delay(1000);
   myspeed=500;
  for(pos = 0; pos <=myspeed; pos += 1)  
  {                                
//    myservoC.write(int(map(pos,1,myspeed,50,40))); // 
    myservoD.write(int(map(pos,1,myspeed,100,70))); //
    myservoE.write(int(map(pos,1,myspeed,40,90)));
    myservoF.write(int(map(pos,1,myspeed,90,50)));
    delay(1);                       
   }   
   delay(1000);
   myspeed=1000;
  for(pos = 0; pos <=myspeed; pos += 1)  
  {                                
    myservoA.write(int(map(pos,1,myspeed,10,100))); // 
    myservoF.write(int(map(pos,1,myspeed,50,110)));    
    delay(1);                       
   }  
    delay(1000);
    myspeed=500;
    for(pos = 0; pos <=myspeed; pos += 1)  
  {                                
    myservoA.write(int(map(pos,1,myspeed,100,50))); //
    myservoC.write(int(map(pos,1,myspeed,40,50))); // 
    myservoB.write(int(map(pos,1,myspeed,120,70))); //
    myservoE.write(int(map(pos,1,myspeed,90,60))); //
    delay(1);                       
  } 
  }
  
  if(mycomflag==0) // Static state
  {
   myservosetup();
  }
}
