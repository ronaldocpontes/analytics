__author__ = 'Ronaldo'

import logging
logging.basicConfig()
log = logging.getLogger("Flight")
log.setLevel(logging.INFO)

class Product:

    def __init__(self, name="Unamed Product"):
        self.name = name
        self.price = 0
        self.space = 1.5
        self.cost = 0
        self.profits = 0
        self.passengers = 0

        self.upgrades=[self]
        self.substitutes=[]

    def add_upgrade(self,upgrade):
        self.upgrades.append(upgrade)

    def order_by_preference(self):
        results = [u for u in self.upgrades if u.space == 5]

    def show_names(self,products_list):
        return [p.name for p in products_list]

    def sort_by_consumer_surplus(self, willingness_to_pay=[]):
        return sorted(self.upgrades, key=lambda upgrade: upgrade.price, reverse=True)



    def select_best_product(self):
        pass

    def __repr__(self):
        #return "%s(%r)" % (self.__class__, self.__dict__)
        properties = self.__dict__.copy()
        properties['upgrades'] = (len(self.upgrades) -1)

        return "%s:%s%r" % (self.__class__.__name__,id(self),properties )






p = Product('Economy')
p.price = 50

u = Product('Business')
u.price = 100
p.upgrades.append(u)

print p.price
print p

print "%s" % p.show_names(p.sort_by_consumer_surplus())
exit()

class Flight2:

    def __init__(self):
        pass

    plane_space  = 60

    __classes = []

    @__classes.setter
    def addClass(self, flightClass):
        if not isinstance(flightClass,Product):
            raise Exception("Not a FlightClass instance")
        self.__classes.append(flightClass)




    def addPassenger(self, willingness_e, willingness_b, check_seats = False, check_space = False):

        e_surplus = willingness_e - self.economy_fare
        b_surplus = willingness_b - self.business_fare
        log.debug("... Adding Passenger %s %s", willingness_e, willingness_b)
        log.debug("    Economy Surplus %s", e_surplus)
        log.debug("    Business Surplus %s", b_surplus)


        if check_space and self.space_left() < self.business_seat_space and self.space_left() < self.economy_seat_space:
            raise Exception("No more space for any additional seat", self.stats())

        if check_seats and self.business_passengers >= self.business_seats and self.economy_passengers >= self.economy_seats:
            raise Exception("Flight is fully booked", self.stats())


        if b_surplus == e_surplus:
            log.debug("EQUAL SURPLUSSES")

        if b_surplus < 0 and  e_surplus < 0:
            log.debug("Fares are too high for this passenger")
            return

        if b_surplus >= e_surplus:
            log.warn("    BUSINESS")
            ok = True
            if check_space and self.space_left() < self.business_seat_space:
                log.info("No more space for an additional business seat\n%s", self.stats())
                ok = False

            if check_seats and self.business_passengers >= self.business_seats:
                log.info("No more business seats\n%s", self.stats())
                ok = False

            if ok:
                self.business_passengers+=1
                self.business_profits += self.business_fare - self.business_cost

        elif e_surplus >= 0:
            log.debug("    ECONOMY")
            ok = True
            if check_space and self.space_left() < self.economy_seat_space:
                log.info("No more space for an additional economy seat\n%s", self.stats())
                ok=False

            if check_seats and self.economy_passengers >= self.economy_seats:
                log.info("No more economy seats\n%s", self.stats())
                ok=False

            if ok:
                self.economy_passengers+=1
                self.economy_profits += self.economy_fare - self.economy_cost
        else:
            raise Exception("Allocation problem")
        log.debug("   %s", self.stats())


    def total_profits(self):
        return self.economy_profits + self.business_profits

    def space_left(self):
        return self.plane_space - self.used_space()

    def used_space(self):
        return self.business_seat_space * self.business_passengers + self.economy_seat_space * self.economy_passengers


    def stats(self):
        str= "Total Profits:", self.total_profits()
        str+= "Economy Fare: ", self.economy_fare
        str+= "Business Fare: ", self.business_fare

        str+= "Business Passengers:", self.business_passengers
        str+= "Economy Passengers:", self.economy_passengers
        str+= "Business Profits: ", self.business_profits
        str+= "Economy Profits:", self.economy_profits
        str+= "Used Space:", self.used_space()
        str+= "Space Left:", self.space_left()
        return str