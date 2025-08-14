#Yazar: Nazife CEYLAN

import time                                    # Zaman gecikmesi  modülü
from libreVNA import libreVNA                  # LibreVNA kütüphanesini içe aktarır

vna = libreVNA(host='localhost', port=19542)   # LibreVNA cihazına bağlanır

response = vna.query('*IDN?')                  # Cihaz kimliğini sorgular
print("Cihaz Bilgisi:", response)              # Cihaz kimliğini ekrana yazdırır

vna.cmd(":DEV:CONN")                           # Cihazla bağlantıyı başlatır
dev = vna.query(":DEV:CONN?")                  # Bağlantı durumunu sorgular
if dev == "Not connected":                     # Eğer bağlı değilse
    print("Cihaz ile bağlantı kurulamadı.")  
    exit(-1)                                   # Programdan çıkar
else:
    print("Bağlantı Kuruldu: " + dev)          # Cihazla bağlantı kurulur 


vna.cmd(":DEV:MODE VNA")                       # Cihazı VNA moduna alır
vna.cmd(":VNA:SWEEP FREQUENCY")                # Sweep türünü frekans olarak ayarlar
vna.cmd(":VNA:STIM:LVL -10")                   # Uyarıcı sinyal seviyesini ayarlar (-10dBm)
vna.cmd(":VNA:ACQ:IFBW 100")                   # IF bant genişliğini ayarlar (100 Hz)
vna.cmd(":VNA:ACQ:AVG 1")                      # Ortalama alınacak ölçüm sayısını ayarlar (1)
vna.cmd(":VNA:ACQ:POINTS 501")                 # Ölçümde kullanılacak nokta sayısını ayarlar (501)
vna.cmd(":VNA:FREQ:START ")          # Başlangıç frekansını ayarlar
vna.cmd(":VNA:FREQ:STOP ")           # Bitiş frekansını ayarlar 
 

vna.cmd(":VNA:CAL:RESET")                      # Önceki kalibrasyonları sıfırlar
vna.cmd(":VNA:CAL:TYPE FULL2PORT")             # İki portlu kalibrasyon

#Port 1 için kalibrasyon adımları
vna.cmd(":VNA:CAL:PORT 1")                     # Port 1 aktif hale getirir

print("Port 1 - SHORT")               
vna.cmd(":VNA:CAL:STANDARD SHORT")             # Kısa devre standardının bağladığını belirtir
vna.cmd(":VNA:CAL:MEAS")                       # Ölçümü gerçekleştirir                           
time.sleep(0.5)

print("Port 1 - OPEN")
vna.cmd(":VNA:CAL:STANDARD OPEN")              # Açık devre standardının bağladığını belirtir
vna.cmd(":VNA:CAL:MEAS")                       # Ölçümü gerçekleştirir
time.sleep(0.5)

print("Port 1 - LOAD")
vna.cmd(":VNA:CAL:STANDARD LOAD")              # 50 ohm yük standardının bağladığını belirtir
vna.cmd(":VNA:CAL:MEAS")                       # Ölçümü gerçekleştirir
time.sleep(0.5)

#Port 2 için kalibrasyon adımları
vna.cmd(":VNA:CAL:PORT 2")                     # Port 2 aktif hale getir

print("Port 2 - SHORT")
vna.cmd(":VNA:CAL:STANDARD SHORT")             # Kısa devre standardının bağladığını belirtir
vna.cmd(":VNA:CAL:MEAS")                       # Ölçümü gerçekleştirir
time.sleep(0.5)

print("Port 2 - OPEN")
vna.cmd(":VNA:CAL:STANDARD OPEN")              # Açık devre standardının bağladığını belirtir
vna.cmd(":VNA:CAL:MEAS")                       # Ölçümü gerçekleştirir
time.sleep(0.5)

print("Port 2 - LOAD")
vna.cmd(":VNA:CAL:STANDARD LOAD")              # 50 ohm yük standardının bağladığını belirtir
vna.cmd(":VNA:CAL:MEAS")                       # Ölçümü gerçekleştirir
time.sleep(0.5)

#THRU ölçümü
print("THRU bağlantısı")              
vna.cmd(":VNA:CAL:STANDARD THRU")              # Port 1 ve 2 birbirine bağlı (THRU) olduğunu belirtir
vna.cmd(":VNA:CAL:MEAS")                       # Geçiş ölçümünü gerçekleştirir
time.sleep(0.5)


vna.cmd(":VNA:CAL:SAVE")                       # Kalibrasyon verilerini kaydeder
vna.cmd(":VNA:CAL:ACT")                        # Kalibrasyonu aktif hale getirir


