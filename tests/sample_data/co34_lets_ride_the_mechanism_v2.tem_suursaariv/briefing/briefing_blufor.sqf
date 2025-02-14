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
Platoon, shit is fucked up totally hard. We're the last unit on this island that has been taken over by CSAT. 
Our only way out is to make it from our temporary base in Suurkyla to a boat all the way in Kiiskinkyla.
Luckily, there is one single road left on the entire island that hasn't been completely blocked off by CSAT armor. However, CSAT recon forces have set up ambushes all along the route.
However, we have no choice, as there is a CSAT air strike inbound to destroy our base. We are a supply platoon, so the only armored vehicles we have are these 50 year old humvees, but they'll have to do.
<br/><br/>

<font size='18'>ENEMY FORCES</font>
<br/>
CSAT Recon light infantry. Expect a lot of them but they won't be heavily armed, and we're not expecting any vehicles.
<br/><br/>

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
Drive from Suurkyla all the way to your water extraction in Kiiskinkyla.
If necessary, you can briefly stop for repairs in the town of Niemenkylä, marked on the map.
"]];

/* ================================================================================
	EXECUTION
	 - Provide an outline as to what the commander of the player's command might give.
*/

private _execution = ["diary", ["Execution","
<br/>
<font size='18'>COMMANDER'S INTENT</font>
<br/>
Get the hell out of there as fast as you can!!!!! 
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
You are equipped with light armored humvees equipped with M2s. Take your pick of what you want. They are resistant but not immune to small arms fire, and the windows can be rolled down and shot out of.
"]];

player createDiaryRecord _administration;
player createDiaryRecord _execution;
player createDiaryRecord _mission;
player createDiaryRecord _situation;