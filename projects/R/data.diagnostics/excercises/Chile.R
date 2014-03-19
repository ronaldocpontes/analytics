library(car)
Chile$yes <- as.factor(ifelse(Chile$vote == "Y", "yes", 
    ifelse(Chile$vote == "N", "no", NA)))
with(Chile, table(yes, vote, exclude=NULL))
Chile$education <- factor(Chile$education, level=c("P", "S", "PS")) # reorder levels
mod.chile <- glm(yes ~ region + population + sex + age + education + income, 
    family=binomial, data=Chile)
summary(mod.chile)
Anova(mod.chile)
library(effects)
plot(allEffects(mod.chile), ask=FALSE)

# unusual data diagnostics
influencePlot(mod.chile)
dfbs <- dfbetas(mod.chile)
nms <- colnames(dfbs)
par(mfrow=c(3,4))
for (name in nms) plot(dfbs[, name], ylab=name)

# nonlinearity
par(mfrow=c(2,2))
for (var in c("population", "age", "income")) cr.plot(mod.chile, var)

# tests of "lack of fit"
table(Chile$population)
table(Chile$income)

mod.chile.1 <- glm(yes ~ region + as.factor(population) + sex + age + education 
    + as.factor(income), family=binomial, data=Chile)
deviance(mod.chile.1)
mod.chile.2 <- glm(yes ~ region + population + sex + age + education 
    + as.factor(income), family=binomial, data=Chile)
deviance(mod.chile.2)
anova(mod.chile.2, mod.chile.1, test="Chisq") # test for nonlinearity of population

mod.chile.3 <- glm(yes ~ region + as.factor(population) + sex + age + education 
    + income, family=binomial, data=Chile)
deviance(mod.chile.3)
anova(mod.chile.3, mod.chile.1, test="Chisq") # test for nonlinearity of income
