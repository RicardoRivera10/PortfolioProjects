SELECT * FROM PortfolioProject1..CovidDeaths WHERE continent is not null
ORDER by 3,4


-- Select the data that we are going to be using

--SELECT Location, date, total_cases, total_deaths, population
--FROM PortfolioProject1..CovidDeaths

SELECT Location, date, total_cases, new_cases, total_deaths, population
FROM PortfolioProject1..CovidDeaths WHERE continent is not null
ORDER by 1,2


-- Object 1: Total cases vs. Total Deaths
--First, I want to clean up and delete any rows with 0 cases as those do not affect us
--Adding the states can give us insight into your specific country
DELETE FROM PortfolioProject1..CovidDeaths WHERE total_cases = 0

SELECT Location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
FROM PortfolioProject1..CovidDeaths WHERE location like '%states%'
ORDER by 1,2


-- Objective 2: Look at total cases vs Population
-- Insight into what percentage of a country got Covid 
SELECT Location, date, population, total_cases, (total_cases/population)*100 as CasePercentage
FROM PortfolioProject1..CovidDeaths WHERE location like '%states%'
ORDER by 1,2

-- Objective 3: Countries with highest infection rate compared to their population

SELECT Location, population, MAX(total_cases) as HighestInfectedct, MAX((total_cases/population))*100 as PercentPopulationInfected
FROM PortfolioProject1..CovidDeaths GROUP by location, population
ORDER by PercentPopulationInfected DESC


-- Objective 4: Show highest death count per population

SELECT Location, MAX(cast(total_deaths as int)) as TotalDeathCt
FROM PortfolioProject1..CovidDeaths WHERE continent is not null GROUP by location
ORDER by TotalDeathCt DESC



-- Now, break things down by continent
SELECT continent, MAX(cast(total_deaths as int)) as TotalDeathCt
FROM PortfolioProject1..CovidDeaths WHERE continent is not null GROUP by continent
ORDER by TotalDeathCt DESC
-- We can see running this that NA is only including the United States

SELECT continent, MAX(cast(total_deaths as int)) as TotalDeathCt
FROM PortfolioProject1..CovidDeaths WHERE continent is not null GROUP by continent
ORDER by TotalDeathCt DESC


-- Global 

SELECT date, SUM(new_cases), SUM(CAST(new_deaths as int)), SUM(CAST(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage --Cannot do SUM(MAX(total_cases)) since it is an aggregate inside aggregate
FROM PortfolioProject1..CovidDeaths
WHERE continent is not null
--GROUP by date
ORDER by 1,2





-- Looking at total population vs Vaccinations by continually adding those new who have been vaccinated
SELECT *
FROM PortfolioProject1..CovidDeaths dea
Join PortfolioProject1..CovidVaccines vac
	On dea.location = vac.location
	and dea.date = vac.date

-- Use CTE now

WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingVaccinated)
as
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(CAST(vac.new_vaccinations as float)) OVER (Partition by
dea.location ORDER by dea.location, dea.date) as RollingVaccinated

FROM PortfolioProject1..CovidDeaths dea
Join PortfolioProject1..CovidVaccines vac
	On dea.location = vac.location
	and dea.date = vac.date
WHERE dea.continent is not null
-- ORDER by 2,3
)
SELECT *, (RollingVaccinated/population)*100
FROM PopvsVac



-- Temp Table

DROP TABLE if exists #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
Continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric
new_vaccinations numeric,
RollingVaccinated numeric
)

INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(CAST(vac.new_vaccinations as float)) OVER (Partition by
dea.location ORDER by dea.location, dea.date) as RollingVaccinated

FROM PortfolioProject1..CovidDeaths dea
Join PortfolioProject1..CovidVaccines vac
	On dea.location = vac.location
	and dea.date = vac.date
-- WHERE dea.continent is not null
-- ORDER by 2,3

SELECT *, (RollingVaccinated/population)*100
FROM PopvsVac

-- Creating view with the format above, this created another place we can select data from
--
USE PortfolioProject1
GO
CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(CAST(vac.new_vaccinations as float)) OVER (Partition by
dea.location ORDER by dea.location, dea.date) as RollingVaccinated

FROM PortfolioProject1..CovidDeaths dea
Join PortfolioProject1..CovidVaccines vac
	On dea.location = vac.location
	and dea.date = vac.date
-- WHERE dea.continent is not null
-- ORDER by 2,3
