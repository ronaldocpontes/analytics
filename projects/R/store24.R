# https://2780fa3c-a-62cb3a1a-s-sites.googlegroups.com/site/rdatamining/docs/RDataMining.pdf?attachauth=ANoY7cqVd6sPk18nTn65enjnpoSSEDWgFlcCNuCyYkXhuvBhauMVBXUyUtJT-E6ESxlaLSvcFc98zvMqFzPFxk_G7FIdbe5jOWiOfftkjuMrY8keAc4vOifLUOlKHe6GGu7XZ6V_HC0kwUsh3S-0a7x9Y5ilD1N0O_da4rd5FfcAtzDOoDigfevVUJb5jB2D3xibhuhGfqyriJUwAjPGf32DBQ3lw8cOaGAly0YisHVNjpZlw0R1dHM%3D&attredirects=0

# R Data Analysis Examples: Robust Regression
#  - http://www.ats.ucla.edu/stat/r/dae/rreg.htm


rm(list = ls())
gc()

require(foreign)
require(MASS)

storeData <- read.csv("store24.csv")
names(storeData)
#begin by running an OLS regression 
summary(ols <- lm(Profit ~ SQRT.Manager + SQRT.Crew + Competitors + Footfall + Residential + Population + X24h + Visibility, data = storeData))

opar <- par(mfrow = c(2, 2), oma = c(0, 0, 1.1, 0))
plot(ols, las = 1)
par(opar)

# Outliars Detection
# ===================================
## Outlier: In linear regression, an outlier is an observation with large residual. In other words, it is an observation whose dependent-variable value is unusual given its value on the predictor variables. An outlier may indicate a sample peculiarity or may indicate a data entry error or other problem.
## Residual: The difference between the predicted value (based on the regression equation) and the actual, observed value.
## Cook's distance (or Cook's D): A measure that combines the information of leverage and residual of the observation.
## Leverage: An observation with an extreme value on a predictor variable is a point with high leverage. Leverage is a measure of how far an independent variable deviates from its mean. High leverage points can have a great amount of effect on the estimate of regression coefficients.
## Influence: An observation is said to be influential if removing the observation substantially changes the estimate of the regression coefficients.  Influence can be thought of as the product of leverage and outlierness.

COOKS.DISTANCE <- cooks.distance(ols)
STD.RESIDUAL <- stdres(ols)
a <- cbind(storeData, COOKS.DISTANCE, STD.RESIDUAL)
cuttting_point <- 4/nrow(storeData)
a[COOKS.DISTANCE >cuttting_point, ]

# Select datapoints for viewing
# storeData[c(9, 25, 51), 1:2]

#summary(storeData)
#str(storeData)
#attributes(storeData)
cor(storeData)
#var(storeData)
pairs(storeData)
aggregate(Sales ~ X24.Hours, summary, data=storeData)
boxplot(Sales~Visibility, data=storeData)
with(storeData, plot(Sales, Profit.Margin, col=Visibility, pch=as.numeric(Visibility)))

## PLOTS...
    hist(storeData$Manager.Tenure)
    plot(density(storeData$Manager.Tenure))
    table(storeData$X24.Hours)
    barplot(table(storeData$X24.Hours))
    pie(table(storeData$X24.Hours))

    distMatrix <- as.matrix(dist(storeData[,1:4]))
    heatmap(distMatrix)

### FITTING

    fit <- lm(storeData$Sales ~ storeData$Manager.Tenure + storeData$X24.Hours)
    fit
    attributes(fit)
    fit$coefficients
    summary(fit)
    plot(residuals(fit))
    plot(fit)
    layout(matrix(c(1,2,3,4),2,2)) # 4 graphs per page
    plot(fit)
    layout(matrix(1)) # change back to one graph per page


    library(scatterplot3d)
    s3d <- scatterplot3d(storeData$Manager.Tenure, storeData$X24.Hours, storeData$Sales, highlight.3d=T, type="h", lab=c(2,3))
    s3d$plane3d(fit)



### CLUSTERING

set.seed(8953)
(kmeans.result <- kmeans(storeData, 3))
table(iris$Species, kmeans.result$cluster)


library(fpc)
pamk.result <- pamk(iris2)
# number of clusters
pamk.result$nc
# check clustering against actual species
table(pamk.result$pamobject$clustering, iris$Species)

layout(matrix(c(1,2),1,2)) # 2 graphs per page
plot(pamk.result$pamobject)
layout(matrix(1)) # change back to one graph per page



#### OUTLIARS
    library(DMwR)
    # remove "Species", which is a categorical column
    iris2 <- iris[,1:4]
    outlier.scores <- lofactor(iris2, k=5)
    plot(density(outlier.scores))


    ###################################################
    ### code chunk number 7: ch-outlier.rnw:105-110
    ###################################################
    # pick top 5 as outliers
    outliers <- order(outlier.scores, decreasing=T)[1:5]
    # who are outliers
    print(outliers)
    print(iris2[outliers,])

    n <- nrow(iris2)
    labels <- 1:n
    labels[-outliers] <- "."
    biplot(prcomp(iris2), cex=.8, xlabs=labels)

    pch <- rep(".", n)
    pch[outliers] <- "+"
    col <- rep("black", n)
    col[outliers] <- "red"
    pairs(iris2, pch=pch, col=col)

#### CLUSTERING
storeData2 <- storeData
storeData2$Profit.Margin <- NULL
storeData2$Sales <- NULL
names(storeData2)

tes = storeData2$SQRT.Crew^2

hc <- hclust(dist(storeData2$SQRT.Crew), method="ave")
plot(hc, hang = -1, labels=storeData2$SQRT.Crew)

hc <- hclust(dist(storeData2), method="ave")
plot(hc, hang = -1, labels=storeData2$Store)

rect.hclust(hc, k=3)
groups <- cutree(hc, k=3)
