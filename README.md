# HolidayPlanner

## Overview
An automated holiday planner which will offer suggestions for a holiday schedule based on location, events, weather ect. Will provide notifications and automated changes to schedule if weather or events change/cancel.

## Environment Set Up
The required packages are captured in holplan_env.yml file. When using conda as package manager you can recreate the environment locally via: <code>conda env create -f holplan_env.yml -n holenv</code>

Once the environment has been set up and github has been linked to your workspace, type <code> pre-commit install </code> in your conda terminal. This will ensure all pre commit coding standards are implemented.

To see these checks occuring in real time, when commiting using <code> git commit -m "{your commit message}" </code>

## Data Sources (draft)
<ol>
  <li>Mapping</li>
  <li>Weather Forecasts</li>
  <li>User Data (Budget, Schedule)</li>
  <li>Nearby Activities</li>
</ol>
