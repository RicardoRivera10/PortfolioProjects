-- Query used for Tableau 
-- Remember to check for nulls, Tableau will mistake

-- Objective 1: 
SELECT SUM(new_cases) as total_cases, SUM(CAST(new_deaths as int)) as total_deaths, SUM(CAST(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage --Cannot do SUM(MAX(total_cases)) since it is an aggregate inside aggregate
FROM PortfolioProject1..CovidDeaths
WHERE continent is not null
--GROUP by date
ORDER by 1,2


-- Objective 2:
-- We take out as they are not included in the above queries, consistency purposes
-- Only inlude the continents, this will be how we showcase the total deaths per cont.
SELECT location, SUM(CAST(new_deaths as float)) as TotalDeathCt
FROM PortfolioProject1..CovidDeaths
WHERE continent is null
and location in ('Europe', 'North America', 'Asia', 'South America', 'Africa','Oceania')
GROUP by location
ORDER by TotalDeathCt desc


-- Objective 3: Get data to work with in Tableau so we can showcase the different percentages through the countries of the globe
SELECT location, population, MAX(total_cases) as HighestInfectionCt, MAX((total_cases/population))*100 as PercentPopulationInfected
FROM PortfolioProject1..CovidDeaths
GROUP by location, population
ORDER by PercentPopulationInfected desc

--Objective 4: Here, we want to essentially gather the same data as before, this time grouping by date as well to showcase a timeline
SELECT location, population, date, MAX(total_cases) as HighestInfectionCt, MAX((total_cases/population))*100 as PercentPopulationInfected
FROM PortfolioProject1..CovidDeaths
GROUP by location, population, date
ORDER by PercentPopulationInfected desc

+