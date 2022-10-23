

## packages
library(ggplot2)
library(dplyr)
library(here)
library(scales)

theme_new <- function(base_size = 24){
  theme_bw(base_size = base_size) %+replace%
    theme(
      panel.grid = element_blank(),   
      panel.border = element_rect(fill = NA, colour = "black", size=1),
      panel.background = element_rect(fill = "white", colour = "black"), 
      strip.background = element_rect(fill = NA),
      axis.text.x = element_text(color = "black"),
      axis.text.y = element_text(color = "black")
    )
}


## load data
dc_filings_crdc <- read.csv(here("intermediate_objects/cleaned_df/dc_filings_wcrdc.csv"),
                            colClasses = c("ncesid_clean" = "character")) %>%
                  rename(total_filings = case_no) %>%
                  mutate(total_filings = case_when(is.na(total_filings) ~ 0,
                                                   TRUE ~ total_filings),
                        filings_perstudent = (total_filings/total_students_iep_data)*100,
                        filings_periep = (total_filings/STUDENTS_WITH_DISABILITIES_SERVED_UNDER_IDEA)*100,
                        binary_filings = total_filings > 0) 

nschools_nofilings = nrow(dc_filings_crdc %>% filter(total_filings == 0))
## plot the distribution of total filings
ggplot(dc_filings_crdc, aes(x = total_filings)) +
  geom_histogram(fill = "wheat4", color = "black") +
  theme_new(base_size = 24)  + 
  ylab("Number of schools") +
  xlab("Number of due process filings:\nSY 2014-2015 to SY 2017-2018") +
  annotate("text",
           x = 30, 
           y = 60,
           color = "red",
           label = "45% of schools have >1 IEP\n but no filings",
           size = 10)

ggsave(here("output/dc_filings_hist.pdf"),
       plot = last_plot(),
       device = "pdf",
       width = 12,
       height = 8)


## look at total discipline rate
disc_rate <- dc_filings_crdc %>% group_by(case_status) %>%
            summarise(mean_disc = mean(TOTAL_DISCIPLINE_rate, na.rm = TRUE)*100,
                      mean_restraint = mean(TOTAL_RESTRAINT_SECLUDE_rate, na.rm = TRUE)*100) %>%
            ungroup() 

ggplot(disc_rate, aes(x = case_status, y = mean_disc,
                      fill = case_status)) +
  geom_bar(stat = "identity", color = "black") +
  ylab("Mean disciplinary rates per 100 students") + 
  xlab("Any filings SY 2014-2015 to SY 2017-2018") +
  theme_new(base_size = 24) +
  guides(fill = "none") +
  scale_fill_manual(values = c("No filings" = "firebrick",
                               "Any filings" = "wheat4"))

ggsave(here("output/dc_filings_discipline.pdf"),
       plot = last_plot(),
       device = "pdf",
       width = 12,
       height = 8)

ggplot(disc_rate, aes(x = case_status, y = mean_restraint,
                      fill = case_status)) +
  geom_bar(stat = "identity", color = "black") +
  ylab("Mean use of restraint or seclusion\nper 100 students\nCRDC SY 2013-2014") + 
  xlab("Any filings SY 2014-2015 to SY 2017-2018") +
  theme_new(base_size = 24) +
  guides(fill = "none") +
  scale_fill_manual(values = c("No filings" = "firebrick",
                               "Any filings" = "wheat4"))

ggsave(here("output/dc_filings_restraint.pdf"),
       plot = last_plot(),
       device = "pdf",
       width = 12,
       height = 8)


## try loading race from api --- doesn't seem to be working
df_race <- read.csv(here("raw_input/dc/dc_ccd_raceperc.csv")) %>%
          mutate(ncesid_clean = sprintf("%s0", as.character(ID)))
colnames(df_race) <- gsub("\\.", "_", tolower(colnames(df_race)))
head(df_race)

## merge onto filings data
dc_filings_crdc_wrace <- merge(dc_filings_crdc,
                               df_race,
                               by = "ncesid_clean",
                               all.x = TRUE)

## summarise
dem_rate <- dc_filings_crdc_wrace %>% group_by(case_status) %>%
  summarise(mean_black = mean(black, na.rm = TRUE)*100,
            mean_hisp = mean(hispanic, na.rm = TRUE)*100,
            mean_white = mean(white, na.rm = TRUE)*100,
            mean_el = mean(el, na.rm = TRUE)*100) %>%
  ungroup() %>%
  reshape2::melt(, id.vars = "case_status") %>%
  mutate(category = case_when(grepl("black", variable) ~ "Black",
                              grepl("hisp", variable) ~ "Hispanic",
                              grepl("white", variable) ~ "White",
                              TRUE ~ "ELL")) 

ggplot(dem_rate, aes(x = reorder(category, value), y = value, group = case_status,
                     fill = case_status)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  theme_new(base_size = 24) +
  theme(legend.position = c(0.2, 0.8),
        legend.background = element_blank()) +
  xlab("Demographic category") +
  ylab("Mean demographic percentages\nfor that case status") +
  labs(fill = "Filings status") +
  scale_fill_manual(values = c("No filings" = "firebrick",
                               "Any filings" = "wheat4")) +
  scale_y_continuous(breaks = pretty_breaks(n = 10))

ggsave(here("output/dc_filings_dem.pdf"),
       plot = last_plot(),
       device = "pdf",
       width = 12,
       height = 8)

