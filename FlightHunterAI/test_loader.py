from app.data.airport_service import AirportService

service = AirportService()

print()

print("========== Buscar Guadalajara ==========")

for aeropuerto in service.buscar("Guadalajara")[:5]:
    print(aeropuerto)

print()

print("========== Buscar GDL ==========")

print(service.buscar("GDL"))

print()

print("========== Buscar Narita ==========")

print(service.buscar("Narita"))