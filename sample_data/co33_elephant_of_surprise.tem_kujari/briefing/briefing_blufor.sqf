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
Sudanese militia have invaded and fortified a part of the Hala'id disputed region. 
Intelligence shows that they have installed a net of antiaircraft defenses, limiting the effect of our Air Force. 
However, it appears that their fuel supplies have been exhausted in the offensive, leaving their ground forces unable to manuever and vulnerable to an armored counter attack tonight. 
<br/>
The weather is expected to start out clear with a waning moon but rapidly worsening conditions as a storm rolls in.
<br/><br/>

<font size='18'>ENEMY FORCES</font>
<br/>
A Sudanese armor group emplaced behind earthen fortifications with militia infantry support. Armor is expected to be T-72 and BMP-2 types with protection packages of around 2012-era technology. Helicopters have been spotted flying too and from the airfield.
<br/><br/>

<font size='18'>FRIENDLY FORCES</font>
<br/>
A platoon of Egyption M1A2SEPv1 Abrams with logistics, engineering and recon support. No other support.
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
- Destroy the artillery battery near the villages of <marker name='Maiwa'>Maiwa</marker>.<br/>
- Secure the crossroads south of <marker name='Danashiwa'>Danashiwa</marker>.<br/>
- Secure the <marker name='Airfield'>Dr. Jones Airfield</marker> to prevent futher resupply.<br/>
- Defend against any counter attacks that may occur.<br/>
"]];

/* ================================================================================
	EXECUTION
	 - Provide an outline as to what the commander of the player's command might give.
*/

private _execution = ["diary", ["Execution","
<br/>
<font size='18'>COMMANDER'S INTENT</font>
<br/>
Tactical recommendation is to secure objectives on the north side of the river before crossing at some point to the south. Attached Drone Operators should be able to advise on the best path to advance.
<br/><br/>

<font size='18'>MOVEMENT PLAN</font>
<br/>
While it is possible to ford the river outside of bridges and crossings, it is not recommended to do so. 
<br/><br/>

<font size='18'>FIRE SUPPORT PLAN</font>
<br/>
No fire support available.
<br/><br/>
"]];

/* ================================================================================
	ADMINISTRATION
	 - Outline of logistics: available resources (equipment/vehicles) and ideally a summary of their capabilities.
	 - Outline of how to use any mission specific features/scripts.
	 - Seating capacities of each vehicle available for use.
*/

private _administration = ["diary", ["Administration","
<br/>
- M1A2SEPv1 Abrams tanks can seat 4 people at maximum. <br/>
- M1134 can seat 4 crew. <br/>
- M977A4-B HEMTT-type repair trucks seat 3 crew and are stocked with 500 points of fuel and ammunition.<br/>
- A Logistics FOB has been established <marker name='fob'>here</marker>.<br/>
"]];

player createDiaryRecord _administration;
player createDiaryRecord _execution;
player createDiaryRecord _mission;
player createDiaryRecord _situation;