# load corpus CSV
corpus <- read.csv(paste(getwd(), sep = "/", "AoFP_corpus_info.csv"))

################################################################################

# Figure 1 (a): rank distribution of nr of tokens by child

################################################################################
par(mar=c(5,5,4,1))

# sum nr of tokens by child
plot_this <- tapply(corpus$nr_child_tokens, corpus$child_name, sum)

# sort in decreasing order (rank-size distribution)
plot_this <- sort(plot_this, decreasing=TRUE)

# plot rank-size distribution
plot(plot_this, type='b', col='black', cex=2, pch=19, xaxt='n',
     cex.lab=2.2, cex.main=1.0, cex.axis=1.5, cex.names=2.5,
     ylab='Number of Tokens', xlab='Child', cex.axis=2.0)

################################################################################
################################################################################

# Figure 1 (b): histogram of number of children per age

################################################################################
par(mar=c(5,5,4,1))

# get all child ages
ages <- as.numeric(corpus$child_age)

# three files in the Bates corpus are marked with child age = 336 months
# this is obviously a data entry error (would be 28 years)
# we ignore these three files
ages <- ages[ ages != 336 ]

# get child names 
names <- as.numeric(corpus$child_name)

# plot histogram
hist(ages, cex.lab=2.2, cex.main=1.0, cex.axis=2.0, cex=0.5, cex.names=2.5,
     main="", ylab='Number of Transcripts', xlab='Child Age', col=c('azure4'))