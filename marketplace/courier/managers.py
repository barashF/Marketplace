from .models import ParcelLocker
from .models_choice import StatusParcelLocker


class ParcelLockerManager():
    #получение всех постаматов на данном адресе
    def get_parcel_lockers(self, address):
        parcel_lockers = ParcelLocker.objects.filter(address=address)
        return parcel_lockers
    
    #найти свободный постамат по адресу
    def get_free_parcel_locker(self, address):
        free_parcel_locker = ParcelLocker.objects.filter(address=address, 
                                                     status=StatusParcelLocker.FREE).first()

        return free_parcel_locker
            