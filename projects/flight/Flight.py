__author__ = 'Ronaldo'

import logging
logging.basicConfig()
log = logging.getLogger("Flight")
log.setLevel(logging.INFO)


class Flight:

    plane_space  = 60

    business_seat_space = 1.5
    business_fare = 0
    business_cost = 0
    business_profits = 0

    economy_seat_space = .5
    economy_seats = 0
    economy_fare = 0
    economy_cost = 0
    economy_profits = 0

    business_passengers = 0
    economy_passengers = 0


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
            log.debug("    BUSINESS")
            ok = True
            if check_space and self.space_left() < self.business_seat_space:
                log.info("No more space for an additional business seat!")
                ok = False

            if check_seats and self.business_passengers >= self.business_seats:
                log.info("No more business seats!")
                ok = False

            if ok:
                self.business_passengers+=1
                self.business_profits += self.business_fare - self.business_cost
                log.debug("   %s", self.stats())
                return

        if e_surplus >= 0:
            log.debug("    ECONOMY")
            ok = True
            if check_space and self.space_left() < self.economy_seat_space:
                log.info("No more space for an additional economy seat!")
                ok=False

            if check_seats and self.economy_passengers >= self.economy_seats:
                log.info("No more economy seats!")
                ok=False

            if ok:
                self.economy_passengers+=1
                self.economy_profits += self.economy_fare - self.economy_cost
                log.debug("   %s", self.stats())
                return

        if b_surplus < 0:
            log.debug("   %s", self.stats())
            return
        else:
            log.debug("    Back to BUSINESS")
            ok = True
            if check_space and self.space_left() < self.business_seat_space:
                log.info("No more space for an additional business seat!")
                ok = False

            if check_seats and self.business_passengers >= self.business_seats:
                log.info("No more business seats!")
                ok = False

            if ok:
                self.business_passengers+=1
                self.business_profits += self.business_fare - self.business_cost
                log.debug("   %s", self.stats())
                return



        raise Exception("Allocation problem")



    def total_profits(self):
        return self.economy_profits + self.business_profits

    def space_left(self):
        return self.plane_space - self.used_space()

    def used_space(self):
        return self.business_seat_space * self.business_passengers + self.economy_seat_space * self.economy_passengers


    def stats(self):
        return self.__dict__
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