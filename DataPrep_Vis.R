library(sp)
library(raster)
library(rgdal)
library(dismo)
library(rJava)
library(plyr)
library(chron)
library(spatstat)
library(spatstat.utils)

#Clean GPS data
originalData <- read.csv("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/AllGrizzlyData/GPS_data/GPS_DATA_FOR_UNIV_IDAHO_FULL.csv")
clean_originalData <- originalData[!is.na(originalData$UTMX),]
clean_originalData <- originalData[!is.na(originalData$UTMY),]

#Get variables from yellowstone data
enviro <- list.files('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/AllGrizzlyData/U_Idaho_Data/U_Idaho_Data/Rasters_30m/', pattern=".tif$", full.names=TRUE)
predictors_YNP <- stack(enviro[1:8])
#get variables from worldclim
predictors_clim <- getData("worldclim",var="bio",res=5)
#Get variables from monthly enviro data
shade<- raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/nlcddata/CONUSAnalytical_2_8_16/Analytical/nlcd2011_usfs_conus_canopy_analytical.img")
c5 <- raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/cloud data/MODCF_monthlymean_05.tif")
c6 <- raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/cloud data/MODCF_monthlymean_06.tif")
c7 <- raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/cloud data/MODCF_monthlymean_07.tif")
c8 <- raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/cloud data/MODCF_monthlymean_08.tif")
c9 <- raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/cloud data/MODCF_monthlymean_09.tif")
r.5<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmin_30yr_normal_800mM2_05_bil.bil")
r.6<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmin_30yr_normal_800mM2_06_bil.bil")
r.7<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmin_30yr_normal_800mM2_07_bil.bil")
r.8<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmin_30yr_normal_800mM2_08_bil.bil")
r.9<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmin_30yr_normal_800mM2_09_bil.bil")
r5<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmax_30yr_normal_800mM2_05_bil.bil")
r6<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmax_30yr_normal_800mM2_06_bil.bil")
r7<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmax_30yr_normal_800mM2_07_bil.bil")
r8<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmax_30yr_normal_800mM2_08_bil.bil")
r9<-raster("C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/PRISM data/PRISM_tmax_30yr_normal_800mM2_09_bil.bil")
#Get variables from Niche Mapper Output
nlw_May <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, water acc, no shade_ready/MONTHOutput/May_raster.bil')
nlw_Jun <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, water acc, no shade_ready/MONTHOutput/Jun_raster.bil')
nlw_Jul <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, water acc, no shade_ready/MONTHOutput/Jul_raster.bil')
nlw_Aug <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, water acc, no shade_ready/MONTHOutput/Aug_raster.bil')
nlw_Sep <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, water acc, no shade_ready/MONTHOutput/Sep_raster.bil')

nlnw_May <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, no water acc, no shade_ready/MONTHOutput/May_raster.bil')
nlnw_Jun <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, no water acc, no shade_ready/MONTHOutput/Jun_raster.bil')
nlnw_Jul <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, no water acc, no shade_ready/MONTHOutput/Jul_raster.bil')
nlnw_Aug <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, no water acc, no shade_ready/MONTHOutput/Aug_raster.bil')
nlnw_Sep <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem nonlac, low act, no water acc, no shade_ready/MONTHOutput/Sep_raster.bil')

lw_May <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, water acc, no shade_ready/MONTHOutput/May_raster.bil')
lw_Jun <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, water acc, no shade_ready/MONTHOutput/Jun_raster.bil')
lw_Jul <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, water acc, no shade_ready/MONTHOutput/Jul_raster.bil')
lw_Aug <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, water acc, no shade_ready/MONTHOutput/Aug_raster.bil')
lw_Sep <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, water acc, no shade_ready/MONTHOutput/Sep_raster.bil')

lnw_May <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, no water acc, no shade_ready/MONTHOutput/May_raster.bil')
lnw_Jun <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, no water acc, no shade_ready/MONTHOutput/Jun_raster.bil')
lnw_Jul <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, no water acc, no shade_ready/MONTHOutput/Jul_raster.bil')
lnw_Aug <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, no water acc, no shade_ready/MONTHOutput/Aug_raster.bil')
lnw_Sep <- raster('C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/Niche Mapper Stuff/Landscape Scale/current climate, fem lac, low act, no water acc, no shade_ready/MONTHOutput/Sep_raster.bil')





#convert to latitude and longitude and prep for correct format
sputm <- SpatialPoints(clean_originalData[8:9], proj4string=CRS("+proj=utm +zone=12T +datum=WGS84"))
spgeo <- spTransform(sputm, crs(predictors_clim))
spYNP <- spTransform(sputm, crs(predictors_YNP))
spc <- spTransform(sputm, crs(c5))
spshade <- spTransform(sputm, crs(shade))
spr <- spTransform(sputm, crs(r5))
xy <- as.data.frame(spc)
colnames(xy) <- c("x", "y")


#Check that all background points are within extent of variables
which(!inside.range(xy$x, c(xmin(NMout), xmax(NMout))))
which(!inside.range(xy$y, c(ymin(NMout), ymax(NMout))))


#perform extractions for presence data
extraction <- extract(predictors_clim, spgeo)
extractionYNP <- extract(predictors_YNP, spYNP)
extractioncloud5 <- (extract(c5, spc)/100)
extractioncloud6 <- (extract(c6, spc)/100)
extractioncloud7 <- (extract(c7, spc)/100)
extractioncloud8 <- (extract(c8, spc)/100)
extractioncloud9 <- (extract(c9, spc)/100)
extractionshade <- extract(shade, spshade)
extractionr5max <- extract(r5,spr)
extractionr6max <- extract(r6,spr)
extractionr7max <- extract(r7,spr)
extractionr8max <- extract(r8,spr)
extractionr9max <- extract(r9,spr)
extractionr5min <- extract(r.5,spr)
extractionr6min <- extract(r.6,spr)
extractionr7min <- extract(r.7,spr)
extractionr8min <- extract(r.8,spr)
extractionr9min <- extract(r.9,spr)
NMout <- stack(c(nlw_May, nlw_Jun, nlw_Jul, nlw_Aug, nlw_Sep, nlnw_May, nlnw_Jun, nlnw_Jul, nlnw_Aug, nlnw_Sep, lw_May, lw_Jun, lw_Jul, lw_Aug, lw_Sep, lnw_May, lnw_Jun, lnw_Jul, lnw_Aug, lnw_Sep))
extractionNMout <- extract(NMout, xy)



#create background (random) data points
#mask <- raster(enviro[2])
mask <- raster(NMout$May_raster.1)
crs(mask) <- CRS( "+proj=longlat +datum=WGS84")
set.seed(1994)
bg <- randomPoints(mask, 31215)
colnames(bg) <- c("x", "y")
bgp <- SpatialPoints(bg, proj4string=CRS("+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0"))

spbgYNP <- spTransform(bgp, CRS("+proj=utm +zone=12 +datum=NAD83 +units=m +no_defs +ellps=GRS80 +towgs84=0,0,0 ") )
spbggeo <-spTransform(spbgYNP, CRS("+proj=longlat +datum=WGS84"))
spbgc <- spTransform(spbgYNP, crs(c5))
spbgshade <- spTransform(spbgYNP, crs(shade))
spbgr <- spTransform(spbgYNP, crs(r5))
xybg <- as.data.frame(bgp)
colnames(xybg) <- c("x","y")

#Check that all background points are within extent of variables
which(!inside.range(xybg$x, c(xmin(NMout), xmax(NMout))))
which(!inside.range(xybg$y, c(ymin(NMout), ymax(NMout))))

#Check that no background points match presence point
which(xy$x == xybg$x  & xy$y == xybg$y)


#perform extractions for background data
extractionbg <-extract(predictors_clim, spbggeo)
extractionbgYNP <-extract(predictors_YNP, spbgYNP)
extractionbgcloud5 <- (extract(c5, spbgc)/100)
extractionbgcloud6 <- (extract(c6, spbgc)/100)
extractionbgcloud7 <- (extract(c7, spbgc)/100)
extractionbgcloud8 <- (extract(c8, spbgc)/100)
extractionbgcloud9 <- (extract(c9, spbgc)/100)
extractionbgshade <- extract(shade, spbgshade)
extractionbgr5max <- extract(r5,spbgr)
extractionbgr6max <- extract(r6,spbgr)
extractionbgr7max <- extract(r7,spbgr)
extractionbgr8max <- extract(r8,spbgr)
extractionbgr9max <- extract(r9,spbgr)
extractionbgr5min <- extract(r.5,spbgr)
extractionbgr6min <- extract(r.6,spbgr)
extractionbgr7min <- extract(r.7,spbgr)
extractionbgr8min <- extract(r.8,spbgr)
extractionbgr9min <- extract(r.9,spbgr)
extractionbgNMout <- extract(NMout, bgp)


#combine final dataset
full_presence_data <- cbind(clean_originalData, extraction, extractionYNP, extractionshade, extractionNMout, extractionr5max, extractionr5min, extractioncloud5, extractionr6max, extractionr6min, extractioncloud6, extractionr7max, extractionr7min, extractioncloud7, extractionr8max, extractionr8min, extractionbgcloud8, extractionr9max, extractionr9min, extractioncloud9)
full_presence_data$presence <-rep(1,nrow(full_presence_data))
full_presence_data$lati <- as.data.frame(spgeo)$UTMX
full_presence_data$long <- as.data.frame(spgeo)$UTMY
full_presence_data <- full_presence_data[c(1:46, 51, 56, 61, 66:68, 47, 52, 57, 62, 69:71, 48, 53, 58, 63, 72:74, 49, 54, 59, 64, 75:77, 50, 55, 60, 65, 78:83)]
colnames(full_presence_data) <- c(colnames(full_presence_data)[1:44], "shade", 
                                  "nlw_May", "nlnw_May", "lw_May", "lnw_May", "tempmax_May", "tempmin_May", "cloud_May",
                                  "nlw_Jun", "nlnw_Jun", "lw_Jun", "lnw_Jun", "tempmax_Jun", "tempmin_Jun", "cloud_Jun",
                                  "nlw_Jul", "nlnw_Jul", "lw_Jul", "lnw_Jul", "tempmax_Jul", "tempmin_Jul", "cloud_Jul",
                                  "nlw_Aug", "nlnw_Aug", "lw_Aug", "lnw_Aug", "tempmax_Aug", "tempmin_Aug", "cloud_Aug",
                                  "nlw_Sep", "nlnw_Sep", "lw_Sep", "lnw_Sep", "tempmax_Sep", "tempmin_Sep", "cloud_Sep",
                                  "presence", "lat", "long")

#Getting telemetry data separated to month and time


full_presence_data$TelemDate <- lapply(full_presence_data$TelemDate, as.character)
dtparts = t(as.data.frame(strsplit(as.character(full_presence_data$TelemDate), ' ')))
row.names(dtparts)= NULL
#thetimes = chron(dates = dtparts[,1], times = dtparts[,2], format = c('m/d/y', 'h:m'))
full_presence_data$Date_telem <- dtparts[,1]
full_presence_data$Time_telem <- dtparts [,2]
full_presence_data <- full_presence_data[,c(1:6, 84,85,8:83)]



full_absence_data <- as.data.frame(cbind(extractionbg, extractionbgYNP, extractionbgshade, extractionbgNMout, extractionbgr5max, extractionbgr5min, extractionbgcloud5, extractionbgr6max, extractionbgr6min, extractionbgcloud6, extractionbgr7max, extractionbgr7min, extractionbgcloud7, extractionbgr8max, extractionbgr8min, extractionbgcloud8, extractionbgr9max, extractionbgr9min, extractionbgcloud9))
full_absence_data$presence <-rep(0,nrow(full_absence_data))
full_absence_data$lati <-as.data.frame(spbggeo)$x
full_absence_data$long <-as.data.frame(spbggeo)$y
full_absence_data$AID <- rep(NA,nrow(full_absence_data))
full_absence_data$ID2 <- rep(NA,nrow(full_absence_data))
full_absence_data$SEX <- rep(NA,nrow(full_absence_data))
full_absence_data$Cohort <- rep(NA,nrow(full_absence_data))
full_absence_data$AGEnum <- rep(NA,nrow(full_absence_data))
full_absence_data$birth.year <- rep(NA,nrow(full_absence_data))
full_absence_data$Date_telem <- rep(NA,nrow(full_absence_data))
full_absence_data$Time_telem <- rep(NA,nrow(full_absence_data))
full_absence_data$UTMX <- rep(NA,nrow(full_absence_data))
full_absence_data$UTMY <- rep(NA,nrow(full_absence_data))
full_absence_data$UTM_ZONE <- rep(NA,nrow(full_absence_data))
full_absence_data$Location_Status <- rep(NA,nrow(full_absence_data))
full_absence_data$FixStatus <- rep(NA,nrow(full_absence_data))
full_absence_data$PDOP <- rep(NA,nrow(full_absence_data))
full_absence_data$HDOP <- rep(NA,nrow(full_absence_data))
full_absence_data$VDOP <- rep(NA,nrow(full_absence_data))
full_absence_data$TDOP <- rep(NA,nrow(full_absence_data))
full_absence_data$TransInf <- rep(NA,nrow(full_absence_data))
#full_absence_data$list <- NULL
full_absence_data <- full_absence_data[,c(67:84,1:66)]
namelist <-colnames(full_absence_data)
full_absence_data <- full_absence_data[,c(1:47, 52, 57, 62, 67:69, 48, 53, 58, 63, 70:72, 49, 54, 59, 64, 73:75, 50, 55, 60, 65, 76:78, 51, 56, 61, 66, 79:84)]
colnames(full_absence_data) <- c(namelist[1:45], "shade", 
                                 "nlw_May", "nlnw_May", "lw_May", "lnw_May", "tempmax_May", "tempmin_May", "cloud_May",
                                 "nlw_Jun", "nlnw_Jun", "lw_Jun", "lnw_Jun", "tempmax_Jun", "tempmin_Jun", "cloud_Jun",
                                 "nlw_Jul", "nlnw_Jul", "lw_Jul", "lnw_Jul", "tempmax_Jul", "tempmin_Jul", "cloud_Jul",
                                 "nlw_Aug", "nlnw_Aug", "lw_Aug", "lnw_Aug", "tempmax_Aug", "tempmin_Aug", "cloud_Aug",
                                 "nlw_Sep", "nlnw_Sep", "lw_Sep", "lnw_Sep", "tempmax_Sep", "tempmin_Sep", "cloud_Sep",
                                 "presence", "lat", "long")





#Everything to file
presence_absence_data <-rbind(full_absence_data, full_presence_data)

write.csv(presence_absence_data, file="C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/full_grizz_dataset.csv")


#Create separate dataframes/files for each month and reproductive class
table(months(full_presence_data$Date_telem))
#Cohort 0 = unknown reproductive status
#Cohort 1 =  adult F with cubs-of-the-year
#Cohort 2 =  adult F with yearlings (none of these)
#Cohort 3 =  adult F with 2-year-olds
#Cohort 4 =  solitary adult F
#Cohort 5 =  subadult F

#########################################################
####PURE PREESNCE TEST
#########################################
#May_data <- full_presence_data[which(months(full_presence_data$Month_telem) == "May"),] #seperate GPS locations from May
#May_data <- May_data[which(May_data$Location_Status == 'Out_of_Den'),] #remove in den locations
#May_nlw <- May_data[which(May_data$Cohort > 1),c(1:47, 51:53,82:84)]
# write.csv(May_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_nlw.csv")
# May_nlnw <- May_data[which(May_data$Cohort > 1),c(1:46, 48, 51:53,82:84)]
# write.csv(May_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_nlnw.csv")
# May_lw <- May_data[which(May_data$Cohort == 1),c(1:46, 49, 51:53,82:84)]
# write.csv(May_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_lw.csv")
# May_lnw <- May_data[which(May_data$Cohort == 1),c(1:46, 50, 51:53,82:84)]
# write.csv(May_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_lnw.csv")


#Jun_data <- full_presence_data[which(months(full_presence_data$Month_telem) == "Jun"),]
# Jun_nlw <- Jun_data[which(Jun_data$Cohort > 1), c(1:46, 54, 58:60, 82:84)]
# write.csv(Jun_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_nlw.csv")
# Jun_nlnw <- Jun_data[which(Jun_data$Cohort > 1), c(1:46, 55, 58:60, 82:84)]
# write.csv(Jun_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_nlnw.csv")
# Jun_lw <- Jun_data[which(Jun_data$Cohort == 1), c(1:46, 56, 58:60, 82:84)]
# write.csv(Jun_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_lw.csv")
# Jun_lnw <- Jun_data[which(Jun_data$Cohort == 1), c(1:46, 57, 58:60, 82:84)]
# write.csv(Jun_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_lnw.csv")


#Jul_data <- full_presence_data[which(months(full_presence_data$Month_telem) == "Jul"),]
# Jul_nlw <- Jul_data[which(Jul_data$Cohort >1), c(1:46, 61, 65:67, 82:84)]
# write.csv(Jul_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_nlw.csv")
# Jul_nlnw <- Jul_data[which(Jul_data$Cohort >1), c(1:46, 62, 65:67, 82:84)]
# write.csv(Jul_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_nlnw.csv")
# Jul_lw <- Jul_data[which(Jul_data$Cohort == 1), c(1:46, 63, 65:67, 82:84)]
# write.csv(Jul_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_lw.csv")
# Jul_lnw <- Jul_data[which(Jul_data$Cohort == 1), c(1:46, 64, 65:67, 82:84)]
# write.csv(Jul_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_lnw.csv")


#Aug_data <- full_presence_data[which(months(full_presence_data$Month_telem) == "Aug"),]
# Aug_nlw <- Aug_data[which(Aug_data$Cohort>1), c(1:46, 68, 72:74, 82:84)]
# write.csv(Aug_nlw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_nlw.csv")
# Aug_nlnw <- Aug_data[which(Aug_data$Cohort>1), c(1:46, 69, 72:74, 82:84)]
# write.csv(Aug_nlnw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_nlnw.csv")
# Aug_lw <- Aug_data[which(Aug_data$Cohort == 1), c(1:46, 70, 72:74, 82:84)]
# write.csv(Aug_lw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_lw.csv")
# Aug_lnw <- Aug_data[which(Aug_data$Cohort == 1), c(1:46, 71, 72:74, 82:84)]
# write.csv(Aug_lnw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_lnw.csv")


#Sep_data <- full_presence_data[which(months(full_presence_data$Month_telem) == "Sep"),]
# Sep_nlw <- Sep_data[which(Sep_data$Cohort > 1), c(1:46, 75, 79:84)]
# write.csv(Sep_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_nlw.csv")
# Sep_nlnw <- Sep_data[which(Sep_data$Cohort > 1), c(1:46, 76, 79:84)]
# write.csv(Sep_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_nlnw.csv")
# Sep_lw <- Sep_data[which(Sep_data$Cohort == 1), c(1:46, 77, 79:84)]
# write.csv(Sep_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_lw.csv")
# Sep_lnw <- Sep_data[which(Sep_data$Cohort == 1), c(1:46, 78:84)]
# write.csv(Sep_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_lnw.csv")



#########################################################
###Create files for class/month combos (Include background sampling across both space and time)
##########################################################
#add column with "Month" as variable, change colname of metabolic rate to "Metabolic Cost (kj/d)", temp max, min, cloud)

May_data <- full_presence_data[which(months(full_presence_data$Date_telem) == "May"),] #seperate GPS locations from May
May_data <- May_data[which(May_data$Location_Status == 'Out_of_Den'),] #remove in den locations
May_nlw <- rbind(May_data[which(May_data$Cohort > 1),c(1:47, 51:53,82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(May_data$Cohort >1))),c(1:47, 51:53,82:84)]) #added random background balanced with amount of data
May_nlnw <- rbind(May_data[which(May_data$Cohort > 1),c(1:46, 48, 51:53,82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(May_data$Cohort >1))), c(1:46, 48, 51:53,82:84)])
May_lw <- rbind(May_data[which(May_data$Cohort == 1),c(1:46, 49, 51:53,82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(May_data$Cohort ==1))), c(1:46, 49, 51:53,82:84)])
May_lnw <- rbind(May_data[which(May_data$Cohort == 1),c(1:46, 50, 51:53,82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(May_data$Cohort ==1))), c(1:46, 50, 51:53,82:84)])

colnames(May_nlw) <- c(colnames(May_nlw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(May_nlw)[51:53])
May_nlw$Month <- rep("May", dim(May_nlw)[1])
May_nlw <- May_nlw[which(!is.na(May_nlw$`Metabolic_Rate_(kj/d)`)),]
colnames(May_nlnw) <- c(colnames(May_nlnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(May_nlnw)[51:53])
May_nlnw$Month <- rep("May", dim(May_nlnw)[1])
May_nlnw <- May_nlnw[which(!is.na(May_nlnw$`Metabolic_Rate_(kj/d)`)),]
colnames(May_lw) <- c(colnames(May_lw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(May_lw)[51:53])
May_lw$Month <- rep("May", dim(May_lw)[1])
May_lw <- May_lw[which(!is.na(May_lw$`Metabolic_Rate_(kj/d)`)),]
colnames(May_lnw) <- c(colnames(May_lnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(May_lnw)[51:53])
May_lnw$Month <- rep("May", dim(May_lnw)[1])
May_lnw <- May_lnw[which(!is.na(May_lnw$`Metabolic_Rate_(kj/d)`)),]

write.csv(May_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_nlw.csv")
write.csv(May_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_nlnw.csv")
write.csv(May_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_lw.csv")
write.csv(May_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/May_lnw.csv")


Jun_data <- full_presence_data[which(months(full_presence_data$Date_telem) == "Jun"),]
Jun_nlw <- rbind(Jun_data[which(Jun_data$Cohort > 1), c(1:46, 54, 58:60, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jun_data$Cohort > 1))), c(1:46, 54, 58:60, 82:84)])
Jun_nlnw <- rbind(Jun_data[which(Jun_data$Cohort > 1), c(1:46, 55, 58:60, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jun_data$Cohort > 1))), c(1:46, 55, 58:60, 82:84)])
Jun_lw <- rbind(Jun_data[which(Jun_data$Cohort == 1), c(1:46, 56, 58:60, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jun_data$Cohort == 1))), c(1:46, 56, 58:60, 82:84)])
Jun_lnw <- rbind(Jun_data[which(Jun_data$Cohort == 1), c(1:46, 57, 58:60, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jun_data$Cohort == 1))), c(1:46, 57, 58:60, 82:84)])


colnames(Jun_nlw) <- c(colnames(Jun_nlw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jun_nlw)[51:53])
Jun_nlw$Month <- rep("Jun", dim(Jun_nlw)[1])
Jun_nlw <- Jun_nlw[which(!is.na(Jun_nlw$`Metabolic_Rate_(kj/d)`)),]
colnames(Jun_nlnw) <- c(colnames(Jun_nlnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jun_nlnw)[51:53])
Jun_nlnw$Month <- rep("Jun", dim(Jun_nlnw)[1])
Jun_nlnw <- Jun_nlnw[which(!is.na(Jun_nlnw$`Metabolic_Rate_(kj/d)`)),]
colnames(Jun_lw) <- c(colnames(Jun_lw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jun_lw)[51:53])
Jun_lw$Month <- rep("Jun", dim(Jun_lw)[1])
Jun_lw <- Jun_lw[which(!is.na(Jun_lw$`Metabolic_Rate_(kj/d)`)),]
colnames(Jun_lnw) <- c(colnames(Jun_lnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jun_lnw)[51:53])
Jun_lnw$Month <- rep("Jun", dim(Jun_lnw)[1])
Jun_lnw <- Jun_lnw[which(!is.na(Jun_lnw$`Metabolic_Rate_(kj/d)`)),]


write.csv(Jun_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_nlw.csv")
write.csv(Jun_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_nlnw.csv")
write.csv(Jun_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_lw.csv")
write.csv(Jun_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jun_lnw.csv")


Jul_data <- full_presence_data[which(months(full_presence_data$Date_telem) == "Jul"),]
Jul_nlw <- rbind(Jul_data[which(Jul_data$Cohort >1), c(1:46, 61, 65:67, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jul_data$Cohort > 1))), c(1:46, 61, 65:67, 82:84)])
Jul_nlnw <- rbind(Jul_data[which(Jul_data$Cohort >1), c(1:46, 62, 65:67, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jul_data$Cohort > 1))), c(1:46, 62, 65:67, 82:84)])
Jul_lw <- rbind(Jul_data[which(Jul_data$Cohort == 1), c(1:46, 63, 65:67, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jul_data$Cohort == 1))), c(1:46, 63, 65:67, 82:84)])
Jul_lnw <- rbind(Jul_data[which(Jul_data$Cohort == 1), c(1:46, 64, 65:67, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Jul_data$Cohort == 1))), c(1:46, 64, 65:67, 82:84)])


colnames(Jul_nlw) <- c(colnames(Jul_nlw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jul_nlw)[51:53])
Jul_nlw$Month <- rep("Jul", dim(Jul_nlw)[1])
Jul_nlw <- Jul_nlw[which(!is.na(Jul_nlw$`Metabolic_Rate_(kj/d)`)),]
colnames(Jul_nlnw) <- c(colnames(Jul_nlnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jul_nlnw)[51:53])
Jul_nlnw$Month <- rep("Jul", dim(Jul_nlnw)[1])
Jul_nlnw <- Jul_nlnw[which(!is.na(Jul_nlnw$`Metabolic_Rate_(kj/d)`)),]
colnames(Jul_lw) <- c(colnames(Jul_lw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jul_lw)[51:53])
Jul_lw$Month <- rep("Jul", dim(Jul_lw)[1])
Jul_lw <- Jul_lw[which(!is.na(Jul_lw$`Metabolic_Rate_(kj/d)`)),]
colnames(Jul_lnw) <- c(colnames(Jul_lnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Jul_lnw)[51:53])
Jul_lnw$Month <- rep("Jul", dim(Jul_lnw)[1])
Jul_lnw <- Jul_lnw[which(!is.na(Jul_lnw$`Metabolic_Rate_(kj/d)`)),]


write.csv(Jul_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_nlw.csv")
write.csv(Jul_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_nlnw.csv")
write.csv(Jul_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_lw.csv")
write.csv(Jul_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Jul_lnw.csv")


Aug_data <- full_presence_data[which(months(full_presence_data$Date_telem) == "Aug"),]
Aug_nlw <- rbind(Aug_data[which(Aug_data$Cohort>1), c(1:46, 68, 72:74, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Aug_data$Cohort > 1))), c(1:46, 68, 72:74, 82:84)])
Aug_nlnw <- rbind(Aug_data[which(Aug_data$Cohort>1), c(1:46, 69, 72:74, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Aug_data$Cohort > 1))), c(1:46, 69, 72:74, 82:84)])
Aug_lw <- rbind(Aug_data[which(Aug_data$Cohort == 1), c(1:46, 70, 72:74, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Aug_data$Cohort == 1))), c(1:46, 70, 72:74, 82:84)])
Aug_lnw <- rbind(Aug_data[which(Aug_data$Cohort == 1), c(1:46, 71, 72:74, 82:84)], full_absence_data[sample(nrow(full_absence_data), length(which(Aug_data$Cohort == 1))), c(1:46, 71, 72:74, 82:84)])

colnames(Aug_nlw) <- c(colnames(Aug_nlw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Aug_nlw)[51:53])
Aug_nlw$Month <- rep("Aug", dim(Aug_nlw)[1])
Aug_nlw <- Aug_nlw[which(!is.na(Aug_nlw$`Metabolic_Rate_(kj/d)`)),]
colnames(Aug_nlnw) <- c(colnames(Aug_nlnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Aug_nlnw)[51:53])
Aug_nlnw$Month <- rep("Aug", dim(Aug_nlnw)[1])
Aug_nlnw <- Aug_nlnw[which(!is.na(Aug_nlnw$`Metabolic_Rate_(kj/d)`)),]
colnames(Aug_lw) <- c(colnames(Aug_lw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Aug_lw)[51:53])
Aug_lw$Month <- rep("Aug", dim(Aug_lw)[1])
Aug_lw <- Aug_lw[which(!is.na(Aug_lw$`Metabolic_Rate_(kj/d)`)),]
colnames(Aug_lnw) <- c(colnames(Aug_lnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Aug_lnw)[51:53])
Aug_lnw$Month <- rep("Aug", dim(Aug_lnw)[1])
Aug_lnw <- Aug_lnw[which(!is.na(Aug_lnw$`Metabolic_Rate_(kj/d)`)),]


write.csv(Aug_nlw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_nlw.csv")
write.csv(Aug_nlnw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_nlnw.csv")
write.csv(Aug_lw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_lw.csv")
write.csv(Aug_lnw, "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Aug_lnw.csv")


Sep_data <- full_presence_data[which(months(full_presence_data$Date_telem) == "Sep"),]
Sep_nlw <- rbind(Sep_data[which(Sep_data$Cohort > 1), c(1:46, 75, 79:84)],  full_absence_data[sample(nrow(full_absence_data), length(which(Sep_data$Cohort > 1))), c(1:46, 75, 79:84)])
Sep_nlnw <- rbind(Sep_data[which(Sep_data$Cohort > 1), c(1:46, 76, 79:84)],  full_absence_data[sample(nrow(full_absence_data), length(which(Sep_data$Cohort > 1))), c(1:46, 76, 79:84)])
Sep_lw <- rbind(Sep_data[which(Sep_data$Cohort == 1), c(1:46, 77, 79:84)],  full_absence_data[sample(nrow(full_absence_data), length(which(Sep_data$Cohort == 1))), c(1:46, 77, 79:84)])
Sep_lnw <- rbind(Sep_data[which(Sep_data$Cohort == 1), c(1:46, 78:84)],  full_absence_data[sample(nrow(full_absence_data), length(which(Sep_data$Cohort == 1))), c(1:46, 78:84)])


colnames(Sep_nlw) <- c(colnames(Sep_nlw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Sep_nlw)[51:53])
Sep_nlw$Month <- rep("Sep", dim(Sep_nlw)[1])
Sep_nlw <- Sep_nlw[which(!is.na(Sep_nlw$`Metabolic_Rate_(kj/d)`)),]
colnames(Sep_nlnw) <- c(colnames(Sep_nlnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Sep_nlnw)[51:53])
Sep_nlnw$Month <- rep("Sep", dim(Sep_nlnw)[1])
Sep_nlnw <- Sep_nlnw[which(!is.na(Sep_nlnw$`Metabolic_Rate_(kj/d)`)),]
colnames(Sep_lw) <- c(colnames(Sep_lw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Sep_lw)[51:53])
Sep_lw$Month <- rep("Sep", dim(Sep_lw)[1])
Sep_lw <- Sep_lw[which(!is.na(Sep_lw$`Metabolic_Rate_(kj/d)`)),]
colnames(Sep_lnw) <- c(colnames(Sep_lnw)[1:46], "Metabolic_Rate_(kj/d)", "Max_temp", "Min_temp", "Cloud", colnames(Sep_lnw)[51:53])
Sep_lnw$Month <- rep("Sep", dim(Sep_lnw)[1])
Sep_lnw <- Sep_lnw[which(!is.na(Sep_lnw$`Metabolic_Rate_(kj/d)`)),]


write.csv(Sep_nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_nlw.csv")
write.csv(Sep_nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_nlnw.csv")
write.csv(Sep_lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_lw.csv")
write.csv(Sep_lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/Sep_lnw.csv")


#########################################################
###Different reproductive class but all months combined
##########################################################
nlw <- rbind(May_nlw, Jun_nlw, Jul_nlw, Aug_nlw, Sep_nlw)
nlnw <- rbind(May_nlnw, Jun_nlnw, Jul_nlnw, Aug_nlnw, Sep_nlnw)
lw <- rbind(May_lw, Jun_lw, Jul_lw, Aug_lw, Sep_lw)
lnw <- rbind(May_lnw, Jun_lnw, Jul_lnw, Aug_lnw, Sep_lnw)

write.csv(nlw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/nlw.csv")
write.csv(nlnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/nlnw.csv")
write.csv(lw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/lw.csv")
write.csv(lnw, file = "C:/Users/Savannah Rogers/Documents/MSGrizzlyProject/GeneticProgram_SpeciesPresence/input_data/lnw.csv")
