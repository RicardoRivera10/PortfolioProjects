
install.packages("tidyverse")

library(tidyverse)
view(starwars)
# Notice, we have missing values, other things we need to clean up FIRST before moving forward


# Viewing Variable types
glimpse(starwars)

# Seeing our variables, there are certain ones I want to make factors for level sake
class(starwars$gender)
# We can use "unique" to see all responses that were used for the category/variable
unique(starwars$gender)



# Let's replace with factor
starwars$gender <- as.factor(starwars$gender)
class(starwars$gender)


# Check levels, let's change feminine position with masculine, make sure to concatenate
levels(starwars$gender)
starwars$gender <- factor((starwars$gender), levels = c("masculine","feminine"))
levels(starwars$gender)
##########################

# Now let's start looking more at our database
names(starwars)

starwars %>% 
  select(name, height, ends_with("color"))

unique(starwars$hair_color)

starwars %>%
  select(name, height, ends_with("color")) %>% 
  filter(hair_color %in% c("blond", "brown") & height < 180)

# Here, I noticed I was not retrieving Luke because blonde is not spelled correctly
# in the dataframe, let's quickly correct that!


# Let's make it TRUE that we are removing NA values
mean(starwars$height, na.rm = TRUE)

# I can use ! to mark all values that have NA present, look where and WHY the data is missing
# I see hair is missing on androids that do not have hair, whereas height just seems to be missing
starwars %>% 
  select(name, gender, hair_color, height) %>% 
  filter(!complete.cases(.))


# After observing data, we can replace NA with "none"
starwars %>% 
  select(name, gender, hair_color, height) %>% 
  filter(complete.cases(.)) %>% 
  drop_na(height)

starwars %>% 
  select(name, gender, hair_color, height) %>% 
  filter(!complete.cases(.)) %>% 
  mutate(hair_color = replace_na(hair_color, "none"))

# starwars %>% 
#   select(name, gender, hair_color, height) %>% 
#   filter(!complete.cases(.)) %>% 
#   mutate(hair_color2 = replace_na(hair_color, "none"))




# Attempt at recoding variables, I want masculine and feminine to become 1 and 2
starwars %>%  select(name, gender)

starwars %>% 
  select(name, gender) %>% 
  mutate(gender = recode(gender,
                         "masculine" = 1,
                         "feminine" = 2))






## Practice with duplicates

Names <- c("Peter", "John", "Andrew", "Peter")
Age <- c(22,33,44,22)
friends <- data.frame(Names, Age)
# Use !duplicated to get rows that ARE NOT duplicates
friends[!duplicated(friends), ]
friends %>% 
  distinct() %>% 
  view()







# CLEAN UP #################################################

# Clear environment
rm(list = ls())

# Clear packages
p_unload(all)  # Remove all add-ons
detach("package:datasets", unload = TRUE)  # For base

# Clear plots
dev.off()  # But only if there IS a plot

# Clear console
cat("\014")  # ctrl+L

