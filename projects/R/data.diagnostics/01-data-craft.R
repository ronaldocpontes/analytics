##-------------------------------------------------##
##            Regression Diagnostics               ##
##                  John Fox                       ##
##                FIOCRUZ Brasil                   ##
##                November 2009                    ##
##                                                 ##
##                 Data Craft                      ##
##                                                 ##
##-------------------------------------------------##


# Univariate Displays

library(car)
head(UN) # first few rows
dim(UN) # dimensions
UN <- na.omit(UN)  # filter out missing data
dim(UN)

    # histograms & stem-and-leaf displays

hist(UN$infant.mortality)
hist(UN$infant.mortality, breaks=seq(0, 170, by=10), col="gray")

box()  # frame around plot

stem(UN$infant.mortality)  # crude stem-and-leaf-display

library(aplpack)
stem.leaf(UN$infant.mortality)  # generally better

    # density estimates

plot(density(UN$infant.mortality))
lines(density(UN$infant.mortality, bw=9), lty=2)  # adjusting bandwidth

    # normal Q-Q plots

qq.plot(UN$infant.mortality)
qq.plot(UN$infant.mortality, distribution="norm", labels=rownames(UN))

    # boxplots

boxplot(UN$infant.mortality)
with(UN, identify(rep(1, length(infant.mortality)), infant.mortality, rownames(UN)))

# bivariate displays

scatterplot(infant.mortality ~ gdp, data=UN)

url <- "http://socserv.socsci.mcmaster.ca/jfox/Books/Applied-Regression-2E/datasets/Vocabulary.txt"
Vocab <- read.table(url, header=TRUE)

some(Vocab)   # sample a few rows
dim(Vocab)

    # jittering scatterplots

scatterplot(vocabulary ~ education, data=Vocab)
scatterplot(vocabulary ~ education, data=Vocab, jitter=list(x=1, y=1))
scatterplot(vocabulary ~ education, data=Vocab, jitter=list(x=2, y=2), lwd=3)

    # parallel boxplots

boxplot(vocabulary ~ education, xlab="Education (years)",
        ylab="Vocabulary Score", data=Vocab)

some(Ornstein)
dim(Ornstein)

boxplot(interlocks ~ nation, xlab="Nation of Control", ylab="Assets, $M", data=Ornstein)

    # coded scatterplot
    
some(Davis)
dim(Davis)

with(Davis,plot(jitter(repwt), jitter(weight), pch=as.character(sex),
    col=ifelse( sex == "M" , "blue", "red"),
    xlab="Reported Weight (kg)", ylab="Measured Weight (kg)"))
abline(0, 1, lwd=2)
with(Davis, identify(repwt, weight))


# multivariate display

some(Duncan)
dim(Duncan)

    # scatterplot matrix

scatterplot.matrix(~ prestige + income + education, data=Duncan)
scatterplot.matrix(~ prestige + income + education | type, diag="oned", data=Duncan)

    # 3D scatterplot
    
library(Rcmdr)


#  transformations

    # for symmetry
    

symbox(UN$infant.mortality)  # to select a transformation

    # for linearity

scatterplot(infant.mortality ~ gdp, data=UN)
scatterplot(log(infant.mortality) ~ gdp, data=UN)
scatterplot(log(infant.mortality) ~ log(gdp), data=UN)

    # to equalize spread

spread.level.plot(interlocks + 1 ~ nation, data=Ornstein)

par("mar")  # plot margins
par(mar=c(5, 4, 4, 4))  # more room at the right
boxplot(log(interlocks + 1, 2) ~ nation, ylab=expression(log[2](interlocks + 1)), data=Ornstein)
power.axis(0, base=2, axis.title="interlocks + 1") # right-side axis

    # of proportions
    
stem.leaf(Prestige$women)
summary(Prestige$women)

?logit
stem.leaf(logit(Prestige$women, adjust=.005))
