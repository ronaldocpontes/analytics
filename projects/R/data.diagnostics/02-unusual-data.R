##-------------------------------------------------##
##            Regression Diagnostics               ##
##                  John Fox                       ##
##                FIOCRUZ Brasil                   ##
##                November 2009                    ##
##                                                 ##
##                Unusual Data                     ##
##                                                 ##
##-------------------------------------------------##

# Preliminary example

library(car)

scatterplot(repwt ~ weight|sex, smooth=FALSE, labels=rownames(Davis), data=Davis)

scatterplot(weight ~ repwt|sex, smooth=FALSE, labels=rownames(Davis), data=Davis)

davis.1 <- lm(repwt ~ weight*sex, data=Davis)
summary(davis.1)

davis.2 <- lm(weight ~ repwt*sex, data=Davis)
summary(davis.2)

fix(Davis)

Davis[11:13,]

davis.1.fixed <- update(davis.1)
summary(davis.1.fixed)

# hat-values

plot(hatvalues(davis.1))
abline(h=c(2,3)*4/183)  # twice and three-times average hat-value
identify(1:183, hatvalues(davis.1))

max(hatvalues(davis.1))
which.max(hatvalues(davis.1))

# studentized residuals

plot(rstudent(davis.1))
abline(h=c(-2, 0, 2))
identify(1:183, rstudent(davis.1))

max(abs(rstudent(davis.1)))
which.max(abs(rstudent(davis.1)))

183*2*(1 - pt(24.3, 178))   # Bonferroni p-value
183*2*pt(24.3, 178, lower.tail=FALSE)  # more accurate

outlier.test(davis.1)

qq.plot(davis.1, simulate=TRUE)

# Cook's distances

plot(cookd(davis.1))
abline(h=4/178)   # cutoff
identify(1:183, cookd(davis.1))

max(cookd(davis.1))
which.max(cookd(davis.1))

# partial-regression (added-variable) plots

duncan <- lm(prestige ~ income + education, data=Duncan)
summary(duncan)

av.plots(duncan, labels=rownames(Duncan))

which.names(c("minister", "conductor"), Duncan)

influencePlot(duncan, labels=rownames(Duncan))

qq.plot(duncan, simulate=TRUE)

outlier.test(duncan)

duncan.2 <- update(duncan, subset= -c(6,16)) # removing ministers & conductors
summary(duncan.2)
