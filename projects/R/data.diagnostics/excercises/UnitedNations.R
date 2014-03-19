library(car)

UN <- read.table(
"http://socserv.socsci.mcmaster.ca/jfox/Books/Applied-Regression-2E/datasets/UnitedNations.txt",
    header=TRUE)
    
UN <- read.table(file.choose(), header=TRUE)
    
UN.1 <- na.omit(UN[, 
    c("region", "tfr", "contraception", "illiteracyFemale", "GDPperCapita")])
dim(UN)
dim(UN.1)

# Q. 1

par(mfrow=c(1, 3))

with(UN.1, {
    hist(tfr)
    boxplot(tfr)
    qq.plot(tfr)
})

with(UN.1, {
    hist(contraception)
    boxplot(contraception)
    qq.plot(contraception)
})

with(UN.1, {
    hist(illiteracyFemale)
    boxplot(illiteracyFemale)
    qq.plot(illiteracyFemale)
})

with(UN.1, {
    hist(GDPperCapita)
    boxplot(GDPperCapita)
    qq.plot(GDPperCapita)
})

# Q. 2

symbox(UN.1$tfr)

par(mfrow=c(1, 3))
with(UN.1, {
    hist(sqrt(tfr))
    boxplot(sqrt(tfr))
    qq.plot(sqrt(tfr))
})

symbox(UN.1$illiteracyFemale)

par(mfrow=c(1, 3))
with(UN.1, {
    hist(sqrt(illiteracyFemale))
    boxplot(sqrt(illiteracyFemale))
    qq.plot(sqrt(illiteracyFemale))
})

with(UN.1, {
    hist(logit(illiteracyFemale))
    boxplot(logit(illiteracyFemale))
    qq.plot(logit(illiteracyFemale))
})

symbox(UN.1$GDPperCapita)

par(mfrow=c(1, 3))
with(UN.1, {
    hist(log10(GDPperCapita))
    boxplot(log10(GDPperCapita))
    qq.plot(log10(GDPperCapita))
})

# Q. 3

scatterplot(tfr ~ GDPperCapita, data=UN.1)

scatterplot(tfr ~ illiteracyFemale, data=UN.1)

scatterplot(tfr ~ contraception, data=UN.1)

boxplot(tfr ~ region, data=UN.1)

# Q. 4

scatterplot(log10(tfr) ~ log10(GDPperCapita), data=UN.1)

scatterplot(sqrt(tfr) ~ contraception, data=UN.1)

# Q. 5

spread.level.plot(tfr ~ region, data=UN.1)

spread.level.plot(1/tfr ~ region, data=UN.1)

boxplot(-1/tfr ~ region, data=UN.1)
