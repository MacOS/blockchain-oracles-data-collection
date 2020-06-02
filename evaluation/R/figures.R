library(extraDistr)
library(car)

set.seed(100)


# Constants
USE.DUMMY <- FALSE


# Saving variables ----
opar <- par()


# Load Data Data -----------
push.inbound.oracle.arrival <- read.csv("./evaluation/python/df_push_inbound_oracle_arrival.csv")

pull.inbound.oracle.order <- read.csv("./evaluation/python/df_pull_inbound_oracle_order.csv")
pull.inbound.oracle.verify.customer <- read.csv("./evaluation/python/df_pull_inbound_oracle_verify_customer.csv")
  
push.outbound.oracle.arrival <- read.csv("./evaluation/python/df_push_outbound_oracle_arrival.csv")

pull.outbound.oracle.arrival <- read.csv("./evaluation/python/df_pull_outbound_oracle_arrival.csv")


# Construct data frames ----
df.push.inbound.oracle <- data.frame(
  dt.transaction.mined.seconds.total = push.inbound.oracle.arrival$dt_transaction_mined_seconds_total,
  dt.transaction.hash.seconds.total = push.inbound.oracle.arrival$dt_transaction_hash_seconds_total,
  transaction.count.in.block = push.inbound.oracle.arrival$transactionCountInBlock)

## Push Inbound part of the pull inbound oracle
df.pull.inbound.oracle.verify.customer <- data.frame(
  dt.transaction.mined.seconds.total = pull.inbound.oracle.order$dt_transaction_mined_seconds_total,
  dt.transaction.hash.seconds.total = pull.inbound.oracle.order$dt_transaction_hash_seconds_total,
  transaction.count.in.block = pull.inbound.oracle.order$transactionCountInBlock)
## Push Outbound part of the pull inbound oracle


df.push.outbound.oracle.arrival <- data.frame(
  dt.transaction.mined.seconds.total = push.outbound.oracle.arrival$dt_transaction_mined_seconds_total,
  dt.round.trip.seconds.total = push.outbound.oracle.arrival$dt_round_trip_time_seconds_total,
  transaction.count.in.block = push.outbound.oracle.arrival$transactionCountInBlock)

# This does not make sense, since we always retrieve the same value. And we hence we always the same transaction.count.in.block.
df.pull.outbound.oracle <- data.frame(
  dt.transaction.hash.seconds.total = pull.outbound.oracle.arrival$dt_transaction_hash_seconds_total,
  transaction.count.in.block = pull.outbound.oracle.arrival$tr)


# Split data ----
sample.space <- 1:nrow(push.inbound.oracle.arrival)
set.seed(100); fit.idx <- sample(sample.space, size = length(sample.space)*0.8)
predict.idx <- setdiff(sample.space, fit.idx)
df.push.inbound.oracle.arrival.fit <- push.inbound.oracle.arrival[ fit.idx , ]
df.push.inbound.oracle.arrival.predict <- push.inbound.oracle.arrival[ predict.idx , ]

sample.space <- 1:nrow(pull.inbound.oracle.verify.customer)
set.seed(100); fit.idx <- sample(sample.space, size = length(sample.space)*0.8)
predict.idx <- setdiff(sample.space, fit.idx)
df.pull.inbound.oracle.verify.customer.fit <- pull.inbound.oracle.verify.customer[ fit.idx, ]
df.pull.inbound.oracle.verify.customer.predict <- pull.inbound.oracle.verify.customer[ predict.idx, ]

sample.space <- 1:nrow(push.outbound.oracle.arrival)
set.seed(100); fit.idx <- sample(sample.space, size = length(sample.space)*0.8)
predict.idx <- setdiff(sample.space, fit.idx)
df.push.outbound.oracle.arrival.fit <- push.outbound.oracle.arrival[ fit.idx, ]
df.push.outbound.oracle.arrival.predict <- df.push.outbound.oracle.arrival[ predict.idx, ]

sample.space <- 1:nrow(push.outbound.oracle.verify.customer)
set.seed(100); fit.idx <- sample(sample.space, size = length(sample.space)*0.8)
predict.idx <- setdiff(sample.space, fit.idx)
df.push.outbound.oracle.arrival.fit <- push.outbound.oracle.arrival[ fit.idx, ]
df.push.outbound.oracle.arrival.predict <- df.push.outbound.oracle.arrival[ predict.idx, ]


# Linear Regression Models ----
push.inbound.oracle.lm.time.transaction.hash <- lm(
  dt_transaction_hash_seconds_total ~ transactionCountInBlock,
  data = df.push.inbound.oracle.arrival.fit)

summary(push.inbound.oracle.lm.time.transaction.hash)

confint(push.inbound.oracle.lm.time.transaction.hash)



pull.inbound.oracle.lm.time.transaction.hash <- lm(
  dt_)


# Predictions ----

push.inbound.oracle.lm.time.transactions.pred.plim <- predict(
  push.inbound.oracle.lm.time.transaction.hash, df.push.inbound.oracle.arrival.predict, interval="prediction")

push.inbound.oracle.lm.time.transactions.pred.clim <- predict(
  push.inbound.oracle.lm.time.transaction.hash, df.push.inbound.oracle.arrival.predict, interval="confidence")

# Plot Regression Result on Plot
pdf("./evaluation/R/qa_push_inbound_oracle_regression_transaction_count_in_block.pdf", width = 14, height = 14)

plot(
  x=df.push.inbound.oracle$transaction.count.in.block,
  y=df.push.inbound.oracle$dt.transaction.hash.seconds.total,
  main="Push Inbound Oracle: Linear Regression of Number of Transactions (in the block) on dt",
  xlab="Number of Transactions in the Block",
  ylab=expression("dt [seconds]"),
  #ylim=c(0, 800000)
)

abline(push.inbound.oracle.lm.time.transaction.hash, col=2, lwd=3)

lines(
  df.push.inbound.oracle.arrival.predict$transactionCountInBlock, push.inbound.oracle.lm.time.transactions.pred.plim[, 2],
  col=3, lwd=3, lty=2)
lines(
  df.push.inbound.oracle.arrival.predict$transactionCountInBlock, push.inbound.oracle.lm.time.transactions.pred.plim[, 3],
  col=3, lwd=3, lty=2)

lines(
  df.push.inbound.oracle.arrival.predict$transactionCountInBlock, push.inbound.oracle.lm.time.transactions.pred.clim[, 2],
  col=4, lwd=4, lty=3)
lines(
  df.push.inbound.oracle.arrival.predict$transactionCountInBlock, push.inbound.oracle.lm.time.transactions.pred.clim[, 3],
  col=4, lwd=4, lty=3)

legend(
  "topright", title="Legend", 
  legend=c("Linear Regression", "Prediction Intervals", "Confidence Interavls"),
  lty=c(1, 3, 4), lwd=c(3, 3, 4), col=c(2, 3, 4))

dev.off()


# Regression Diagnostics -----
pdf("./evaluation/R/qa_push_inbound_oracle_diagnostic_plots_lm_time_ntransactions.pdf", width = 14, height = 14)
par(mfrow = c(2, 2))
plot(push.inbound.oracle.lm.time.transaction.hash)
mtext("(Push Inbound Oracle) Diagnostic Plots for the regression dt ~ transactionCountInBlock.", outer = TRUE, cex = 1.5, line = -2, font = 2)
dev.off()
