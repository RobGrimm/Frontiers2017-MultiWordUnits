par(mai=c(1.3, 1.4, 0.6, 0.42))
set.seed(100)

# number of bootstraps for 95 % CIs for correlation coefficients 
# and for 95 % CIs for differences between correlation coefficients
N_BOOT = 1000

# get helper functions
source('r_helper_functions.R')

################################################################################
################################################################################

# EXPERIMENT 2: COMPARE ADS TO CDS PREDICTOR VARIANTS

################################################################################
################################################################################

# read in data 
data <- read.csv(paste(getwd(), sep = "/", 'results.csv'))

################################################################################

# full correlations with #MWUs 

boot_RTs_MWUs_CDS_full <- get_bootstrap(data, 
                                        correlation_type='full',
                                        IV='CDS_MWUs',
                                        DV='RTs',
                                        control_for=NA,
                                        n_boot=N_BOOT) 

boot_RTs_MWUs_ADS_full <- get_bootstrap(data, 
                                        correlation_type='full',
                                        IV='ADS_MWUs',
                                        DV='RTs',
                                        control_for=NA,
                                        n_boot=N_BOOT) 

boot_AoFP_MWUs_CDS_full <- get_bootstrap(data, 
                                         correlation_type='full',
                                         IV='CDS_MWUs',
                                         DV='AoFP',
                                         control_for=NA,
                                         n_boot=N_BOOT) 

boot_AoFP_MWUs_ADS_full <- get_bootstrap(data, 
                                         correlation_type='full',
                                         IV='ADS_MWUs',
                                         DV='AoFP',
                                         control_for=NA,
                                         n_boot=N_BOOT) 

pdf(file='ADS_vs_CDS_MWUs-full.pdf', width=7, height=5.5)
par(mai=c(1.3, 1.4, 0.6, 0.42))

plot_correlations_ADS_vs_CDS(boot_RTs_MWUs_CDS_full, 
                             boot_RTs_MWUs_ADS_full,
                             boot_AoFP_MWUs_CDS_full,
                             boot_AoFP_MWUs_ADS_full,
                             ylim=c(-0.5, 0.0),
                             main='',
                             legend=TRUE, 
                             legend_place='bottomleft')
x <- c(0.00, -0.10, -0.20, -0.30, -0.40, -0.50)
axis(2, at = x, lwd=2.0, cex.axis=2.0)
dev.off()

################################################################################


# full correlations with #Freq 

boot_RTs_Freq_CDS_full <- get_bootstrap(data, 
                                        correlation_type='full',
                                        IV='CDS_freq',
                                        DV='RTs',
                                        control_for=NA,
                                        n_boot=N_BOOT) 

boot_RTs_Freq_ADS_full <- get_bootstrap(data, 
                                        correlation_type='full',
                                        IV='ADS_freq',
                                        DV='RTs',
                                        control_for=NA,
                                        n_boot=N_BOOT) 

boot_AoFP_Freq_CDS_full <- get_bootstrap(data, 
                                         correlation_type='full',
                                         IV='CDS_freq',
                                         DV='AoFP',
                                         control_for=NA,
                                         n_boot=N_BOOT) 

boot_AoFP_Freq_ADS_full <- get_bootstrap(data, 
                                         correlation_type='full',
                                         IV='ADS_freq',
                                         DV='AoFP',
                                         control_for=NA,
                                         n_boot=N_BOOT) 

pdf(file='ADS_vs_CDS_Freq-full.pdf', width=7, height=5.5)
par(mai=c(1.3, 1.4, 0.6, 0.42))

plot_correlations_ADS_vs_CDS(boot_RTs_Freq_CDS_full, 
                  boot_RTs_Freq_ADS_full,
                  boot_AoFP_Freq_CDS_full,
                  boot_AoFP_Freq_ADS_full,
                  ylim=c(-0.5, 0.0),
                  main='',
                  legend=TRUE, 
                  legend_place='bottomleft')
x <- c(0.00, -0.10, -0.20, -0.30, -0.40, -0.50)
axis(2, at = x, lwd=2.0, cex.axis=2.0)
dev.off()


################################################################################

# partial correlations with #MWUs

boot_RTs_MWUs_CDS_partial <- get_bootstrap(data, 
                                           correlation_type='partial',
                                           IV='CDS_MWUs',
                                           DV='RTs',
                                           control_for='CDS_freq',
                                           n_boot=N_BOOT) 

boot_RTs_MWUs_ADS_partial <- get_bootstrap(data, 
                                           correlation_type='partial',
                                           IV='ADS_MWUs',
                                           DV='RTs',
                                           control_for='ADS_freq',
                                           n_boot=N_BOOT) 

boot_AoFP_MWUs_CDS_partial <- get_bootstrap(data, 
                                            correlation_type='partial',
                                            IV='CDS_MWUs',
                                            DV='AoFP',
                                            control_for='CDS_freq',
                                            n_boot=N_BOOT) 

boot_AoFP_MWUs_ADS_partial <- get_bootstrap(data, 
                                            correlation_type='partial',
                                            IV='ADS_MWUs',
                                            DV='AoFP',
                                            control_for='ADS_freq',
                                            n_boot=N_BOOT) 

pdf(file='ADS_vs_CDS_MWUs-partial.pdf', width=7, height=5.5)
par(mai=c(1.3, 1.4, 0.6, 0.42))

plot_correlations_ADS_vs_CDS(boot_RTs_MWUs_CDS_partial, 
                             boot_RTs_MWUs_ADS_partial,
                             boot_AoFP_MWUs_CDS_partial,
                             boot_AoFP_MWUs_ADS_partial,
                             ylim=c(-0.20, 0.0),
                             main='',
                             legend=TRUE, 
                             legend_place='bottomleft')
x <- c(0.00, -0.05, -0.10, -0.15, -0.20)
axis(2, at=x, lwd=2.0, cex.axis=2.0)
dev.off()


################################################################################

# partial correlations with #Freq

boot_RTs_Freq_CDS_partial <- get_bootstrap(data, 
                                           correlation_type='partial',
                                           IV='CDS_freq',
                                           DV='RTs',
                                           control_for='CDS_MWUs',
                                           n_boot=N_BOOT) 

boot_RTs_Freq_ADS_partial <- get_bootstrap(data, 
                                           correlation_type='partial',
                                           IV='ADS_freq',
                                           DV='RTs',
                                           control_for='ADS_MWUs',
                                           n_boot=N_BOOT) 

boot_AoFP_Freq_CDS_partial <- get_bootstrap(data, 
                                            correlation_type='partial',
                                            IV='CDS_freq',
                                            DV='AoFP',
                                            control_for='CDS_MWUs',
                                            n_boot=N_BOOT) 

boot_AoFP_Freq_ADS_partial <- get_bootstrap(data, 
                                            correlation_type='partial',
                                            IV='ADS_freq',
                                            DV='AoFP',
                                            control_for='ADS_MWUs',
                                            n_boot=N_BOOT) 

pdf(file='ADS_vs_CDS_Freq-partial.pdf', width=7, height=5.5)
par(mai=c(1.3, 1.4, 0.6, 0.42))

plot_correlations_ADS_vs_CDS(boot_RTs_Freq_CDS_partial, 
                             boot_RTs_Freq_ADS_partial,
                             boot_AoFP_Freq_CDS_partial,
                             boot_AoFP_Freq_ADS_partial,
                             ylim=c(-0.20, 0.0),
                             main='',
                             legend=TRUE, 
                             legend_place='bottomleft')
x <- c(0.00, -0.05, -0.10, -0.20)
axis(2, at = x, lwd=2.0, cex.axis=2.0)
dev.off()


################################################################################
################################################################################

# BOOTSTRAP CIs FOR DIFFERENCES BETWEEN CORRELATION COEFFICIENTS

################################################################################
################################################################################


# FULL CORRELATIONS -- ADS vs. CDS

# RTs: ADS-MWUs vs CDS-MWUs
diffs <- bootstrap_differences(data, IV1='ADS_MWUs', IV2='CDS_MWUs', DV1='RTs', 
                               DV2='RTs', correlation_type='full', n_boot=N_BOOT)
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences

# RTs: ADS-Freq vs CDS-Freq
diffs <- bootstrap_differences(data, IV1='ADS_freq', IV2='CDS_freq', DV1='RTs', 
                               DV2='RTs', correlation_type='full', n_boot=N_BOOT)
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences

# AoFP: ADS-MWUs vs CDS-MWUs
diffs <- bootstrap_differences(data, IV1='ADS_MWUs', IV2='CDS_MWUs', DV1='AoFP', 
                               DV2='AoFP', correlation_type='full', n_boot=N_BOOT)
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences

# AoFP: ADS-Freq vs CDS-Freq
diffs <- bootstrap_differences(data, IV1='ADS_freq', IV2='CDS_freq', DV1='AoFP', 
                               DV2='AoFP', correlation_type='full', n_boot=N_BOOT)
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences



# PARTIAL CORRELATIONS -- ADS vs. CDS
# RTs: ADS-MWUs vs CDS-MWUs
diffs <- bootstrap_differences(data, IV1='ADS_MWUs', IV2='CDS_MWUs', DV1='RTs',
                               DV2='RTs', correlation_type='partial', 
                               n_boot=N_BOOT, control_for1='ADS_freq',
                               control_for2='CDS_freq')
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences

# RTs: ADS-Freq vs CDS-Freq
diffs <- bootstrap_differences(data, IV1='ADS_freq', IV2='CDS_freq', DV1='RTs',
                               DV2='RTs', correlation_type='partial', 
                               n_boot=N_BOOT, control_for1='ADS_MWUs',
                               control_for2='CDS_MWUs')
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences

# AoFP: ADS-MWUs vs CDS-MWUs
diffs <- bootstrap_differences(data, IV1='ADS_MWUs', IV2='CDS_MWUs', DV1='AoFP',
                               DV2='AoFP', correlation_type='partial', 
                               n_boot=N_BOOT, control_for1='ADS_freq',
                               control_for2='CDS_freq')
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences

# AoFP: ADS-Freq vs CDS-Freq
diffs <- bootstrap_differences(data, IV1='ADS_freq', IV2='CDS_freq', DV1='AoFP', 
                               DV2='AoFP', correlation_type='partial', 
                               n_boot=N_BOOT, control_for1='ADS_MWUs',
                               control_for2='CDS_MWUs')
boot.ci(diffs, type = "perc")$t0              # mean difference
boot.ci(diffs, type = "perc")$percent[1, 4:5] # CIs of differences

