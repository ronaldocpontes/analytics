library(car)
mod.1 <- lm(prestige ~ income + education + women, data=Prestige)
summary(mod.1)

# distribution of studentized residuals

par(mfrow=c(1, 3))
plot(density(rstudent(mod.1)))
qq.plot(rstudent(mod.1))
boxplot(rstudent(mod.1))

# non-constant variance

plot(fitted(mod.1), rstudent(mod.1))
abline(h=0)

spread.level.plot(mod.1)

ncv.test(mod.1)
ncv.test(mod.1, var= ~ income + education + women, data=Prestige)

# nonlinearity

cr.plots(mod.1, ask=FALSE)

mod.2 <- lm(prestige ~ log(income, 2) + education + poly(women, degree=2, raw=TRUE), data=Prestige)
summary(mod.2)

library(effects)
plot(allEffects(mod.2, default.levels=100), ask=FALSE)

cr.plots(mod.2, ask=FALSE)

box.tidwell(prestige ~ income,
    other.x = ~ education + poly(women, degree=2, raw=TRUE), data=Prestige)

mod.bt <- lm(prestige ~ income + education + poly(women, degree=2, raw=TRUE)
    + I(income*log(income)), data=Prestige)
av.plot(mod.bt, "I(income * log(income))")

# alternative view of the data

scatterplot.matrix(~ prestige + income + education + women | type, 
    span=1, by.groups=TRUE, data=Prestige)
    
mod.3 <- lm(prestige ~ (income + education + women)*type, data=Prestige)
Anova(mod.3)
plot(allEffects(mod.3), ask=FALSE)

mod.4 <- lm(prestige ~ (income + women)*type + education, data=Prestige)
plot(allEffects(mod.4), ask=FALSE)
