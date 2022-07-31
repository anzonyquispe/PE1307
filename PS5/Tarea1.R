# Prior to use, install the following packages:
install.packages("ggplot2")
install.packages("tibble")
install.packages("dplyr")
install.packages("gridExtra")
install.packages("Lock5Data")
install.packages("ggthemes")
install.packages("extrafont")
install.packages("maps")
install.packages("mapproj")
install.packages("corrplot")
install.packages("fun")
install.packages("zoo")
install.packages("egg")
install.packages("tidyverse")

#Load Libraries
library("ggplot2")
library("tibble")
library("extrafont")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("tidyverse")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")
library("egg")

#Set pathname for the directory where you have data
setwd( "C:/Users/Anzony/Documents/GitHub/PE1307/PS5")
#Check working directory
getwd()


#Load the data files
df <- read.csv("_data/gapminder-data.csv")
df2 <- read.csv("_data/xAPI-Edu-Data.csv")
df3 <- read.csv("_data/LoanStats.csv")

#Summary of the three datasets
str(df)
str(df2)
str(df3)

############################################
###############Plot 1#######################
############################################
# Original PLot
p1 <- ggplot(df,aes(x=Electricity_consumption_per_capita)) + 
  geom_histogram(bins=15) + xlab("Electricity consumption per capita")
p1
ggsave(p1, filename = "_figures/p1.png", 
       height = 5, width = 4, units = "in")

# New plot
# Importing Word Fonts
font_import()
loadfonts(device="win")

# Generating new plot
p1_new <- ggplot(df,aes(x=Electricity_consumption_per_capita)) + 
  geom_histogram(bins=20, fill = 'dodgerblue') + 
  ggtitle( "Electricity Consumption Per Capita", subtitle =  "(kWh/pp)") +
  xlab("") + ylab("Count") +
  theme_bw() + 
  theme(
    text=element_text(family="Times New Roman"),
    plot.title = element_text( face = "bold", size = 12, 
                               hjust = -0.65, vjust=2.12),
    plot.subtitle = element_text( hjust = -0.15, vjust=2.12),
    legend.background = element_rect(fill = "white", 
                                     size = 4, colour = "white"),
    axis.ticks = element_line(colour = "grey70", size = 0.2),
    panel.grid.major = element_line(colour = "grey70", size = 0.2),
    panel.grid.minor = element_blank()
  )

# Save plots
ggsave(p1_new, filename = "_figures/p1_new.png", 
       height = 5, width = 4, units = "in")


############################################
###############Plot 2#######################
############################################
# Original PLot
# Original plot
p2 <- ggplot(df, aes( x = gdp_per_capita, y = Electricity_consumption_per_capita )) + 
  geom_point() + 
  facet_grid(Country ~ .) + 
  facet_grid(. ~ Country) + 
  facet_wrap(~Country, )
# Save plots
ggsave(p2, filename = "_figures/p2.png", 
       height = 5, width = 4, units = "in")


# New Plot
p2_new <- ggplot(df, 
                 aes( x = gdp_per_capita, 
                      y = Electricity_consumption_per_capita)) + 
  geom_point( size = 0.5  ) + 
  scale_x_continuous( guide = guide_axis(check.overlap = TRUE) ) +
  # facet_grid(Country ~ .) + 
  # facet_grid(. ~ Country) + 
  facet_wrap(~Country, scale = c("free" ) ) + 
  ggtitle( "GDP and Electricity Consumption", subtitle =  "Per Capita") +
  xlab("GDP") + ylab("Electricity Cosumption") +
  theme_bw() +
  theme(
    axis.text=element_text(size=6), 
    text=element_text(family="Times New Roman"),
    plot.title = element_text( face = "bold", size = 12, 
                               hjust = -0.8, vjust=2.12),
    plot.subtitle = element_text( hjust = -0.2, vjust=2.12),
    legend.background = element_rect(fill = "white", size = 4, colour = "white"),
    axis.ticks = element_line(colour = "grey70", size = 0.2),
    panel.grid.major = element_line(colour = "grey70", size = 0.2),
    panel.grid.minor = element_blank(), 
    panel.grid.major.x = element_blank(),
    panel.spacing.x = unit(4, "mm"), 
    strip.background = element_blank(),
    panel.background = element_rect(colour = "white", fill = "white"),
    strip.text = element_text(size=8)
  )
p2_new

ggsave(p2_new, filename = "_figures/p2_new.png", 
       height = 5, width = 4, units = "in")

############################################
###############Plot 3#######################
############################################
# Original PLot
dfn <- subset(HollywoodMovies2013, Genre %in% c("Action","Adventure","Comedy","Drama","Romance")
              & LeadStudio %in% c("Fox","Sony","Columbia","Paramount","Disney"))
# Developing the plot
p3 <- ggplot( dfn, aes( Genre, WorldGross ) ) + 
  geom_bar( stat = "Identity", aes( fill = LeadStudio ), position = "dodge" ) + 
  theme( axis.title.x = element_text( size = 15 ),
         axis.title.y=element_text(size=15),
         plot.background=element_rect(fill="gray87"),
         panel.background = element_rect(fill="beige"),
         panel.grid.major = element_line(color="Gray",linetype=1)
)
p3
# Saving Original Plot
ggsave(p3, filename = "_figures/p3.png", 
       height = 5, width = 4, units = "in")

# New plot
dfn$LeadStudio = as.character(dfn$LeadStudio) 

# Working with the dataset
# Getting statistics by group
dfn2 = dfn %>% 
  dplyr::group_by( Genre, LeadStudio  ) %>% 
  dplyr::summarise( WorldGross = sum(WorldGross)) %>% 
  group_by(Genre) %>% 
  mutate(position = rank(WorldGross))

# Developing the new plot
p3_new <- ggplot(dfn2,aes(Genre,WorldGross, fill=LeadStudio, group = position)) + 
  geom_bar(stat="Identity", position="dodge") +
  coord_flip() + scale_x_discrete( limits = rev ) + 
  ggtitle( "Total World Gross by Genre and Lead Studio") +
  xlab("Genre") + ylab("World Gross") +
  theme_bw() +
  theme(
    # axis.text=element_text(size=6), 
    text=element_text(family="Times New Roman", size= 10),
    plot.title = element_text( face = "bold", size = 12, 
                               hjust = -0.28, 
                               margin = margin(0,0,10,0)),
    axis.title.y = element_text(margin=margin(0,0,0,0)), 
    legend.background = element_rect(fill = "white", size = 4, colour = "white"),
    axis.ticks = element_line(colour = "grey70", size = 0.2),
    legend.direction = "horizontal",
    legend.box = "vertical",
    legend.position = "top", 
    legend.justification='left',
    legend.margin=margin(), 
    legend.text=element_text(size=6),) +
  guides(size=guide_legend(direction='horizontal'), 
         fill=guide_legend(title="Lead Studio")) +
  scale_fill_brewer(palette="Paired")
p3_new
# Saving Original Plot
ggsave(p3_new, filename = "_figures/p3_new.png", 
       height = 5, width = 7, units = "in")