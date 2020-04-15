library(extraDistr)
library(car)

# Saving variables ----
opar <- par()

# Generating Dummy Data -----------
n <- 200
mean <- 30
std <- 10

push.inbound.oracle.time <- rnorm(n = n, mean = mean, sd = std)
push.inbound.oracle.gas <- rnorm(n = n, mean = mean, sd = std)
push.inbound.oracle.n.transactions <- rdnorm(n = n, mean = mean, sd = std)

push.outbound.oracle.time <- rnorm(n = n, mean = mean, sd = std)
push.outbount.oracle.gas <- rnorm(n = n, mean = mean, sd = std)

pull.inbound.oracle.time <- rnorm(n = n, mean = mean, sd = std)
pull.inbound.oracle.gas <- rnorm(n = n, mean = mean, sd = std)

pull.outbound.oracle.time <- rnorm(n = n, mean = mean, sd = std)
pull.outbound.oracle.gas <- rnorm(n = n, mean = mean, sd = std)

# Loading oracles as data frames ----------
push.inbound.oracle <- data.frame(
  time = push.inbound.oracle.time, gas = push.inbound.oracle.gas, n.transactions = push.inbound.oracle.n.transactions)

push.outbound.oracle <- data.frame(
  time = push.outbound.oracle.time, gas = push.outbount.oracle.gas)

pull.inbound.oracle <- data.frame(
  time = pull.inbound.oracle.time, gas = pull.inbound.oracle.gas)

pull.outbound.oracle <- data.frame(
  time = pull.outbound.oracle.time, gas = pull.outbound.oracle.gas)


# Linear Regression Models ----
push.inbound.oracle.lm.time.transactions <- lm(time ~ n.transactions, data = push.inbound.oracle)
summary(push.inbound.oracle.lm.time.transactions)
confint(push.inbound.oracle.lm.time.transactions)


# Regression Diagnostics -----
pdf("push_inbound_oracle_diagnostic_plots_lm_time_ntransactions.pdf", width = 14, height = 14)
par(mfrow = c(2, 2))
plot(push.inbound.oracle.lm.time.transactions)
mtext("(Push Inbound Oracle) Diagnostic plost for the regression time ~ n.transactions.", outer = TRUE, cex = 1.5, line = -2, font = 2)
dev.off()

qq