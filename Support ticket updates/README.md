# Support ticket updates (global / follow-the-sun customer service)


**Goal:** Report on the performance of customer support/service agents across timezones, including the degree to which each global office provides follow-the-sun (FTS) support.

**Approach:** Create a fictional dataset by using an Excel-based random person and support ticket generator, ensuring the data includes realistic patterns and outliers. Then build a Power BI report that summarises patterns and highlights outlers to prompt managerial review.


## RESULT
**[My Power BI visualisation](https://community.powerbi.com/t5/Data-Stories-Gallery/Follow-the-sun-customer-service-support/m-p/2168279)**

![My Power BI visualisation](https://datamesse.github.io/static/media/img-2021-11-power-bi-follow-the-sun-customer-support.04103ee9.png)

Original Data Sources: 
* See below


## INSTRUCTIONS TO CREATE RANDOMISED DATASET

### Random business and people's name generator

* [https://github.com/datamesse/data-visualisation-datasets/blob/main/Support ticket updates/Random name and business generator.xlsx](https://github.com/datamesse/data-visualisation-datasets/raw/main/Support%20ticket%20updates/Random%20name%20and%20business%20generator.xlsx?raw=true)

By default this creates 3000 random names across 500 random businesses.

![Random name generator](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/01.png?raw=true)

![Random business generator](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/02.png?raw=true)

Revise your output for duplicates or other such data. Once your output is cleaned up, use the Full Name and Location details to populate the Support Ticket Update Generator below.


### Random support ticket update generator

* [https://github.com/datamesse/data-visualisation-datasets/blob/main/Support ticket updates/Support ticket updates generator.xlsx](https://github.com/datamesse/data-visualisation-datasets/raw/main/Support%20ticket%20updates/Support%20ticket%20updates%20generator.xlsx?raw=true)

Sample output can be downloaded here:
* [https://github.com/datamesse/data-visualisation-datasets/blob/main/Support ticket updates/Support ticket updates.xlsx](https://github.com/datamesse/data-visualisation-datasets/raw/main/Support%20ticket%20updates/Support%20ticket%20updates.xlsx?raw=true)

Because Excel's randomisation appears to create a discrete uniform distribution, the **Main** worksheet is used to define deliberate trends.

In this case, there are 2 areas:
* *Ticket criticality ranges by country*: The probability range of an End-user raising the ticket as Critical, High, Medium, or Low based on their *Country*.
* *Development escalation by country*: The probability that an End-user's support ticket is escalated to development based on their *Country*.

How *Ticket criticality ranges by country* works: 

**Updates 1** randomises between 1 and 100, and if the value is:
 - Greater than or equal to *High*, then the ticket is "Critical".
 - Greater than or equal to *Medium*, then the ticket is "High".
 - Greater than or equal to *Low*, then the ticket is "Medium"
 - If it meets none of the conditions, it is "Low".

![Main tab of ticket update generator](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/03.png?raw=true)

**Note:** The current data in this worksheet is based on the randomised people I extracted using the first generator. If you have additional clients for other countries which are not provided here, you will need to add them in manually.


After deciding on the names to be used for the support agents, populate the relevant columns under the **Staff** worksheet (indicated in red). The columns which are autopopulated using vlookups should be left alone (e.g. *Timezone* and *Randomiser helper*). 

![Filling in support agent names in ticket update generator](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/04.png?raw=true)

There are a number of columns representing the statistics for each agent that need to be manually defined  (indicated in blue).

![Filling in support agent statistics](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/05.png?raw=true)

The following 3 columns are used by the **Updates 1** worksheet's *Assignee name* column to distribute tickets among agents belonging to the same *Office region*.

* *Region Agent number*: Sequential ID for each agent in the region beginning from 1 to *Number of agents in Office region* as the maximum.
* *Assignment proportion*: Number between 1 and 100. Recommend between 60 and 90.
* *Assignment break*: Number less than *Number of agents in Office region*.

The *Assignment proportion* and *Assignment break* values need to be the same for all users per *Office region*.

How it works: 

**Updates 1** randomises between 1 and 100, and if the value is:
 - Less than or equal to the *Assignment propotion*, then randomise between 1 and *Assignment break*.
 - More than *Assignment proportion*, randomise between *Assignment break* and *Number of agents in Office region*.
The *Randomiser Helper* column uses the resulting value to specify the Agent for **Updates 1**.

Using an example of:
 - Assignment proportion = 85
 - Assignment break = 5
 - Number of agents in Office region = 7

Excel's randomisation tries to distribute 85% of the ticket assignments to Region Agent numbers 1 to 5, and the remaining 15% is distributed to the remaining *Region Agent number*s 6 and 7. This allows defining data deliberate assignment trends. Otherwise, Excel will near-equally distribute the tickets.

These columns are specific to each agent.

* *Minimum responses*: Should at least be 1 (representing someone who closes tickets in a single response).
* *Maximum responses*: Should be higher than *Minimum responses* with maximum being the number of **Updates** worksheets dedicated to agent responses.
* *Assignment earliest time*: Earliest time in minutes for agent to pick up tickets.
* *Assignment latest time*: Latest time in minutes for agent to pick up tickets.
* *Minimum response time*: Earliest time in minutes for agent to reply to client.
* *Maximum response time*: Latest time in minutes for agent to reply to client.
* *Dev ticket self raise probability*: Probability the agent reports the development ticket for their support ticket.
* *Photo ID*: Optional field.
* *Photo URL*: Optional field.

Agent photos for the sample dataset are here:
* [https://github.com/datamesse/data-visualisation-datasets/tree/main/Support ticket updates/agents](https://github.com/datamesse/data-visualisation-datasets/tree/main/Support%20ticket%20updates/agents)

Photographs were taken from [Pixabay.com](https://pixabay.com/service/license/) and [Pexels.com](https://www.pexels.com/license/) for non-commercial use, edited to fit the appearance of an organisational profile photo, and direct URL attribution included in the dataset for each photo.

![Sample dataset agent photos](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/06.png?raw=true)

After deciding on the names to be used for the clients, populate the relevant columns under the **Client** worksheet (indicated in red).

![Filling in client names in ticket update generator](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/07.png?raw=true)

Then manually define the response times for each client.
* *Minimum response time*: Earliest time in minutes for client to reply to agent.
* *Maximum response time*: Latest time in minutes for client to reply to agent.

**Important notes:** 

1. All the numbers used in the *Office region* column of the **Client** worksheet must exist against at least one record for the *Office region* column of the **Agent** worksheet. This mapping process is what ensures agents exist to respond to clients.

2. Because the generators rely on Excel formula randomisation and Excel is typically defaulted to Automatic Workbook Calculation, each time the generator workbooks are opened or edited (or click Enter in a cell), new values are generated.

3. Based on the previous point, copying data from the ticket updates generator to another open Excel workbook risks the **Updates** and **Assignment** worksheets re-randomising during that process, and causing discrepancies. To get around that, you can Save As each worksheet as a new tab delimited flat text file. Then copy-and-paste from those flat text files into the new Excel workbook, to avoid that problem.

A third optional Excel dataset below was extracted from Wikipedia with relative data points on when Daylight Savings are applied for different timezones and the hour offsets, which I've referred to as "anchors".

### Standard and Daylight Saving Observations dataset
* [https://github.com/datamesse/data-visualisation-datasets/blob/main/Support ticket updates/Time zone offsets and DST observations.xlsx](https://github.com/datamesse/data-visualisation-datasets/raw/main/Support%20ticket%20updates/Time%20zone%20offsets%20and%20DST%20observations.xlsx?raw=true)

You can find details on how this dataset was created using Power BI in this blog post:
**[https://datamesse.github.io/#/post/1633183200](https://datamesse.github.io/#/post/1633183200)**


## POWER BI REPORT CODE

Because agents and users are based in different time zones, and date/times cover different daylight saving offsets, the Power Query code below implements a combination of concepts from a couple of my blog posts:

* [Find date for the nth day of a month in Power BI](https://datamesse.github.io/#/post/1632578400)
* [Dynamically apply time zone and daylight savings on date/times in Power BI](https://datamesse.github.io/#/post/1633784400)
* [Find aggregate value for grouped rows based on column value](https://datamesse.github.io/#/post/1634389200)

### Power Query for custom functions

* The Standard and Daylight Saving Observation dataset uses hour offsets in text format that appear like this: "+09:30", i.e. offset is 9 hours and 30 minutes after UTC time. This function converts the hour component as a numerical value e.g. +9, so that it can be used by later functions.

```
let
  AnchorOffsetHours = (Offset as nullable text) => 
    Number.FromText(Text.Start(Offset,Text.Length(Offset) - (Text.Length(Offset)-Text.PositionOf(Offset,":"))))
in
  AnchorOffsetHours
```

* Similar to the above function, but converts the minute component to a numerical value.

```
let
  AnchorOffsetMinutes = (Offset as nullable text) => 
    Number.FromText(Text.End(Offset,Text.PositionOf(Offset,":")-1))
in
  AnchorOffsetMinutes
```

* Because the markers which define when standard and daylight savings (a.k.a. "anchors") are of different data structures for different countries (e.g. some abide by a specific date like the 31st May, and others are more dynamic like the 1st Sunday of October), a function is needed to take in a UTC datetime value, then add the time zone offset so that it converts the input value into a datetimezone that reflects the anchor's date/time for the orginal datetime's year.

```
let
  AnchorToDatetimezone = (DateTimestamp as datetime, MonthAnchor as nullable number, DayAnchor as nullable number, PositionAnchor as nullable number, DateAnchor as nullable number, Time as nullable time, Offset as nullable text) => 
  /* Error-handling based on insufficient data or incorrect value combination */
  if (MonthAnchor = null) 
    or (DateAnchor = null and DayAnchor = null)
    or (DateAnchor <> null and DayAnchor <> null)
    or (DayAnchor <> null and PositionAnchor = null)
    or (DayAnchor = null and PositionAnchor <> null)
    or (Time = null)
    or (Offset = null)
  then "Incomplete data"
  /* Applying time zone to DateTimestamp, with separate conditions for position anchor = 9 i.e. "Last" */
  else if DateAnchor <> null
    then Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor)  & "/" & Text.From(DateAnchor) & " " & Text.From(Time) & Offset
  else if DayAnchor < 6 and PositionAnchor > 0 and PositionAnchor < 5
  /* Optional parameter in Date.DayOfWeek 1 = Day.Monday will get Sunday, hence DayAnchor (Sunday = 0) + 1 */
    then Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/" & Text.From( (7 - Date.DayOfWeek(Date.FromText(Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/1"), DayAnchor + 1)) + (-7 + (7 * PositionAnchor)) ) & " " & Text.From(Time) & Offset
  /* Need to pass Day.Sunday to get Saturday */
  else if DayAnchor = 6 and PositionAnchor > 0 and PositionAnchor < 5
    then Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/" & Text.From( (7 - Date.DayOfWeek(Date.FromText(Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/1"), Day.Sunday )) + (-7 + (7 * PositionAnchor)) ) & " " & Text.From(Time) & Offset
  /* handling for last specific day of month */
  else if DayAnchor = 0 and PositionAnchor = 9
    then Text.From(Date.AddDays(Date.EndOfMonth(Date.From(Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/1")),(-1 * Number.From(Date.DayOfWeek(Date.EndOfMonth(Date.From(Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/1")), Day.Sunday))))) & " " & Text.From(Time) & Offset
  else if DayAnchor > 0 and PositionAnchor = 9
    then Text.From(Date.AddDays(Date.EndOfMonth(Date.From(Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/1")),(-1 * (Number.From(Date.DayOfWeek(Date.EndOfMonth(Date.From(Text.From(Date.Year(DateTimestamp)) & "/" & Text.From(MonthAnchor) & "/1")), Day.Sunday)) + ( 7 - DayAnchor ))))) & " " & Text.From(Time) & Offset
  else null
in
  AnchorToDatetimezone
```

* Since the previous function provided an actual anchor date/timezone that can be used to define if an offset is applicable to a date/time value, we then construct a function that checks for if and when offset should be applied by using the output of the previous function, then actually apply that offset.

```
let
  DatetimeAppendZone = (DateTimestamp as datetime, Difference as number, StandardOffset as nullable text, DaylightOffset as nullable text, DSTstartAncDate as nullable number, DSTstartAncPosition as nullable number, DSTstartAncDay as nullable number, DSTstartAncMonth as nullable number, DSTstartAncUTC as nullable time, DSTstartAncLocal as nullable time, DSTendAncDate as nullable number, DSTendAncPosition as nullable number, DSTendAncDay as nullable number, DSTendAncMonth as nullable number, DSTendAncUTC as nullable time, DSTendAncLocal as nullable time) => 
  /* Validation to ensure same time anchor types for start and end are used */
  if Difference <> 0 and ( (DSTstartAncLocal = null and DSTstartAncUTC = null) or (DSTendAncLocal = null and DSTendAncUTC = null) )
    then "Incomplete data"

  /* Where DST is not observed, just append Standard UTC offset */
  else if Difference = 0
    then DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))

  /* From this point on, if using a data source that doesn't properly account for Daylight Savings offsets, you can factor those into the calculations */

  /* Where DST is observed with Standard time result */
  else if Difference <> 0
    and (
          (
           /* Where local offset is used, 1 DST period in same year, datetimestamp is outside daylight savings */
           DSTstartAncLocal <> null and DSTstartAncMonth < DSTendAncMonth
           and ( DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) < DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, StandardOffset))
                or DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) > DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, StandardOffset)) )
          )
      or  (
           /* Where local offset is used, 2 DST periods in same year, datetimestamp is outside both daylight savings periods */
           DSTstartAncLocal <> null and DSTstartAncMonth > DSTendAncMonth 
           and Date.Month(DateTimestamp) >= DSTendAncMonth and Date.Month(DateTimestamp) <= DSTstartAncMonth
           and DateTime.AddZone(DateTimestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) > DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, DaylightOffset))
           and DateTime.AddZone(DateTimestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) < DateTimeZone.From(AnchorToDatetimezone(Date.AddYears(DateTimestamp,1), DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, DaylightOffset))           
          )
      or  (
           /* Where UTC offset is used, 1 DST period in same year, datetimestamp is inside daylight savings */
           DSTstartAncUTC <> null and DSTstartAncMonth < DSTendAncMonth
           and ( DateTimeZone.ToUtc(DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) <  DateTimeZone.FromText(AnchorToDatetimezone(DateTimestamp, DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncUTC, "+00:00"))
                 or DateTimeZone.ToUtc(DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) > DateTimeZone.FromText(AnchorToDatetimezone(DateTimestamp, DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncUTC, "+00:00")) )
          )
    )
    then DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))

  /* Where DST is observed with Daylight Saving time result */
  else if Difference <> 0
    and (
          (
           /* Where local offset is used, 1 DST period within same year, datetimestamp is inside daylight savings */    
           DSTstartAncLocal <> null and DSTstartAncMonth < DSTendAncMonth
           and ( DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) >= DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, StandardOffset))
                or DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) <= DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, StandardOffset)) )
          )
      or  (
           /* Where local offset is used, 2 DST periods in same year, datetimestamp is inside 1st daylight savings period */
           DSTstartAncLocal <> null and DSTstartAncMonth > DSTendAncMonth and Date.Month(DateTimestamp) <= DSTendAncMonth
           and DateTime.AddZone(DateTimestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) <= DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, DaylightOffset))
          )
      or  (
           /* Where local offset is used, 2 DST periods in same year, datetimestamp is inside 2nd daylight savings period */
           DSTstartAncLocal <> null and DSTstartAncMonth > DSTendAncMonth and Date.Month(DateTimestamp) >= DSTendAncMonth
           and DateTime.AddZone(DateTimestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) >= DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, DaylightOffset))
          )
      or  (
           /* Where UTC offset is used, 1 DST period in same year, datetimestamp is outside daylight savings */
           DSTstartAncUTC <> null and DSTstartAncMonth < DSTendAncMonth
           and DateTimeZone.ToUtc(DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) >=  DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncUTC, "+00:00"))
           and DateTimeZone.ToUtc(DateTime.AddZone(DateTimestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) <= DateTimeZone.From(AnchorToDatetimezone(DateTimestamp, DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncUTC, "+00:00")) 
          )
    )
    then DateTime.AddZone(DateTimestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset))
  else null
in
  DatetimeAppendZone
```

```
let
  DatetimeSwitchZone = (DateTimeZonestamp as datetimezone, Difference as number, StandardOffset as nullable text, DaylightOffset as nullable text, DSTstartAncDate as nullable number, DSTstartAncPosition as nullable number, DSTstartAncDay as nullable number, DSTstartAncMonth as nullable number, DSTstartAncUTC as nullable time, DSTstartAncLocal as nullable time, DSTendAncDate as nullable number, DSTendAncPosition as nullable number, DSTendAncDay as nullable number, DSTendAncMonth as nullable number, DSTendAncUTC as nullable time, DSTendAncLocal as nullable time) => 
  /* Validation to ensure same time anchor types for start and end are used */
  if Difference <> 0 and ( (DSTstartAncLocal = null and DSTstartAncUTC = null) or (DSTendAncLocal = null and DSTendAncUTC = null) )
    then "Incomplete data"

  /* Where DST is not observed, just append Standard UTC offset */
  else if Difference = 0
    then DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))

  /* From this point on, if using a data source that doesn't properly account for Daylight Savings offsets, you can factor those into the calculations */

  /* Where DST is observed with Standard time result */
  else if Difference <> 0
    and (
          (
           /* Where local offset is used, 1 DST period in same year, datetimestamp is outside daylight savings */
           DSTstartAncLocal <> null and DSTstartAncMonth < DSTendAncMonth
           and ( DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) < DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, StandardOffset))
                or DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) > DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, StandardOffset)) )
          )
      or  (
           /* Where local offset is used, 2 DST periods in same year, datetimestamp is outside both daylight savings periods */
           DSTstartAncLocal <> null and DSTstartAncMonth > DSTendAncMonth 
           and Date.Month(DateTimeZone.RemoveZone(DateTimeZonestamp)) >= DSTendAncMonth and Date.Month(DateTimeZone.RemoveZone(DateTimeZonestamp)) <= DSTstartAncMonth
           and DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) > DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, DaylightOffset))
           and DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) < DateTimeZone.From(AnchorToDatetimezone(Date.AddYears(DateTimeZone.RemoveZone(DateTimeZonestamp),1), DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, DaylightOffset))           
          )
      or  (
           /* Where UTC offset is used, 1 DST period in same year, datetimestamp is inside daylight savings */
           DSTstartAncUTC <> null and DSTstartAncMonth < DSTendAncMonth
           and ( DateTimeZone.ToUtc(DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) <  DateTimeZone.FromText(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncUTC, "+00:00"))
                 or DateTimeZone.ToUtc(DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) > DateTimeZone.FromText(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncUTC, "+00:00")) )
          )
    )
    then DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))

  /* Where DST is observed with Daylight Saving time result */
  else if Difference <> 0
    and (
          (
           /* Where local offset is used, 1 DST period within same year, datetimestamp is inside daylight savings */    
           DSTstartAncLocal <> null and DSTstartAncMonth < DSTendAncMonth
           and ( DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) >= DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, StandardOffset))
                or DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset)) <= DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, StandardOffset)) )
          )
      or  (
           /* Where local offset is used, 2 DST periods in same year, datetimestamp is inside 1st daylight savings period */
           DSTstartAncLocal <> null and DSTstartAncMonth > DSTendAncMonth and Date.Month(DateTimeZone.RemoveZone(DateTimeZonestamp)) <= DSTendAncMonth
           and DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) <= DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncLocal, DaylightOffset))
          )
      or  (
           /* Where local offset is used, 2 DST periods in same year, datetimestamp is inside 2nd daylight savings period */
           DSTstartAncLocal <> null and DSTstartAncMonth > DSTendAncMonth and Date.Month(DateTimeZone.RemoveZone(DateTimeZonestamp)) >= DSTendAncMonth
           and DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset)) >= DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncLocal, DaylightOffset))
          )
      or  (
           /* Where UTC offset is used, 1 DST period in same year, datetimestamp is outside daylight savings */
           DSTstartAncUTC <> null and DSTstartAncMonth < DSTendAncMonth
           and DateTimeZone.ToUtc(DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) >=  DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTstartAncMonth, DSTstartAncDay, DSTstartAncPosition, DSTstartAncDate, DSTstartAncUTC, "+00:00"))
           and DateTimeZone.ToUtc(DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(StandardOffset),AnchorOffsetMinutes(StandardOffset))) <= DateTimeZone.From(AnchorToDatetimezone(DateTimeZone.RemoveZone(DateTimeZonestamp), DSTendAncMonth, DSTendAncDay, DSTendAncPosition, DSTendAncDate, DSTendAncUTC, "+00:00")) 
          )
    )
    then DateTimeZone.SwitchZone(DateTimeZonestamp,AnchorOffsetHours(DaylightOffset),AnchorOffsetMinutes(DaylightOffset))
  else null
in
  DatetimeSwitchZone
```


### Power Query for Updates data

```
let
    Source = Excel.Workbook(File.Contents("C:\Support ticket updates.xlsx"), null, true),
    Updates_Table = Source{[Item="Updates",Kind="Table"]}[Data],
    #"change types for Source" = Table.TransformColumnTypes(Updates_Table,{{"Ticket ID", Int64.Type}, {"Update timestamp", type datetime}, {"Update ticket status", type text}, {"Updater name", type text}, {"Public comments", Int64.Type}, {"Internal comments", Int64.Type}}),
    #"rename column for Source" = Table.RenameColumns(#"change types for Source",{{"Update timestamp", "Update timestamp original"}}),
    #"add column Report timezone" = Table.AddColumn(#"rename column for Source", "Report timezone", each "Australia, Sydney", type text),
    #"merge Report timezone" = Table.NestedJoin(#"add column Report timezone", {"Report timezone"}, Timezones, {"Timezone"}, "Timezones", JoinKind.Inner),
    #"expand Report timezone" = Table.ExpandTableColumn(#"merge Report timezone", "Timezones", {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}, {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}),
    #"add column Report update timestamp" = Table.AddColumn(#"expand Report timezone", "Report update timestamp", each DatetimeAppendZone([#"Update timestamp original"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"sort Report update timestamp asc" = Table.Sort(#"add column Report update timestamp",{{"Report update timestamp", Order.Ascending}}),
    #"add column Update ID" = Table.AddIndexColumn(#"sort Report update timestamp asc", "Update ID", 1, 1, Int64.Type),
    #"remove Report timezone" = Table.SelectColumns(#"add column Update ID",{"Ticket ID", "Update ID", "Report update timestamp", "Update ticket status", "Updater name", "Public comments", "Internal comments"}),
    #"merge Updater" = Table.NestedJoin(#"remove Report timezone", {"Updater name"}, Updaters, {"Full Name"}, "Updaters", JoinKind.Inner),
    #"expand Updater" = Table.ExpandTableColumn(#"merge Updater", "Updaters", {"Timezone", "Role"}, {"Updater timezone", "Updater role"}),
    #"merge Updater timezone" = Table.NestedJoin(#"expand Updater", {"Updater timezone"}, Timezones, {"Timezone"}, "Timezones", JoinKind.Inner),
    #"expand Updater timezone" = Table.ExpandTableColumn(#"merge Updater timezone", "Timezones", {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}, {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}),
    #"add column Updater's timestamp" = Table.AddColumn(#"expand Updater timezone", "Updater's timestamp", each DatetimeSwitchZone([#"Report update timestamp"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"add column Updater's day" = Table.AddColumn(#"add column Updater's timestamp", "Updater's day", each DateTimeZone.ToText([#"Updater's timestamp"],"ddd"), type text),
    #"add column Updater's hour" = Table.AddColumn(#"add column Updater's day", "Updater's hour", each Time.Hour([#"Updater's timestamp"]), Int64.Type),
    #"add column Updater's zone" = Table.AddColumn(#"add column Updater's hour", "Updater's zone", each DateTimeZone.ToText([#"Updater's timestamp"],"zzz"), type text),
    #"add column Update type" = Table.AddColumn(#"add column Updater's zone", "Update type", each if [Updater role] = "End user" and [Public comments] = 1
then "User message"
else if [Updater role] = "Agent" and [Public comments] = 1 and [Internal comments] = 0
then "Agent reply"
else if [Updater role] = "Agent" and [Internal comments] = 1 and [Public comments] = 0
then "Agent internal note"
else "Invalid", type text),
    #"add column UTC update timestamp" = Table.AddColumn(#"add column Update type", "UTC update timestamp", each DateTimeZone.ToUtc([Report update timestamp]),type datetimezone),
    #"remove Updater timezone" = Table.SelectColumns(#"add column UTC update timestamp",{"Ticket ID", "Update ID", "Update ticket status", "Updater name", "Updater role", "Update type", "Updater's timestamp", "Updater's day", "Updater's zone", "Updater's hour", "UTC update timestamp", "Public comments", "Internal comments"})
in
    #"remove Updater timezone"
```


### Power Query for Assignment data

```
let
    Source = Excel.Workbook(File.Contents("C:\Support ticket updates.xlsx"), null, true),
    Assignment_Table = Source{[Item="Assignment",Kind="Table"]}[Data],
    #"change types for Source" = Table.TransformColumnTypes(Assignment_Table,{{"Ticket ID", Int64.Type}, {"Assignee name", type text}, {"Created timestamp", type datetime}, {"Assignment timestamp", type datetime}, {"Solved timestamp", type datetime}, {"Priority", type text}, {"Requester", type text}, {"Development ID", type text}, {"Reporter", type text}, {"Development timestamp", type datetime}, {"Survey good", Int64.Type}, {"Survey bad", Int64.Type}, {"SDR", Int64.Type}}),
    #"rename columns Source" = Table.RenameColumns(#"change types for Source",{{"Created timestamp", "Created timestamp original"}, {"Assignment timestamp", "Assignment timestamp original"}, {"Solved timestamp", "Solved timestamp original"}, {"Development timestamp", "Development timestamp original"}}),
    #"add column Report timezone" = Table.AddColumn(#"rename columns Source", "Report timezone", each "Australia, Sydney",type text),
    #"merge Report timezone" = Table.NestedJoin(#"add column Report timezone", {"Report timezone"}, Timezones, {"Timezone"}, "Timezones", JoinKind.Inner),
    #"expand Report timezone" = Table.ExpandTableColumn(#"merge Report timezone", "Timezones", {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}, {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}),
    #"add column Report create timestamp" = Table.AddColumn(#"expand Report timezone", "Report create timestamp", each DatetimeAppendZone([#"Created timestamp original"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"add column Report assign timestamp" = Table.AddColumn(#"add column Report create timestamp", "Report assign timestamp", each DatetimeAppendZone([#"Assignment timestamp original"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"add column Report solve timestamp" = Table.AddColumn(#"add column Report assign timestamp", "Report solve timestamp", each DatetimeAppendZone([#"Solved timestamp original"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"add column Report escalate timestamp" = Table.AddColumn(#"add column Report solve timestamp", "Report escalate timestamp", each if [Development ID] = ""
then null
else DatetimeAppendZone([#"Development timestamp original"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"remove Report timezone" = Table.SelectColumns(#"add column Report escalate timestamp",{"Ticket ID", "Assignee name", "Priority", "Requester", "Report create timestamp", "Report assign timestamp", "Report solve timestamp", "Development ID", "Reporter", "Report escalate timestamp", "Survey good", "Survey bad", "SDR"}),
    #"merge Assignee" = Table.NestedJoin(#"remove Report timezone", {"Assignee name"}, Agents, {"Full Name"}, "Agents", JoinKind.Inner),
    #"expand Assignee" = Table.ExpandTableColumn(#"merge Assignee", "Agents", {"Timezone"}, {"Agent timezone"}),
    #"merge Assignee timezone" = Table.NestedJoin(#"expand Assignee", {"Agent timezone"}, Timezones, {"Timezone"}, "Timezones", JoinKind.Inner),
    #"expand Assignee timezone" = Table.ExpandTableColumn(#"merge Assignee timezone", "Timezones", {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}, {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}),
    #"add column Assignee's assign timestamp" = Table.AddColumn(#"expand Assignee timezone", "Assignee's assign timestamp", each DatetimeSwitchZone([#"Report assign timestamp"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"add column Assignee's assign day" = Table.AddColumn(#"add column Assignee's assign timestamp", "Assignee's assign day", each DateTimeZone.ToText([#"Assignee's assign timestamp"],"ddd"), type text),
    #"add column Assignee's assign hour" = Table.AddColumn(#"add column Assignee's assign day", "Assignee's assign hour", each Time.Hour([#"Assignee's assign timestamp"]),Int64.Type),
    #"add column Assignee's assign zone" = Table.AddColumn(#"add column Assignee's assign hour", "Assignee's assign zone", each DateTimeZone.ToText([#"Assignee's assign timestamp"],"zzz"), type text),
    #"add column Assignee's solve timestamp" = Table.AddColumn(#"add column Assignee's assign zone", "Assignee's solve timestamp", each DatetimeSwitchZone([#"Report solve timestamp"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"remove Assignee timezone" = Table.SelectColumns(#"add column Assignee's solve timestamp",{"Ticket ID", "Assignee name", "Priority", "Requester", "Report create timestamp", "Assignee's assign timestamp",  "Assignee's assign day", "Assignee's assign hour", "Assignee's assign zone", "Assignee's solve timestamp", "Development ID", "Reporter", "Report escalate timestamp", "Survey good", "Survey bad", "SDR"}),
    #"merge Reporter" = Table.NestedJoin(#"remove Assignee timezone", {"Reporter"}, Agents, {"Full Name"}, "Agents", JoinKind.LeftOuter),
    #"expand Reporter" = Table.ExpandTableColumn(#"merge Reporter", "Agents", {"Timezone"}, {"Reporter timezone"}),
    #"merge Reporter timezone" = Table.NestedJoin(#"expand Reporter", {"Reporter timezone"}, Timezones, {"Timezone"}, "Timezones", JoinKind.LeftOuter),
    #"expand Reporter timezone" = Table.ExpandTableColumn(#"merge Reporter timezone", "Timezones", {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}, {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}),
    #"add column Reporter's escalate timestamp" = Table.AddColumn(#"expand Reporter timezone", "Reporter's escalate timestamp", each if [Development ID] = ""
then null
else DatetimeSwitchZone([#"Report escalate timestamp"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"add column Reporter's escalate day" = Table.AddColumn(#"add column Reporter's escalate timestamp", "Reporter's escalate day", each if [Development ID] = ""
then null
else DateTimeZone.ToText([#"Reporter's escalate timestamp"],
"ddd"), type text),
    #"remove Reporter timezone" = Table.SelectColumns(#"add column Reporter's escalate day",{"Ticket ID", "Assignee name", "Priority", "Requester", "Report create timestamp", "Assignee's assign timestamp",  "Assignee's assign day", "Assignee's assign hour", "Assignee's assign zone", "Assignee's solve timestamp", "Development ID", "Reporter", "Reporter's escalate timestamp", "Reporter's escalate day", "Survey good", "Survey bad", "SDR"}),
    #"merge Requester" = Table.NestedJoin(#"remove Reporter timezone", {"Requester"}, Clients, {"Full Name"}, "Clients", JoinKind.Inner),
    #"expand Requester" = Table.ExpandTableColumn(#"merge Requester", "Clients", {"Timezone"}, {"Requester timezone"}),
    #"merge Requester timezone" = Table.NestedJoin(#"expand Requester", {"Requester timezone"}, Timezones, {"Timezone"}, "Timezones", JoinKind.Inner),
    #"expand Requester timezone" = Table.ExpandTableColumn(#"merge Requester timezone", "Timezones", {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}, {"Standard UTC offset", "Daylight Saving UTC offset", "Daylight offset - Standard offset", "DST start (date anchor)", "DST start (position anchor)", "DST start (day anchor)", "DST start (month anchor)", "DST start (UTC time anchor)", "DST start (local time anchor)", "DST end (date anchor)", "DST end (position anchor)", "DST end (day anchor)", "DST end (month anchor)", "DST end (UTC time anchor)", "DST end (local time anchor)"}),
    #"add column Requester's create timestamp" = Table.AddColumn(#"expand Requester timezone", "Requester's create timestamp", each DatetimeSwitchZone([#"Report create timestamp"], [#"Daylight offset - Standard offset"], [Standard UTC offset], [Daylight Saving UTC offset], [#"DST start (date anchor)"], [#"DST start (position anchor)"], [#"DST start (day anchor)"], [#"DST start (month anchor)"], [#"DST start (UTC time anchor)"], [#"DST start (local time anchor)"], [#"DST end (date anchor)"], [#"DST end (position anchor)"], [#"DST end (day anchor)"], [#"DST end (month anchor)"], [#"DST end (UTC time anchor)"], [#"DST end (local time anchor)"]), type datetimezone),
    #"add column Requester's create day" = Table.AddColumn(#"add column Requester's create timestamp", "Requester's create day", each DateTimeZone.ToText([#"Requester's create timestamp"],"ddd"), type text),
    #"add column Requester's create zone" = Table.AddColumn(#"add column Requester's create day", "Requester's create zone", each DateTimeZone.ToText([#"Requester's create timestamp"],"zzz"), type text),
    #"remove Requester timezone" = Table.SelectColumns(#"add column Requester's create zone",{"Ticket ID", "Assignee name", "Priority", "Requester", "Requester's create timestamp", "Requester's create day", "Requester's create zone", "Assignee's assign timestamp",  "Assignee's assign day", "Assignee's assign hour", "Assignee's assign zone", "Assignee's solve timestamp", "Development ID", "Reporter", "Reporter's escalate timestamp", "Reporter's escalate day", "Survey good", "Survey bad", "SDR"}),
    #"add column UTC create timestamp" = Table.AddColumn(#"remove Requester timezone", "UTC create timestamp", each DateTimeZone.ToUtc([#"Requester's create timestamp"]),type datetimezone),
    #"add column UTC assign timestamp" = Table.AddColumn(#"add column UTC create timestamp", "UTC assign timestamp", each DateTimeZone.ToUtc([#"Assignee's assign timestamp"]),type datetimezone),
    #"add column UTC escalate timestamp" = Table.AddColumn(#"add column UTC assign timestamp", "UTC escalate timestamp", each DateTimeZone.ToUtc([#"Reporter's escalate timestamp"]),type datetimezone),
    #"add column UTC solve timestamp" = Table.AddColumn(#"add column UTC escalate timestamp", "UTC solve timestamp", each DateTimeZone.ToUtc([#"Assignee's solve timestamp"]),type datetimezone),
    #"add column UTC create hour" = Table.AddColumn(#"add column UTC solve timestamp", "UTC create hour", each Time.Hour([UTC create timestamp]), Int64.Type),
    #"add column Priority order" = Table.AddColumn(#"add column UTC create hour", "Priorty order", each if [Priority] = "Critical"
then 1
else if [Priority] = "High"
then 2
else if [Priority] = "Medium"
then 3
else 4, Int32.Type),
    #"add column Escalated?" = Table.AddColumn(#"add column Priority order", "Escalated?", each if [Development ID] <> ""
then "Escalated"
else "Normal",type text),
    #"add column Surveyed?" = Table.AddColumn(#"add column Escalated?", "Surveyed?", each if [Survey good] = 1 
then "Good survey"
else if [Survey bad] = 1
then "Bad survey"
else "No survey response",type text)
in
    #"add column Surveyed?"
```

### Power Query for Replies data

```
let
    Source = Updates,
    #"remove Comments columns" = Table.SelectColumns(Source,{"Ticket ID", "Update ID", "Update ticket status", "Updater name", "Updater role", "Update type", "Updater's timestamp", "Updater's day", "Updater's zone", "Updater's hour", "UTC update timestamp"}),
    #"sort by Ticked ID then Update timestamp" = Table.Sort(#"remove Comments columns",{{"Ticket ID", Order.Ascending},{"UTC update timestamp", Order.Ascending}}),
    #"filter for messages and replies" = Table.SelectRows(#"sort by Ticked ID then Update timestamp", each ([Update type] <> "Agent internal note")),
    #"add column Index from 0" = Table.AddIndexColumn(#"filter for messages and replies", "Index 0", 0, 1, Int64.Type),
    #"add column Index from 1" = Table.AddIndexColumn(#"add column Index from 0", "Index 1", 1, 1, Int64.Type),
    #"merge Replies" = Table.NestedJoin(#"add column Index from 1", {"Index 0"}, #"add column Index from 1", {"Index 1"}, "merge Responses", JoinKind.Inner),
    #"expand Replies" = Table.ExpandTableColumn(#"merge Replies", "merge Responses", {"Ticket ID", "Update ID", "Update ticket status", "Updater name", "Updater role", "Update type", "Updater's timestamp", "Updater's day", "Updater's hour", "Updater's zone", "UTC update timestamp"}, {"Prior ticket ID", "Prior update ID","Prior update ticket status", "Prior updater name", "Prior updater role", "Prior update type", "Prior updater's timestamp", "Prior updater's day", "Prior updater's hour", "Prior updater's zone", "Prior UTC update timestamp"}),
    #"add column Reply type" = Table.AddColumn(#"expand Replies", "Reply type", each if [Ticket ID] = [Prior ticket ID] and [Prior update type] = "User message" and [Update type] = "Agent reply"
then "Agent to user"
else if [Ticket ID] = [Prior ticket ID] and [Prior update type] = "Agent reply" and [Update type] = "User message"
then "User to agent"
else if [Ticket ID] = [Prior ticket ID] and [Prior update type] = "Agent reply" and [Update type] = "Agent reply"
then "Agent after agent"
else if [Ticket ID] = [Prior ticket ID] and [Prior update type] = "User message" and [Update type] = "User message"
then "User after user"
else "Invalid", type text),
    #"merge Assignment" = Table.NestedJoin(#"add column Reply type", {"Ticket ID"}, Assignment, {"Ticket ID"}, "Assignment", JoinKind.Inner),
    #"expand Assignment" = Table.ExpandTableColumn(#"merge Assignment", "Assignment", {"Assignee name", "Assignee's assign zone"}, {"Assignee name", "Assignee's assign zone"}),
    #"add column Support type" = Table.AddColumn(#"expand Assignment", "Support type", each if [Reply type] = "Agent to user" and [Assignee name] = [Updater name]
then "Assignee reply"
else if [Reply type] = "Agent to user" and [Assignee name] <> [Updater name] and [#"Updater's zone"] = [#"Assignee's assign zone"]
then "Team reply"
else if [Reply type] = "Agent to user" and [Assignee name] <> [Updater name] and [#"Updater's zone"] <> [#"Assignee's assign zone"]
then "FTS reply"
else if [Reply type] = "Agent after agent" and [Assignee name] = [Updater name]
then "Assignee reply"
else if [Reply type] = "Agent after agent" and [Assignee name] <> [Updater name] and [#"Updater's zone"] = [#"Assignee's assign zone"]
then "Team reply"
else if [Reply type] = "Agent after agent" and [Assignee name] <> [Updater name] and [#"Updater's zone"] <> [#"Assignee's assign zone"]
then "FTS reply"
else if [Reply type] = "User to agent"
then "User message"
else if [Reply type] = "User after user"
then "User message"
else "Invalid", type text),
    #"add column Support ordinal" = Table.AddColumn(#"add column Support type", "Support ordinal", each if [Support type] = "FTS reply"
then 3
else if [Support type] = "Team reply"
then 2
else if [Support type] = "Assignee reply"
then 1
else 0, Int64.Type),
    #"order by Ticket ID & Update ID asc" = Table.Sort(#"add column Support ordinal",{{"Ticket ID", Order.Ascending}, {"Update ID", Order.Ascending}}),
    #"filter for valid Support type" = Table.SelectRows(#"order by Ticket ID & Update ID asc", each ([Support type] <> "Invalid"))
in
    #"filter for valid Support type"
```

### Power Query for Ticket type data

```
let
    Source = Replies,
    #"remove Replies" = Table.SelectColumns(Source,{"Ticket ID", "Support ordinal"}),
    #"group rows for max Support ordinal" = Table.Group(#"remove Replies", {"Ticket ID"}, {{"Max support ordinal", each List.Max([Support ordinal]), Int64.Type}}),
    #"add column Ticket type" = Table.AddColumn(#"group rows for max Support ordinal", "Ticket type", each if [Max support ordinal] = 3
then "FTS ticket"
else if [Max support ordinal] = 2
then "Team ticket"
else if [Max support ordinal] = 1
then "Regular ticket"
else "Error")
in
    #"add column Ticket type"
```

## Power BI Report Model

The data model for the report appears as below. The reason why the Updates table is referenced as a separate Replies table is because the Replies table is catered specifically for public messages and replies, and involves a self-merge, whereas the Updates table is retained as-is for other potential analysis such as non-public internal updates. In a similar vein the Assignee table is referenced from the Agent table to allow filtering and visualisation of Assignee fields (e.g. country, city), and avoid the need to have non-performant merges with the Replies table.

![Report data model](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/screenshots/08.png?raw=true)



# Excel report code

The Excel dashboard created for this dashboard is significantly smaller and simpler than the Power BI one above, hence the data model and its code are much smaller and streamlined.

* [Customer support agent performance dashboard](https://datamesse.github.io/#/project/ExcelCustomerSupportAgentPerformance)

### Power Query for People

```
let
    Source = Excel.Workbook(Web.Contents(#"File location"), null, true),
    Clients_Table = Source{[Item="Clients",Kind="Table"]}[Data],
    #"change type" = Table.TransformColumnTypes(Clients_Table,{{"Full Name", type text}, {"Region", type text}, {"Country", type text}, {"State", type text}, {"City", type text}, {"Timezone", type text}}),
    #"remove other columns" = Table.SelectColumns(#"change type",{"Full Name", "Country"}),
    #"add column Role" = Table.AddColumn(#"remove other columns", "Role", each "Client", type text),
    #"append Agents" = Table.Combine({#"add column Role", Agents})
in
    #"append Agents"
```

### Power Query for Agents

```
let
    Source = Excel.Workbook(Web.Contents(#"File location"), null, true),
    Agents_Table = Source{[Item="Agents",Kind="Table"]}[Data],
    #"change type" = Table.TransformColumnTypes(Agents_Table,{{"Full Name", type text}, {"Region", type text}, {"Country", type text}, {"State", type text}, {"City", type text}, {"Timezone", type text}, {"Photo ID", Int64.Type}, {"Photo URL", type text}}),
    #"rename columns" = Table.RenameColumns(#"change type",{{"Photo URL", "Original Image URL"}}),
    #"add column Photo URL" = Table.AddColumn(#"rename columns", "Photo URL", each "https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/Support%20ticket%20updates/agents/" & Text.From([Photo ID]) & ".png", type text),
    #"add column Photo code" = Table.AddColumn(#"add column Photo URL", "Photo code", each "photo_" & Text.From([Photo ID]), type text),
    #"remove other columns" = Table.SelectColumns(#"add column Photo code",{"Full Name", "Country", "Photo code"}),
    #"add column Role" = Table.AddColumn(#"remove other columns", "Role", each "Staff", type text),
    #"reorder columns" = Table.ReorderColumns(#"add column Role",{"Full Name", "Country", "Role", "Photo code"})
in
    #"reorder columns"
```

### Power Query for Ticket Assignments

```
let
    Source = Excel.Workbook(Web.Contents(#"File location"), null, true),
    Assignment_Table = Source{[Item="Assignment",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Assignment_Table,{{"Ticket ID", Int64.Type}, {"Assignee name", type text}, {"Created timestamp", type datetime}, {"Assignment timestamp", type datetime}, {"Solved timestamp", type datetime}, {"Priority", type text}, {"Requester", type text}, {"Development ID", type text}, {"Reporter", type text}, {"Development timestamp", type datetime}, {"Survey good", Int64.Type}, {"Survey bad", Int64.Type}, {"SDR", Int64.Type}}),
    #"add column Escalated?" = Table.AddColumn(#"Changed Type", "Escalated?", each if [Development ID] <> ""
then "Yes"
else "No", type text),
    #"remove other columns" = Table.SelectColumns(#"add column Escalated?",{"Ticket ID", "Assignee name", "Created timestamp", "Assignment timestamp", "Solved timestamp", "Priority", "Requester", "Escalated?", "Survey good", "Survey bad", "SDR"}),
    #"merge query: assignee country" = Table.NestedJoin(#"remove other columns", {"Assignee name"}, Agents, {"Full Name"}, "People", JoinKind.Inner),
    #"expand assignee country" = Table.ExpandTableColumn(#"merge query: assignee country", "People", {"Country"}, {"Assignee country"}),
    #"merge query: requester country" = Table.NestedJoin(#"expand assignee country", {"Requester"}, People, {"Full Name"}, "People", JoinKind.Inner),
    #"expand requester country" = Table.ExpandTableColumn(#"merge query: requester country", "People", {"Country"}, {"Requester country"})
in
    #"expand requester country"
```

### Power Query for Ticket Updates

The calculation for reply times needed to be moved from DAX back into Power Query, as other subsequent DAX calculations used in the Power BI report did not work for the Excel version.

```
let
    Source = Excel.Workbook(Web.Contents(#"File location"), null, true),
    Updates_Table = Source{[Item="Updates",Kind="Table"]}[Data],
    #"change data type" = Table.TransformColumnTypes(Updates_Table,{{"Ticket ID", Int64.Type}, {"Update timestamp", type datetime}, {"Update ticket status", type text}, {"Updater name", type text}, {"Public comments", Int64.Type}, {"Internal comments", Int64.Type}}),
    #"remove column Internal comments" = Table.SelectColumns(#"change data type",{"Ticket ID", "Update timestamp", "Update ticket status", "Updater name", "Public comments"}),
    #"filter out non-public responses" = Table.SelectRows(#"remove column Internal comments", each ([Public comments] = 1)),
    #"sort by Update timestamp then Ticket ID asc" = Table.Sort(#"filter out non-public responses",{{"Ticket ID", Order.Ascending},{"Update timestamp", Order.Ascending}}),
    #"add column Index 0" = Table.AddIndexColumn(#"sort by Update timestamp then Ticket ID asc", "Index 0", 0, 1, Int64.Type),
    #"add column Index 1" = Table.AddIndexColumn(#"add column Index 0", "Index 1", 1, 1, Int64.Type),
    #"merge query: self-join" = Table.NestedJoin(#"add column Index 1", {"Index 1"}, #"add column Index 1", {"Index 0"}, "add column Index 1", JoinKind.Inner),
    #"expand self-join" = Table.ExpandTableColumn(#"merge query: self-join", "add column Index 1", {"Ticket ID", "Update timestamp", "Update ticket status", "Updater name"}, {"Reply ticket ID", "Reply timestamp", "Reply ticket status", "Replier name"}),
    #"add column Same ticket?" = Table.AddColumn(#"expand self-join", "Same ticket?", each if [Ticket ID] = [Reply ticket ID]
then "Yes"
else "No", type text),
    #"filter out different tickets" = Table.SelectRows(#"add column Same ticket?", each ([#"Same ticket?"] = "Yes")),
    #"remove unneeded columns 1" = Table.SelectColumns(#"filter out different tickets",{"Ticket ID", "Update timestamp", "Update ticket status", "Updater name", "Reply timestamp", "Reply ticket status", "Replier name"}),
    #"merge query: updater role" = Table.NestedJoin(#"remove unneeded columns 1", {"Updater name"}, People, {"Full Name"}, "People", JoinKind.Inner),
    #"expand updater role" = Table.ExpandTableColumn(#"merge query: updater role", "People", {"Role"}, {"Updater role"}),
    #"merge query: replier role" = Table.NestedJoin(#"expand updater role", {"Replier name"}, People, {"Full Name"}, "People", JoinKind.Inner),
    #"expand replier role" = Table.ExpandTableColumn(#"merge query: replier role", "People", {"Role"}, {"Replier role"}),
    #"merge query: assignments" = Table.NestedJoin(#"expand replier role", {"Ticket ID"}, #"Ticket Assignments", {"Ticket ID"}, "Ticket Assignments", JoinKind.Inner),
    #"expand assignments" = Table.ExpandTableColumn(#"merge query: assignments", "Ticket Assignments", {"Assignee name"}, {"Assignee name"}),
    #"add column Reply type" = Table.AddColumn(#"expand assignments", "Reply type", each if [Updater role] = "Client" and [Replier role] = "Staff" and [Replier name] = [Assignee name]
then "Assignee reply to client"
else if [Updater role] = "Client" and [Replier role] = "Staff" and [Replier name] <> [Assignee name]
then "Colleague reply to client"
else if [Updater role] = "Staff" and [Replier role] = "Client"
then "Client reply to staff"
else if [Updater role] = "Client" and [Replier role] = "Client"
then "Client follow up"
else if [Updater role] = "Staff" and [Replier role] = "Staff" and [Replier name] = [Assignee name]
then "Assignee follow up"
else if [Updater role] = "Staff" and [Replier role] = "Staff" and [Replier name] <> [Assignee name]
then "Colleague follow up"
else null, type text),
    #"remove unneeded columns 2" = Table.SelectColumns(#"add column Reply type",{"Ticket ID", "Update timestamp", "Updater name", "Reply timestamp", "Replier name", "Replier role", "Reply type"}),
    #"merge query: 1st reply timestamp" = Table.NestedJoin(#"remove unneeded columns 2", 
                                       {"Ticket ID"},
                                       Table.Group(
                                           Table.SelectRows(#"remove unneeded columns 2", each ([Replier role] = "Staff")),
                                                   {"Ticket ID"},
                                                   {{"1st reply timestamp",
                                                   each List.Min([#"Reply timestamp"]), type nullable datetime}}),
                                       {"Ticket ID"},
                                       "Merged group by table",
                                       JoinKind.Inner),
    #"expand 1st reply timestamp" = Table.ExpandTableColumn(#"merge query: 1st reply timestamp", "Merged group by table", {"1st reply timestamp"}, {"1st reply timestamp"}),
    #"add column 1st reply?" = Table.AddColumn(#"expand 1st reply timestamp", "1st reply?", each if [Reply timestamp] = [1st reply timestamp] and [Replier role] = "Staff"
then "Yes"
else "No", type text),
    #"remove column 1st reply timestamp" = Table.RemoveColumns(#"add column 1st reply?",{"1st reply timestamp"}),
    #"add column Reply time (seconds)" = Table.AddColumn(#"remove column 1st reply timestamp", "Reply time (seconds)", each Duration.TotalSeconds([Reply timestamp] - [Update timestamp]), Int64.Type),
    #"add column Reply time within SLA?" = Table.AddColumn(#"add column Reply time (seconds)", "Reply time within SLA?", each if ([#"Reply time (seconds)"] <= #"Filter SLA reply time (seconds)" and [#"1st reply?"] = "Yes")
then "Yes"
else if ([#"Reply time (seconds)"] > #"Filter SLA reply time (seconds)" and [#"1st reply?"] = "Yes")
then "No"
else null, type text)
in
    #"add column Reply time within SLA?"
```

### Power Query for SLA reply time filter applied from a worksheet cell

```
let
    Source = Excel.CurrentWorkbook(){[Name="prm_SLA"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"SLA time", Int64.Type}}),
    #"SLA time" = #"Changed Type"{0}[SLA time]
in
    #"SLA time"
```

### DAX measures for Agents table

Only key DAX measures are listed. See Excel file for the full list.

Median 1st reply time (secs)

```
=CALCULATE([Median reply time (secs)],'Ticket Updates'[1st reply?]="Yes",USERELATIONSHIP(Agents[Full Name],'Ticket Updates'[Replier name]))
```

Median 1st reply time

```
=VAR Duration = [Median 1st reply time (secs)]
VAR Hours = INT ( Duration / 3600)
VAR Minutes = INT ( MOD( Duration - ( Hours * 3600 ),3600 ) / 60)
VAR Seconds = ROUNDUP(MOD ( MOD( Duration - ( Hours * 3600 ),3600 ), 60 ),0)
VAR H = IF ( LEN ( Hours ) = 1, "0" & Hours, Hours )
VAR M = IF ( LEN ( Minutes ) = 1, "0" & Minutes, Minutes )
VAR S = IF ( LEN ( Seconds ) = 1, "0" & Seconds, Seconds )
VAR OUTPUT = IF ( AND(H = "", M = ""), "", H & ":" & M & ":" & S )
RETURN OUTPUT
```

"# SLA met (agent's tickets)"

```
=CALCULATE(DISTINCTCOUNT('Ticket Updates'[Ticket ID]),'Ticket Updates'[Reply time within SLA?]="Yes", USERELATIONSHIP(Agents[Full Name], 'Ticket Assignments'[Assignee name]))
```

"# SLA breached (agent's tickets)"

```
=CALCULATE(DISTINCTCOUNT('Ticket Updates'[Ticket ID]),'Ticket Updates'[Reply time within SLA?]="No", USERELATIONSHIP(Agents[Full Name], 'Ticket Assignments'[Assignee name]))
```

% SLA

```
=CALCULATE(DIVIDE([#  SLA met (agent's tickets)],([#  SLA met (agent's tickets)]+[#  SLA breached (agent's tickets)]),0),USERELATIONSHIP(Agents[Full Name],'Ticket Assignments'[Assignee name]))
```

"# SDR"

```
=CALCULATE(SUM('Ticket Assignments'[SDR]),USERELATIONSHIP(Agents[Full Name],'Ticket Assignments'[Assignee name]))
```

% SDR

```
=CALCULATE(DIVIDE('Agents'[#  SDR],'Agents'[#  Tickets],1),USERELATIONSHIP(Agents[Full Name],'Ticket Assignments'[Assignee name]))
```