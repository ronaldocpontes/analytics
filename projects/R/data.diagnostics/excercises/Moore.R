library(car)
options(contrasts=c("contr.sum", "contr.poly")) # use deviation regressors (not really necessary)

Moore$fcategory <- factor(Moore$fcategory, c("low", "medium", "high")) # reorder levels
Moore$partner.status <- factor(Moore$partner.status, c("low", "high"))

moore.anova <- lm(conformity ~ fcategory*partner.status, data=Moore) # fit ANOVA model
Anova(moore.anova)

# unusual data diagnostics

influencePlot(moore.anova)
av.plots(moore.anova, ask=FALSE)
outlier.test(moore.anova)

# plot means with and without subjects 16 and 19

with(Moore, interaction.plot(fcategory, partner.status, conformity,
    type="b", main="With Subjects 16 and 19"))
with(Moore[-c(16,19),] , interaction.plot(fcategory, partner.status, conformity,
    type="b", main="Removing Subjects 16 and 19"))

moore.anova.1 <- update(moore.anova, subset=-c(16, 19)) # redo analysis
Anova(moore.anova.1)

# Alternative ANCOVA (or dummy regression)

scatterplot(conformity ~ fscore|partner.status, data=Moore, smooth=FALSE, labels=1:45)

Moore$fscored <- with(Moore, fscore - mean(fscore)) # mean deviations (not strictly necessary)
moore.ancova <- lm(conformity ~ fscored*partner.status, data=Moore) # fit ANCOVA model
summary(moore.ancova)

# unusual data diagnostics

influencePlot(moore.ancova)
av.plots(moore.ancova, ask=FALSE)
outlier.test(moore.ancova)

# remove influential obs.

moore.ancova.1 <- update(moore.ancova, subset=-c(16, 19))
summary(moore.ancova.1)
moore.ancova.2 <- update(moore.ancova, subset=-c(16, 19, 23))
summary(moore.ancova.2)
moore.ancova.3 <- update(moore.ancova, subset=-c(16, 19, 23, 36))
summary(moore.ancova.3)

# fit of original and final models

library(effects)
plot(effect("fscored:partner.status", moore.ancova), multiline=TRUE)
plot(effect("fscored:partner.status", moore.ancova.3), multiline=TRUE)
