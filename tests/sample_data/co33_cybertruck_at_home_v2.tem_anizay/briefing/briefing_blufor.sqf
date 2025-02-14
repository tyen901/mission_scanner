/* ================================================================================
	GENERAL BRIEFING NOTES
	 - Uses HTML style syntax. All supported tags can be found here - https://community.bistudio.com/wiki/createDiaryRecord
	 - For images use <img image='FILE'></img> (for those familiar with HTML note it is image rather than src).
	 - Note that using the " character inside the briefing block is forbidden use ' instead of ".
*/

/* ================================================================================
	SITUATION
	 - Outline of what is going on, where we are we and what has happened before the mission has started? This needs to contain any relevant background information.
	 - Draw attention to friendly and enemy forces in the area. The commander will make important decisions based off this information.
	 - Outline present weather conditions, players will typically assume that it is daylight with sunny weather.
*/

private _situation = ["diary", ["Situation","
<br/>
<font size='18'>SITUATION</font>
<br/>
202X, OCT 24, 13:55. Open war rages throughout the country of Anizay. Our enemies, the foreigner-supplied Anizay Liberation Army is pushing us out and steadily towards the northeast. However, in the haste to exfiltrate, we left behind our most important assets. Our commander's favorite cousin's prize vehicle projects are stuck inside FOB Obeh: a disarmed BTR-70 (sorry, 'artisan crafted Cybertruck'), and a handmade Mozzie 'helicopter' (the value is largely sentimental). Therefore, you have been assembled: the most expendable - sorry, we mean, 'elite' - militia platoon that Command could organize in a day, sent to retrieve these valuable assets and return them under our safe control.
<br/><br/>

<font size='18'>ENEMY FORCES</font>
<br/>
A sizeable warband (200-400 fighters) claims control over the area in and around Anizay. The warband is equipped with a mix of old SKSes and AKMs, but some of their more elite units are slowly being supplied with newer guns. They are riding in technicals, generally equipped with HMGs or GMGs. Assume that enemies have occupied most built-up areas in the AO, though they are unlikely to have significantly fortified them.
<br/><br/>

<font size='18'>FRIENDLY FORCES</font>
<br/>
Anywhere between 10-40 'volunteers' who unwisely replied to the commander's email before reading the whole thing. No reinforcements are forthcoming.
"]];

/* ================================================================================
	MISSION
	 - Describe any objectives that the team is expected to complete.
	 - Summarize(!) the overall task. This MUST be short and clear.
*/

private _mission = ["diary", ["Mission","
<br/>
<font size='18'>MISSION</font>
<br/>
- Retrieve the unarmed BTR-70 from FOB Obeh<br/>
- If able, also retrieve the Mozzie helicopter<br/>
- Escape the AO to the northwest, beyond the marked line, without exploding
"]];

/* ================================================================================
	EXECUTION
	 - Provide an outline as to what the commander of the player's command might give.
*/

private _execution = ["diary", ["Execution","
<br/>
<font size='18'>COMMANDER'S INTENT</font>
<br/>
Keep an eye out for enemy forces from the south and east. It is quite possible that they may flank around our east with their superior mobility. Command's directive in that instance is 'simply don't be flanked'.
<br/><br/>

<font size='18'>MOVEMENT PLAN</font>
<br/>
Proceed on foot towards FOB Obeh. Command's cousin says they left the keys inside both vehicles and are OK with us borrowing them for the exfil, provided we promise not to scratch the paint on purpose.
<br/><br/>

<font size='18'>SPECIAL TASKS</font>
<br/>
Squad leaders have been given wirecutters to facilitate entry to the FOB.
"]];

/* ================================================================================
	ADMINISTRATION
	 - Outline of logistics: available resources (equipment/vehicles) and ideally a summary of their capabilities.
	 - Outline of how to use any mission specific features/scripts.
	 - Seating capacities of each vehicle available for use.
*/

private _administration = ["diary", ["Administration","
<br/>
The Beofeng 888 is our standard radio. CoyCo got a great deal on a bulk shipment from AliExpress.
"]];

player createDiaryRecord _administration;
player createDiaryRecord _execution;
player createDiaryRecord _mission;
player createDiaryRecord _situation;