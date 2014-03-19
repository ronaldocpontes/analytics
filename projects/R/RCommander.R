rm(list = ls())
gc()


csv = "QKITCH.csv"
csv = "store24.csv"


Dataset <- read.table(csv, header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
names(Dataset)
points_to_identify=4
### Transformations
Dataset$Crew.Tenure <- Dataset$SQRT.Crew.Tenure^2
Dataset$Manager.Tenure <- Dataset$SQRT.Manager.Tenure^2
Dataset$Manager.New <- Dataset$Manager.Tenure<20
Dataset$Small.Town <- Dataset$Population <5000
Dataset$Large.Footfall <- Dataset$Footfall==5
Dataset$Medium.Footfall <- Dataset$Footfall<5 & Dataset$Footfall>1
Dataset$Small.Footfall <- Dataset$Footfall==1

Dataset[c(18,19,20)]
Dataset$s = Dataset$Large.Footfall + Dataset$Medium.Footfall + Dataset$Small.Footfall
Dataset[c(18,19,20,21)]


Dataset$Manager.Tenure
Dataset$Manager.New
Dataset$Large.Footfall
Dataset$Small.Footfall
Dataset$Footfall
Dataset$Small.Footfall

### Remove Outliers
C_Dataset <- Dataset[-50,]



##
# Analyse Model Subsets
#
library(leaps, pos=4)
plot(regsubsets(Profit ~ Competitors + Footfall + Population + Residential 
                + SQRT.Crew.Tenure + SQRT.Manager.Tenure + Visibility + X24h, data=Dataset, 
                nbest=1, nvmax=9), scale='adjr2')




##
# Create Model
#
fit <- lm(Profit ~ Competitors + Footfall + Population + 
  Residential + SQRT.Crew.Tenure + SQRT.Manager.Tenure + Visibility + X24h, 
  data=Dataset)
c_fit <- lm(Profit ~ Competitors + Footfall + Population + 
            Residential + SQRT.Crew.Tenure + SQRT.Manager.Tenure + Visibility + X24h, 
          data=C_Dataset)

summary(fit)
t_fit = fit
summary(t_fit)$adj.r.squared
summary(t_fit<-update(t_fit, . ~ . + sqrt(SQRT.Crew.Tenure) + sqrt(SQRT.Manager.Tenure) - SQRT.Crew.Tenure -SQRT.Manager.Tenure))$adj.r.squared
summary(t_fit<-update(t_fit, . ~ . + log(Footfall)  -Footfall))$adj.r.squared
summary(t_fit<-update(fit, . ~ . + I(Crew.Tenure^(1)) -SQRT.Crew.Tenure ))$adj.r.squared
summary(t_fit<-update(t_fit, . ~ . + I(Population^(1/2)) -Population ))$adj.r.squared
summary(t_fit<-(update(t_fit, subset= Crew.Tenure < 11.5 & Manager.Tenure < 10000 &  SQRT.Manager.Tenure <13)))$adj.r.squared
summary(a_fit<-update(t_fit, . ~ . + I(Manager.Tenure^(1/2)) + Manager.New + Small.Town -SQRT.Manager.Tenure))$adj.r.squared
summary(a_fit<-update(a_fit, . ~ . -Visibility +Large.Footfall - Medium.Footfall -Footfall))$adj.r.squared
summary(a_fit)

summary(all_fit<-(update(a_fit, subset= Crew.Tenure > -1)))$adj.r.squared

summary(m_fit<-(update(a_fit, subset= Crew.Tenure < 11.5 &  SQRT.Manager.Tenure <15)))$adj.r.squared
summary(m_fit<-update(m_fit, . ~ . -I(Population^(1/2)) -Manager.New))$adj.r.squared
summary(m_fit<-update(m_fit, . ~ . -I(Crew.Tenure^(1)) +I(Crew.Tenure^(1/2)) ))$adj.r.squared
crPlots(m_fit)
summary(m_fit)
summary(all_fit<-(update(m_fit, subset= Crew.Tenure > -1)))$adj.r.squared


summary(m_fit<-(update(a_fit, subset= Crew.Tenure < 11.5)))$adj.r.squared
summary(m_fit<-update(m_fit, . ~ . -I(Population^(1/2)) ))$adj.r.squared
crPlots(m_fit)
summary(m_fit)


#Crew > 13 months: aR2 = .75
summary(l_fit<-(update(fit, subset= Crew.Tenure >= 13)))$adj.r.squared
summary(l_fit<-update(l_fit, . ~ . +Residential +Population -Visibility))$adj.r.squared
summary(l_fit<-update(l_fit, . ~ . - I(Population^(1/2)) -Population ))$adj.r.squared
summary(l_fit<-update(l_fit, . ~ . +Small.Town))$adj.r.squared
summary(l_fit)

crPlots(fit)
crPlots(l_fit)

names(Dataset)
summary(t_fit)
summary(l_fit)
summary(a_fit)
#compareCoefs(fit, t_fit)
avPlots(a_fit)
crPlots(l_fit)
crPlots(a_fit)
summary(c_fit)$adj.r.squared
compareCoefs(fit, c_fit)

Dataset$Small.Footfall
Dataset$Large.Footfall

##
# Component + Residual Plots
#

crPlots(fit, span=0.5)
#ceresPlots (fit, span=0.5)

##
# MARGINAL MODEL PLOTS
#
library("marginalmodelplots")
marginalModelPlots(fit)


##
# ADDED-VARIABLE PLOTS
# http://www.uk.sagepub.com/upm-data/38503_Chapter6.pdf
# The added-variable plot allows us to visualize the effect of each regressor after adjusting for all the other regressors in the model.
# The added-variable plot has several interesting and useful properties:
#  - The least-squares line on the added-variable plot for the regressor equal to the partial slope in the regression
#  - Extreme values (marked) are unusual data points
# 
show_ellipse=TRUE
#leveragePlots(fit,  id.n=points_to_identify/2, id.cex=0.6) # leverage plots
avPlots(fit, id.n=points_to_identify/2, id.cex=0.6, ellipse=show_ellipse, ellipse.args=list(robust=TRUE))
avPlots(c_fit, id.n=points_to_identify/2, id.cex=0.6, ellipse=show_ellipse, ellipse.args=list(robust=TRUE))

if(show_ellipse) avPlots(fit, id.n=points_to_identify/2, id.cex=0.6, ellipse=show_ellipse)

##
# Unusual Data
# Unusual data in regression include outliers, high-leverage points, and in?uential observations
####
outlierTest(fit)

##
# OUTLIERS AND quantile-comparison plot of STUDENTIZED RESIDUALS
# Unusual data in regression include outliers, high-leverage points, and in?uential observations
####
qqPlot(fit, simulate=TRUE, id.method="y", id.n=points_to_identify)

##
# INFLUENCE PLOT - UNUSUAL POINTS
# LEVERAGE: HAT-VALUES, COOK'S DISTANCE, BONFERRONI P-VALUE
# *** look for Bonferroni p-values much lesser than 1 ***
####

influenceIndexPlot(fit, id.n=points_to_identify)

#A bubble-plot, combining the display of Studentized residuals, hat-values, and Cook?s distances, with the areas of the circles proportional to Cook?s D
influencePlot(fit, id.n=points_to_identify)


