/*

    Copyright (C) 2017 Libelium Comunicaciones Distribuidas S.L.
   http://www.libelium.com

    By using it you accept the MySignals Terms and Conditions.
    You can find them at: http://libelium.com/legal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Version:           2.0
    Design:            David Gascon
    Implementation:    Luis Martin / Victor Boria
*/
#include <Adafruit_GFX_AS.h>
#include <Adafruit_ILI9341_AS.h>
#include <MySignals.h>
#include "Wire.h"
#include "SPI.h"

Adafruit_ILI9341_AS tft = Adafruit_ILI9341_AS(TFT_CS, TFT_DC);

int glucometer = 0;
char hun, ten, one;

void setup()
{
  Serial.begin(115200);

  MySignals.begin();

  MySignals.initSensorUART();
  MySignals.enableSensorUART(GLUCOMETER);
  delay(1000);
  MySignals.getGlucose();
  MySignals.serialFlush();
  Serial.begin(115200);
  glucometer = MySignals.glucometerData[0].glucose;
  Serial.println(glucometer);
  MySignals.disableSensorUART();

//  tft.init();
//  tft.setRotation(2);
//  tft.fillScreen(ILI9341_BLACK);
//  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
//  tft.drawString("Your arduino number is: 123456", 0, 0, 2);
//  tft.drawString("Glucometer:", 0, 15, 2);
//  tft.drawNumber(glucometer, 100, 15, 2);

  hun = glucometer / 100 + '0';
  ten = (glucometer / 10) % 10 + '0';
  one = glucometer % 10 + '0';
  //Enable WiFi ESP8266 Power -> bit1:1
  bitSet(MySignals.expanderState, EXP_ESP8266_POWER);
  MySignals.expanderWrite(MySignals.expanderState);

  MySignals.initSensorUART();

  MySignals.enableSensorUART(WIFI_ESP8266);
  delay(1000);

  // Checks if the WiFi module is started
  int8_t answer = sendATcommand("AT", "OK", 6000);
  if (answer == 0)
  {
    MySignals.println("Error");
    // waits for an answer from the module
    while (answer == 0)
    {
      // Send AT every two seconds and wait for the answer
      answer = sendATcommand("AT", "OK", 6000);
    }
  }
  else if (answer == 1)
  {

    MySignals.println("WiFi succesfully working!");


    if (sendATcommand("AT+CWMODE=1", "OK", 6000))
    {
      MySignals.println("CWMODE OK");
    }
    else
    {
      MySignals.println("CWMODE Error");

    }


    //Change here your WIFI_SSID and WIFI_PASSWORD
    if (sendATcommand("AT+CWJAP=\"Hiphone\",\"zhao123456\"", "OK", 20000))
    {
      MySignals.println("Connected!");
      if (sendATcommand("AT+CIPSTART=\"TCP\",\"18.220.113.18\",8000", "OK", 100000)) {
        MySignals.println("Connected to google!");
        sendATcommand("AT+CIPSEND=111", "OK", 100000);
        char *httprequest = "GET /diabetes/arduino/?arduino_board_no=123456&glucose=000 HTTP/1.1\r\nHost: 172.20.10.2:8000\r\nConnection: close\r\n";
        httprequest[55] = hun;
        httprequest[56] = ten;
        httprequest[57] = one;
        sendATcommand(httprequest, "OK", 20000);
        sendATcommand("AT+CIPCLOSE", "OK", 20000);
      } else {
        MySignals.println("Error of TCP");
      }
    }
    else
    {
      MySignals.println("Error");
    }

    
  }
}

void loop()
{ 
  
  delay(5000);
}



int8_t sendATcommand(char* ATcommand, char* expected_answer1, unsigned int timeout)
{

  uint8_t x = 0,  answer = 0;
  char response[500];
  unsigned long previous;

  memset(response, '\0', sizeof(response));    // Initialize the string

  delay(100);

  while ( Serial.available() > 0) Serial.read();   // Clean the input buffer

  delay(1000);
  Serial.println(ATcommand);    // Send the AT command

  x = 0;
  previous = millis();

  // this loop waits for the answer
  do
  {

    if (Serial.available() != 0)
    {
      response[x] = Serial.read();
      x++;
      
      // check if the desired answer is in the response of the module
      if (strstr(response, expected_answer1) != NULL)
      {
        answer = 1;
        //MySignals.println(response);
      }
    }
    // Waits for the asnwer with time out
  }while ((answer == 0) && ((millis() - previous) < timeout));
  MySignals.print("Response: ");
  MySignals.println(response);
  return answer;
}



    
