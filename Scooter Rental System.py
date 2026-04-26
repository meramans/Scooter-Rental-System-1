from datetime import datetime


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.rental_history = []

    def view_rental_history(self):
        return self.rental_history


class Guest(User):
    def __init__(self, session_id):
        super().__init__(0, "Guest", "")
        self.session_id = session_id

    def register(self, user_id, name, email, password):
        return RegisteredUser(user_id, name, email, password)


class RegisteredUser(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email)
        self.__password = password

    def rent_scooter(self, scooter, duration_minutes):
        if scooter.status != "Available":
            raise Exception("Scooter is not available for rental.")
        rental = Rental(len(self.rental_history) + 1, self, scooter, duration_minutes)
        rental.start_rental()
        self.rental_history.append(rental)
        return rental

    def reserve_scooter(self, scooter):
        if scooter.status != "Available":
            raise Exception("Scooter cannot be reserved.")
        scooter.update_status("Reserved")
        return Reservation(self, scooter)


class Scooter:
    def __init__(self, scooter_id, scooter_type, battery_level, station):
        self.scooter_id = scooter_id
        self.scooter_type = scooter_type
        self.battery_level = battery_level
        self.status = "Available"
        self.station = station

    def update_status(self, status):
        self.status = status

    def unlock(self):
        if self.status in ["Available", "Reserved"]:
            self.status = "In Use"
        else:
            raise Exception("Scooter cannot be unlocked.")

    def report_fault(self, issue):
        self.status = "Maintenance"
        return MaintenanceRecord(self, issue)


class Station:
    def __init__(self, station_id, name, location, capacity):
        self.station_id = station_id
        self.name = name
        self.location = location
        self.capacity = capacity
        self.scooters = []

    def add_scooter(self, scooter):
        if len(self.scooters) >= self.capacity:
            raise Exception("Station capacity is full.")
        self.scooters.append(scooter)
        scooter.station = self
        scooter.update_status("Available")

    def remove_scooter(self, scooter):
        if scooter in self.scooters:
            self.scooters.remove(scooter)

    def available_scooters(self):
        return [s for s in self.scooters if s.status == "Available"]


class Rental:
    def __init__(self, rental_id, user, scooter, duration_minutes):
        self.rental_id = rental_id
        self.user = user
        self.scooter = scooter
        self.duration_minutes = duration_minutes
        self.start_time = None
        self.end_time = None
        self.total_cost = 0
        self.status = "Created"

    def start_rental(self):
        self.start_time = datetime.now()
        self.scooter.unlock()
        self.status = "Active"


def calculate_cost(self):
    rate = 0.50 if self.scooter.scooter_type == "Standard" else 0.80
    self.total_cost = self.duration_minutes * rate
    return self.total_cost


def end_rental(self, station):
    self.end_time = datetime.now()
    self.calculate_cost()
    station.add_scooter(self.scooter)
    self.status = "Completed"
    return self.total_cost


class Reservation:
    def __init__(self, user, scooter):
        self.user = user
        self.scooter = scooter
        self.status = "Confirmed"
        self.reservation_time = datetime.now()

    def cancel_reservation(self):
        self.status = "Cancelled"
        self.scooter.update_status("Available")


class MaintenanceRecord:
    def __init__(self, scooter, issue):
        self.scooter = scooter
        self.issue = issue
        self.repair_status = "Pending"
        self.created_at = datetime.now()

    def mark_repaired(self):
        self.repair_status = "Repaired"
        self.scooter.update_status("Available")


# Sample test
station = Station(1, "ZU Main Station", "Abu Dhabi Campus", 5)
scooter = Scooter(101, "Standard", 90, station)
station.add_scooter(scooter)
user = RegisteredUser(1, "Munera", "student@example.com", "1234")
rental = user.rent_scooter(scooter, 30)
cost = rental.end_rental(station)
print("Rental completed. Total cost:", cost)
print("Scooter status:", scooter.status)