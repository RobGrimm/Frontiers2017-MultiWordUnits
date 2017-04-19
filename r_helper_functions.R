library(ppcor) # partial correlations
library(boot)  # bootstrapping

# for parallel processing to speed up bootstrapping, 
# specify how many CPU cores should be used
NR_CPU_CORES=8


get_bootstrap <- function(data,
                          IV, DV,
                          correlation_type, 
                          control_for,
                          n_boot,
                          n_cpu_cores=NR_CPU_CORES) {
  # return object of 'type' boot, containing bootstrapped statistics 
  # for the correlation of the indendent and the dependent variable
  
  # Arguments: 
  # - CSV:                R data frame, with columns 'IV' and 'DV'
  
  # - 'IV':               string, name of the independent variable 
  
  # - 'DV':               string, name of the dependent variable 
  
  # - 'correlation_type': string, either 'full' or 'partial'
  
  # - 'control_for':      string, name of the variable that is to be partialed out,
  #                       in case 'correlation_type' is 'partial'
  
  # - 'n_boot':           number of bootstraps 
  
  # 'n_cpu_cores':        integer, number of CPU cores that to be used in parallel
  bootFunPartial <- function(d, i){
    d2 <- d[i,]
    pcor.test(x=d2[[IV]], y=d2[[DV]], z=d2[[control_for]], 
              method='kendall')$estimate
  }
  
  bootFunFull <- function(d, i){
    d2 <- d[i,]
    cor.test(x=d2[[IV]], y=d2[[DV]], method='kendall')$estimate
  }
  
  if (correlation_type == 'partial') {
    bootFun <- bootFunPartial
  }
  else {
    bootFun <- bootFunFull
  }  
  
  ret <- boot(data, bootFun, R=n_boot, ncpus=n_cpu_cores, parallel='multicore')
  return(ret)
}



bootstrap_differences <- function(data, IV1, IV2, DV1, DV2, correlation_type, 
                                  n_boot, control_for1=NA, control_for2=NA, 
                                  n_cpu_cores=NR_CPU_CORES) {
  # return object of 'type' boot, containing bootstrapped statistics 
  # for the difference between the correlation of (a) 'IV1' and 'DV1' and 
  # (b) 'IV2' and 'DV2'
  
  # Arguments:
  # - data: R data frame, with columns 'IV1', 'IV2', 'DV1', 'DV2', and
  # -- in case of partial correlations -- 'control_for1' and 'control_for2'
  
  # - 'IV1':              string, name of independent variable 1
  
  # - 'IV2':              string, name of independent variable 2
  
  # - 'DV1':              string, name of dependent variable 1
  
  # - 'DV2':              string, name of dependent variable 2
  
  # - 'correlation_type': string, either 'full' or 'partial'
  
  # - 'n_boot':           number of bootstraps 
  
  # - 'control_for1':     'string, name of the variable that is 
  #                       to be partialled out when correlating 'IV1' with 'DV1' 
  
  # - 'control_for2':     'string, name of the variable that is 
  #                       to be partialled out when correlating 'IV2 with 'DV2'                        
  
  # 'n_cpu_cores':        integer, number of CPU cores that to be used in parallel
  bootFunFull <- function(d, i){
    d2 <- d[i,]
    cor1 <- cor.test(x=d2[[IV1]], y=d2[[DV1]], method='kendall')$estimate
    cor2 <- cor.test(x=d2[[IV2]], y=d2[[DV2]], method='kendall')$estimate
    return(abs(cor1 - cor2))
  }
  
  bootFunPar <- function(d, i){
    d2 <- d[i,]
    cor1 <- pcor.test(x=d2[[IV1]], y=d2[[DV1]], z=d2[[control_for1]], 
                      method='kendall')$estimate
    cor2 <- pcor.test(x=d2[[IV2]], y=d2[[DV2]], z=d2[[control_for2]], 
                      method='kendall')$estimate
    return(abs(cor1 - cor2))
  }
  
  if (correlation_type == 'full'){
    bootFun <- bootFunFull
  }
  
  if (correlation_type == 'partial'){
    bootFun <- bootFunPar
  }  
  
  b <- boot(data, bootFun, R=n_boot, ncpus=n_cpu_cores, parallel='multicore')
  
}



plot_correlations_ADS_vs_CDS <- function(boot_RTs_CDS,
                                         boot_RTs_ADS,
                                         boot_AoFP_CDS,
                                         boot_AoFP_ADS,
                                         ylim,
                                         main,
                                         legend=TRUE, 
                                         legend_place='bottomleft') {
  # plot the results for Experiment 2
  
  # Arguments: 
  
  # 'boot_RTs_CDS':   object of type 'boot', containing statistics for the 
  #                   correlation of the dependent variable estimated from CDS 
  #                   (CDS-#MWUs or CDS-#Freq) with RTs
  
  # 'boot_RTs_ADS':   object of type 'boot', containing statistics for the 
  #                   correlation of the DV estimated from ADS with RTs
  
  # 'boot_AoFP_CDS':  ...containing statistics for the 
  #                   correlation of the DV estimated from CDS with AoFP
  
  # 'boot_AoFP_ADS':  ...containing statistics for the 
  #                   correlation of the DV estimated from ADS with AoFP
  
  # 'ylim':           start, stop coordinates for the y-axis
  
  # 'main':           title of the plot
  
  # 'legend':         boolean, whether or not to display the legend
  
  # 'legend_place':   position of the legend
  corsA <- c()
  cis0A <- c()
  cis1A <- c()
  
  for (b in list(boot_RTs_CDS, boot_AoFP_CDS)) {
    cor <- b$t0
    cis <- boot.ci(b, type = "perc")$percent[1, 4:5] 
    corsA <- c(corsA, cor)
    cis0A <- c(cis0A, cis[1])
    cis1A <- c(cis1A, cis[2])
  }
  
  corsB <- c()
  cis0B <- c()
  cis1B <- c()
  
  for (b in list(boot_RTs_ADS, boot_AoFP_ADS)) {
    cor <- b$t0
    cis <- boot.ci(b, type = "perc")$percent[1, 4:5] 
    corsB <- c(corsB, cor)
    cis0B <- c(cis0B, cis[1])
    cis1B <- c(cis1B, cis[2])
  }
  
  plot_me <- rbind(corsA, corsB)
  
  names <- c('reaction times', 'AoFP')
  
  bar <- barplot(plot_me, main=main, ylab="Kendall's Tau", xlab="", 
                 ylim=ylim, beside=TRUE, 
                 col=c('grey', 'grey30'), cex.lab=2.0, cex.main=2.0, 
                 cex.axis=2.0, cex=0.5, cex.names=2.0, names.arg=names, axes=FALSE)
  
  arrows(x0=bar, y0=rbind(cis0A, cis0B), y1=rbind(cis1A, cis1B), 
         cex=10, code=3, angle=90, length=.1, col='black', lwd=3)
  
  if (legend == TRUE) {
    legend(legend_place, c("CDS", "ADS"), pch=15, col=c('grey', 'grey30'), 
           cex=2.5, bty="n")
  }

}



plot_correlations_baseline <- function(boot_random_RTs,
                                       boot_random_AoFP,
                                       boot_mwu_RTs,
                                       boot_mwu_AoFP,
                                       ylim,
                                       main,
                                       legend=TRUE, 
                                       legend_place='bottomleft') {
  # plot the results for Experiment 3
  # this function is similar to the previos plot function -- it differs in the 
  # 'boot' arguments it expects and the labels it prints on the plot
  
  # Arguments that differ from previous function: 
  
  # 'boot_random_RTs':  object of type 'boot', containing statistics for the 
  #                     correlation of the dependent variable estimated via the 
  #                     random baseline (ADS-#baseline) with RTs
  
  # 'boot_random_AoFP': ...containing statistics for the correlation of 
  #                     #CDS-baseline with AoFP
  
  # 'boot_mwu_RTs':     ...containing statistics for the correlation of ADS-#MWUs
  #                     with RTs
  
  # 'boot_mwu_AoFP':    ...containing statistics for the correlation of CDS-#MWUs
  #                     with AoFP
  corsA <- c()
  cis0A <- c()
  cis1A <- c()
  
  for (b in list(boot_random_RTs, boot_random_AoFP)) {
    cor <- b$t0
    cis <- boot.ci(b, type = "perc")$percent[1, 4:5] 
    corsA <- c(corsA, cor)
    cis0A <- c(cis0A, cis[1])
    cis1A <- c(cis1A, cis[2])
  }
  
  corsB <- c()
  cis0B <- c()
  cis1B <- c()
  
  for (b in list(boot_mwu_RTs, boot_mwu_AoFP)) {
    cor <- b$t0
    cis <- boot.ci(b, type = "perc")$percent[1, 4:5] 
    corsB <- c(corsB, cor)
    cis0B <- c(cis0B, cis[1])
    cis1B <- c(cis1B, cis[2])
  }
  
  plot_me <- rbind(corsA, corsB)
  
  print(plot_me)
  
  names <- c('reaction times', 'AoFP')
  
  bar <- barplot(plot_me, main=main, ylab="Kendall's Tau", xlab="", 
                 ylim=ylim, beside=TRUE, 
                 col=c('grey', 'grey30'), cex.lab=2.0, cex.main=2.0, 
                 cex.axis=2.0, cex=0.5, cex.names=2.0, names.arg=names, axes=FALSE)
  
  arrows(x0=bar, y0=rbind(cis0A, cis0B), y1=rbind(cis1A, cis1B), 
         cex=10, code=3, angle=90, length=.1, col='black', lwd=3)
  
  if (legend == TRUE) {
    legend(legend_place, c("#baseline", "#MWUs"), pch=15, col=c('grey', 'grey30'), 
           cex=2.5, bty="n")
  }
  
}



plot_correlations_across_DVs <- function(boot_freq_RTs,
                                         boot_freq_AoFP,
                                         boot_mwu_RTs,
                                         boot_mwu_AoFP,
                                         main,
                                         ylim,
                                         legend_names,
                                         legend=TRUE, 
                                         legend_place='bottomleft') {
  # plot the results for Experiment 4
  # this function is similar to the previos plot function -- it differs in the 
  # 'boot' arguments it expects and the labels it prints on the plot
  
  # Arguments that differ from previous function: 
  
  # 'boot_freq_RTs':    object of type 'boot', containing statistics for the 
  #                     correlation of ADS-#Freq with RTs
  
  # 'boot_freq_AoFP':   ...containing statistics for thecorrelation of 
  #                     CDS-#Freq with AoFP
  
  # 'boot_mwu_RTs':     ...containing statistics for the correlation of ADS-#MWUs
  #                     with RTs
  
  # 'boot_mwu_AoFP':    ...containing statistics for the correlation of CDS-#MWUs
  #                     with AoFP
  corsFreq <- c()
  cis0Freq <- c()
  cis1Freq <- c()
  
  for (b in list(boot_freq_RTs, boot_freq_AoFP)) {
    cor <- b$t0
    cis <- boot.ci(b, type = "norm")$normal[1, 2:3] 
    corsFreq <- c(corsFreq, cor)
    cis0Freq <- c(cis0Freq, cis[1])
    cis1Freq <- c(cis1Freq, cis[2])
  }
  
  corsMWU <- c()
  cis0MWU <- c()
  cis1MWU <- c()
  
  for (b in list(boot_mwu_RTs, boot_mwu_AoFP)) {
    cor <- b$t0
    cis <- boot.ci(b, type = "norm")$normal[1, 2:3] 
    corsMWU <- c(corsMWU, cor)
    cis0MWU <- c(cis0MWU, cis[1])
    cis1MWU <- c(cis1MWU, cis[2])
  }
  
  plot_me <- cbind(corsFreq, corsMWU)
  
  names <- c('frequency', '#MWUs')
  
  bar <- barplot(plot_me, main=main, ylab="Kendall's Tau", xlab="", 
                 ylim=ylim, beside=TRUE, 
                 col=c('grey', 'grey30'), cex.lab=2.0, cex.main=2.0, 
                 cex.axis=2.0, cex=0.5, cex.names=2.0, names.arg=names, axes=FALSE)
  
  arrows(x0=bar, y0=cbind(cis0Freq, cis0MWU), y1=cbind(cis1Freq, cis1MWU), 
         cex=10, code=3, angle=90, length=.1, col='black', lwd=3)
  
  if (legend == TRUE) {
    legend(legend_place, legend_names, pch=15, col=c('grey', 'grey30'), 
           cex=2.0, bty="n")
  }
}